Run this checkout's configured job search. Read README.md, run_preferences.json,
search_rules.md, candidate_evidence.json and both candidate profiles first. Use
only this candidate's confirmed profession, titles, capabilities, languages, metro, countries and
work preferences. Keep the total site list at or below 200.

This prompt is the work performed by an existing heartbeat or a manual run; it
does not register a schedule. During interactive onboarding, finish README.md's
"Finish setup: create and verify the heartbeat" procedure after result acceptance
and scheduling approval. First complete its required cadence/output interview
checkpoint; ask missing questions interactively instead of treating configuration
defaults as candidate answers. Read saved interview_preferences for confirmed
runtime/site limits and report format, preserving explicit deferrals. Previously
confirmed preferences remain valid even if saved outside this object; ask only
for genuinely missing answers. In a manual
chat, confirm concrete limits for that run if unresolved. In an unattended run,
report unresolved required execution limits without starting an unbounded scan
or inferring consent. During a scheduled run, do not create another heartbeat,
change its cadence or reactivate a paused task. Report scheduler/configuration
mismatches as questions without treating saved preferences as proof of activation.

Read career_context before choosing questions, search terms or adjacent roles.
Use profession-relevant responsibilities, results, credentials and transferable
skills. Empty tools lists are valid. Never inject programming/cloud requirements
or an engineering seniority ladder into another profession. For legacy profiles,
ask only missing career-context questions and update private files in place.
For Project Management, use confirmed industries, project scope, delivery methods,
stakeholder responsibilities and credentials. Do not assume software delivery,
PMP certification, or equivalence with product/program management; confirm adjacent
titles against the candidate's experience and preferences.

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
Read application_tracking in candidate_evidence.json. Preserve the candidate's
local/install/connect choice; do not repeat an answered onboarding question or
install JobTracker during a scheduled run. If guided setup is incomplete, report
the saved next step and continue local discovery. If recurring tracker reads were
approved, perform the recorded, tested read/export conversion before local history
reconciliation. Otherwise report that external history was not refreshed. Never
interpret installation or a stored endpoint as automatic sync or write consent.
An optional tracker export or refresh failure must not end the whole run. Continue
independent discovery and review using valid local history, and label external
history as unchecked or not refreshed. If local history is missing or invalid,
report that reconciliation is blocked, preserve existing records, and complete
independent discovery; never create empty history to bypass the error. Finish the
available report with source/history limitations and the specific next action.
In an interactive setup chat, resume the next unanswered interview questions or
authorized onboarding stage instead of ending with an offer to continue. Follow
README.md's onboarding completion criteria; a scheduled run must not claim user
acceptance or reactivate an incomplete integration without permission.
When user input is needed in an interactive chat, use the supported interactive
question tool for the current mode and purpose, including result feedback and
schedule choices. If unavailable or failing, ask directly in chat. Present the
specific question before stopping; a status summary is not a request for input.
Preserve unanswered questions and wait before dependent work; never infer consent
from a suggested option or timeout. In unattended runs, record and notify the user
of required questions through the supported channel, then finish independent work
without starting a blocking interview or repeatedly notifying unchanged questions.
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

Finish every run with README.md's "End-of-run delivery: reports, resumes and cover
letters" procedure. Create the dated Markdown/HTML reports even when there are no
matches or a later document stage fails; deliver the preferred report format.
Report new actionable verified roles, gaps/questions, applied matches and source
failures. Keep unavailable sources distinct from zero matches. Preserve prior
outputs and exact-posting decisions. Reserve time within the approved run budget
for document production and verification; report any unfinished artifacts.

Read the candidate's standing document approval and run_preferences.json's
document_generation flag. When enabled and validated, produce the appropriate
resume and cover letter for each current strictly qualified, unapplied posting.
Do not ask again for recurring approval already given or stop with an offer to
make documents later. Only the current strict dated resume-ready queue, matching
review and reconciled application snapshot permit production. An empty queue
needs no documents; invalid/missing history or review is blocked, not empty.
Consult resume_sources in candidate_evidence.json and select the confirmed
validated template suited to the role; multiple versions may be current. Ask
about ambiguity interactively, or record it as pending in an unattended run.
Preserve originals. Never invent experience or use placeholder contact details.

For approval covering both document types, execute the dated plan's
produce_resumes.py command after strict review. That CLI
produces both resumes and cover letters and refreshes the HTML report. Inspect
both production manifests, actual DOCX files and rendered pages; verify truthful
role-specific content and links before reporting success. Honor a narrower saved
document choice with the corresponding producer instead of the combined CLI.
Reuse documents only
for the exact posting with still-current evidence, template and tailoring.
Report generated/reused files per posting and any blocked or pending artifacts.
If documents were declined/deferred, preserve that choice; if setup is incomplete
or generation fails, report the exact blocker and continue available reports.
Save a dated delivery summary with report and verified document links on every
run. Report delivery separately from document success. Never submit applications,
send messages, publish analytics or upload documents to a tracker without the
separate relevant authorization.
Stay quiet when results are unchanged and non-actionable; notify for meaningful
changes, failures or required user action.
