import { useState } from "react";
import { useSite } from "../SiteContext.jsx";
import { postJSON } from "../api.js";

const EMPTY = {
  name: "", email: "", phone: "",
  pickup_address: "", pickup_postcode: "", pickup_datetime: "",
  destination_address: "", dropoff_postcode: "",
  vehicle: "", passengers: 1, luggage: "",
  journey_type: "one_way", return_pickup_address: "", return_pickup_datetime: "",
};

// Current local time in the format <input type="datetime-local"> uses, e.g. "2026-09-25T12:30"
function nowLocal() {
  const d = new Date();
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().slice(0, 16);
}

export default function QuoteForm() {
  const { vehicles } = useSite();
  const [form, setForm] = useState(EMPTY);
  const [status, setStatus] = useState({ type: "", text: "" });
  const [sending, setSending] = useState(false);

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setSending(true);
    setStatus({ type: "", text: "" });
    try {
      const data = { ...form, passengers: Number(form.passengers) };
      const res = await postJSON("/api/quotes", data);
      setStatus({ type: "ok", text: `${res.message} Your reference is ${res.reference}.` });
      setForm(EMPTY);
    } catch (err) {
      setStatus({ type: "error", text: err.message });
    } finally {
      setSending(false);
    }
  }

  const isReturn = form.journey_type === "return";
  const chosen = vehicles.find((v) => v.id === form.vehicle);
  const minTime = nowLocal();

  return (
    <form className="quote-form" onSubmit={submit}>
      <h2>Get a quote</h2>

      <div className="field-row">
        <label>Pickup address
          <input name="pickup_address" value={form.pickup_address} onChange={update} required />
        </label>
        <label className="short">Postcode
          <input name="pickup_postcode" value={form.pickup_postcode} onChange={update} />
        </label>
      </div>

      <div className="field-row">
        <label>Destination
          <input name="destination_address" value={form.destination_address} onChange={update} required />
        </label>
        <label className="short">Postcode
          <input name="dropoff_postcode" value={form.dropoff_postcode} onChange={update} />
        </label>
      </div>

      <label>Pickup date and time
        <input type="datetime-local" name="pickup_datetime" min={minTime} value={form.pickup_datetime} onChange={update} required />
      </label>

      <div className="field-row">
        <label>Vehicle
          <select name="vehicle" value={form.vehicle} onChange={update} required>
            <option value="">Choose a vehicle</option>
            {vehicles.map((v) => (
              <option key={v.id} value={v.id}>{v.name} ({v.seats} seats)</option>
            ))}
          </select>
        </label>
        <label className="short">Passengers
          <input type="number" min="1" max={chosen ? chosen.seats : 16} name="passengers" value={form.passengers} onChange={update} required />
        </label>
      </div>

      <label>Luggage
        <input name="luggage" placeholder="e.g. 2 suitcases" value={form.luggage} onChange={update} />
      </label>

      <fieldset className="toggle">
        <legend>Journey</legend>
        <label><input type="radio" name="journey_type" value="one_way" checked={!isReturn} onChange={update} /> One way</label>
        <label><input type="radio" name="journey_type" value="return" checked={isReturn} onChange={update} /> Return</label>
      </fieldset>

      {isReturn && (
        <div className="field-row">
          <label>Return pickup address
            <input name="return_pickup_address" value={form.return_pickup_address} onChange={update} />
          </label>
          <label>Return date and time
            <input type="datetime-local" name="return_pickup_datetime" min={form.pickup_datetime || minTime} value={form.return_pickup_datetime} onChange={update} required />
          </label>
        </div>
      )}

      <label>Name
        <input name="name" autoComplete="name" value={form.name} onChange={update} required />
      </label>
      <div className="field-row">
        <label>Email
          <input type="email" name="email" autoComplete="email" value={form.email} onChange={update} required />
        </label>
        <label>Phone
          <input type="tel" name="phone" autoComplete="tel" value={form.phone} onChange={update} required />
        </label>
      </div>

      <button className="btn btn-amber btn-block" disabled={sending}>
        {sending ? "Sending…" : "Get my quote"}
      </button>

      {status.text && <p className={`form-status ${status.type}`} role="status">{status.text}</p>}
    </form>
  );
}
