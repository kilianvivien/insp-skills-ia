# Factiva Advanced Search Syntax

Use this reference for Free Text Search / Search Builder. The syntax below was cross-checked against Factiva's official advanced-search examples and the authenticated interface. Factiva capitalization is ignored; lowercase operators make generated queries easier to audit.

## Query construction

Use explicit grouping even when operator precedence would make the query valid:

```text
(entity alias 1 or entity alias 2) and (issue phrase or issue synonym*)
```

Factiva commonly treats consecutive unconnected words as a phrase, but use straight double quotes when an exact phrase matters, when a phrase includes a common word, or when a literal word is also an operator:

```text
"same store sales"
"research and development"
"Bill Gates"
```

Reserved words such as `and`, `or`, `not`, `same`, and `near` must be quoted when searched literally.

Factiva processes grouped expressions first, then proximity operators, then `atleastN` and field qualifiers, then `not`, `and`, and `or`. Parentheses remove doubt.

## Operators

| Need | Syntax | Notes |
|---|---|---|
| All concepts | `A and B` | Use between distinct concept groups. |
| Any synonym | `(A or B)` | Parenthesize synonym families. |
| Exclude | `A not B` | Use only for verified false positives. |
| Same paragraph | `A same B` | Do not chain it. Use `A same (B and C)`, not `A same B same C`. |
| Ordered proximity | `A w/3 B` | `B` is within the specified position/range after `A`; valid `N` is 1–10. |
| Ordered proximity | `A adj5 B` | Terms remain in order; valid `N` is 1–10. |
| Unordered proximity | `A near5 B` | Either order; valid `N` is 1–500. `near` means `near1`. |
| Unordered proximity | `A /N30/ B` | Equivalent explicit form; a number from 1–500 is required. |
| Early mention | `term/F50/` | Term must occur within the first `N` words, with `N` from 1–500. Full-text search only. |
| Mention frequency | `atleast3 term` | Requires at least `N` mentions, with `N` from 1–50. Full-text search only. |
| Word count | `wc>500` | Comparisons such as `wc>500` or `wc<1000`; never use thousands separators. |

`atleastN` cannot wrap a grouped expression. Repeat it for each alternative:

```text
(atleast3 battery or atleast3 batteries)
```

Do not combine `/FN/` with a field-qualified expression, an `atleastN` expression, or a word-count range.

## Wildcards

- `telecom*` matches any ending. Use at least three literal characters and place `*` only at the end.
- `earn$4` allows a bounded suffix of up to four characters. `$` accepts 1–9; without a number Factiva uses 5. Use at least three literal characters and place it only at the end.
- `globali?ation` uses `?` for a one-character spelling variation. Put at least three literal characters before `?`.

Use wildcards selectively. Short stems often create false positives and can make proximity logic opaque.

## Field qualifiers

Prefer the interface's indexed filters because they validate names and codes. These free-text qualifiers are useful when a verified value is available:

| Field | Syntax | Meaning |
|---|---|---|
| Headline | `hd=(terms)` | Terms in the headline. |
| Headline or lead paragraph | `hlp=(terms)` | Strong relevance constraint. |
| Lead paragraph | `lp=(terms)` | Terms in the lead paragraph. |
| Author/byline | `by=(name)` | Author field. |
| Source | `rst=CODE` | Source code; obtain the code from Factiva rather than guessing. |
| Language | `la=CODE` | Language code; prefer the Language panel unless verified. |
| Indexed company | `fds=CODE` | Dow Jones company code; select the company in the Company panel unless verified. |
| Word count | `wc>NUMBER` | Numeric word-count constraint. |
| Publication date | `date from YYYYMMDD to YYYYMMDD` | Inclusive date range. Repeat the same date for a single day. |

Never invent a source, language, company, subject, industry, or region code. Use the relevant Factiva panel and select the displayed index entry.

Common language qualifiers include `la=fr`, `la=en`, `la=de`, and `la=es`. Use the language of the user's request for the primary query unless they specify a different publication language. For multiple languages, include the corresponding language qualifiers in a grouped `or` expression and include search terms in each language.

