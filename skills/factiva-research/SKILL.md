---
name: factiva-research
description: Plan, execute, refine, and document advanced Factiva searches, or return a paste-ready Factiva Boolean when browser control is unavailable. Use for Factiva research on news, companies, people, industries, events, media coverage, or for formulating and repairing Factiva free-text queries; do not use for ordinary web search.
---

# Factiva Research

Turn a research question into a reproducible Factiva search and, when possible, run it in the user's authenticated browser session.

Read [references/syntax.md](references/syntax.md) before composing or repairing a query. When operating Factiva or assessing results, also read [references/workflow.md](references/workflow.md).

## Choose the mode first

- **Browser execution:** use this only when computer or browser control is available and an authenticated Factiva page can be controlled.
- **Boolean-only:** use this when computer/browser control is unavailable, when the user asks only for a query, or after one recovery attempt fails during browser execution. Do not substitute a general web search or claim Factiva findings. Return one copy-paste-ready Factiva query in a single `text` code block. Add no prose unless a required constraint cannot be encoded safely.

Do not ask the user to open Factiva in an environment that cannot control it. In Boolean-only mode, encode text scope, language, and dates in the query when the syntax is known; never invent an index code.

## Frame the search

Infer the research objective, focal entities, event or issue, date range, geography, languages, source constraints, exclusions, and desired output from the request. Ask one concise question only when an unresolved ambiguity would materially change the search; otherwise state necessary assumptions and proceed.

Treat the language of the request as the default language of the primary corpus as well as the response unless the user specifies otherwise. Never silently replace a French request with an English search. For international coverage, run a clearly labeled secondary language pass only when requested or demonstrably useful; keep language passes separate so their coverage can be compared.

Build a small concept map before writing syntax:

- canonical names, former names, aliases, acronyms, translations, and distinctive product or program names;
- issue terms, specialist vocabulary, common journalistic wording, spelling variants, and useful stems;
- likely false positives and safe exclusions;
- evidence that would count as relevant, not merely a passing mention.

Use web research only to discover or verify terminology when needed. Do not substitute web results for the requested Factiva research.

## Design the query

Create one balanced query first. Add a precision-first and/or recall-first variant only when they will help diagnose coverage.

- Group synonyms with `or`; join distinct concepts with `and`; parenthesize every mixed Boolean expression.
- Quote exact names and phrases when ambiguity, stop words, or reserved operator words could change interpretation.
- Prefer proximity, headline/lead scope, indexed company selection, or modest mention-frequency constraints to make the focal subject central.
- Default to **Title and first paragraph / Headline and lead paragraph** for topical news research. Use full article only for an explicit recall-first pass or when the focused search is too sparse.
- Encode relationships, not just co-occurrence. When the request concerns what a person said, decided, denied, announced, or did, place the actor close to the action or reporting verb with `nearN` inside the relevant field. Separate `hlp=(actor)` and `hlp=(verb)` clauses do not prove that the actor performed the action.
- Keep the first query compact and high-signal. Do not treat capitals, generic demonyms, or broad words such as `production`, `market`, or `exports` as interchangeable with the focal entity or subject unless context makes them discriminating.
- Use `not` sparingly and only for demonstrated false-positive families; a broad exclusion can silently remove relevant coverage.
- Prefer Factiva's displayed index filters for source, company, subject, industry, region, language, and date. Do not invent internal codes.
- Keep query syntax and UI filters complementary; do not duplicate constraints unless doing so intentionally improves precision.

Before execution, provide or internally record the exact query and intended filters so every iteration is auditable.

## Operate Factiva

Use the existing authenticated browser session. Prefer the user's named browser; otherwise use the already-open Factiva surface. Never request, read, store, or expose credentials. If authentication has expired in an otherwise controllable browser, ask the user to sign in.

Use the Free Text Search interface, not the simple natural-language search. Leave Search Genius off when running handcrafted advanced syntax unless the user explicitly asks for it. Set the date range deliberately; never accept the three-month default without checking it against the question.

Run the focused query first. For news-article research, select **Publications** before interpreting the count; Factiva's **All** total can also include websites, blogs, and photos. Inspect a representative spread of titles, dates, sources, and snippets, then broaden only when coverage is insufficient. For relationship or attribution searches, refine if the inspected sample frequently mentions both concepts without expressing the requested relationship. Preserve a query ledger containing each materially different query, its filters, active content type, result count, and the reason for the next change.

Use fresh accessibility state after every menu, navigation, or form-structure change. Never reuse element indices from an older state. Prefer semantically labeled controls; use coordinates only as a last resort after a fresh screenshot. Verify the visible query, date range, language, text scope, and duplicate setting before searching.

When refining from the results page, prefer the browser Back control or an accessible Factiva search/edit control. Do not use a coordinate click on **Modify search** when Back is available.

If the browser or control session disappears, make one recovery attempt using the existing browser/window inventory. Do not repeatedly type proxy URLs into the address bar. If recovery fails or the browser becomes unstable again, switch to Boolean-only mode. Describe it as a browser-control failure, not as Factiva closing the browser, unless there is direct evidence.

Do not create alerts, save searches, download batches, or modify account settings unless the user explicitly asks. Do not mass-scrape, redistribute full articles, or build a persistent article archive; work within the user's institutional license and summarize licensed content.

## Report the work

Match the output to the request. For a completed investigation, include:

1. the interpreted scope and any assumptions;
2. the final exact query plus date, language, source, duplicate, text-scope, and index filters;
3. the main findings, separating article claims from your synthesis;
4. a concise source list with title, publication, publication date, author when available, and Factiva link or document identifier when available;
5. coverage limitations, unresolved ambiguity, and useful follow-up queries.

Only summarize findings from the final query and filters that were visibly executed. If refinement was not completed, label earlier results preliminary or omit them; never present a planned query as executed.

If the user asked only for a query or Boolean-only mode applies, return only the paste-ready query code block.
