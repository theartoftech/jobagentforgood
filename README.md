# Job Agent

Job Agent helps you find jobs that fit your experience, location and goals. An AI assistant guides you through setup, asks about the work you want, and helps you review the results. It never submits applications for you.

## Start here — no coding experience needed

You need an AI assistant that can work with files and run commands on your computer, with web access for research. Examples include Codex, Claude Code and Antigravity; available features depend on your installation. A chat that can only exchange messages cannot complete the setup on its own. You do not need a separate model API key or a job-tracking account.

1. **Open your assistant.** If you do not have one installed, get help installing your chosen assistant first. Job Agent does not install the assistant itself.
2. **Open a project chat.** If you already downloaded Job Agent, open that folder. Otherwise, create an empty folder called **Job Agent** in Documents, open it in your assistant, and start a chat there. The assistant will help download the project and, on Windows, choose the final working folder after setup.
3. **Copy and send this message:**

```text
Help me set up Job Agent and run my first job search.

If this folder contains Job Agent, read its README.md. Otherwise, read
https://github.com/theartoftech/jobagentforgood/blob/main/README.md
and help me download the project into a suitable folder without overwriting anything.
Follow the section “Instructions for the assistant: start here”.

First ask whether I use Windows, Mac or Linux, and check what is already installed.
Do the setup work you can safely do yourself. When I need to do something,
give me just one step, tell me exactly where to click or paste, and wait for my reply.
Do not give me a full page of commands. Explain unfamiliar terms in plain language.
Help me resume after a restart. Ask about optional JobTracker separately;
I can start searching without it. Then interview me and show me my first results.
Keep going through the interview, setup and first search. If an optional tracker
export or connection is unfinished, record it and continue the steps that do not
depend on it. Ask the next interview questions instead of stopping to ask whether
I want to continue. Pause only for an answer, permission or action you actually
need, or if I ask you to stop. Do not call setup complete until we review real results.
Whenever you need my input, ask an interactive question using your question tool
if available, with simple choices when useful. Use this throughout setup, reviews
and scheduling, not just the opening questions. If no question tool is available,
ask a clear question directly in chat and wait for my answer.
Invite me to attach one or more resumes in chat instead of asking me to type file
paths. Different versions may emphasize different work, such as consulting or
development; ask what each version is for and keep those distinctions.
Before finishing the interview, ask me about search frequency, timezone, days/time,
time and site limits, report format, and recurring resume/cover-letter production. Use small
groups of interactive questions; do not silently choose these preferences for me.
End each run with reports and the appropriate tailored resume and cover letter
for each qualified, unapplied job. Help validate my document setup before enabling
this recurring step. Report missing inputs or failures instead of silently skipping
documents; never submit applications.
After we review the first results, confirm my search cadence and create the
recurring heartbeat using your supported scheduling tool if I choose automatic
searches. Verify it exists and is active; saving preferences alone is not scheduling.
```

**You can stop reading here.** The rest is reference material for your assistant. You do not need to install Python, learn Git commands, or work through the Windows instructions by yourself before starting the chat.

On Windows, the assistant may help install a Windows feature called **WSL** and an app called **Ubuntu**, which provide the environment Job Agent runs in. You may need to approve an installation and restart your computer. If you choose the optional JobTracker app, there is an additional Docker installation. You can leave that for later and track applications in Job Agent's local files instead.

If your assistant cannot open the web link, open this README yourself and copy everything below **Instructions for the assistant: start here** through the end into that project chat. If it cannot access files or run commands, it should explain that limitation and guide you through the next step; it must not claim setup is complete.

<details>
<summary>Manual installation reference — for the assistant or users who prefer commands</summary>

## Install

