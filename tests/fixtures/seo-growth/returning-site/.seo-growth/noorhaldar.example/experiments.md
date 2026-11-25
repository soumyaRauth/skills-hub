# Experiments · noorhaldar.example

Results: IMPROVED · NO CHANGE · WORSE · INCONCLUSIVE. Decisions: KEEP · EXTEND · REVERT · RE-EVALUATE (references/experimentation.md).

### EXP-001 · Name and role in the homepage title and h1
- Task: SEO-002 · Pages: /
- Hypothesis: naming the owner and role in the title and h1 makes the homepage the result for name searches, because the old title "Home" said nothing about whose site it is
- Baseline: snapshot 2026-10-20, web search tool, location unknown: "noor haldar" → homepage not in the first 10 results; GitHub profile at 4; 3 results about different people (VERIFIED, data/serp-2026-10-20.md). No Search Console.
- Change: <title>Home</title> → <title>Noor Haldar · Data engineer and Apache Airflow consultant</title>; h1 "Portfollio" → "Noor Haldar"
- Implemented: 2026-10-20 · Deployed: 2026-10-21 (owner) · Recrawled: UNKNOWN
- Expected: homepage appears for "noor haldar"
- Evaluate: from 2026-11-24, repeating the same query set with the same tool
- Result: —
- Interpretation: —
- Decision: —
