# Technical accuracy and educational trust

A reader who types a command from a book and gets an error does not think
"the book is out of date". They think "I am not good at this". Technical
accuracy in teaching material is an empathy issue first.

## Contents

- What to check
- Verifying code and commands
- Versions and staleness
- Security in teaching examples
- Claims, references and citations
- Changing technical content
- Reporting accuracy

## What to check

- **Code correctness:** runs, produces the output the book shows, handles the
  case the text describes.
- **API usage:** functions, parameters and imports exist in the version the
  book names; deprecated or removed APIs.
- **Version compatibility:** language, framework, library, OS and tool
  versions stated, consistent across chapters, and still installable.
- **Commands:** exact syntax, platform differences (macOS, Linux, Windows
  shells; `python` versus `python3`; `pip` versus `pip3`), required
  privileges, the directory they must be run from.
- **Configuration examples:** complete, valid syntax, matching the code that
  reads them.
- **Dependencies:** everything the reader must install is named before it is
  used.
- **Prerequisites:** accounts, keys, tools, prior chapters.
- **Terminology:** technical terms used correctly and consistently.
- **Security implications:** see below.
- **Outdated instructions:** UI paths in screenshots, renamed products, moved
  documentation.

## Verifying code and commands

1. **Extract** every code block and command in scope, keeping the order and
   the chapter's stated environment.
2. **Classify** each: complete program, fragment meant to be added to an
   earlier file, output, or pseudocode. Fragments are checked in the program
   they belong to.
3. **Run what can be run** in an isolated directory (a scratch folder, a
   virtual environment, a container), with the versions the book states
   pinned. Never run a book's commands against the person's real system,
   accounts or data, and never run anything destructive or anything that
   needs credentials.
4. **Compare** actual output with the book's shown output.
5. **Follow the reader's path:** run the chapter's steps in order, from the
   state the previous chapter left. Many defects only appear in sequence (a
   file the book never told the reader to create, an import added silently
   between listings).
6. **Record** each item as:
   - `EXECUTED · PASS` — ran, matched;
   - `EXECUTED · FAIL` — ran, and what happened instead;
   - `CHECKED` — not run, but verified against official documentation for the
     stated version (name the source);
   - `UNVERIFIED` — neither, with the reason (needs credentials, a paid
     service, hardware, network access unavailable).

Never report a code example as correct because it looks correct. Looking
correct is how most broken examples got into print.

## Versions and staleness

- Find the stated versions. If none are stated, that is itself a finding for
  any fast-moving tool: the reader cannot reproduce the book's environment.
- Check the code against those versions, and note where current versions
  differ in ways the reader will hit if they install the latest (a moved
  import, a renamed option, a changed default).
- Use available research tools (web search, official changelogs, the
  package's own documentation) for anything that may have changed after your
  training data; state what you checked and when. If you cannot check, say the
  claim is `UNVERIFIED` for current versions.

## Security in teaching examples

Readers copy examples into real projects. Flag:

- secrets, keys or passwords in code; disabled TLS verification; `chmod 777`;
  running as root without need;
- SQL built by string concatenation; unescaped user input in HTML; `eval` of
  input; deserializing untrusted data;
- permissive CORS or authentication bypasses presented without warning;
- `curl … | sh` installers without explanation.

A simplified example is acceptable when the book says it is simplified and
shows, or points to, the safe version. Silently teaching an unsafe pattern is
a high-severity finding. For a security assessment of a product rather than a
book, hand off to `standards-compass`.

## Claims, references and citations

- Factual claims (history, performance numbers, adoption figures, research
  findings) are checked or marked for checking.
- References and citations exist, say what the text says they say, and are
  findable. Never invent a reference, an author, a title, a DOI, a quotation
  or a statistic, including as a "suggested" source. If a claim needs a source
  and you cannot find one, say so.
- Links work and point to the intended page.

## Changing technical content

- Never silently change technically significant content. Every change to
  code, commands, versions or technical claims is listed with its reason.
- Verify the replacement the same way as the original: run it, or check it
  against official documentation for the stated version.
- Check the consequences: a renamed variable in listing 3.4 must be renamed
  in 3.5–3.9, in the prose, in the downloadable code and in the exercises'
  answers.
- Upgrading the book's target version is a direction change (rule 9): it can
  ripple through every chapter. Propose it with the scope it implies.

## Reporting accuracy

Summarize as counts you actually produced, then list the failures:

```
TECHNICAL ACCURACY — Chapter 3 (Python 3.12, FastAPI as stated in ch. 1)
  Code blocks     9    EXECUTED · PASS 5 · EXECUTED · FAIL 2 · CHECKED 1 · UNVERIFIED 1
  Commands        4    EXECUTED · PASS 3 · EXECUTED · FAIL 1

  FAIL  Listing 3.4   `from pydantic import BaseSettings` — ImportError on Pydantic 2;
                      BaseSettings moved to the separate pydantic-settings package
  FAIL  §3.1 step 2   `uvicorn main:app` — uvicorn was never installed (§1.3 installs
                      fastapi only)
  UNVERIFIED  §3.6    Deploy command needs a cloud account; not run
```
