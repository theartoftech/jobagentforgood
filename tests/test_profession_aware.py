from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import discover_jobs, review_job_fit, search_jobs, setup_jobagent
from scripts.career_context import compensation_review
from tests.test_portable_setup import answers


def career(profession: str) -> dict[str, object]:
    return {"profession": profession, "experience_level": "Experienced individual contributor",
            "specializations": [], "transferable_skills": [], "tools": [], "credentials": []}


def pay(period: str = "annual", minimum: float = 70000) -> dict[str, object]:
    return {"base_pay_period": period, "minimum_base": minimum, "target_total_annual": 0,
            "variable_pay": "acceptable", "notes": ""}


class ProfessionAwareTests(unittest.TestCase):
    def test_nontechnical_setup_search_and_review(self) -> None:
        for profession, title, strength, gap in [
            ("Sales", "Account Executive", "negotiation", "enterprise sales"),
            ("Customer service", "Customer Service Representative", "customer support", "insurance license"),
            ("Administration", "Administrative Assistant", "calendar management", "payroll processing"),
        ]:
            with self.subTest(profession=profession), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                data = {**answers(), "career_context": career(profession),
                        "compensation_preferences": pay("annual", 0),
                        "title_targets": [title], "adjacent_titles": [], "strong_keywords": [strength],
                        "do_not_claim": [gap], "last_role": title, "evidence": [f"Professional {strength}."]}
                setup_jobagent.configure(data, root)
                profile = discover_jobs.load_yaml(root / "candidate_profile.yml")["target_profile"]
                workflow = discover_jobs.load_yaml(root / "candidate_workflow_profile.yml")
                evidence = json.loads((root / "candidate_evidence.json").read_text())
                for output in (profile, workflow, evidence):
                    self.assertEqual(career(profession), output["career_context"])
                    self.assertEqual(data["compensation_preferences"], output["compensation_preferences"])
                plan = search_jobs.write_search_plan(today="2026-10-24", companies=data["companies"],
                    profile=profile, rules_text="", out_dir=root).read_text()
                self.assertIn(profession, plan)
                for term in ("Java", "Kafka", "engineering", "technical interview"):
                    self.assertNotIn(term, plan)
                for description, blocked in [(f"Requirements: {strength}.", False),
                                              (f"Requirements: {strength}; {gap} required.", True),
                                              (f"Requirements: {strength}. Preferred qualifications: {gap}.", False)]:
                    job = discover_jobs.JobPosting(company="Example", title=title,
                        url="https://example.test/jobs/1", description=description, location="Berlin, Germany",
                        work_model="onsite", posted_age_days=1)
                    discover_jobs.score_job(job, profile, 30)
                    result = review_job_fit.classify_review(job=dataclasses.asdict(job), workflow_profile=workflow)
                    self.assertEqual(blocked, bool(result.required_gaps))
                    self.assertFalse(any(x in str(result) for x in ("AWS", "Java", "Kafka")))
                    packet = "\n".join(review_job_fit.format_packet(result))
                    self.assertIn("Qualification gaps", packet)
                    self.assertNotIn("Technical gaps", packet)

    def test_malformed_profession_and_pay_refused_before_any_writes(self) -> None:
        changes = [
            {"career_context": None}, {"career_context": {}},
            {"career_context": {**career("Sales"), "profession": ""}},
            {"career_context": {**career("Sales"), "tools": "Salesforce"}},
            {"career_context": {**career("Sales"), "credentials": [False]}},
            {"compensation_preferences": None}, {"compensation_preferences": {}},
            {"compensation_preferences": pay("weekly", 20)},
            {"compensation_preferences": pay("annual", -1)},
            {"compensation_preferences": pay("annual", True)},
            {"compensation_preferences": pay("annual", float("nan"))},
            {"compensation_preferences": {**pay(), "variable_pay": "maybe"}},
            {"compensation_preferences": {**pay(), "notes": []}},
            {"compensation_preferences": pay(), "salary_floor": 0},
            {"compensation_preferences": pay("hourly", 25), "salary_floor": 70000},
        ]
        for change in changes:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):
                    setup_jobagent.configure({**answers(), **change}, Path(tmp))
                self.assertEqual([], list(Path(tmp).iterdir()))

    def test_sales_ote_does_not_clear_base_pay_requirement(self) -> None:
        profile = {"confirmed_strengths": ["negotiation"], "salary_floor": 70000,
                   "salary_currency": "USD", "compensation_preferences": pay()}
        for description in ["Base salary $40,000-$50,000. OTE $150,000-$200,000.",
                            "On-target earnings $180,000; uncapped commission.",
                            "Annual salary $80,000 plus bonus."]:
            with self.subTest(description=description):
                result = review_job_fit.classify_review(job={"title": "Account Executive", "fit_score": 95,
                    "url": "https://example.test/1", "description": description}, workflow_profile=profile)
                self.assertTrue(result.gap_questions_needed)
                self.assertFalse(result.should_generate_resume)
                self.assertIn("base", " ".join(result.questions_for_candidate).lower())
                self.assertIn("compensation", result.final_action.lower())

    def test_hourly_pay_and_total_earnings_target_need_separate_review(self) -> None:
        for prefs in (pay("hourly", 25), pay("monthly", 4000),
                      {**pay("annual", 0), "target_total_annual": 150000},
                      {**pay("annual", 0), "variable_pay": "excluded"}):
            profile = {"compensation_preferences": prefs, "salary_currency": "USD", "salary_floor": None}
            result = review_job_fit.classify_review(job={"title": "Account Executive", "fit_score": 95,
                "description": "Competitive pay", "url": "https://example.test/2"}, workflow_profile=profile)
            self.assertTrue(result.gap_questions_needed)
            self.assertFalse(result.should_generate_resume)

    def test_workday_probe_has_no_profession_filter(self) -> None:
        with mock.patch.object(discover_jobs, "request_json", return_value={"jobPostings": []}) as request:
            self.assertTrue(discover_jobs.is_valid_workday_board("https://example.wd1.myworkdayjobs.com/Careers"))
        self.assertEqual("", request.call_args.kwargs["payload"]["searchText"])

    def test_check_setup_validates_edited_career_fields(self) -> None:
        import yaml
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            setup_jobagent.configure({**answers(), "career_context": career("Administration")}, root)
            self.assertEqual(2, setup_jobagent.check_setup(root))
            path = root / "candidate_workflow_profile.yml"
            for invalid in ([], {"career_context": {}}):
                path.write_text(yaml.safe_dump(invalid))
                with self.assertRaises(ValueError):
                    setup_jobagent.check_setup(root)

    def test_title_sort_has_no_engineering_seniority_preference(self) -> None:
        titles = ["Staff Engineer", "Enterprise Account Executive"]
        self.assertEqual("Enterprise Account Executive", sorted(titles, key=discover_jobs.title_specificity_sort_key)[0])

    def test_compensation_evidence_is_exact_posting_and_does_not_clear_skill_gaps(self) -> None:
        url = "https://example.test/sales/1"
        profile = {"salary_floor": 70000, "salary_currency": "USD", "compensation_preferences": pay(),
                   "compensation_reviews": {url: {"status": "meets_preferences", "evidence": "Verified base and commission terms against candidate preferences.", "reviewed_on": "2026-10-24"}}}
        self.assertEqual(([], [], True), compensation_review("OTE $150000", url, profile))
        self.assertTrue(compensation_review("OTE $150000", url + "2", profile)[1])
        result = review_job_fit.classify_review(job={"title": "Account Executive", "fit_score": 95,
            "url": url, "description": "Requirements: insurance license required. OTE $150000."},
            workflow_profile={**profile, "do_not_claim": ["insurance license"]})
        self.assertFalse(result.should_generate_resume)
        self.assertIn("insurance license", result.required_gaps)
        profile["compensation_reviews"][url]["status"] = "below_preferences"
        self.assertTrue(compensation_review("OTE $150000", url, profile)[0])
        for reviews in ([], {url: {}}, {url: {"status": "meets_preferences", "evidence": "", "reviewed_on": "2026-10-24"}},
                        {url: {"status": "meets_preferences", "evidence": "Checked", "reviewed_on": "yesterday"}},
                        {url: {"status": "meets_preferences", "evidence": "Checked", "reviewed_on": False}}):
            with self.subTest(reviews=reviews), self.assertRaises(ValueError):
                compensation_review("", url, {**profile, "compensation_reviews": reviews})

    def test_pay_legacy_compatibility_and_valid_new_options(self) -> None:
        self.assertEqual(([], [], False), compensation_review("Annual salary $80000", "", {}))
        for period, minimum in (("annual", 0), ("annual", 70000), ("monthly", 5000), ("hourly", 25)):
            for policy in ("acceptable", "required", "excluded", "unspecified"):
                data = {**answers(), "compensation_preferences": {**pay(period, minimum), "variable_pay": policy},
                        "salary_floor": minimum if period == "annual" else 0}
                setup_jobagent.validate_answers(data)
        prefs = {"compensation_preferences": pay(), "salary_floor": 70000, "salary_currency": "USD"}
        self.assertFalse(compensation_review("Annual base salary $80000", "", prefs)[1])
        self.assertTrue(compensation_review("Undisclosed pay", "", prefs)[1])
        self.assertTrue(compensation_review("Annual base 80000 EUR", "", {**prefs, "salary_currency": "EUR"})[1])
        # Legacy interviews are not assigned an invented profession or pay structure.
        with tempfile.TemporaryDirectory() as tmp:
            setup_jobagent.configure(answers(), Path(tmp))
            evidence = json.loads((Path(tmp) / "candidate_evidence.json").read_text())
            self.assertNotIn("career_context", evidence)

    def test_fresh_sales_checkout_runs_mocked_ats_through_html_review(self) -> None:
        import contextlib
        import datetime as dt
        import io
        import os
        import sys
        from scripts import discover_jobs_sharded, mark_applied_jobs

        data = {**answers(), "career_context": career("Sales"), "title_targets": ["Account Executive"],
                "adjacent_titles": [], "strong_keywords": ["negotiation", "account growth"],
                "evidence": ["Handled customer renewals and negotiations."], "do_not_claim": ["insurance license"]}
        data["companies"][0]["careers_url"] = "https://boards.greenhouse.io/syntheticemployer"
        today = dt.date.today().isoformat()
        payload = {"jobs": [{"id": 1, "title": "Account Executive", "location": {"name": "Berlin, Germany"},
            "updated_at": today, "absolute_url": "https://boards.greenhouse.io/syntheticemployer/jobs/1",
            "content": "Requirements: negotiation and account growth. Onsite."}]}
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            setup_jobagent.configure(data, root)
            original = Path.cwd()
            try:
                os.chdir(root)
                with mock.patch.object(sys, "argv", ["search_jobs"]):
                    search_jobs.main()
                with mock.patch.object(discover_jobs, "request_json", return_value=payload), mock.patch.object(discover_jobs, "request_text", return_value=""), mock.patch.object(sys, "argv", ["discover", "--no-rotation", "--startup-count", "0", "--limit-companies", "1", "--ats-only"]):
                    discover_jobs_sharded.main()
                output = root / "outputs"
                with mock.patch.object(mark_applied_jobs, "fetch_tracker_jobs", side_effect=AssertionError("No external tracker")), mock.patch.object(sys, "argv", ["history", "--daily-report", str(output / f"{today}-daily-job-search.md"), "--local-applied", "applied_jobs.json", "--applied-jobs-out", str(output / f"{today}-applied-jobs.json")]):
                    mark_applied_jobs.main()
                with mock.patch.object(sys, "argv", ["review", "--discovered-jobs", str(output / f"{today}-discovered-jobs.json"), "--workflow-profile", "candidate_workflow_profile.yml", "--applied-jobs", str(output / f"{today}-applied-jobs.json"), "--out", str(output), "--date", today]):
                    review_job_fit.main()
                records = json.loads((output / f"{today}-workflow-review.json").read_text())["reviews"]
                self.assertEqual("Account Executive", records[0]["title"])
                self.assertEqual("STRONG APPLY", records[0]["workflow_decision"])
                self.assertTrue((output / f"{today}-workflow-review.html").is_file())
                self.assertFalse((output / "resumes").exists())
            finally:
                os.chdir(original)
