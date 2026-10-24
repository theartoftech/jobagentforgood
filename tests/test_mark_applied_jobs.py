from __future__ import annotations

import tempfile
import unittest
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from unittest import mock

from scripts import mark_applied_jobs

from scripts.mark_applied_jobs import (
    ReportJob,
    TrackerJob,
    extract_requisition_id,
    load_tracker_jobs_snapshot,
    match_tracker_job,
    update_section,
    write_tracker_jobs_snapshot,
)


class MarkAppliedJobsTests(unittest.TestCase):
    def test_default_uses_local_history_even_with_tracker_environment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "report.md"
            report.write_text("# Jobs\n")
            write_tracker_jobs_snapshot(root / "applied_jobs.json", jobs=[], ssh_host="local")
            with mock.patch("sys.argv", ["mark", "--daily-report", str(report)]), mock.patch.dict(os.environ, {"JOBTRACKER_SSH_HOST": "old-host", "JOBTRACKER_DB_PATH": "/old.db"}), mock.patch.object(mark_applied_jobs, "fetch_tracker_jobs") as remote:
                previous = Path.cwd()
                try:
                    os.chdir(root)
                    mark_applied_jobs.main()
                finally:
                    os.chdir(previous)
                remote.assert_not_called()

    def test_external_read_requires_opt_in_and_complete_configuration(self) -> None:
        cases = [
            ["--ssh-host", "host", "--jobtracker-db-path", "/data/jobs.db"],
            ["--enable-jobtracker-read"],
            ["--enable-jobtracker-read", "--ssh-host", "host"],
            ["--enable-jobtracker-read", "--jobtracker-db-path", "/data/jobs.db"],
            ["--enable-jobtracker-read", "--ssh-host", "host", "--jobtracker-db-path", "/data/jobs.db", "--local-applied", "local.json"],
        ]
        for arguments in cases:
            with self.subTest(arguments=arguments), mock.patch.dict(os.environ, {}, clear=True), mock.patch("sys.argv", ["mark", "--daily-report", "missing.md", *arguments]), mock.patch.object(mark_applied_jobs, "fetch_tracker_jobs") as remote:
                with self.assertRaises(SystemExit):
                    mark_applied_jobs.main()
                remote.assert_not_called()

    def test_opted_in_tracker_read_and_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "report.md"
            report.write_text("# Jobs\n")
            output = root / "snapshot.json"
            with mock.patch("sys.argv", ["mark", "--daily-report", str(report), "--enable-jobtracker-read", "--ssh-host", "approved-host", "--jobtracker-db-path", "/approved.db", "--applied-jobs-out", str(output)]), mock.patch.object(mark_applied_jobs, "fetch_tracker_jobs", return_value=[]) as remote:
                mark_applied_jobs.main()
                remote.assert_called_once_with("approved-host", "/approved.db")
            self.assertEqual(json.loads(output.read_text())["ssh_host"], "approved-host")

    def test_tracker_sqlite_connection_is_read_only(self) -> None:
        with mock.patch.object(mark_applied_jobs.subprocess, "run", return_value=mock.Mock(stdout="[]")) as run:
            self.assertEqual([], mark_applied_jobs.fetch_tracker_jobs("approved-host", "/approved.db"))
        program = run.call_args.kwargs["input"]
        self.assertIn("mode=ro", program)
        self.assertIn("uri=True", program)

    def test_approved_legacy_query_reads_real_sqlite_without_creating_missing_database(self) -> None:
        execute = subprocess.run

        def run_remote_locally(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            return execute([sys.executable, "-"], **kwargs)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tracker.db"
            with sqlite3.connect(path) as database:
                database.execute("create table jobs (data text)")
                database.execute("insert into jobs values (?)", (json.dumps({"company": "Example", "status": "applied", "jobUrl": "https://example.com/jobs/123"}),))
            original = path.read_bytes()
            with mock.patch.object(mark_applied_jobs.subprocess, "run", side_effect=run_remote_locally):
                jobs = mark_applied_jobs.fetch_tracker_jobs("approved-host", str(path))
                self.assertEqual("Example", jobs[0].company)
                self.assertTrue(jobs[0].already_applied)
                missing = path.parent / "missing.db"
                with self.assertRaises(subprocess.CalledProcessError):
                    mark_applied_jobs.fetch_tracker_jobs("approved-host", str(missing))
                self.assertFalse(missing.exists())
            self.assertEqual(original, path.read_bytes())

    def test_missing_local_history_never_falls_back_to_remote(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.json"
            with mock.patch("sys.argv", ["mark", "--daily-report", "missing.md", "--local-applied", str(missing)]), mock.patch.object(mark_applied_jobs, "fetch_tracker_jobs") as remote:
                with self.assertRaises(FileNotFoundError):
                    mark_applied_jobs.main()
                remote.assert_not_called()

    def test_update_section_marks_new_discovery_candidate_heading(self) -> None:
        lines = [
            "## Discovery Candidates — Higher Signal",
            "",
            "| Priority | Company | Role | Posted | Location / Work Model | Fit | URL | Already Applied |",
            "|---|---|---|---|---|---|---|---|",
            "| 1 | ExampleCo | Senior Engineer | 2026-07-23 | Remote | 88 | https://example.com/jobs/123 | No |",
        ]
        tracker = TrackerJob(
            company="ExampleCo",
            title="Senior Engineer",
            status="applied",
            job_url="https://example.com/jobs/123",
            applied_date="2026-07-22",
        )

        updated = update_section(lines, "Discovery Candidates — Higher Signal", [tracker])

        self.assertIn("Yes (2026-07-22)", "\n".join(updated))

    def test_update_section_preserves_escaped_pipes_in_job_title(self) -> None:
        lines = [
            "## Discovery Candidates — Higher Signal",
            "",
            "| Priority | Company | Role | Posted | Location / Work Model | Fit | URL |",
            "|---|---|---|---|---|---|---|",
            "| 1 | Grafana Labs | Staff Software Engineer - Platform, Application Core Services \\| USA \\| Remote | 2026-07-29 | United States (Remote) / Remote | 81 | https://example.com/jobs/1 |",
        ]

        updated = update_section(lines, "Discovery Candidates — Higher Signal", [])
        rendered = "\n".join(updated)

        self.assertIn(
            "Staff Software Engineer - Platform, Application Core Services \\| USA \\| Remote",
            rendered,
        )
        self.assertIn("| 81 | https://example.com/jobs/1 | No |", rendered)

    def test_distinct_requisition_ids_do_not_fall_back_to_company_and_title(self) -> None:
        report_job = ReportJob(
            company="Block",
            title="Senior Software Engineer, Product Platform",
            posted="",
            location="New York",
            fit="88",
            url="https://block.xyz/careers/jobs/5239566008?gh_jid=5239566008",
        )
        tracker_job = TrackerJob(
            company="Block",
            title="Senior Software Engineer, Product Platform",
            status="applied",
            job_url="https://block.xyz/careers/jobs/5231964008?gh_jid=5231964008",
            applied_date="2026-07-22",
        )

        self.assertIsNone(match_tracker_job(report_job, [tracker_job]))

    def test_intuit_uses_the_final_posting_identifier_not_shared_job_family_segment(self) -> None:
        trust_and_safety = (
            "https://jobs.intuit.com/job/new-york/"
            "principal-software-engineer-trust-and-safety/27595/96922204080"
        )
        traffic = (
            "https://jobs.intuit.com/job/san-diego/"
            "staff-software-engineer-traffic/27595/98200474400"
        )

        self.assertEqual("96922204080", extract_requisition_id(trust_and_safety))
        self.assertEqual("98200474400", extract_requisition_id(traffic))

    def test_extracts_cvs_style_requisition_id_without_separator_after_r(self) -> None:
        url = (
            "https://cvshealth.wd1.myworkdayjobs.com/CVS_Health_Careers/job/"
            "IL---Work-from-home/Staff-Software-Development-Engineer_R0993767-1"
        )

        self.assertEqual("R0993767-1", extract_requisition_id(url))

    def test_company_title_fallback_remains_available_without_requisition_ids(self) -> None:
        report_job = ReportJob(
            company="ExampleCo",
            title="Principal Engineer",
            posted="",
            location="Remote",
            fit="90",
            url="https://example.com/careers/principal-engineer",
        )
        tracker_job = TrackerJob(
            company="ExampleCo",
            title="Principal Engineer",
            status="interviewing",
            job_url="",
            applied_date="",
        )

        self.assertEqual(tracker_job, match_tracker_job(report_job, [tracker_job]))

    def test_tracker_snapshot_round_trip_preserves_application_evidence(self) -> None:
        jobs = [
            TrackerJob(
                company="ReadyCo",
                title="Senior Engineer",
                status="applied",
                job_url="https://example.com/jobs/123456",
                applied_date="2026-07-20",
            )
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "2026-07-22-applied-jobs.json"
            write_tracker_jobs_snapshot(path, jobs=jobs, ssh_host="jobtracker-host")
            loaded = load_tracker_jobs_snapshot(path)

        self.assertEqual(jobs, loaded)

    def test_tracker_snapshot_rejects_a_different_run_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "2026-07-21-applied-jobs.json"
            write_tracker_jobs_snapshot(path, jobs=[], ssh_host="jobtracker-host")

            with self.assertRaisesRegex(ValueError, "does not match workflow date"):
                load_tracker_jobs_snapshot(path, expected_date="2026-07-22")


if __name__ == "__main__":
    unittest.main()
