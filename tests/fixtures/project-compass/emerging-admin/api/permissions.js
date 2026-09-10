const ROLES = ['support', 'support_lead', 'admin'];

function can(staff, action) {
  if (staff.role === 'admin') return true;
  if (action === 'view') return true;
  if (action === 'export') return staff.role === 'support_lead';
  if (action === 'bulk') return staff.role === 'support_lead';
  if (action === 'reassign') return staff.role === 'support_lead';
  return false;
}

module.exports = { can, ROLES };
