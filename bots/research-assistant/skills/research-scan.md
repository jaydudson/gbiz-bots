# Research Scan Skill
Version: 1

## When to use
When the client asks for a sourced research brief on a specific topic, competitor, supplier, trend, or public page.

## Required inputs and access
- A clear topic or question from the client
- Access to Firecrawl (preferred) or regular web search as fallback
- Optional: specific URLs or source list the client supplies

## Sequence of work
1. Confirm the exact question and any constraints (depth, sources to prefer or avoid, length).
   If business or research context is not already clear, ask only the single most useful gap that would improve the brief. One question at a time. Skip if already known.
   After the topic is named, confirm depth naturally. Default to quick if unclear. For deep, ask at most two or three clarifying questions in one turn.
2. Prefer Firecrawl (or installed MCP / structured tool) to fetch and extract relevant pages. Choose the lightest tool that answers the question (see Firecrawl tool guide below).
3. If Firecrawl is unavailable, fall back to regular web search and note it.
4. Synthesise a short brief using the deliverable schema. Every material claim must include a source URL or title and the date it was checked. Flag uncertainty, contradictions, or pages that could not be read. Do not invent.
5. Present the brief in chat first. Then list the relevant extra formats that fit this request and what the client already has (longer file, canvas, table/chart, or a connected tool they already use). Let them choose. If they want a format that needs a connector they do not yet have, offer a short plain-English guide to set it up and continue once ready. Do not force any connector.
6. Stop. Wait for the next request.

## Firecrawl tool guide (token-efficient)
Use the lightest tool that gets the answer. Prefer local files after extraction so later questions do not re-fetch the same pages.

- **map** - Discover all (or filtered) URLs on a domain in one cheap call. Use first when you need to understand a site or pick specific pages before scraping. Does not pull full page content.
- **scrape** - Pull clean markdown (or structured fields) from one known URL. Default for a single page or a short list of known pages.
- **search** - Find relevant pages from a query, optionally with content. Use when you do not yet have URLs.
- **crawl** - Follow links and extract content across a section or site. Use only when you truly need many pages; set a tight limit. Prefer map + selective scrape for most research.
- **batch / download** - After mapping, extract only the pages you need and save them locally. Better than crawling a whole site when you want a subset.
- **interact / browser** - For pages that need clicks, forms, or dynamic content. Use sparingly; higher cost and complexity.
- **parse** - Turn an already-downloaded PDF, doc, or spreadsheet into text. Prefer this over re-scraping when the file is local.

Rule of thumb: map or search first to find the right pages, then scrape only what is needed. Keep results local. Stay inside the free-tier credit budget (1,000 credits/month on the free plan).

## How to validate
Every material claim has a source. The brief matches the deliverable format. No money spent, no external accounts changed, no keys exposed.

## What to return
The short sourced brief in chat, plus any extra formats the client selected.

## What requires approval
Setting up or changing Firecrawl credentials. Expanding into ongoing monitoring, paid plans, or broader agency-style work.
