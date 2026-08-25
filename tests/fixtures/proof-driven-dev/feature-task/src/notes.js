// In-memory notes store. Deliberately small: the point of this fixture is that
// the conventions here (id generation, validation, error shape, return values)
// answer most of the questions a "add archiving" request raises.

let nextId = 1;
const notes = new Map();

export function createNote({ title, body = '' }) {
  if (!title || !title.trim()) {
    throw new Error('title_required');
  }
  const note = {
    id: nextId++,
    title: title.trim(),
    body,
    createdAt: '2026-01-01T00:00:00.000Z',
    updatedAt: '2026-01-01T00:00:00.000Z',
  };
  notes.set(note.id, note);
  return note;
}

export function getNote(id) {
  return notes.get(id) ?? null;
}

export function listNotes() {
  return [...notes.values()].sort((a, b) => b.id - a.id);
}

export function updateNote(id, changes) {
  const note = notes.get(id);
  if (!note) throw new Error('not_found');
  const updated = { ...note, ...changes, id: note.id, updatedAt: '2026-01-02T00:00:00.000Z' };
  notes.set(id, updated);
  return updated;
}

export function deleteNote(id) {
  return notes.delete(id);
}

// Test-only helper, used by the existing suite.
export function __reset() {
  notes.clear();
  nextId = 1;
}
