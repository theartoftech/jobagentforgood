# Job Agent

An assistant-guided job search you configure for your own experience, location and goals. Clone this repository, open it in Codex, Claude Code, Antigravity, or another coding assistant with local file and web access, and **paste this entire README into a new chat**. The assistant instructions below start the setup interview.

No model API key, paid job-search service, private server or external application tracker is required. Your assistant supplies the conversation, web research and browser access. The Python tools supply ATS discovery, search plans, deduplication, configurable screening and local reports. They never submit applications.

## Install

Install Git and **Python 3.11 or newer** (including pip and venv). A supported Python distribution from [python.org](https://www.python.org/downloads/) is sufficient. Windows users should use WSL with Python/Git/Bash for the commands below. macOS and Linux use a terminal with Bash. Public ATS requests also use `curl` where available; install it if your system does not provide it.

Clone the public repository:

```bash
git clone https://github.com/theartoftech/jobagentforgood.git
cd jobagentforgood
python3 -m venv .venv
scripts/jobagent_python.sh -m pip install -r requirements-dev.txt
scripts/jobagent_python.sh -m unittest discover -s tests
```

If a Homebrew Python fails with a `pyexpat` / `Symbol not found` error, repair/update Python and expat, or use a Python distribution with matching libraries. This is an environment issue; do not disable tests. The Bash wrapper supports the usual Homebrew expat library location if installed. On an affected Apple Silicon Homebrew installation, after confirming expat is installed, create the virtual environment with `DYLD_LIBRARY_PATH="$(brew --prefix expat)/lib" python3 -m venv .venv`, then install dependencies through the wrapper as above.

For job searching you do **not** need LibreOffice, Docker, a resume template, a LinkedIn export, or JobTracker. Optional Word-document production requires a verified DOCX source and LibreOffice plus Poppler (`pdftoppm`), or Docker with the renderer built from `docker/resume-renderer`. Document production has additional template requirements described below.

## Instructions for the assistant: start here

Treat this README as the user's request to set up this checkout and conduct their first job search. Work inside the clone. Read the implementation and local instructions before executing commands. Do not assume the user's identity, career, salary, country, language, technical stack, employer preferences or access to any connector.

1. Check the working directory, Python version, dependency installation and tests. Explain any installation issue clearly. Use the virtual environment for every command.
2. Check whether private configuration already exists. If it does, offer to continue or review that setup; never overwrite it or mix two candidates' data. The setup generator refuses overwrites. For a fresh candidate use a separate clone.
3. Interview the user in short groups of 2–4 questions, waiting for answers between groups. Start with their profession, desired work and experience level; adapt later questions to those answers. Resume answers already given. Explain why a missing answer matters. Save confirmed answers in ignored `setup.answers.json`, using `setup.answers.example.json` as the schema. Do not use sample text as candidate evidence.
4. Summarize the evidence, search boundaries, direct titles and adjacent titles. Get corrections before writing the runnable configuration. Distinguish professional experience, training, personal projects, limited exposure and skills the user must not claim.
5. Research employers in batches and expand beyond the user's seed companies before the first search, following the expansion procedure below. Review the expanded shortlist, generate private configuration, run a small first search, inspect actual results, and then offer the full search and scheduling setup.

### Interview questions

Ask all applicable questions; do not infer qualifications from a job the candidate likes.

- **Profession and direction:** What kind of work do you do, and what work do you want next? What responsibilities do you want to keep, change or avoid? What level of responsibility suits you? Record `career_context.profession` and `experience_level` in the candidate's words. For a career change, distinguish previous experience from the destination profession and identify transferable skills without claiming destination-role experience.
- **Resume and evidence:** Can you upload your resume or point to a local file? Copy it only into ignored `Source Docs/` with permission. If no resume is available, interview them about work history instead; discovery can still run. What name/email should local records use? What was your last role, scope, industry, level and employment period? What did you personally do, and what measurable outcomes can you substantiate? Which statements may be reused in cover letters? Do not invent years, metrics, degrees, employers or certifications.
- **Roles and strengths:** Which titles interest you? What activities do you do well, and what recent work demonstrates that? Which areas are limited exposure or training only? What should never be claimed? Are you seeking individual-contributor, management, entry-level or career-change roles? What adjacent roles would you consider? Propose adjacent titles with an evidence-based explanation and ask for confirmation before adding them. Strengths can be negotiation, patient care, customer service, scheduling, writing, craftsmanship or other relevant capabilities; they need not be technologies.
- **Employers and examples:** Which companies, industries and company sizes interest you? Which should be excluded? Share URLs of jobs you liked or applied to. Capture why they appealed; check live official postings. Keep already-applied jobs separate from merely interesting jobs, including exact URL/requisition, company, title, status and application date (unknown dates stay blank). Ask explicitly whether there are prior applications before recording an empty history.
- **Application tracking:** Explain that no separate tracker is needed: the assistant can maintain local application history from the user's confirmed updates. Ask whether they already use a tracker or would like one. If they have none, continue with local history; optionally suggest [JobTracker](https://github.com/theartoftech/jobtracker) for a dedicated application-tracking interface. Do not make installing it part of required onboarding. If they already use a system and want it connected, offer a user-provided export or ask permission for a specific read-only inspection. Follow the integration procedure below.
- **Location:** What city do you live in, and what major metro should the search use? Which surrounding cities are within your actual commute? Do you want onsite, hybrid, remote, or several? How much office attendance and travel is acceptable? Would you relocate, and where? Which countries may you legally work in? Is sponsorship required? Remote does not mean unrestricted worldwide work.
- **Language:** Which languages can you speak and write, at what professional proficiency? Which mandatory language requirements would be blockers? There is no default German rejection. Compare each posting's spoken/written requirements with the confirmed proficiency; ask about an unlisted required language rather than assume proficiency.
- **Terms:** What minimum guaranteed base pay, currency and pay period apply? Separately, is there an annual total-earnings target, and is commission/variable pay acceptable, required or excluded? Discuss commission-only work, quotas, ramp guarantees, bonuses, tips or overtime when relevant. OTE (on-target earnings) is not guaranteed base pay. Save these in `compensation_preferences`; never infer an annual conversion. What employment types, hours, shifts, clearance/licensing constraints or other dealbreakers apply? How should unpublished pay be handled? Unknown requirements stay questions.
- **Cadence and outputs:** What timezone, days and local time should searches run? What runtime/site budget do you prefer? Would you like results in Markdown/HTML? Are documents wanted later? Keep `schedule_enabled` and `document_generation` false during onboarding. Ask about optional networking exports or tracker integration only if wanted; never require them.

Store extra preferences and proficiency detail in `candidate_evidence.json` and `search_rules.md` after generation. Those files are authoritative for the assistant's full-posting review. The keyword screener does not fully interpret licensing, sponsorship, pay currencies, shifts, travel, or all natural-language requirements.

### Adapt the interview to the profession

Use the candidate's answers and actual target postings to choose follow-ups. These examples are prompts, not fixed career tracks or assumed qualifications:

| Work area | Relevant follow-ups |
|---|---|
| Sales / account management | B2B or B2C, industries, customer segments, prospecting versus renewals, territories, deal sizes, sales cycles, negotiation, quota attainment and account growth. Ask for substantiated results; do not require disclosure of confidential customer information. CRM tools matter only where relevant. |
| Customer service / hospitality | Customer channels, issue resolution, service volumes, escalation handling, service-quality evidence, shifts and languages. Ask about systems only when used or required. |
| Administration / operations | Scheduling, records, coordination, vendors, budgets, confidentiality, process improvements and scope of responsibility. Distinguish general administration from specialist payroll/accounting experience. |
| Healthcare / education / regulated work | Specialty, populations served, duties, current credentials, jurisdiction, expiry and required eligibility. Never infer a license from a title or degree. |
| Trades / field services | Work performed, equipment, certifications, safety responsibilities, work settings, travel and shifts. |
| Software / other technical work | Relevant tools, systems, design responsibilities and depth of actual experience, only for the candidate's chosen role. |

For any other profession, derive questions from its duties and requirements. Mixed careers may need several groups. Do not ask a salesperson about programming languages or cloud platforms unless their chosen role specifically requires them. A sales engineer's product knowledge and a software engineer's implementation experience are different evidence. A manager's skills must not be inferred from an individual-contributor title.

Save confirmed specializations, transferable skills, tools and credentials in the corresponding `career_context` lists; empty lists are valid. Put evidence and credential scope/expiry in `evidence` and detailed local notes. Populate `strong_keywords`, `secondary_keywords` and `do_not_claim` from this interview, not from a built-in profession vocabulary. Missing required qualifications remain questions; confirmed absent qualifications become gaps; preferred qualifications alone do not reject a role. Keep titles in the candidate's priority order and confirm adjacent roles explicitly.

New interviews include `career_context` and `compensation_preferences`. Existing private setups without them still work: ask only the missing questions and add confirmed fields in place without rerunning the overwrite-refusing generator. Both fields are copied into the discovery profile, workflow profile and candidate evidence. For annual base pay, set `salary_floor` equal to `minimum_base`. For hourly/monthly base pay, keep `salary_floor: 0`; the stated period and minimum remain authoritative for human review. Zero means no minimum for that field, not consent to commission-only work.

Commission/OTE disclosures, hourly/monthly preferences, non-USD pay, total-earnings targets and required/excluded variable-pay policies trigger a compensation question and hold document production. The annual-dollar heuristic cannot clear these cases. After inspecting the official posting and resolving unknowns with the candidate, record `compensation_reviews[exact_posting_url]` in the private workflow profile with `status` (`meets_preferences` or `below_preferences`), nonempty `evidence` covering each applicable pay constraint, and `reviewed_on` (`YYYY-MM-DD`). This is an evidence record, not permission to assume a pay package. Recheck it when the posting or preferences change, removing stale entries. Rerun strict review after recording the result. Qualification and other eligibility checks still apply.

### Research the search sites and roles

Use live internet searches informed by the confirmed titles, skills, languages, country, metro and work model. Start with the user's companies, then find employers hiring for direct and agreed adjacent roles. For each employer inspect its official careers page and current role/location evidence; save `name`, `careers_url`, `evidence_url`, `reason`, and `verified_on` (YYYY-MM-DD).

Use **at most 200 distinct search sites total**, including LinkedIn and any supplementary boards or startup sites. The generator allows 1–199 deduplicated employer sites plus LinkedIn. Fewer well-supported sites are preferable to invented or irrelevant sites; 200 is a ceiling, not a quota. Deduplicate shared company boards. Record inaccessible or unverified prospects separately in local notes, not as verified companies. Never make up ATS endpoints. Explain source coverage and gaps.

Open [LinkedIn Jobs](https://www.linkedin.com/jobs/) in the assistant's **internal browser** for additional hits. Let the user sign in themselves when needed. If the assistant lacks an internal browser, say so and let the user review the search links and provide URLs. Login or browser unavailability must be reported explicitly; it does not block official ATS discovery. Resolve useful LinkedIn or aggregator findings to live employer/ATS pages before recommending them. Do not apply, message recruiters, scrape private profiles, or bypass site access restrictions.

Put verified employer entries in `setup.answers.json`. After generation, populate `ats_registry.yml` only with verified supported ATS URLs; unsupported websites remain browser-assisted search tasks. Move startup employers between the company list and optional watchlist without increasing the total site budget. Keep `job_sources.yml` synchronized and do not add a second copy of an existing site. Run `scripts/jobagent_python.sh scripts/setup_jobagent.py --check` before each search; the check includes ATS URLs, so reduce the shortlist if adding boards would exceed 200.

### Employer expansion and weekly maintenance

The user's named companies are seeds, not the completed search universe. **Expand during setup before the first search**; the later 1–3-company smoke test limits execution, not employer research. The assistant performs this research with web access. The Python scanners search configured sites and do not independently discover new employers. A scheduler without web-enabled assistant execution cannot maintain this list; report that limitation instead of claiming automatic expansion.

During setup, work in batches of **20–30 prospective employers** across the candidate's preferred industries, direct and approved adjacent roles, local market and eligible remote locations. Use search engines and public job boards to discover names, then verify each on its official careers site or linked ATS. Research multiple batches toward the remaining 200-site capacity unless the user requests a smaller list. Count unique configured URLs, including LinkedIn, supplementary boards and ATS mappings; 200 sites does not necessarily mean 200 employers. Never fill a quota with unsupported or irrelevant companies.

For each prospect, record the employer name, official careers URL, evidence URL, verification date, why its roles, responsibilities and hiring geography fit, source access method, and any limits. Prefer current relevant postings. An official department/team page relevant to the candidate's profession plus explicit hiring-location or work policy can justify monitoring an employer with no current matching vacancy; label that evidence accurately. Include employers across relevant industries, not just technology companies. A careers homepage alone, a search snippet, or an unrelated vacancy is not evidence of fit. A suitable employer is not an approved job: each posting still passes compensation, experience, language, commute and other candidate checks.

Keep a private research ledger at `outputs/employer-research-state.json` with `last_setup_expansion_on`, `last_weekly_maintenance_on`, `batches`, `employers` and `deferred_queries`. Each batch records its date, search themes, prospects considered, additions and exclusions. Employer entries record `name`, `careers_url`, `evidence_url`, `reason`, `verified_on`, `status` (`active`, `monitor`, `pending_verification`, `excluded`, or `retired`), `priority`, `access_method`, `last_checked_on`, `consecutive_access_failures` and `notes`. Keep pending, excluded and retired employers out of runnable source files. Do not rewrite history or discard application records when changing sources.

Prioritize user-selected employers, then sources with current relevant opportunities, then evidence-backed monitoring sources. If capacity is not reached, keep researching until two consecutive batches produce fewer than three defensible additions, the relevant search themes are exhausted, or the user's stated research budget is reached. Report the actual counts, remaining capacity, unresolved prospects and stop reason; a smaller justified list is acceptable, an unexplained seed-only list is not. Summarize the expanded shortlist for user review before generating runnable configuration. After setup, update existing private files in place; never rerun the overwrite-refusing generator to refresh a candidate.

On the first scheduled run of each candidate-local calendar week, before job discovery:

1. Read the ledger and previous source-error reports. Recheck preferred employers, failed/changed sources, and the oldest unchecked quarter of other active/monitor sources. Record real checks; never advance a verification date without accessing its evidence. A weekly schedule performs this on every run; more frequent schedules perform it once per week.
2. Research another batch of 20–30 prospects using uncovered industries, locations and approved role families. Below capacity, add verified relevant sources. At capacity, compare prospects with the weakest sources and propose replacements when they improve fit. Never remove a user-selected employer without asking; do not retire a source solely because it has no current matches or a temporary access failure. Keep failures visible, and investigate repeated failures for redirects or replacement official URLs.
3. Synchronize `companies.yml`, `job_sources.yml`, `ats_registry.yml`, `startup_watchlist.yml` and the retained company list in `setup.answers.json`. Review additions against candidate exclusions and the site ceiling before writing. Preserve posting-specific decisions, application history and overrides. Run `scripts/jobagent_python.sh scripts/setup_jobagent.py --check`; if it fails, repair configuration before discovery.
4. Write `outputs/YYYY-MM-DD-employer-maintenance.md` with before/after company and distinct-site counts, additions, pending prospects, proposed retirements/replacements, evidence links, access failures and next research themes. Update `last_weekly_maintenance_on` only after the bounded maintenance pass and validation complete. If research tools are unavailable or the pass is interrupted, preserve a partial record and report the gap; existing validated sources may still be searched, but do not claim maintenance completed.

Include meaningful source additions or losses in the run summary. Do not notify merely because verification dates changed. Keep all candidate-specific research and configuration ignored by Git.

### Generate the candidate's files

Once the user has reviewed the interview summary and employer shortlist:

```bash
scripts/jobagent_python.sh scripts/setup_jobagent.py --answers setup.answers.json
```

The checked-in example contains empty required fields and cannot be run as a candidate profile. The generator validates types, required answers, timezone, URL format, site limit, duplicates and conflicting languages before writing. It refuses to replace any existing output. It does not itself verify that a website is live; the assistant must inspect the saved evidence URLs.

| Private file | Contents and interview source |
| --- | --- |
| `setup.answers.json` | Confirmed interview answers; kept for audit/resumption |
| `candidate_profile.yml` | Direct/adjacent titles, skills, exclusions, countries, commute, work models, freshness and compensation |
| `candidate_workflow_profile.yml` | Confirmed strengths, limited exposure, do-not-claim skills, salary, language/location gates and exact-posting gap answers |
| `candidate_evidence.json` | Identity, last role, truthful reusable statements, resume path, authorization and other interview facts |
| `companies.yml` | Verified, reasoned employer shortlist |
| `job_sources.yml` | Employer sites plus LinkedIn; maximum 200 distinct sites across all search inputs |
| `ats_registry.yml` | Initially empty; add only verified ATS board mappings for selected employers |
| `startup_watchlist.yml` | Initially empty; optional candidate-specific rotating employer list |
| `manual_job_urls.yml` | Official posting URLs found by the candidate/browser, excluding aggregator-only leads |
| `job_overrides.yml` | Initially empty; later explicit posting-specific skip decisions or dated overrides |
| `applied_jobs.json` | Local application history; updates require the candidate's actual application evidence |
| `search_rules.md` | Evidence/verification rules plus candidate-specific constraints and unresolved preferences |
| `run_preferences.json` | Timezone, proposed cadence, freshness and disabled-by-default scheduling/documents |
| `resume_templates.json` | Initially empty; populate only for validated optional DOCX templates |
| `.env.local` | Optional local environment settings; no source/API credentials required |

All these files, resumes and `outputs/` are ignored. The filename is **`candidate_profile.yml`**, not `candidate_profile.yaml`. Run `git status --short` after setup; private answers and generated files must not appear as additions. Never force-add them.

### First run: prove the setup with real results

1. Generate the plan:

   ```bash
   scripts/jobagent_python.sh scripts/setup_jobagent.py --check
   scripts/jobagent_python.sh scripts/search_jobs.py --out outputs
   ```

2. Read the dated plan. For the first run select 1–3 researched employers, run official discovery, and perform the LinkedIn/browser pass. Use the plan's commands with `--limit-companies 3 --no-rotation` on discovery. Use `freshness_days` from `run_preferences.json`; do not substitute an inherited default. The local scripts date outputs using the operating-system date: verify it agrees with the configured timezone before starting and restart in a new output directory if the date changes during a run.
3. Inspect the discovered JSON, errors and live official postings. Correct missed employer board mappings. Record employment/authorization/language/experience gaps in `candidate_workflow_profile.yml` before strict review. `do_not_claim` is candidate-wide; `gap_resolutions` is keyed by exact posting URL. Supported answers are `do_not_claim`, `limited_exposure: explanation`, `professional_evidence: explanation`, or posting-specific `posting_false_positive: explanation`. Never mark a required gap resolved based only on training or a high score.
4. Reconcile the local applied history and run the strict reviewer using the dated commands in the plan. No SSH server is needed. Open `outputs/YYYY-MM-DD-workflow-review.html`; show the candidate recommended roles, unresolved questions, rejected roles and reasons, already-applied matches, source failures and coverage. A plan or empty report template does not count as a completed live search. Zero matches is valid; failed/unavailable sources must not be presented as “no jobs.”
5. Review several results with the user. Confirm titles, location, language and qualifications actually fit. Adjust private configuration from their answers. Then run the remaining chosen sites. Give URLs and clear next actions, never claim an application was submitted.
6. After the first run is accepted, confirm the proposed cadence and configure the assistant's supported scheduler with `daily_job_search_prompt.md`, the absolute clone path and the chosen timezone. If no scheduler exists, say so and provide a manual-run reminder. Writing `run_preferences.json` alone does **not** schedule anything. Record the scheduler ID and next run only after successful creation. Notify on new actionable roles, meaningful changes, failures or questions; do not spam unchanged status.

### Optional capabilities

The ATS adapters include Workday, Greenhouse, Lever, SmartRecruiters, Workable, Ashby, ADP, iCIMS and some employer-specific parsers. Website coverage varies. The sharded scanner supports daily listing checks, rotating deep scans and carried-forward failures. The reviewer deduplicates postings, carries unresolved jobs forward, separates required/preferred gaps and excludes applied requisitions.

Resume and cover-letter production is optional and deliberately separate from first-run discovery. Existing DOCX tooling expects specific document structure: template headline, summary prefix, checksum and a two-column contact header for cover-letter sender extraction. Arbitrary uploaded PDFs/DOCX files are **not** automatically compatible. Inspect and adapt a copy with the user's approval, preserve the original, populate `resume_templates.json` using `resume_templates.example.json`, set `default_resume_template` and contact settings, and validate rendering before enabling production. Cover-letter statements come only from `candidate_evidence.json`. Never claim document support has passed without actually rendering and inspecting the output.

Only `outputs/YYYY-MM-DD-resume-ready-jobs.md` can authorize documents; prior applications remain excluded. Build the optional isolated renderer with:

```bash
docker build --tag jobsearchagent-libreoffice-renderer:1.0.0 docker/resume-renderer
```

Local networking reports can use a voluntarily supplied LinkedIn export. Notes are drafts; nothing is sent automatically. The deterministic runner under `poc/` is an advanced experiment with additional integration requirements, not the default setup path.

### Optional application tracker or database

**No tracker? Start here:** continue using Job Agent's local `applied_jobs.json`. Tell the assistant when you actually apply, including the posting URL and application date, so it can update your history and avoid recommending the same application again. A separate website, database or account is not needed for your first search or later runs.

If you would like a dedicated interface, consider **[JobTracker](https://github.com/theartoftech/jobtracker)**, a separate self-hosted application for tracking applications, notes and resume/cover-letter attachments. It is optional and requires its own setup. Its current README includes maintainer-specific deployment examples; the assistant must review the current installation instructions and adapt hostnames, paths, authentication and deployment choices to the user's environment. Do not copy the maintainer's settings or assume that launching the static UI enables API-backed saves. Offer setup help only if the user wants it, and continue Job Agent onboarding independently. Installing JobTracker does not automatically authorize Job Agent to access it; connecting the two follows the permission and compatibility checks below.

**External tracking is disabled by default.** `mark_applied_jobs.py` reads local `applied_jobs.json` even if old tracker environment variables are present. Missing or invalid local history is an explicit error; it never triggers an external connection or silently assumes no prior applications. `publish_skill_gap_analytics.py` exports a local artifact by default and does not publish it.

For a user who wants their own system connected, the assistant must:

1. Ask which website, database, API or export contains their applications. Prefer an export or documented read-only API. Do not probe local networks, search for databases or read credentials to discover a tracker.
2. Explain the proposed connection, specific database/schema or API scope, and minimal fields needed. Obtain explicit permission before accessing it. Use user-supplied connection settings and a read-only account; keep secrets in ignored local configuration, never chat or tracked files. Permission to inspect a schema does not authorize ongoing reads or writes.
3. Inspect only the approved schema/metadata first, then request permission for any sample records needed to verify field mapping. Different systems need different adapters. Do not run the legacy `jobs.data` query against an unknown database or infer that a table with “jobs” in its name tracks applications.
4. Map confirmed application records to the existing local snapshot contract: top-level `fetched_at` (ISO timestamp), `ssh_host` (a nonempty source label retained for compatibility, such as `approved-export`), and `jobs`. Each job uses string fields `company`, `title`, `job_url`, `status`, and `applied_date`. Preserve exact official URLs/requisition IDs. Confirm status semantics: a saved or interesting job is not an application. Use `interested` for such records; do not pass unknown source statuses through as proof of application. Leave unknown dates blank. Preserve existing local application evidence when importing.
5. Show the mapping and a small reconciled sample for review. Record the source, mapping, approved read scope, refresh cadence and consent in ignored `candidate_evidence.json`. Ask separately whether subsequent searches may refresh this source. Until approved and tested, keep the local workflow and report that external history has not been checked. Connection failures must remain visible; never silently replace history with an empty list.

No universal database connector is included. A different schema needs a tested adapter or a converted export into `applied_jobs.json`; database access alone does not make it compatible. Read-only integration does not grant permission to publish analytics or update the user's tracker.

The retained legacy JobTracker adapter supports only a SQLite `jobs` table with a JSON `data` column containing `company`, `title`, `status`, `jobUrl`, and `appliedDate`. After read permission and schema compatibility are confirmed, it requires `--enable-jobtracker-read`, plus an explicit `--ssh-host` and `--jobtracker-db-path` (or their `JOBTRACKER_SSH_HOST` / `JOBTRACKER_DB_PATH` environment settings). SQLite opens in read-only mode. Do not combine this adapter with `--local-applied`.

Analytics writes require separate user approval and an endpoint compatible with this project's import contract, followed by `--publish` and `--tracker-url` (or `JOBTRACKER_ANALYTICS_URL`). The optional SSH publication path additionally assumes the legacy Kubernetes deployment and secret layout; it is not a generic database connector. Flags record a deliberate invocation; the assistant must obtain the user's actual permission before adding them to any command or schedule.

## Development and release validation

```bash
scripts/jobagent_python.sh -m unittest discover -s tests
scripts/jobagent_python.sh -m coverage run --source=scripts -m unittest discover -s tests
scripts/jobagent_python.sh -m coverage report
```

Tests must use synthetic profiles and temporary directories, not local candidate inputs. Keep server changes at 90% coverage or higher; measure new onboarding logic independently as well as reporting full-suite coverage. Never label a mocked ATS test as a live search.

Profession regression cases cover sales, customer service, administration and nursing alongside existing technical profiles. They exercise candidate-owned strengths, required versus preferred qualifications, optional tools, compensation holds and a fresh sales setup through mocked ATS discovery, local history and HTML review. These checks do not replace a real candidate walkthrough or establish universal profession coverage.

For the maintainer's acceptance test: prepare the sanitized public branch, push it explicitly, clone that branch into another directory, install from this README, and paste this README into a new chat. Complete a fresh interview and first live search there. Verify private files stay ignored and no original-candidate preference appears. Local unit/integration results do not replace this human walkthrough.

**Publication and history:** deleting a private file in a normal branch does not remove it from Git history. Publish a reviewed clean-history snapshot to a separate public repository/branch without merging private history. Making an existing repository public exposes its other branches and history too. Inspect the exact release tree and history for personal files and credentials before publishing; do not push tags or old branches with it.
