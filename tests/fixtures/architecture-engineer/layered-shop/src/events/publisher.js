const events = [];

async function publish(name, payload) {
  events.push({ name, payload, at: new Date() });
}

module.exports = { publish, events };
