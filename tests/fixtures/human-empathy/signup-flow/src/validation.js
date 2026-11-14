// Password policy agreed with the security review.
export const PASSWORD_RULES = {
  minLength: 12,
  needsUpper: true,
  needsNumber: true,
  needsSymbol: true,
};

export function validatePassword(pw) {
  if (pw.length < PASSWORD_RULES.minLength) return false;
  if (PASSWORD_RULES.needsUpper && !/[A-Z]/.test(pw)) return false;
  if (PASSWORD_RULES.needsNumber && !/[0-9]/.test(pw)) return false;
  if (PASSWORD_RULES.needsSymbol && !/[^A-Za-z0-9]/.test(pw)) return false;
  return true;
}

export function validatePhone(phone) {
  // E.164 only
  return /^\+[1-9]\d{7,14}$/.test(phone);
}

export function validate(form) {
  const errors = {};
  if (!form.firstName) errors.firstName = "Required";
  if (!form.lastName) errors.lastName = "Required";
  if (!/^\S+@\S+\.\S+$/.test(form.email)) errors.email = "Invalid email";
  if (!validatePassword(form.password)) errors.password = "Invalid password";
  if (form.password !== form.confirmPassword) errors.confirmPassword = "Passwords do not match";
  if (!validatePhone(form.phone)) errors.phone = "Invalid phone";
  if (!form.companyName) errors.companyName = "Required";
  if (!form.companySize) errors.companySize = "Required";
  if (!form.country) errors.country = "Required";
  if (!form.acceptTerms) errors.acceptTerms = "Required";
  return errors;
}
