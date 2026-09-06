// The adjustment lifecycle, in one place.
const TRANSITIONS = {
  draft: ['submitted'],
  submitted: ['approved', 'rejected'],
  approved: [],
  rejected: ['draft'],
};

function canTransition(from, to) {
  return (TRANSITIONS[from] || []).includes(to);
}

function assertTransition(from, to) {
  if (!canTransition(from, to)) {
    throw new Error(`illegal transition ${from} -> ${to}`);
  }
}

module.exports = { TRANSITIONS, canTransition, assertTransition };
