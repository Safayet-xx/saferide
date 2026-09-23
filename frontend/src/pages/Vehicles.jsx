import { Link } from "react-router-dom";
import { useSite } from "../SiteContext.jsx";
import PageHeader from "../components/PageHeader.jsx";

export default function Vehicles() {
  const { vehicles } = useSite();
  return (
    <>
      <PageHeader title="Our vehicles" intro="Pick the size that fits your group and luggage." />
      <section className="section">
        <div className="container vehicle-list">
          {vehicles.map((v) => (
            <article key={v.id} className="vehicle">
              <h2>{v.name}</h2>
              <p>{v.text}</p>
              <dl>
                <div><dt>Seats</dt><dd>{v.seats}</dd></div>
                <div><dt>Bags</dt><dd>{v.bags}</dd></div>
              </dl>
            </article>
          ))}
        </div>
        <div className="container center-cta">
          <Link className="btn btn-amber" to="/book">Get a quote</Link>
        </div>
      </section>
    </>
  );
}
