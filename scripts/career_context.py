"""Candidate-owned career context and explicit compensation review boundaries."""
from __future__ import annotations

import datetime as dt
import math
import re
from collections.abc import Mapping
from typing import Any

CAREER_LISTS = ("specializations", "transferable_skills", "tools", "credentials")
VARIABLE_PAY = re.compile(r"\b(?:OTE|on[- ]target earnings|commissions?|commission[- ]only|bonus(?:es)?|variable (?:pay|compensation)|total (?:compensation|earnings))\b", re.I)


def validate_career_fields(data: Mapping[str, Any]) -> None:
    """Legacy interviews may omit new fields; supplied fields must be complete."""
    if "career_context" in data:
        career = data["career_context"]
        if not isinstance(career, dict):
            raise ValueError("career_context must be an object")
        for key in ("profession", "experience_level"):
            if not isinstance(career.get(key), str) or not career[key].strip():
                raise ValueError(f"career_context.{key} must be nonempty text")
        for key in CAREER_LISTS:
            items = career.get(key)
            if not isinstance(items, list) or any(not isinstance(x, str) or not x.strip() for x in items):
                raise ValueError(f"career_context.{key} must be a list of nonempty strings")
    if "compensation_preferences" in data:
        pay = data["compensation_preferences"]
        if not isinstance(pay, dict):
            raise ValueError("compensation_preferences must be an object")
        if pay.get("base_pay_period") not in ("annual", "monthly", "hourly"):
            raise ValueError("base_pay_period must be annual, monthly or hourly")
        if pay.get("variable_pay") not in ("acceptable", "required", "excluded", "unspecified"):
            raise ValueError("variable_pay must be acceptable, required, excluded or unspecified")
        for key in ("minimum_base", "target_total_annual"):
            value = pay.get(key)
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise ValueError(f"{key} must be a nonnegative finite number")
        if not isinstance(pay.get("notes"), str):
            raise ValueError("compensation_preferences.notes must be text")
        expected_floor = pay["minimum_base"] if pay["base_pay_period"] == "annual" else 0
        if (data.get("salary_floor") or 0) != expected_floor:
            raise ValueError("salary_floor must equal annual minimum_base, or be 0 for hourly/monthly pay; never infer a conversion")


def compensation_review(
    text: str, job_url: str, profile: Mapping[str, Any],
) -> tuple[list[str], list[str], bool]:
    """Return blockers, questions, and whether to bypass the annual-dollar heuristic.

    Variable earnings cannot prove base pay. Nonannual/cross-currency amounts and
    total-earnings targets require a documented posting-specific review.
    """
    validate_career_fields(profile)
    reviews = profile.get("compensation_reviews", {})
    if not isinstance(reviews, dict):
        raise ValueError("compensation_reviews must be a mapping keyed by exact posting URL")
    if job_url in reviews:
        review = reviews[job_url]
        if (not isinstance(review, dict) or review.get("status") not in ("meets_preferences", "below_preferences")
                or not isinstance(review.get("evidence"), str) or not review["evidence"].strip()):
            raise ValueError("Compensation review requires status and nonempty evidence")
        try:
            dt.date.fromisoformat(review.get("reviewed_on", ""))
        except (TypeError, ValueError) as exc:
            raise ValueError("Compensation review requires reviewed_on YYYY-MM-DD") from exc
        blockers = ["verified compensation does not meet candidate preferences"] if review["status"] == "below_preferences" else []
        return blockers, [], True
    pay = profile.get("compensation_preferences", {})
    needs_review = bool(VARIABLE_PAY.search(text)) or (
        bool(pay) and (pay["base_pay_period"] != "annual" or pay["target_total_annual"] > 0
                       or pay["variable_pay"] in ("required", "excluded")
                       or profile.get("salary_currency", profile.get("currency", "USD")) != "USD"
                       or (pay["minimum_base"] > 0 and not re.search(r"\$\s*\d", text)))
    )
    if needs_review:
        return [], ["Verify compensation against this candidate's base pay, pay period, currency, variable-pay policy and total-earnings target separately; OTE/commission is not guaranteed base pay. Record the exact-posting evidence in compensation_reviews."], True
    return [], [], False
