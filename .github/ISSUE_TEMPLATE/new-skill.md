---
name: New skill proposal
about: Propose an additional skill for this repository
title: "[skill] "
labels: skill-proposal
---

## Skill name

<!-- kebab-case, e.g. change-guard -->

## Problem it solves

<!-- What does a developer get wrong today without it? Be concrete. -->

## When an agent should invoke it

<!-- The trigger conditions, in the words a developer would actually use. -->

## Proposed workflow

<!-- The phases the skill would run. What does it inspect, in what order? -->

1.
2.
3.

## Output

<!-- What does the skill produce? Sketch the structure. -->

## Relationship to impact-map

<!-- Does it consume an impact map, extend it, or stand alone? -->

## Why a skill rather than a tool

<!-- Skills are instructions. If this needs an engine, index, or server, say so
     and explain why that is justified — this repository deliberately avoids
     building infrastructure. -->

## Evidence discipline

<!-- How does the skill avoid presenting speculation as fact? -->

## Checklist

- [ ] It does not require an MCP server, custom CLI, or hosted service
- [ ] It works from ordinary repository inspection
- [ ] It is read-only, or its write behavior is explicitly gated on user consent
- [ ] I can supply at least one test fixture and its expected findings
