import { findInvoicesByUser } from './store.js';

// Sessions are created by the auth layer. A missing session means the request
// was not authenticated.
export function listInvoices(session) {
  if (!session) return { status: 401, body: { error: 'unauthenticated' } };

  return {
    status: 200,
    body: { invoices: findInvoicesByUser(session.userId) },
  };
}

// GET /invoices/:id  —  not implemented yet.
