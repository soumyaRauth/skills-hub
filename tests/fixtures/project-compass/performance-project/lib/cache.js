// In-process cache. Cleared on every deploy, not shared between instances.
const store = new Map();
const TTL_MS = 15 * 60 * 1000;

function get(key) {
  const hit = store.get(key);
  if (!hit) return null;
  if (Date.now() - hit.at > TTL_MS) {
    store.delete(key);
    return null;
  }
  return hit.value;
}

function set(key, value) {
  store.set(key, { value, at: Date.now() });
}

module.exports = { get, set };
