Run this checkout's configured job search. Read README.md, run_preferences.json,
search_rules.md, candidate_evidence.json and both candidate profiles first. Use
only this candidate's confirmed profession, titles, capabilities, languages, metro, countries and
work preferences. Keep the total site list at or below 200.

Read career_context before choosing questions, search terms or adjacent roles.
Use profession-relevant responsibilities, results, credentials and transferable
skills. Empty tools lists are valid. Never inject programming/cloud requirements
or an engineering seniority ladder into another profession. For legacy profiles,
ask only missing career-context questions and update private files in place.

Verify the configured timezone/run date. Before discovery, follow README.md's
"Employer expansion and weekly maintenance" procedure. Read
outputs/employer-research-state.json. If setup expansion is missing, complete it
and review the expanded shortlist with the candidate before the first search.
On the first run of each candidate-local calendar week, recheck preferred and
failed sources plus the oldest unchecked quarter; research 20–30 new prospects.
Use official role/responsibility and hiring-location evidence, not snippets alone. Keep
pending prospects out of runnable files; no-match weeks do not justify removal.
Ask before removing a user-selected employer. Synchronize companies.yml,
job_sources.yml, ats_registry.yml, startup_watchlist.yml and setup.answers.json;
validate the 200-site ceiling with scripts/setup_jobagent.py --check via the
project Python wrapper. Record counts, evidence, changes, failures and next themes
in outputs/YYYY-MM-DD-employer-maintenance.md. Advance the weekly ledger date
only after maintenance and validation complete. If web research is unavailable,
report incomplete maintenance and search only previously validated sources.
Python scanning alone does not perform employer expansion.

Generate the dated plan and execute its
discovery, local application-history reconciliation and strict-review steps.
External tracking remains disabled unless this candidate has explicitly approved
and tested an adapter and its recurring read scope. Never discover databases or
reuse another environment's tracker settings. Report tracker failures; do not
replace missing history with an empty list. Analytics publication needs separate
write authorization and is disabled by default.
Open LinkedIn Jobs in the internal browser for additional hits if available;
otherwise report that gap and provide search links. Resolve all discoveries to
live official employer/ATS pages. Inspect complete required qualifications, salary
currency, location restrictions and language/authorization evidence before review.
Review guaranteed base pay separately from commission/OTE, pay period and total
earnings targets in compensation_preferences. Resolve compensation holds with
evidence in exact-URL compensation_reviews; remove stale reviews when preferences
or posting terms change. Never infer annual conversions or use OTE as base pay.
Check required licenses and credentials by jurisdiction; preferred qualifications
alone are not blockers.
Ask about missing experience; never invent it or import another candidate's rules.

Report new actionable verified roles, gaps/questions, applied matches and source
failures. Keep unavailable sources distinct from zero matches. Preserve prior
outputs and exact-posting decisions. Never submit applications, send messages,
publish analytics or create documents without the relevant user authorization.
Only the strict dated resume-ready queue can authorize optional documents.
Stay quiet when results are unchanged and non-actionable; notify for meaningful
changes, failures or required user action.
