const notes = [];

export function listNotes() {
  return notes;
}

export function createNote(text) {
  const note = { id: notes.length + 1, text, createdAt: new Date().toISOString() };
  notes.push(note);
  return note;
}
