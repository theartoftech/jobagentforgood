from __future__ import annotations

import importlib.util
import io
import json
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import render_daily_job_search_html, render_workflow_review_html


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "search_jobs.py"
SPEC = importlib.util.spec_from_file_location("search_jobs", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load module from {MODULE_PATH}")

search_jobs = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = search_jobs
SPEC.loader.exec_module(search_jobs)


class SearchJobsPlanTests(unittest.TestCase):
    def test_plan_requires_daily_site_count_and_expansion_question(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = search_jobs.write_search_plan(
                today="2026-06-23", companies=[], profile={}, rules_text="",
                out_dir=Path(directory),
            ).read_text()
        for required in (
            "Job sites scanned", "unique sites", "configured sites",
            "failed", "partial", "unverified", "employer count",
            "Would you like me to research more job sites for the next search?",
            "Expand coverage", "Keep current coverage", "interactive question",
            "even when results are unchanged", "do not wait",
            "Do not infer consent", "200-site ceiling",
        ):
            self.assertIn(required, plan)
        self.assertNotIn("unchanged run needs no notification", plan)

    def test_plan_report_commands_render_zero_match_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            date = "2026-06-23"
            companies = [{"name": "Example Co", "careers_url": "https://example.com/careers"}]
            plan = search_jobs.write_search_plan(
                today=date, companies=companies, profile={}, rules_text="", out_dir=root,
            ).read_text()
            search_jobs.write_report_template(today=date, out_dir=root, human_search_companies=companies)
            (root / f"{date}-networking-matches.md").write_text("# Networking\n\nNot performed.\n")
            (root / f"{date}-workflow-review.json").write_text(json.dumps({
                "generated_on": date, "reviews": [],
            }))
            renderers = {
                "scripts/render_daily_job_search_html.py": render_daily_job_search_html.main,
                "scripts/render_workflow_review_html.py": render_workflow_review_html.main,
            }
            rendered: list[str] = []
            for line in plan.splitlines():
                if not line.startswith("scripts/jobagent_python.sh scripts/render_"):
                    continue
                arguments = shlex.split(line)[1:]
                with patch.object(sys, "argv", arguments), patch("sys.stdout", new_callable=io.StringIO):
                    renderers[arguments[0]]()
                rendered.append(arguments[0])
            self.assertEqual(set(renderers), set(rendered))
            broad = root / f"{date}-daily-job-search.html"
            workflow = root / f"{date}-workflow-review.html"
            self.assertIn(f'href="{workflow.name}"', broad.read_text())
            self.assertIn(f'href="{broad.name}"', workflow.read_text())
            self.assertEqual([], list(render_daily_job_search_html.build_detail_directory(broad).glob("*.html")))

    def test_plan_delivers_both_dated_reports_before_optional_documents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            out_dir = Path(directory)
            plan = search_jobs.write_search_plan(
                today="2026-06-23", companies=[], profile={}, rules_text="",
                out_dir=out_dir,
            ).read_text()

        broad = (
            "scripts/jobagent_python.sh scripts/render_daily_job_search_html.py "
            f"--report {out_dir}/2026-06-23-daily-job-search.md "
            f"--networking {out_dir}/2026-06-23-networking-matches.md"
        )
        workflow = (
            "scripts/jobagent_python.sh scripts/render_workflow_review_html.py "
            f"--workflow-review {out_dir}/2026-06-23-workflow-review.json"
        )
        for command in (broad, workflow):
            self.assertIn(command, plan)
            self.assertLess(plan.index("scripts/review_job_fit.py"), plan.index(command))
            self.assertLess(plan.index(command), plan.index("scripts/produce_resumes.py"))
        for required in (
            "Populate", "not a completed report", "not-performed",
            "both HTML reports", "outputs/latest-report.html", "outputs/report-index.md",
            "zero matches", "partial", "JSON evidence",
        ):
            self.assertIn(required, plan)

    def test_plan_requires_employer_maintenance_before_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = search_jobs.write_search_plan(
                today="2026-10-24", companies=[], profile={}, rules_text="",
                out_dir=Path(directory),
            )
            plan = path.read_text()
        self.assertLess(plan.index("## Employer expansion and weekly maintenance"), plan.index("scripts/discover_jobs_sharded.py"))
        for required in ("README.md", "outputs/employer-research-state.json", "200", "setup_jobagent.py --check", "job_sources.yml", "not an employer-research engine"):
            self.assertIn(required, plan)

    def test_human_search_rotation_prefers_company_specific_search_url(self) -> None:
        lines = search_jobs.format_human_search_companies(
            [
                {
                    "name": "Cognizant",
                    "careers_url": "https://careers.cognizant.com/us-en/jobs/",
                    "human_search_url": (
                        "https://careers.cognizant.com/us-en/jobs/"
                        "?keyword=Java&location=United%20States&cname=United%20States&pagesize=20#results"
                    ),
                }
            ]
        )

        self.assertEqual(
            lines,
            [
                "1. Cognizant - https://careers.cognizant.com/us-en/jobs/"
                "?keyword=Java&location=United%20States&cname=United%20States&pagesize=20#results"
            ],
        )

    def test_select_human_search_companies_uses_unsearched_companies_first(self) -> None:
        companies = [
            {"name": "Company A", "careers_url": "https://a.example.com"},
            {"name": "Company B", "careers_url": "https://b.example.com"},
            {"name": "Company C", "careers_url": "https://c.example.com"},
            {"name": "Company D", "careers_url": "https://d.example.com"},
            {"name": "Company E", "careers_url": "https://e.example.com"},
            {"name": "Company F", "careers_url": "https://f.example.com"},
        ]
        state = {"suggested_company_names": ["Company A"]}

        selected = search_jobs.select_human_search_companies(companies, state, count=5)

        self.assertEqual([company["name"] for company in selected], [
            "Company B",
            "Company C",
            "Company D",
            "Company E",
            "Company F",
        ])

    def test_select_human_search_companies_starts_new_cycle_after_all_companies_used(self) -> None:
        companies = [
            {"name": "Company A", "careers_url": "https://a.example.com"},
            {"name": "Company B", "careers_url": "https://b.example.com"},
        ]
        state = {"suggested_company_names": ["Company A", "Company B"]}

        selected = search_jobs.select_human_search_companies(companies, state, count=5)

        self.assertEqual([company["name"] for company in selected], ["Company A", "Company B"])

    def test_select_human_search_companies_fills_count_across_cycle_boundary(self) -> None:
        companies = [
            {"name": f"Company {letter}", "careers_url": f"https://{letter.casefold()}.example.com"}
            for letter in "ABCDEFG"
        ]
        state = {
            "suggested_company_names": [
                "Company A",
                "Company B",
                "Company C",
                "Company D",
                "Company E",
            ]
        }

        selected = search_jobs.select_human_search_companies(companies, state, count=5)
        updated = search_jobs.update_human_search_state(state, selected, companies)

        self.assertEqual(
            [company["name"] for company in selected],
            ["Company F", "Company G", "Company A", "Company B", "Company C"],
        )
        self.assertEqual(
            updated["suggested_company_names"],
            ["Company A", "Company B", "Company C"],
        )

    def test_write_human_search_rotation_updates_state_and_writes_dated_file(self) -> None:
        companies = [
            {"name": "Company A", "careers_url": "https://a.example.com/careers"},
            {"name": "Company B", "careers_url": "https://b.example.com/careers"},
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir)
            selected = search_jobs.write_human_search_rotation(
                today="2026-07-07",
                companies=companies,
                out_dir=out_dir,
                count=1,
            )
            markdown = (out_dir / "2026-07-07-human-search-companies.md").read_text(encoding="utf-8")
            state = search_jobs.load_human_search_state(out_dir)

        self.assertEqual([company["name"] for company in selected], ["Company A"])
        self.assertIn("## Human Search Companies - 2026-07-07", markdown)
        self.assertIn("Company A", markdown)
        self.assertIn("https://a.example.com/careers", markdown)
        self.assertEqual(state["suggested_company_names"], ["Company A"])


    def test_write_report_template_includes_freshness_verification_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir)
            path = search_jobs.write_report_template(
                today="2026-06-27",
                out_dir=out_dir,
                human_search_companies=[
                    {"name": "Example Co", "careers_url": "https://example.com/jobs"}
                ],
            )

            markdown = path.read_text(encoding="utf-8")

        self.assertIn("## Needs Freshness Verification", markdown)
        self.assertIn("## Gap Questions for Candidate", markdown)
        self.assertIn("| Priority | Company | Role | Public Freshness Signal |", markdown)
        self.assertIn("Carry forward active roles from the latest strict workflow review", markdown)
        self.assertIn("Remove roles from the active carry-forward set after local application history confirms they were applied to", markdown)
        self.assertIn("manually surfaced official live job URLs", markdown)
        self.assertIn(
            "browser-reviewed job findings from LinkedIn, Indeed, or any other site",
            markdown,
        )
        self.assertIn("strict workflow HTML is the actionable report", markdown)
        self.assertIn("Discovery Candidates — Higher Signal", markdown)
        self.assertIn("Do not run Word resume or cover-letter generation", markdown)
        self.assertIn("## Human Search Calibration", markdown)
        self.assertIn("Example Co", markdown)

    def test_build_title_queries_includes_company_official_search_domains(self) -> None:
        queries = search_jobs.build_title_queries(
            {
                "name": "Insight Global Staffing",
                "careers_url": "https://jobs.insightglobal.com/",
                "official_search_domains": [
                    "jobs.insightglobal.com/find_a_job",
                    "insightglobal.com/jobs/find_a_job",
                ],
            },
            {
                "title_targets": ["Senior Software Engineer", "Technical Consultant"],
                "strong_keywords": ["Java"],
            },
        )

        self.assertTrue(any("site:jobs.insightglobal.com/find_a_job" in query for query in queries))
        self.assertTrue(any("site:insightglobal.com/jobs/find_a_job" in query for query in queries))

    def test_build_title_queries_includes_forward_deployed_search(self) -> None:
        queries = search_jobs.build_title_queries(
            {
                "name": "Platform Co",
                "careers_url": "https://platform.example.com/careers",
            },
            {
                "title_targets": [
                    "Forward Deployed Engineer",
                    "Forward Deployed Architect",
                ],
                "strong_keywords": ["Java"],
            },
        )

        self.assertTrue(any("Forward Deployed Engineer" in query for query in queries))
        self.assertTrue(any("Forward Deployed Architect" in query for query in queries))


if __name__ == "__main__":
    unittest.main()
