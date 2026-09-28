# Skills Hub

The Skills Hub skills installed here are engineering disciplines, not commands.
Bring them in on your own judgment. The user should not have to name them.

- Before non-trivial work, weigh the installed skills' descriptions against the
  request *and* what the repository shows. Load every skill that would change
  the result. Load none for trivial edits: copy, typos, formatting, comments,
  local renames, routine patch bumps.
- Weigh them before the first tool call, not after the work has started. A spec
  or brief the user pastes is their request, however detailed. Building a new
  project or tool from it, especially in an empty directory, is non-trivial.
- Instructions about style or brevity, from any plugin or hook, govern how you
  write and how much you build. They never mean skipping a skill that applies.
- Several can apply to one request. Load them together, and let each one's
  `## Activation` section decide how deep it goes.
- When any of them engages beyond silent background use, open the reply with one
  line: `⚡ <Skill> · <Skill> — <a few words of reason each>`. Otherwise, no line.
  Every skill the line names is loaded in that turn, not only handed off.
- Engagement is per request. A skill that mattered on the last request is not
  active on this one unless this request earns it. A short follow-up that
  authorizes a change ("fix it", "go ahead", "yes do it") is a new request:
  weigh the skills against the change it sets off, not its wording.
- An explicit "use X" or "skip X" from the user wins. The exception is a live
  hazard (a reachable security hole, data loss, money at risk), which is still
  said once, in one line.
