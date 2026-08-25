import { config } from './config.js';

const users = new Map(); // email -> user
let nextId = 1;

export const ROLES = ['member', 'admin'];

export function createUser({ email, name, role = 'member' }) {
  const normalized = config.normalizeEmail(email ?? '');

  if (!normalized.includes('@')) throw new Error('invalid_email');
  if (!name || !name.trim()) throw new Error('name_required');
  if (!ROLES.includes(role)) throw new Error('invalid_role');
  if (users.has(normalized)) throw new Error('email_taken');

  const user = { id: nextId++, email: normalized, name: name.trim(), role };
  users.set(normalized, user);
  return user;
}

export function findByEmail(email) {
  return users.get(config.normalizeEmail(email)) ?? null;
}

export function listUsers() {
  return [...users.values()];
}

export function __reset() {
  users.clear();
  nextId = 1;
}
