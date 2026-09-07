# Guardrail mode — "add document upload"

The half of the skill that runs during ordinary work. No audit, no report, no
standards lecture. Two short blocks around the implementation.

---

**Request:** *"Add drag-and-drop file upload so customers can attach documents
to a case."*

## Before

```markdown
### Standards consideration

Uploads bring a few requirements with them, so I'll build it with:

- server-side type and size limits (the client-side check is a UX nicety)
- generated filenames, not the client's
- storage in the object store rather than under the web root
- authorization on download as strict as on upload
- a keyboard-accessible file picker alongside the drop zone

Implementing now.
```

Five lines. It names what will be built, not what could go wrong.

## During

Partway through, the storage path is being built from the uploaded filename:

> Switching the storage key to a generated UUID — building it from the
> client-supplied filename would let `../` in the name write outside the case
> directory.

One line, fixed in place, no ceremony.

## After

```markdown
### Standards check — document upload

✓ Type allowlist and 25 MB limit enforced server-side — src/upload/validate.ts
✓ Storage key is a generated UUID; original name kept as metadata only
✓ Download authorization reuses the case access policy — src/api/files/[id].ts
✓ Drop zone has a keyboard-operable file input with a visible label
⚠ No malware scanning. Files are only downloadable by users on the same case,
  so I didn't add it — worth revisiting if documents ever become shareable
  outside the case
⚠ No retention rule. Case documents currently live forever; that's a decision
  someone should make rather than a default
```

The two warnings are the useful part. Neither blocks the work, both are real,
and the second is the kind of thing that becomes a privacy finding in a year.

---

## The same feature, at three risk levels

| Request | Classification | Response |
| --- | --- | --- |
| *"Rename 'Attachments' to 'Documents'"* | `LOW` | Just do it. Say nothing |
| *"Let users attach documents to a case"* | `HIGH` | The above |
| *"Let users share document links publicly"* | `HIGH`, different | Named before building: link unguessability, expiry, revocation, whether the document contains personal data, and whether a public link should be possible at all for case documents |

The classification is about the change, not the words in it.

---

## What did not happen

- No audit was triggered by a feature request.
- No standards were named at the user. "WCAG 2.2 success criterion 2.5.7
  Dragging Movements" is what the keyboard alternative is *for*; the user did
  not need to hear it.
- No permission was requested. The requirements were built in, and the work
  continued.
- Nothing was blocked.
