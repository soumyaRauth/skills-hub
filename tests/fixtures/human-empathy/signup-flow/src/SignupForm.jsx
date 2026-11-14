import { useState } from "react";
import { validate } from "./validation";
import { createAccount } from "./api";
import { track } from "./analytics";

const initial = {
  firstName: "", lastName: "", email: "", password: "", confirmPassword: "",
  phone: "", companyName: "", companySize: "", country: "",
  acceptTerms: false, marketing: true,
};

export default function SignupForm({ onDone }) {
  const [form, setForm] = useState(initial);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState(null);

  const set = (k) => (e) =>
    setForm({ ...form, [k]: e.target.type === "checkbox" ? e.target.checked : e.target.value });

  const isComplete = Object.keys(initial)
    .filter((k) => k !== "marketing")
    .every((k) => Boolean(form[k]));

  async function submit(e) {
    e.preventDefault();
    const found = validate(form);
    setErrors(found);
    if (Object.keys(found).length) {
      track("signup_validation_failed", { fields: Object.keys(found) });
      return;
    }
    try {
      await createAccount(form);
      track("signup_completed");
      onDone();
    } catch (err) {
      setServerError(err.message);
      setForm(initial); // start clean after a failed attempt
      track("signup_server_error");
    }
  }

  return (
    <form onSubmit={submit} className="signup">
      <h1>Create your Ledgerly account</h1>

      <div className="row">
        <input placeholder="First name" value={form.firstName} onChange={set("firstName")} />
        <input placeholder="Last name" value={form.lastName} onChange={set("lastName")} />
      </div>
      {errors.firstName && <span className="err">{errors.firstName}</span>}
      {errors.lastName && <span className="err">{errors.lastName}</span>}

      <input placeholder="Email" value={form.email} onChange={set("email")} />
      {errors.email && <span className="err">{errors.email}</span>}

      <input type="password" placeholder="Password" value={form.password} onChange={set("password")} />
      {errors.password && (
        <span className="err">
          Invalid password. Passwords need 12+ characters, an uppercase letter, a number and a symbol.
        </span>
      )}
      <input type="password" placeholder="Confirm password" value={form.confirmPassword} onChange={set("confirmPassword")} />
      {errors.confirmPassword && <span className="err">{errors.confirmPassword}</span>}

      <input placeholder="Phone (+15551234567)" value={form.phone} onChange={set("phone")} />
      {errors.phone && <span className="err">{errors.phone}</span>}

      <input placeholder="Company name" value={form.companyName} onChange={set("companyName")} />
      <select value={form.companySize} onChange={set("companySize")}>
        <option value="">Company size</option>
        <option>2-10</option>
        <option>11-50</option>
        <option>51-200</option>
        <option>200+</option>
      </select>
      <select value={form.country} onChange={set("country")}>
        <option value="">Country</option>
        <option>United States</option>
        <option>United Kingdom</option>
        <option>Germany</option>
        <option>India</option>
      </select>

      <label className="check">
        <input type="checkbox" checked={form.acceptTerms} onChange={set("acceptTerms")} />
        I accept the <a href="/terms">Terms of Service</a>
      </label>
      <label className="check subtle">
        <input type="checkbox" checked={form.marketing} onChange={set("marketing")} />
        Send me tips and offers. (Uncheck if you don't want to grow your business.)
      </label>

      {serverError && <div className="banner-error">{serverError}</div>}

      <button type="submit" disabled={!isComplete}>Submit</button>
    </form>
  );
}
