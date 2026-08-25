import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { createNote, getNote, listNotes, updateNote, deleteNote, __reset } from '../src/notes.js';

beforeEach(() => __reset());

test('creates a note', () => {
  const note = createNote({ title: 'Groceries', body: 'milk' });
  assert.equal(note.id, 1);
  assert.equal(note.title, 'Groceries');
});

test('rejects an empty title', () => {
  assert.throws(() => createNote({ title: '   ' }), /title_required/);
});

test('lists notes newest first', () => {
  createNote({ title: 'first' });
  createNote({ title: 'second' });
  assert.deepEqual(listNotes().map((n) => n.title), ['second', 'first']);
});

test('gets a note by id, or null', () => {
  const note = createNote({ title: 'find me' });
  assert.equal(getNote(note.id).title, 'find me');
  assert.equal(getNote(999), null);
});

test('updates a note', () => {
  const note = createNote({ title: 'draft' });
  const updated = updateNote(note.id, { title: 'final' });
  assert.equal(updated.title, 'final');
  assert.notEqual(updated.updatedAt, note.updatedAt);
});

test('deletes a note', () => {
  const note = createNote({ title: 'temporary' });
  assert.equal(deleteNote(note.id), true);
  assert.equal(getNote(note.id), null);
});
