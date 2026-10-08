# Factiva Execution and Refinement Workflow

Use this reference when operating the authenticated Factiva interface or reviewing results.

## Enter the authenticated session

First verify that computer or browser control exists. If it does not, stop this workflow and use the Boolean-only output rules in [syntax.md](syntax.md).

Use computer control to locate the existing Factiva window or tab in the user's named browser. School-library proxy hostnames may wrap the Factiva hostname; identify the page by the visible Factiva product and authenticated search controls, not by one hard-coded URL.

If the page redirects to an identity-provider or Dow Jones login, do not type credentials or attempt to bypass authentication. Ask the user to complete sign-in, then continue.

Navigate to **Search / Rechercher** and **Free Text Search / Recherche de texte libre**. Do not use the simple-search page for advanced syntax. Confirm that **Search Genius / Recherche Genius** is off before entering a handcrafted Boolean query.

## Set controls deliberately

The authenticated interface exposes these controls:

- Date: last day, previous week, last month, last 3 months, last 6 months, previous year, last 2 years, last 5 years, all dates, or a custom period.
- Duplicates: disabled, identical, or similar.
- Indexed panels: Source, Author, Company, Factiva Expert Search, Subject, Industry, Region, Look for, and Language.
- More options: free-text scope (full article, headline and lead paragraph, headline, or byline); exclusions for republished news, recurring market data, and obituaries/sports/calendars; result ordering.
- Result content tabs: All, Publications, Websites, Blogs, and Photos. Use Publications for ordinary news-article research.

Use **Similar** duplicate suppression for ordinary topic research. Use **Identical** or disable suppression only when the task concerns syndication, republication, or volume measurement, and disclose that choice.

Default to **Title and first paragraph / Headline and lead paragraph** for topical news research. Use full article for an explicit recall-first pass or after the focused pass proves too sparse. Use headline only for very strict focus or when locating known coverage. Do not combine a restrictive UI text scope with `atleastN` or `/FN/` unless Factiva accepts the resulting query and the restriction is substantively justified.

Use the language of the request for the primary query and primary language filter unless the user specifies otherwise. Add query synonyms in the selected language; the language filter does not translate search terms. If international coverage is useful, run a separate, labeled language pass rather than silently searching English or mixing languages in the primary query.

For Source, Company, Subject, Industry, Region, and similar indexed panels, search by the human-readable name and select the displayed match. Record the chosen label. Do not rely on an unverified internal code.

## Run a calibration loop

Start with a focused query and inspect:

- result count for the active content type, normally Publications; do not report the broader All count as the article count;
- the first 10–20 titles and snippets, with attention to different dates and sources;
- whether the focal entity or issue is central or incidental;
- repeated false-positive patterns;
- obvious missing aliases, spellings, languages, or event terminology;
- duplicate concentration and source diversity.

Refine from evidence:

| Observation | Useful adjustment |
|---|---|
| Mostly passing mentions | Move the entity or issue to headline/lead, add a modest `atleast2`, or tighten proximity. |
| Actor and verb both appear but the actor is not the speaker | Replace separate co-occurrence clauses with `hlp=((ACTOR) near8 (REPORTING_VERBS))`; choose a proximity of roughly 5–8 words and remove generic nouns such as `statement*` from the focused pass. |
| Entity-name ambiguity | Add a role, organization, location, product, or indexed Company filter. |
| Excessive noise from one meaning | Add a narrow grouped context requirement before considering `not`. |
| Too few results | Expand aliases/translations, widen proximity, relax headline scope, widen date/source coverage, or remove an exclusion. |
| Known relevant article missing | Test its title vocabulary and source/date independently; then add the missing wording to the recall variant. |
| Many republications | Keep Similar suppression for topic synthesis; disable it only for propagation analysis. |
| Syntax rejected | Validate the base query and add advanced clauses back one at a time. |

Do not optimize only for result count. The target is a defensible balance of relevance, coverage, source diversity, and reproducibility.

Keep a compact ledger:

```text
Round | Exact query | Date/language/source/text scope/duplicates | Content type + result count | Precision notes | Change
```

Usually one to four materially different rounds are enough. Continue beyond that only when the task's stakes or ambiguity justify it.

## Keep browser control stable

- Fetch fresh accessibility state after every menu selection, navigation, modal, or expansion because element indices may change.
- Resolve controls from their current labels and roles. Do not carry numeric element indices from an earlier state into a later interaction.
- Prefer `setValue`, labeled clicks, and keyboard navigation on accessible controls. Use coordinate clicks only after a fresh screenshot and only when no accessible target exists.
- Treat segmented date inputs as fragile. Enter one segment or field at a time, refresh state, and verify the displayed start and end dates before pressing Search.
- Verify the query text, language, duplicate mode, and text scope immediately before execution.
- Do not batch a fragile form edit with unrelated navigation. A failed interaction must not be mistaken for a successful setting change.
- From a results page, use the browser Back control or an accessible Factiva search/edit element to revise the query. Do not coordinate-click **Modify search** when Back is available.
- A coordinate-action timeout counts as browser-control instability. Do not repeat the same coordinate action.

When language or date is encoded in the free-text query, Factiva may still display its unchanged UI defaults in the separate Date or Language summary rows. Verify the constraint in the displayed Text query and spot-check result dates and language; do not mistake the unchanged UI row for proof that the Boolean restriction failed.

If the app or controlled surface disappears, inspect the current browser/window inventory and make one recovery attempt. Reattach to the existing Factiva surface if present. Do not repeatedly relaunch Safari or type school-proxy URLs into the address bar; this can lose the authenticated route and creates more failure modes. If recovery fails, or instability recurs, stop browser actions and return the paste-ready Boolean query.

Never say that Factiva closed or crashed Safari unless the UI or system provides direct evidence. Report the observable fact: the browser-control surface became unavailable.

## Review and capture evidence

Open a representative sample, prioritizing primary reporting, source diversity, recency appropriate to the question, and articles that directly address the research objective. Capture only what is needed:

- title;
- publication and publication date;
- author, if shown;
- Factiva document identifier or stable link, if available;
- concise paraphrase of the relevant evidence;
- a short quote only when wording is essential.

Separate publication claims, quoted-party claims, and your synthesis. Note contradictions and coverage gaps rather than forcing agreement.

Only report findings from the query/filter combination that was actually run and visibly produced those results. Do not combine a broad English preliminary result set with an unexecuted French refinement. If the final pass could not be executed, omit findings and return the Boolean query instead.

Respect the user's institutional license. Do not bulk-download, mass-copy, bypass paywalls or access controls, redistribute full text, or create a persistent article archive. Keep extracts minimal and tied to the user's research purpose.

## Handoff format

For an executed search, report:

```text
Research scope
Final query
Filters
Refinement summary
Findings
Key sources
Coverage and limitations
Suggested follow-ups
```

Always include the exact final query and filter labels so the user can reproduce the search manually.
