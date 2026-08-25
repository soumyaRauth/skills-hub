import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { createUser, findByEmail, __reset } from '../src/users.js';

beforeEach(() => __reset());

test('creates a user with a normalized email', () => {
  const user = createUser({ email: '  Ada@Example.COM ', name: 'Ada' });
  assert.equal(user.email, 'ada@example.com');
  assert.equal(user.role, 'member');
});

test('rejects a duplicate email', () => {
  createUser({ email: 'ada@example.com', name: 'Ada' });
  assert.throws(() => createUser({ email: 'ADA@example.com', name: 'Ada again' }), /email_taken/);
});

test('rejects an invalid role', () => {
  assert.throws(() => createUser({ email: 'g@example.com', name: 'G', role: 'owner' }), /invalid_role/);
});

test('finds a user case-insensitively', () => {
  createUser({ email: 'ada@example.com', name: 'Ada' });
  assert.equal(findByEmail('ADA@EXAMPLE.COM').name, 'Ada');
});