Install Git and **Python 3.11 or newer** (including pip and venv). On macOS/Linux, use a terminal with Bash; a supported Python distribution from [python.org](https://www.python.org/downloads/) is sufficient. **Windows users: follow [Windows setup with the assistant](#windows-setup-with-the-assistant) below first.** It covers installing WSL 2, Linux Python/Git and, only if you choose JobTracker, Docker Desktop. Run the Bash commands below inside Ubuntu on Windows. Public ATS requests also use `curl` where available; install it if your system does not provide it.

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

</details>

The assistant reads the instructions below. You can use the short message above, or paste everything below the following heading into a chat with access to the project folder.

## Instructions for the assistant: start here

Treat these instructions as the user's request to set up Job Agent and conduct their first job search. Read the full README, including collapsed reference sections. If the project has not been downloaded, help obtain the public repository after checking the selected folder and required tools; never overwrite an existing checkout or candidate's files. On Windows, establish WSL and its final Linux project folder before cloning there. Once available, work inside the clone and read the implementation and local instructions before executing project commands. Do not assume the user's identity, career, salary, country, language, technical stack, employer preferences or access to any connector.

### How to guide someone who is not technical

Start with a short welcome and one question: **“Are you using Windows, Mac or Linux?”** Use an answer already supplied rather than asking again. Inspect the environment to verify the answer and identify what is already installed. Do not start by listing prerequisites, asking the user to clone a repository, or sending all the commands below.

- **Do the routine work.** Use your available tools to check files, download the project, install project dependencies and run checks within the user's authorized setup. Confirm your actual access; do not assume a Windows app can execute commands inside Ubuntu. When user action is needed, give one action and wait for the result. Do not ask the user to repeat a check you can perform yourself.
- **Make each instruction concrete.** Say which app to open, how to find it, what to click or paste, and what they should see. For example: “Click Start, type PowerShell, right-click Windows PowerShell, and choose Run as administrator. Tell me when the window opens.” Only then provide the single command needed. When switching to Ubuntu, explicitly say to open Ubuntu from Start; never expect the user to recognize a shell from its prompt.
- **Explain only what matters now.** Describe WSL/Ubuntu as the environment Job Agent needs on Windows, Python as a program that runs the search tools, and Docker as a program needed for the optional tracker. Do not make the user choose distributions, interpreters, virtual environments, ports or database schemas without explaining a concrete need. Use the documented defaults when appropriate.
- **Check before advancing.** Ask what happened or inspect the result yourself. If something fails, explain the error in plain language and give the next corrective step. A missing administrator permission or unavailable assistant tool is a setup blocker, not a reason to claim success. Users enter passwords locally; never request passwords or secrets in chat.
- **Plan for restarts.** Before a restart, tell the user how to reopen the assistant and this chat, which steps are complete, and the exact next step. Ask them to return with “I'm back”; then recheck the environment. If a new project folder/chat is required, supply a short handoff with completed steps and the next action, without credentials or candidate answers. Do not make them start the interview over.
- **Separate optional features.** Ask about JobTracker in plain language: “Would you like a separate app to track applications, or keep a simple history here? You can add the app later.” Explain the additional installation before proceeding. Do not install Docker during basic job-search setup unless the user chooses a feature that needs it. Keep document production and scheduling for their later workflow stages.

The command blocks below are a reference for you, not a checklist to dump into chat. Success means the user reaches a verified working setup and real first-search results, not that you supplied installation instructions. The Windows flow still needs a real Windows/nontechnical-user walkthrough; do not call these wording changes proof of usability or Windows compatibility.

### Ask interactively whenever user input is needed

Use the assistant's supported interactive question tool whenever it is available for the current mode and purpose. This applies throughout onboarding: installation checks the user must perform, interview answers, summary and employer-shortlist corrections, tracker choices, qualification gaps, first-result review, and scheduling. Follow the tool's limits and permission rules; do not change modes or use an unrelated onboarding/approval tool merely to display a form. If no suitable question tool is available or it fails, ask the same concrete question directly in chat. Never silently skip the question.

Ask 1–3 short questions at a time (or fewer if the tool requires it). Offer clear choices for decisions while allowing a free-text correction; use free text for experience, job titles and other answers that should not be constrained. A suggested choice is not an answer or permission. Do not request passwords, file uploads or screenshots through a text-only question tool; use the chat's normal attachment flow where needed.

**Resume requests belong in the main chat with attachment support, not a text-only question card.** Invite the user to attach one or several files using the app's attachment control or drag-and-drop where supported. Do not require them to type filenames, folders or full paths. Use an already attached file without asking for it again. Question cards can ask which attached version fits a target role; they must not substitute a path question for an upload. If attachments are unavailable, explain that and offer pasted resume text or work-history questions; a local file location is an optional route only if the user prefers it.

When an onboarding stage is waiting for the user, **actually present the question before ending the turn**. A report link, status summary, “awaiting your input,” or “let me know if you want to continue” is not a question. Save the pending question and the stage it blocks in the progress record. Wait for the answer before dependent work; an asynchronous question can remain pending while you perform independent work. Do not mark a stage answered after a timeout, re-ask a still-pending question on each update, or repeat questions already answered. After receiving the answer, save it and advance to the next authorized action or unanswered question.

Examples of questions at later checkpoints:

| Checkpoint | Interactive question |
| --- | --- |
| Interview summary and employer shortlist shown | “Are these preferences and companies correct, or what should I change?” Choices: Looks correct / I have changes. |
| Optional tracker export unavailable | “What job titles are you interested in?” if that interview answer is still missing; keep the tracker issue recorded separately. |
| First results shown | “How well do these roles fit?” Choices: Good fit / Some changes needed / None fit. Ask what needs changing when appropriate. |
| Scheduling after results are accepted | “Would you like me to create a recurring job-search heartbeat here?” Choices: Create heartbeat / Run manually / Decide later. Collect or confirm days, time and timezone, then actually create and verify the approved heartbeat using the procedure below. If the user already approved the exact cadence and creation, proceed without asking again. |

Do not manufacture questions merely to keep a conversation open. If no input is needed, continue the authorized work. If the user explicitly stops or onboarding is complete, close with its actual status. For unattended scheduled runs, record and notify the user of a specific required question through the supported channel; complete independent work without assuming an answer. Do not launch an interactive interview or wait indefinitely in an unattended process.

### Setup sequence

1. Identify the operating system and terminal before running commands. On Windows, walk the user through **Windows setup with the assistant** below, including missing WSL/dependencies; do not merely tell them to install prerequisites and return later. Check the working directory, Python version, dependency installation and tests. Explain any installation issue clearly. After creating the virtual environment, use it for every project Python command.
2. Check whether private configuration already exists. If it does, offer to continue or review that setup; never overwrite it or mix two candidates' data. The setup generator refuses overwrites. For a fresh candidate use a separate clone.
3. Interview the user in short groups of 1–3 interactive questions, waiting for answers between groups. Start with their profession, desired work and experience level; adapt later questions to those answers. Complete **Required checkpoint: cadence and output preferences** before presenting the final interview summary or generating configuration. Resume answers already given. Explain why a missing answer matters. Save confirmed answers in ignored `setup.answers.json`, using `setup.answers.example.json` as the schema. Do not use sample text as candidate evidence.
4. Summarize the evidence, search boundaries, direct titles and adjacent titles. Get corrections before writing the runnable configuration. Distinguish professional experience, training, personal projects, limited exposure and skills the user must not claim.
5. Research employers in batches and expand beyond the user's seed companies before the first search, following the expansion procedure below. Review the expanded shortlist, generate private configuration, run a small first search, and inspect actual results with the user. Incorporate their feedback, then continue the remaining chosen sites and confirm the scheduling choice as described in **First run: prove the setup with real results**. Do not stop at an offer to continue work already requested.

### Continue until onboarding is finished

The initial setup request authorizes the interview, routine setup and first search. **An unfinished optional tracker export or connection does not pause that work.** If tracker setup cannot proceed, briefly state what is pending and ask the next unanswered interview questions in the same response. Do not end with only “we can continue,” “let me know when you are ready,” or an offer to do the next already-requested step. After each answer, carry out the next authorized step or ask the next required question.

Keep a short progress record in ignored `outputs/onboarding-progress.json` once local file access is available. Track installation, interview, employer research, configuration, first search, result review, full search, document setup/delivery, scheduling and optional tracker setup separately. For each stage record `status` (`not_started`, `in_progress`, `waiting_for_user`, `blocked`, `complete`, `declined`, or `deferred`), evidence/output paths, any blocker, and `next_action`. Record only actual progress, without secrets. This is an assistant-maintained checkpoint, not an automatic installer or scheduler. Before the checkout is available, keep the checkpoint in chat; resume from it after a restart rather than repeating completed work.

- **Missing optional export or tracker access:** Record the specific missing item and continue the interview, employer research and available discovery. Use existing valid local application history for reconciliation and label external history as unchecked or not refreshed. Do not access the tracker without the required permission, treat an unanswered permission request as consent, or invent an export. Ask explicitly about prior applications; never create empty history just because the export is unavailable. Missing/invalid local history still needs correction before strict reconciliation, but it does not prevent collecting answers or researching employers.
- **Selected tracker still unfinished:** Preserve the user's choice and next step. Complete any authorized, actionable setup work and return to the remaining tracker step after first-result review. Do not silently abandon a requested integration or call it connected. Ask for the particular input/action needed, or let the user explicitly defer/decline it; an unavailable dependency stays visibly blocked.
- **Required interview answer, correction or permission:** Ask the specific question and wait for that answer before dependent work. Continue independent authorized work where possible. Keep the interview in short groups; finishing the workflow does not authorize guessing candidate facts, skipping summary/shortlist review, accessing private data, enabling a schedule or submitting applications.
- **Installation failure or unavailable tool:** Explain the exact blocker and next recovery action. Complete unaffected interview/research work. If every remaining step depends on the user or an unavailable capability, state that setup is incomplete and what will resume it. Respect a user request to stop.

Before saying onboarding is complete, verify the interview and reviewed employer shortlist are saved, private configuration validates and remains ignored, and a real first search has produced a report the user has reviewed. Zero matches can be valid; a plan, empty template or all-failed discovery cannot establish a completed search. Incorporate the user's feedback, run the remaining chosen sites unless they explicitly defer, and resolve the schedule choice: either verify an approved schedule was created, record that the user declined/deferred it, or explain that scheduling is unavailable and provide manual-run instructions. Report core-search readiness separately from document delivery, tracker and scheduling status. List any blocked or deferred work with its next action instead of claiming everything is finished.

### Windows setup with the assistant

<details>
<summary>Windows technical reference — the assistant walks you through only the steps you need</summary>

The Windows path uses **WSL 2 (Windows Subsystem for Linux) with Ubuntu**. This gives the project the Bash shell and Linux Python environment its scripts expect. Native PowerShell-only execution is not supported by these instructions. A complete Windows/WSL acceptance walkthrough has not yet been performed; passing tests on macOS does not establish Windows validation.

Guide the user one stage at a time, inspect each result, and resume after any restart. Say whether each command belongs in **Windows PowerShell** or **Ubuntu (WSL Bash)**. Let the user handle administrator prompts, restarts and passwords locally. If the assistant cannot operate a terminal or installer, give the next exact step and ask for its non-secret result. Keep the interview available while setup is blocked, but do not claim a runnable search until dependencies and checks succeed.

1. **Check Windows and existing WSL — Windows PowerShell.** Have the user check their Windows version with `winver`. Consult Microsoft's current [WSL installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install) for system requirements and troubleshooting. Inspect existing distributions before installing anything:

   ```powershell
   wsl --status
   wsl --list --verbose
   ```

   If WSL is missing, open PowerShell with **Run as administrator**, run the following, and restart Windows if prompted:

   ```powershell
   wsl --install -d Ubuntu
   ```

   Open **Ubuntu** from the Start menu and complete its first-launch Linux username/password prompts. The password may show no characters while typing; do not paste it into chat. If WSL already exists, reuse a suitable distribution. Back in PowerShell, run `wsl --update` and `wsl --list --verbose`; confirm the chosen distribution shows version **2**. If it shows version 1, explain the conversion and use `wsl --set-version Ubuntu 2`, substituting its exact listed name. Never unregister or reinstall an existing distribution to fix setup. For virtualization, Windows-version or organization-policy errors, explain the specific blocker and follow Microsoft's guidance with the user or their administrator.

2. **Install the job-search dependencies — Ubuntu (WSL Bash).** Open the chosen Ubuntu terminal. These commands install Linux tools, separate from any Windows Python installation:

   ```bash
   sudo apt update
   sudo apt install -y git python3 python3-pip python3-venv curl ca-certificates
   python3 --version
   git --version
   curl --version
   ```

   Confirm Python is **3.11 or newer** before continuing. An older existing Ubuntu installation may need a supported newer distribution or Python package; explain the options and preserve its files before making changes. Do not replace the system Python or use `sudo pip`. If a package/download fails, resolve that error before treating installation as complete.

3. **Prepare the checkout and Python environment — Ubuntu (WSL Bash).** For a fresh installation, keep the repository in the Linux home directory, following Microsoft's [WSL environment guidance](https://learn.microsoft.com/en-us/windows/wsl/setup/environment). This avoids mixing Windows and Linux virtual environments:

   ```bash
   mkdir -p ~/projects
   cd ~/projects
   git clone https://github.com/theartoftech/jobagentforgood.git
   cd jobagentforgood
   python3 -m venv .venv
   scripts/jobagent_python.sh -m pip install -r requirements-dev.txt
   scripts/jobagent_python.sh -m unittest discover -s tests
   scripts/jobagent_python.sh -c "import sys; print(sys.executable); print(sys.version)"
   ```

   If a checkout already exists, inspect and reuse it where suitable; skip cloning over it. Preserve existing private configuration and resumes before any move. A Windows-created `.venv` with `Scripts/python.exe` cannot serve as this project's Linux `.venv/bin/python`; preserve/rename it before creating a separate Linux environment. Confirm the printed interpreter is inside this checkout's `.venv/bin/` and all tests pass. Do not bypass failures or mark mocked discovery tests as a live search.

4. **Connect the assistant to this same checkout.** Open the Linux project folder using the assistant/editor's WSL integration where available. In Ubuntu, `pwd` shows its actual path; `explorer.exe .` opens it in Windows File Explorer if needed. A Windows app may see it through `\\wsl.localhost\Ubuntu\home\<linux-user>\projects\jobagentforgood` (use the actual distribution and username). Verify the assistant can read the README there and execute project commands in that distribution's Bash terminal, using the Linux virtual environment. File access alone does not establish WSL command access. If command access is unavailable, guide the user through running the commands in Ubuntu and inspecting the results. Continue the interview in the chat associated with that folder, using everything below **Instructions for the assistant: start here** through the end of this README.

5. **Install Docker only if the user chooses JobTracker.** Continue the interview using local application history if they decline or defer JobTracker. If they choose it, perform the following before the tracker clone/configuration steps:

   - Inspect any existing Docker installation first. Follow the current [Docker Desktop for Windows installation guide](https://docs.docker.com/desktop/setup/install/windows-install/) to check supported Windows versions, hardware/virtualization and WSL requirements, and select the installer matching the computer's architecture. WSL working alone does not prove Docker Desktop requirements are met.
   - Install Docker Desktop **on Windows**, let the user handle its license/administrator prompts, then start it from the Start menu. Follow [Docker's WSL integration guide](https://docs.docker.com/desktop/features/wsl/): enable **Use WSL 2 based engine** where that option is shown, use **Linux containers**, and enable the chosen Ubuntu distribution under **Settings → Resources → WSL Integration**. Apply changes and wait for Docker to start.
   - Do not also install `docker.io` or a second Docker daemon in Ubuntu for this path. If an engine already exists there, explain the potential conflict and preserve its containers/data before agreeing on a migration. Do not remove another installation automatically.
   - In **Ubuntu (WSL Bash)**, check the connection and install OpenSSL for the tracker's login setup:

     ```bash
     sudo apt install -y openssl
     openssl version
     docker --version
     docker compose version
     docker info
     ```

     Docker Desktop provides Compose; a separate legacy `docker-compose` installation is not required. `docker info` must reach the running Linux engine. If the command is missing or the daemon is unreachable, check Docker Desktop startup and integration for this exact distribution before proceeding; do not assume a successful CLI version check is sufficient.
   - Continue **Guided JobTracker installation and connection** below from Ubuntu, using a separate sibling checkout such as `~/projects/jobtracker`. Verify the actual loopback URL from the Windows browser, authenticated persistence, and the approved history connection as described there. If Docker cannot run, save the unfinished step and continue Job Agent with local history. Keep Docker Desktop running when using the tracker; explain that stopping it makes the tracker unavailable.

Before scheduling on Windows, verify the chosen scheduler can invoke the assistant and commands in this exact WSL checkout. A schedule saved in configuration alone does not run searches, and a local schedule cannot be assumed to run while the computer is asleep or off. Record any limitation and provide manual-run instructions if needed.

</details>

### Interview questions

Ask all applicable questions; do not infer qualifications from a job the candidate likes.

- **Profession and direction:** What kind of work do you do, and what work do you want next? What responsibilities do you want to keep, change or avoid? What level of responsibility suits you? Record `career_context.profession` and `experience_level` in the candidate's words. For a career change, distinguish previous experience from the destination profession and identify transferable skills without claiming destination-role experience.
- **Resume and evidence:** Ask in the main chat: “Can you attach your resume here? You can attach more than one version—for example, one focused on consulting and another on development. Tell me what each is intended for, if you know. If you don't have one handy, we can start with work-history questions.” Follow **Working with multiple resume versions** below. Copy files only into ignored `Source Docs/` with permission. What name/email should local records use? What was your last role, scope, industry, level and employment period? What did you personally do, and what measurable outcomes can you substantiate? Which statements may be reused in cover letters? Do not invent years, metrics, degrees, employers or certifications.
- **Roles and strengths:** Which titles interest you? What activities do you do well, and what recent work demonstrates that? Which areas are limited exposure or training only? What should never be claimed? Are you seeking individual-contributor, management, entry-level or career-change roles? What adjacent roles would you consider? Propose adjacent titles with an evidence-based explanation and ask for confirmation before adding them. Strengths can be negotiation, patient care, customer service, scheduling, writing, craftsmanship or other relevant capabilities; they need not be technologies.
- **Employers and examples:** Which companies, industries and company sizes interest you? Which should be excluded? Share URLs of jobs you liked or applied to. Capture why they appealed; check live official postings. Keep already-applied jobs separate from merely interesting jobs, including exact URL/requisition, company, title, status and application date (unknown dates stay blank). Ask explicitly whether there are prior applications before recording an empty history.
- **Application tracking:** Ask explicitly: “Would you like to use local application history, install JobTracker with guided setup, or connect a tracker you already have?” Explain that local history needs no additional application; [JobTracker](https://github.com/theartoftech/jobtracker) provides a separate interface and needs its own installation. If they choose JobTracker, follow **Guided JobTracker installation and connection** below through download, installation, verification and connection. A yes starts the walkthrough, not just a link to another README. If they decline or defer, continue onboarding with local history. Record their choice and progress in ignored `setup.answers.json`, then preserve it in `candidate_evidence.json` after generation; do not ask the same question again on every run.
- **Location:** What city do you live in, and what major metro should the search use? Which surrounding cities are within your actual commute? Do you want onsite, hybrid, remote, or several? How much office attendance and travel is acceptable? Would you relocate, and where? Which countries may you legally work in? Is sponsorship required? Remote does not mean unrestricted worldwide work.
- **Language:** Which languages can you speak and write, at what professional proficiency? Which mandatory language requirements would be blockers? There is no default German rejection. Compare each posting's spoken/written requirements with the confirmed proficiency; ask about an unlisted required language rather than assume proficiency.
- **Terms:** What minimum guaranteed base pay, currency and pay period apply? Separately, is there an annual total-earnings target, and is commission/variable pay acceptable, required or excluded? Discuss commission-only work, quotas, ramp guarantees, bonuses, tips or overtime when relevant. OTE (on-target earnings) is not guaranteed base pay. Save these in `compensation_preferences`; never infer an annual conversion. What employment types, hours, shifts, clearance/licensing constraints or other dealbreakers apply? How should unpublished pay be handled? Unknown requirements stay questions.
- **Cadence and outputs:** Complete the required interactive checkpoint below; this item must not be skipped or silently filled from defaults. Keep `schedule_enabled` false during initial generation; set it true only after the final heartbeat creation and verification step succeeds. Keep `document_generation` false until separately authorized and validated. Those flags record activation, not whether the candidate was asked. Optional networking exports and tracker integrations are not prerequisites.

Store extra preferences and proficiency detail in `candidate_evidence.json` and `search_rules.md` after generation. Those files are authoritative for the assistant's full-posting review. The keyword screener does not fully interpret licensing, sponsorship, pay currencies, shifts, travel, or all natural-language requirements.

### Required checkpoint: cadence and output preferences

**Ask these questions before closing the interview, even if optional tracker setup is unfinished.** Present them through the supported interactive question tool, or directly in chat when unavailable. Do not merely display this list or say these preferences can be configured later. Check prior answers first and ask only what is missing; a sample value or a default in a file is not a confirmed answer. Ask each group and wait for its answers before presenting the next group.

**Group 1 — when to search (up to three questions):**

1. “Would you like searches daily, weekly, only when you ask, or would you prefer to decide later?” Use these as choices with room for another cadence. This records a preference; final heartbeat activation is still confirmed after result review.
2. “Which timezone should your search use?” If the user already gave a city, propose the corresponding timezone for confirmation; never assume it from this machine. Save a confirmed IANA timezone for the generator even if automatic searches are declined or deferred, because report dates also need it.
3. If automatic searches are chosen: “Which days and what local time should searches run?” Accept a plain-language answer, summarize its meaning and resolve any ambiguity. If manual/decide-later is chosen, record days/time as not applicable/deferred rather than inventing a schedule.

**Group 2 — search size and reports (three questions):**

1. “How much time would you like each search to spend?” Offer “Suggest a time limit for me,” “I'll give you a limit,” and “Decide later.” If they request a suggestion, propose a concrete number of minutes, explain the coverage tradeoff, and get confirmation; do not quietly install a default or promise exact completion time.
2. “How many job sites should a full search check—up to 200?” Offer “Suggest a limit for me,” “I'll choose a number,” and “Decide later.” Confirm an actual number when resolved. Explain that the 1–3-employer first test is separate from the recurring full-search limit; the total configured source list still cannot exceed 200. Never interpret 200 as a target the candidate selected.
3. “How would you like to read the results?” Offer “Browser report (HTML),” “Text report (Markdown),” “Both,” or “Decide later,” within the question tool's option limits. Explain the names in plain language. This is a delivery preference; the scripts may still generate supporting files in both formats.

**Group 3 — documents at the end of each run (one question):**

1. Explain: “Each run can deliver its reports plus a tailored resume and cover letter for every qualified job you haven't applied to. Shall we set that up?” Offer “Reports and both documents,” “Reports only,” and “Decide later.” Reuse an explicit request for recurring documents as approval; do not ask again. A yes authorizes recurring production after template/evidence validation, not applications. Complete the document setup below rather than recording only future interest. Keep `document_generation: false` until that setup passes. Existing resume-only or cover-letter-only preferences must be honored; the combined command produces both, so use the appropriate producer function or standalone cover-letter CLI for a narrower choice.

Save each confirmed answer and any explicit deferral in an `interview_preferences` object in ignored `setup.answers.json`. Use entries for `cadence`, `timezone`, `days_and_time`, `runtime_minutes`, `site_limit`, `report_format`, and `documents_later`, each with `status` (`answered`, `deferred`, or `not_applicable`) and `value`. An unasked or unanswered question stays pending in `outputs/onboarding-progress.json`; it must not be marked deferred without the user's choice. Also fill the generator's existing `timezone` and `schedule` fields from confirmed answers; for manual/deferred scheduling, use descriptive text such as “Manual searches only” or “Automatic schedule undecided” with `schedule_enabled: false`.

The current generator does not copy this additional object. After generation, preserve `interview_preferences` in ignored `candidate_evidence.json` and `run_preferences.json`. The assistant must honor confirmed time/site limits when planning execution and stop with a partial-coverage report if the budget is reached; these notes alone do not enforce a scanner timeout. Before a search with unresolved limits or format, propose concrete values for that run and ask for confirmation. Keep the long-term decision deferred if that is what the user chose.

Include these answers in the interview summary and mark this checkpoint complete only when every applicable question was actually answered or explicitly deferred. Revisit unresolved cadence details at final heartbeat setup; a deferred cadence cannot be activated. If a previous setup skipped the checkpoint, resume with these questions without overwriting candidate files or repeating the rest of the interview. Retain `documents_later` for older saved interviews, but also record the actual recurring approval and selected document types in `candidate_evidence.json`; old interest alone is not recurring approval. An explicit document deferral does not block search reports.

### Working with multiple resume versions

Several resumes can be equally current and useful. A consulting-focused resume may emphasize client advice and engagements, while a development-focused resume emphasizes implementation and delivery. These are examples, not assumed career categories; ask the candidate what each version represents. Do not force a single “latest” version or treat one as obsolete merely because another file was uploaded later.

1. Identify the attached files by their displayed names and verify you can read their content. Ask only for missing context: which target roles each supports, whether any is outdated, and whether there is a preferred general version. Do not infer the intended use or recency solely from a filename. If an attachment cannot be read, say which one and offer reattachment, pasted text or work-history questions; do not claim to have reviewed it.
2. Preserve each original separately. With permission, save copies under ignored `Source Docs/`, using distinct names if uploads share a filename; never overwrite an earlier version. The assistant resolves and records available attachment/local paths, not the user. If attachments cannot be saved, record their chat references and that persistence is incomplete. Do not invent a local path.
3. Compare shared facts and ask about genuine conflicts in employers, dates, titles, metrics or qualifications. Differences in emphasis or omitted bullets are not automatically contradictions. Keep each statement tied to its source and the candidate's confirmation; do not combine versions into stronger claims than either supports.
4. Save a `resume_sources` list in ignored `candidate_evidence.json` after generation, with each source's original filename, saved path or attachment reference, candidate-confirmed focus, applicable target roles, current/outdated/unknown status, and any unresolved conflicts. Preserve this information in ignored interview notes while setup is unfinished. The generator currently accepts one `resume_path`: populate it with a confirmed primary saved source if there is one, otherwise leave it empty. After generation, add the complete `resume_sources` list; the single field must not discard the other versions.
5. Use all confirmed relevant experience for discovery while retaining the different target-role emphases. When preparing optional documents for a specific job, select the source that best fits the candidate's stated purpose and ask if the choice is ambiguous. Tell the user which version is being used. A preferred evidence source is not automatically a compatible DOCX template: follow the separate template validation and document authorization rules before producing files.

### Adapt the interview to the profession

Use the candidate's answers and actual target postings to choose follow-ups. These examples are prompts, not fixed career tracks or assumed qualifications:

| Work area | Relevant follow-ups |
|---|---|
| Sales / account management | B2B or B2C, industries, customer segments, prospecting versus renewals, territories, deal sizes, sales cycles, negotiation, quota attainment and account growth. Ask for substantiated results; do not require disclosure of confidential customer information. CRM tools matter only where relevant. |
| Customer service / hospitality | Customer channels, issue resolution, service volumes, escalation handling, service-quality evidence, shifts and languages. Ask about systems only when used or required. |
| Administration / operations | Scheduling, records, coordination, vendors, budgets, confidentiality, process improvements and scope of responsibility. Distinguish general administration from specialist payroll/accounting experience. |
| Project Management | Industries and project types, scope, budgets, timelines, team size, stakeholder management, dependencies, risk/change management, vendors and delivery outcomes. Ask about Agile, waterfall or other methods, tools and credentials such as PMP or PRINCE2 only where relevant; never assume certification or software-delivery experience. Discuss Project Manager, Project Coordinator, Program Manager or PMO roles based on demonstrated scope and confirm each target. Distinguish project management from product management. |
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
5. Review several results with the user. Confirm titles, location, language and qualifications actually fit. Adjust private configuration from their answers. Then run the remaining chosen sites and complete **End-of-run delivery: reports, resumes and cover letters** below. Give links to the reports and verified documents with clear next actions, never claim an application was submitted.
6. After the first run is accepted, complete **Finish setup: create and verify the heartbeat** below. This is a required onboarding stage with an explicit outcome, not a suggestion for the user to perform later. Writing `run_preferences.json` alone does **not** schedule anything.

### Finish setup: create and verify the heartbeat

The Python generator saves a proposed cadence with `schedule_enabled: false`; it cannot create an automation in the user's assistant. **The assistant must invoke its actual scheduling tool at the end of setup when automatic searches are approved.** A heartbeat is a recurring return to this job-search chat to carry out the search workflow, not just a reminder to run a command. Codex supports [scheduled tasks inside an existing chat](https://developers.openai.com/codex/app/automations#schedule-a-task-inside-a-chat); other assistants must use a verified equivalent if available.

1. **Resolve the choice interactively.** After reviewing results, ask whether to create the heartbeat, run manually, or decide later. Reuse any explicit approval already given. Confirm the candidate's days, local time, timezone and run budget using their saved preferences; never inherit the maintainer's schedule. A cadence mentioned during the interview alone is not approval to activate it. If they decline/defer, record that outcome and keep `schedule_enabled: false`.
   First check that **Required checkpoint: cadence and output preferences** was completed. If it was skipped, ask its missing questions now rather than using defaults from `run_preferences.json`. Do not create a heartbeat with unresolved cadence or recurring-run limits.
2. **Find the scheduler and prevent duplicates.** Discover the current assistant's scheduling capability and inspect its tool instructions before use. In Codex, discover `automation_update` and use a thread heartbeat (`kind: heartbeat`, attached to this chat) by default. Use a standalone cron/new-chat task only when the user requests that behavior; do not replace an unavailable heartbeat with one silently. Inspect a saved scheduler ID and matching existing tasks by chat/project and absolute checkout path before creating anything. Reuse a matching active task; update it only within the approved change. Do not reactivate a paused task without explicit permission, or alter unrelated searches. If a prior creation outcome is uncertain, inspect existing tasks before retrying.
3. **Prepare the recurring work.** Read `daily_job_search_prompt.md` and supply its current instructions in the scheduler prompt, along with the absolute checkout path, the candidate's timezone and run budget. Instruct each run to read that file again for updates, perform employer maintenance when due, discovery, local-history reconciliation, strict review, reporting and the approved end-of-run document production. Retain tracker-read permissions, the no-application-submission rule and the candidate's standing document approval; publishing needs separate authorization. Request silence for unchanged non-actionable results and notifications for new actionable roles, meaningful changes, failures or required input. A bare reminder or a shell-only scanner omits the assistant's research/review work. Verify access to this same checkout and ignored candidate files, including the correct WSL distribution on Windows; an empty worktree will not contain them.
4. **Create or update it now.** Invoke the scheduling tool with the approved cadence, active status and prepared prompt. In Codex use the actual create/update operation, not only a suggested-create response or text describing what should be scheduled. Use the tool's supported schedule format and timezone behavior; do not handwrite automation directives or raw scheduler configuration files as a substitute. If UI confirmation is required, present that action and keep the stage pending until it is completed. Once approval is available, do not stop with “I can set this up.”
5. **Read back and verify.** Use the scheduler's view/read capability to confirm the returned ID, active status, intended chat/checkout, prompt, cadence and timezone interpretation. Report the next run in the candidate's local time if the scheduler supplies it. If it does not, explicitly say the next-run timestamp is unavailable; do not invent one or label a calculated time scheduler-confirmed. On an API error, unsupported timezone/cadence, pending suggestion, paused task or ambiguous response, keep scheduling incomplete and explain the next recovery step. Successful creation/readback verifies registration, not that a future search has already run.
6. **Save the verified result locally.** Only after verification, merge `schedule_enabled: true` and a `scheduler` object into ignored `run_preferences.json`, preserving other preferences. Record `provider`, `kind`, `id`, `status`, `timezone`, `cadence`, `checkout_path`, `verified_at`, and `next_run_at` only when supplied by the scheduler. Save the scheduling stage and evidence in `outputs/onboarding-progress.json`. If the tool creates the heartbeat but saving local metadata fails, report the active task ID and repair the record; do not create another heartbeat.
7. **Close with the actual outcome.** Tell the user whether the heartbeat is active, its cadence/timezone, next-run availability, where results will appear, and how to ask for it to be paused or changed. Explain any local execution requirements, such as leaving the computer and assistant running. If the assistant lacks a suitable scheduler, clearly say **“Automatic searches are not set up”**, record the blocker and provide the manual instruction: “Open this project chat and ask: Run my job search using daily_job_search_prompt.md.” Core search can be ready while automation is unavailable; never report the heartbeat as finished in that case.

Do not delay this stage because optional tracker integration or document production is unfinished. Use the approved local-history workflow and keep those tasks separate. If an actual search prerequisite is unresolved, report why activation is blocked and continue independent work instead of scheduling a known-broken run. Do not create a personal heartbeat merely while editing these reusable instructions.

### Optional capabilities

The ATS adapters include Workday, Greenhouse, Lever, SmartRecruiters, Workable, Ashby, ADP, iCIMS and some employer-specific parsers. Website coverage varies. The sharded scanner supports daily listing checks, rotating deep scans and carried-forward failures. The reviewer deduplicates postings, carries unresolved jobs forward, separates required/preferred gaps and excludes applied requisitions.

### End-of-run delivery: reports, resumes and cover letters

**Every manual and scheduled run ends with reports and an explicit document outcome.** Reports are always required. Once the candidate approves recurring documents, create the appropriate resume and cover letter for each eligible, unapplied posting at the end of each run; do not stop with an offer to create them later or ask for the same approval every week. A candidate can choose reports only or defer document setup. This shared workflow never inherits another candidate's approval or resume.

**Set up documents during onboarding.** Existing DOCX tooling expects specific document structure: template headline, summary prefix, checksum and a two-column contact header for cover-letter sender extraction. Arbitrary uploaded PDFs/DOCX files are **not** automatically compatible. Inspect and adapt a copy with the user's approval, preserve the original, populate `resume_templates.json` using `resume_templates.example.json`, set `default_resume_template` and candidate contact settings, and validate rendering before enabling production. Configure candidate settings in ignored `.env.local`; the Python wrapper loads `.env` and `.env.local` before running commands. Do not deliver placeholder names, email addresses or sample profile/portfolio links. If the candidate lacks fields the existing template requires, adapt and validate the template/tooling or report the incompatibility rather than inventing them. Cover-letter statements come only from confirmed `candidate_evidence.json`. Never claim document support has passed without actually rendering and inspecting the output.

Record the candidate's standing approval, selected document types, source/template mapping and validation evidence in ignored `candidate_evidence.json`. After validation, merge `document_generation: true` into `run_preferences.json` without rerunning the overwrite-refusing generator. Track document setup separately in `outputs/onboarding-progress.json`. If setup fails, continue reports but mark document delivery blocked with the exact next question/action. Do not call the requested report-and-document workflow complete while this stage is unfinished.

At the end of **every** run:

1. Finish the dated Markdown and HTML review reports, including coverage, errors, applied matches and unresolved questions. An interrupted search still needs an honest partial-results report. Reserve part of the confirmed runtime budget for delivery; if exhausted, list pending artifacts instead of claiming they were created.
2. Use only the current strict `outputs/YYYY-MM-DD-resume-ready-jobs.md` queue, matching workflow review and reconciled application snapshot. Complete the assistant's full-posting qualification review first. Never broaden eligibility because documents were requested. An empty queue means “No eligible jobs; no documents needed.” A missing/invalid queue or history is a blocker, not zero matches.
3. For enabled production, select the validated source suited to each role from `resume_sources` and the queue's template mapping. Preserve consulting/development or other source distinctions; ask about ambiguity in an interactive run, or report it as pending in an unattended run. Tailor only from confirmed evidence. The existing producers mainly apply template positioning and confirmed evidence text; inspect relevance to the actual posting rather than assuming a generated file is sufficiently tailored.
4. Execute the dated plan's `scripts/produce_resumes.py` command for a nonempty eligible queue. Its CLI creates **both resumes and cover letters**, writes both production manifests and refreshes the HTML report; a second cover-letter invocation is unnecessary. Use the same dated applied snapshot and validated template configuration. Read the actual result, not just the planned command. On failure preserve available reports and report which document stage failed.
5. Inspect both manifests, actual DOCX files and rendered pages for correct identity, employer, role, relevant truthful content, formatting and working links. The producer's structural/PNG checks do not establish visual or editorial quality. Reuse existing validated documents only when the exact posting, candidate evidence, source/template and tailoring remain current; do not mistake a reused file for newly generated work. If these changed, invalidate the affected reusable artifact record and regenerate in an isolated output location while preserving previous files. Confirm the refreshed report links to the verified artifacts.
6. Finish with report links and resume/cover-letter links per posting, plus counts of generated, reused, blocked and pending documents. If production was declined/deferred, state that saved choice. If enabled but blocked, state the specific recovery action; never silently omit documents. Save this delivery summary in the dated outputs even when notification rules keep an unchanged run quiet. Files are drafts for the candidate's review; no application, message or tracker upload is authorized by producing them.

For the document renderer, use installed LibreOffice plus Poppler, or build the isolated Docker renderer (Docker is not required when the native renderer works):

```bash
docker build --tag jobsearchagent-libreoffice-renderer:1.0.0 docker/resume-renderer
```

Local networking reports can use a voluntarily supplied LinkedIn export. Notes are drafts; nothing is sent automatically. The deterministic runner under `poc/` is an advanced experiment with additional integration requirements, not the default setup path.

### Optional application tracker or database

**No tracker? Start here:** continue using Job Agent's local `applied_jobs.json`. Tell the assistant when you actually apply, including the posting URL and application date, so it can update your history and avoid recommending the same application again. A separate website, database or account is not needed for your first search or later runs.

If you would like a dedicated interface, choose **[JobTracker](https://github.com/theartoftech/jobtracker)** during the interview. The assistant will walk you through its setup and connection. It is optional; installation difficulties do not prevent Job Agent from searching with local history. Installing JobTracker does not by itself authorize access to existing records or ongoing reads and writes.

#### Guided JobTracker installation and connection

When the user chooses to install JobTracker, complete these steps with them. Explain each stage in plain language and record the next unfinished step so another chat can resume. Do not claim installation or connection succeeded from commands alone. Follow **Continue until onboarding is finished** above: waiting for an optional export, login or connection permission must not end the interview or other independent setup work. A tracker checkpoint is not the end of onboarding.

1. **Choose the installation.** Read the current [JobTracker README](https://github.com/theartoftech/jobtracker/blob/main/README.md) and inspect its installation files before executing them. Ask which computer should run it, whether an installation already exists, and where to put the checkout. Default to a local laptop installation unless the user requests a server. Use a separate directory alongside Job Agent; never clone the tracker into this repository or overwrite an existing checkout. Record the checkout path and Git revision. The user's yes authorizes ordinary download/setup work; do not ask again for every reversible step.

   From the chosen parent directory, for a new checkout:

   ```bash
   git clone https://github.com/theartoftech/jobtracker.git jobtracker
   cd jobtracker
   ```

2. **Check prerequisites and install missing ones.** The current laptop path requires Docker with Docker Compose and OpenSSL, plus a POSIX shell (macOS/Linux or WSL on Windows). On Windows, complete the Docker stage in **Windows setup with the assistant** above, including Docker Desktop's integration with the selected WSL distribution, then return here. Check `git --version`, `docker --version`, `docker compose version`, `docker info` and `openssl version`. Explain any missing tool or stopped Docker engine and guide the user through the appropriate official installation/startup instructions for their operating system. Let the user complete administrator, license and account prompts. Do not substitute Kubernetes or a private server for a missing laptop prerequisite. If they prefer to defer installation, save progress and continue the search locally.

3. **Create private settings and a login.** Follow JobTracker's current instructions to create `.local/jobtracker.htpasswd` and `.local/runtime.json` from its generic runtime example. Inspect whether files already exist before writing; never reset an existing login, settings file or data store. Ask for the desired login name and timezone, and keep optional calendar feeds and task templates empty unless requested. Have the user enter the password in their local terminal or login UI; never ask them to paste it into chat or put it in a command argument, tracked file or log. Explain where private settings and persistent data live. Use the documented file permissions. Do not reuse credentials or settings from the maintainer or another candidate.

4. **Start and verify the complete application.** From the tracker checkout, use its documented Compose command:

   ```bash
   docker compose up --build -d
   docker compose ps
   ```

   The currently documented default is `http://127.0.0.1:8765/`, bound to laptop loopback. Check the actual Compose configuration and port; resolve conflicts without stopping unrelated services. Open the UI, let the user sign in, check `/api/health`, and verify that an unauthenticated `/api/state` request is denied. A static page or standalone file server is not proof that API-backed saves work. Ask the user to create a clearly labeled disposable test entry, reload the page and confirm it persists; let them remove it afterward. Do not silently create an applied-job record as a test. Do not expose the service to the network as part of laptop setup.

5. **Choose and approve the read connection.** Follow the integration procedure below. Prefer a user-provided export if the user does not want direct access. For the current Compose version, the authenticated read route is `GET /api/state`, not `/api/jobs`; verify this against the installed `server/app.py`. Its response includes jobs **and task/checklist notes/settings**, so explain that broader response before requesting access. Current Basic authentication is not a read-only account: it can also authorize writes. Use only explicitly approved GET requests, or have the user provide a jobs-only export instead. Never call `PUT /api/state` to establish a read connection—it replaces tracker state. Use HTTP only for the verified loopback installation; a remote connection needs a verified HTTPS endpoint. Keep authentication material in user-managed private local configuration, not chat or tracked files. The user can authorize the known response scope and first sample read together; schema inspection alone does not grant permission to read records.

6. **Map and prove the connection.** Inspect the approved response/export and convert its `jobs` to the local snapshot contract below: `jobUrl` → `job_url`, `appliedDate` → `applied_date`, with confirmed company, title and status semantics. Use an ignored staging file under `outputs/`, validate all required field types and show a small sample before merging. Preserve existing local applications; never replace history with an empty tracker or treat a saved/interested item as applied. Fail visibly on authentication errors, HTML login pages, invalid JSON, missing `jobs`, unknown status meanings or incompatible schemas. Back up local history before an approved merge. A fresh empty tracker is a valid connection test only after confirming it is genuinely empty; also exercise the conversion with synthetic applied/interested records in an isolated temporary directory. Test the merged history through `mark_applied_jobs.py --local-applied applied_jobs.json` and strict review: an exact previously applied posting must be excluded, while an interested-only posting must remain eligible. If there are no real applications, report that the deduplication test was synthetic. Do not claim a tested connection until these checks pass.

7. **Record and explain ongoing use.** Save an `application_tracking` object in ignored `candidate_evidence.json` with `choice` (`local`, `install_jobtracker`, or `connect_existing`), installation path/revision, endpoint or export source, setup stage, mapping, approved data scope, validation result, and any separate recurring-read approval. Do not store passwords there. Ask whether later searches may refresh the approved source, and record how that refresh will actually run before adding it to a schedule. The default scripts still read `applied_jobs.json`: a URL or an installed tracker does not create automatic sync. The assistant must perform the approved export/read and tested conversion before local reconciliation, or explicitly report that tracker history was not refreshed. Explain how the user records an actual application in JobTracker. Uploads, tracker writes and analytics publishing remain separate choices.

Finish with the local URL, startup/shutdown instructions, storage/backup locations, connection status and any unresolved step. `docker compose down` stops the current laptop setup while preserving its data volume; do not use `docker compose down -v`, which deletes that data. If installation or connection fails, keep the local job search working and say exactly what remains incomplete. This walkthrough guides the assistant; no universal installer or automatic two-way sync is included.

**External tracking is disabled by default.** `mark_applied_jobs.py` reads local `applied_jobs.json` even if old tracker environment variables are present. Missing or invalid local history is an explicit error; it never triggers an external connection or silently assumes no prior applications. `publish_skill_gap_analytics.py` exports a local artifact by default and does not publish it.

For a user who wants their own system connected, the assistant must:

1. Ask which website, database, API or export contains their applications. Prefer an export or documented read-only API. Do not probe local networks, search for databases or read credentials to discover a tracker.
2. Explain the proposed connection, specific database/schema or API scope, and minimal fields needed. Obtain explicit permission before accessing it. Use user-supplied connection settings and a read-only account where supported; if the account can also write, explain that limitation and use an approved read-only operation or user-provided export. Keep secrets in ignored local configuration, never chat or tracked files. Permission to inspect a schema does not authorize ongoing reads or writes.
3. Inspect only the approved schema/metadata first, then read sample records only within the explicitly approved scope. If that sample access has not already been authorized, request it before reading. Different systems need different adapters. Do not run the legacy `jobs.data` query against an unknown database or infer that a table with “jobs” in its name tracks applications.
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

Profession regression cases cover sales, customer service, administration, Project Management and nursing alongside existing technical profiles. They exercise candidate-owned strengths, required versus preferred qualifications, optional tools, compensation holds and a fresh sales setup through mocked ATS discovery, local history and HTML review. These checks do not replace a real candidate walkthrough or establish universal profession coverage.

For the maintainer's acceptance test: prepare the sanitized public branch, push it explicitly, clone that branch into another directory, install from this README, and paste everything below “Instructions for the assistant: start here” through the end of this file into a new chat associated with that clone. Complete a fresh interview and first live search there. Verify private files stay ignored and no original-candidate preference appears. Local unit/integration results do not replace this human walkthrough.

Also exercise onboarding interruption cases: withhold an optional tracker export and verify the assistant asks the next interview questions immediately; decline tracker access and verify no external read occurs; leave a required candidate answer unanswered and verify it is requested rather than guessed; supply missing/invalid local history and verify discovery continues while reconciliation stays blocked. Resume the chat and verify it uses the saved progress, produces and reviews real results, addresses scheduling, and revisits a selected unfinished tracker. These are conversational acceptance checks; passing Python tests alone does not prove the assistant follows them.

Check question delivery beyond the opening interview: summary review, first-result feedback and scheduling must each display a supported interactive question when an answer is needed. Repeat with the question tool unavailable and verify a direct chat question appears instead. Leave a question unanswered and verify dependent work stays pending without repeated prompts or assumed consent; answer it and verify the workflow advances. An unattended run must report required input without opening a blocking interview. Do not count a status-only response as passing these checks.

For resume intake, attach consulting-focused and development-focused versions without typing paths. Verify both are retained, their purposes are confirmed, and a later upload does not automatically supersede the earlier one. Exercise duplicate filenames, conflicting employment dates, an unreadable attachment, and an assistant without attachment support. Verify no source is overwritten, no facts or paths are invented, the no-resume interview remains available, and optional document preparation identifies the selected source without bypassing template validation.

For scheduling acceptance, approve a cadence and verify an actual heartbeat is created and read back as active before local `schedule_enabled` becomes true. Repeat setup and verify the same task is reused rather than duplicated. Exercise decline/defer, an existing paused task, unavailable scheduling, a failed/ambiguous create response, and a pending UI confirmation; none may be reported as an active newly verified heartbeat. Verify missing next-run timestamps are disclosed and creation success is distinguished from a successful scheduled search. A local preference file or a mocked test is not evidence of a live heartbeat.

For interview completeness, start without cadence/output answers and verify the assistant asks all three groups before the final summary. Try weekly searches with no chosen day, a city without a confirmed timezone, explicit manual searches, deferred budgets, HTML-only delivery, and recurring document approval. Verify existing answers are reused, missing answers remain pending, explicit deferrals are preserved, documents are enabled only after validation, and no heartbeat is activated with unresolved settings. Inspect the saved preferences after generation to ensure none were dropped.

For end-of-run delivery, use synthetic candidates from sales, project management and software roles. Exercise a qualified unapplied job, an empty queue, an already-applied job, unresolved qualifications, missing templates/evidence, a renderer failure and an unchanged repeated run. Verify reports survive document failures, only eligible jobs receive approved document types, both actual DOCX files and their report links are checked, reused files are distinguished from new files, and blockers are explicit. Confirm standing approval is reused without another weekly permission question and reports-only/deferred choices remain respected. Mocked rendering verifies control flow, not visual quality; a real rendered walkthrough is required before claiming a candidate's document setup works.

**Publication and history:** deleting a private file in a normal branch does not remove it from Git history. Publish a reviewed clean-history snapshot to a separate public repository/branch without merging private history. Making an existing repository public exposes its other branches and history too. Inspect the exact release tree and history for personal files and credentials before publishing; do not push tags or old branches with it.
