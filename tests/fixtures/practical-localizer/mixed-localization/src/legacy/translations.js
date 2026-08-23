// Older translation table, still imported by the settings and admin screens.
export const bn = {
  login: "প্রবেশ করুন",
  logout: "প্রস্থান করুন",
  password: "পাসওয়ার্ড",
  settings: "সেটিংস",
  delete: "ডিলিট করুন",
  save: "সেভ করুন",
  cancel: "বাতিল",
  download: "ডাউনলোড করুন",
  upload: "আপলোড করুন",
  server_error: "সার্ভার সাড়া দিচ্ছে না",
};

export function tr(key) {
  return bn[key] || key;
}
