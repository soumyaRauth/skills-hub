export const config = {
  // Applies to every upload endpoint.
  maxUploadBytes: 5 * 1024 * 1024,
  allowedUploadTypes: ['text/csv'],
  // Users are matched case-insensitively on email everywhere in this app.
  normalizeEmail: (email) => email.trim().toLowerCase(),
};