Use the unambiguous `YYYYMMDD` form for dates:

```text
date from 20260915 to 20260915
date from 20260901 to 20260915
```

## Precision patterns

Company as the focal subject:

```text
hlp=("COMPANY NAME" or ALIAS) and (ISSUE_A or ISSUE_B or STEM*)
```

Relationship or event where closeness matters:

```text
("ENTITY A" or ALIAS_A) near15 ("ENTITY B" or EVENT_TERM)
```

Sustained coverage rather than a passing mention:

```text
hlp=("ENTITY") and (atleast2 TERM_A or atleast2 TERM_B)
```

Default topical-news pattern when the browser cannot set **Title and first paragraph**:

```text
hlp=(ENTITY_TERMS) and hlp=(TOPIC_TERMS) and la=LANGUAGE and date from YYYYMMDD to YYYYMMDD
```

Use separate `hlp=` clauses for the focal entity and subject. This is usually clearer and less fragile than placing a large nested proximity expression inside one field qualifier.

### Relational and attribution searches

Separate field clauses express co-occurrence, not attribution:

```text
hlp=("Donald Trump") and hlp=(said or statement*)
```

This can retrieve an article in which Trump is mentioned but someone else made the statement. When the user's question depends on who said or did something, bind the actor to a high-signal verb with proximity:

```text
hlp=(("Donald Trump" or "President Trump" or "U.S. President Trump") near8 (said or told or announced or declared or warned or wrote or posted))
```

Prefer canonical full-name and title variants in the focused pass. Add a surname-only variant only in a later recall pass because it can match relatives, organizations, administrations, or unrelated people. Avoid nouns such as `statement*`, `comment*`, and `remark*` in the first attribution pass: they often describe statements by other people *about* the target. Add them only after inspecting missed relevant articles.

Useful statement-search progression:

1. focused: actor `near5`–`near8` a direct reporting verb in headline/lead;
2. broader: add verbs such as `called`, `claimed`, `denied`, `urged`, `suggested`, or platform-specific wording such as `posted` and `wrote`;
3. recall: widen proximity, add surname-only variants, or move to full text.

Keep placeholders out of the final query. Generate language-specific synonyms when the selected publication languages require them; do not assume an English query retrieves equivalent non-English wording.

## Query checks

Before running, verify that:

- every mixed `and`/`or` expression is grouped;
- quotes are straight ASCII quotes and delimiters are balanced;
- proximity numbers stay within their supported ranges;
- `atleastN` applies to terms rather than parenthesized groups;
- `/FN/` is not attached to a field qualifier, frequency term, or range;
- UI filters use displayed, selected index values rather than guessed codes;
- exclusions are narrow enough not to suppress relevant evidence.

## Boolean-only output

When computer/browser control is unavailable, generate the final query without attempting to operate Factiva or replacing it with web research.

Return exactly one single-line query in a fenced `text` block. Include:

- `hlp=(...)` for each central concept by default;
- `la=...` matching the user's language unless another corpus language was requested;
- `date from ... to ...` when the request supplies or implies an absolute date range;
- only verified source, company, subject, industry, or region codes.

Do not add a filter recipe or claim search results. If an essential requested restriction has no safe textual equivalent and its index code is unknown, add one short note after the code block naming that single Factiva UI filter.

Example for a French, single-day topical-news request:

```text
hlp=("Arabie saoudite" or "Royaume d'Arabie saoudite" or saoudien*) and hlp=(pétrole or brut or OPEP or Aramco or oléoduc* or "marché pétrolier") and la=fr and date from 20260915 to 20260915
```

Example for statements attributed to a person:

```text
hlp=(("Donald Trump" or "President Trump" or "U.S. President Trump") near8 (said or told or announced or declared or warned or wrote or posted)) and la=en and date from 20260913 to 20260915
```

If Factiva returns a syntax error, simplify by removing the most advanced clause, validate the base expression, and add clauses back one at a time. Do not silently fall back to simple search.

## Authoritative reference

Factiva's official examples page: <https://global.factiva.com/help/en/text/ft_exmpl.html>
