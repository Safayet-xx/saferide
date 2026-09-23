import { useState } from "react";
import { postJSON } from "../api.js";

const TOPICS = ["General", "Personal account", "Business account", "Driving for us", "Lost property", "Feedback"];

export default function ContactForm({ defaultTopic = "General", buttonText = "Send message" }) {
  const empty = { name: "", email: "", phone: "", topic: defaultTopic, message: "" };
  const [form, setForm] = useState(empty);
  const [status, setStatus] = useState({ type: "", text: "" });
  const [sending, setSending] = useState(false);

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setSending(true);
    setStatus({ type: "", text: "" });
    try {
      const res = await postJSON("/api/messages", form);
      setStatus({ type: "ok", text: res.message });
      setForm(empty);
    } catch (err) {
      setStatus({ type: "error", text: err.message });
    } finally {
      setSending(false);
    }
  }

  return (
    <form className="contact-form" onSubmit={submit}>
      <label>Name<input name="name" value={form.name} onChange={update} required /></label>
      <div className="field-row">
        <label>Email<input type="email" name="email" value={form.email} onChange={update} required /></label>
        <label>Phone<input type="tel" name="phone" value={form.phone} onChange={update} /></label>
      </div>
      <label>Topic
        <select name="topic" value={form.topic} onChange={update}>
          {TOPICS.map((t) => <option key={t}>{t}</option>)}
        </select>
      </label>
      <label>Message<textarea name="message" rows="5" value={form.message} onChange={update} required /></label>
      <button className="btn btn-navy" disabled={sending}>{sending ? "Sending…" : buttonText}</button>
      {status.text && <p className={`form-status ${status.type}`} role="status">{status.text}</p>}
    </form>
  );
}
