---
name: google-scholar-profile
description: Use an author's Google Scholar profile as a discovery hop — not a host itself — to reach their homepage, the paper's other versions, and links that lead to the replication package. Step-by-step to mine a Scholar profile for package leads.
---

# Source: Google Scholar profile (a discovery hop)

## When you get routed here
You can't find an author's homepage or repo directly. Scholar rarely hosts the package
itself, but it reliably surfaces the author's **homepage link**, co-authors, and the
paper's **other versions** (preprint, university repository) that do carry package links.

## Step-by-step: LOCATE
> Scholar can't be fetched directly (403 — see Gotchas), so drive it through `web_search`:
> one query typically returns **both** the profile URL *and* the author's homepage.
1. `web_search` `"<author full name>" <university/field>`. In the results, identify the
   **Google Scholar profile** URL (`scholar.google.com/citations?user=…`) — use it to
   **disambiguate** (confirm the affiliation and that this paper is theirs), not to crawl.
2. In the same results, grab the author's **homepage / departmental page** (Scholar profiles
   also carry a "Homepage" link, but the search usually surfaces it directly) → hand off to
   `author-homepage`.
3. Also search the paper title for **other versions** — a preprint / working-paper /
   institutional-repository copy often includes the availability statement or a repo link the
   journal HTML omits. (Scholar's "All N versions" is the manual equivalent.)
4. **Enumerate co-authors** from the results and check each one (route by role, SOP §2.2).

## Step-by-step: DOWNLOAD
5. Scholar links lead *out* to a host — follow to the homepage/repo/deposit and use that
   host skill's download steps. Scholar itself has nothing to download.

## Gotchas
- **Scholar blocks automated fetch (verified 2026-07: `scholar.google.com` returns HTTP
  403 to a programmatic GET).** The agent **cannot crawl a profile page directly.** Use
  Scholar as a *lead surfaced through `web_search`* (the profile URL, the "Cited by",
  "Homepage", and "All N versions" links usually appear in search snippets) and then fetch
  the **destination** host (homepage / repo / preprint), which is not bot-walled. If the only
  path to the package runs through the profile page itself, treat it as a human hop →
  `needs_review`, don't assert you scraped it.
- **Disambiguation**: common names have multiple profiles / merged entries — confirm the
  affiliation and that *this* paper appears before trusting a profile's links.
- No profile ≠ no package — many authors have none; fall through to `author-homepage`,
  `github-repository-and-pages`, and `data-repository`.
- Scholar's cached PDF is a copy for reading, not a provenance source — verify the real host.

## Worked example (from corpus) — incarceration-racial-privilege (v3-10-190), Scholar hop
Verified live 2026-07-04. Reaching the `incarceration-racial-privilege` package (Lance
Hannon) *when you don't already have the homepage*, using Scholar as a `web_search`-surfaced
signpost (Scholar itself 403s a bot):
1. `web_search` `"Lance Hannon" Villanova sociology` returns, in one result set, **both** his
   **Google Scholar profile** — `https://scholar.google.com/citations?user=ZfzwxMgAAAAJ` —
   **and** his Villanova homepage `http://www88.homepage.villanova.edu/lance.hannon/`.
2. **Use the Scholar profile to disambiguate** (Villanova Sociology; "Can Incarceration Really
   Strip People of Racial Privilege?" appears in his publication list → right author). Don't
   crawl the profile — the 403 makes that impossible; it is a signpost only.
3. **Follow the homepage result** → `author-homepage`. (Apply that skill's http→https fix: the
   `http://` host is dead; the page loads over `https://`.) On the page, pick the
   **"NLSY79 Stata Dataset in Person-Years & Code"** item and download `Hannon_DeFina.dta` +
   `Hannon_DeFina_prg.do`.

> Scholar was the *pointer that disambiguated the author and co-surfaced the homepage*; the
> verified find lives at the homepage destination. This is the realistic Scholar workflow
> under the 403 constraint — search-surfaced, not crawled.

## After download → `calibration-honesty`
Scholar only points; provenance still comes from the destination (owner is an author +
citation match). Open the tree, then let `agent.toml [verdict]` assign the status.
