import { useSite } from "../SiteContext.jsx";
import PageHeader from "../components/PageHeader.jsx";
import QuoteForm from "../components/QuoteForm.jsx";

export default function Airport() {
  const { airports } = useSite();
  return (
    <>
      <PageHeader
        title="Airport transfers"
        intro="Fixed prices to and from the airport, with flight tracking and meet and greet."
      />
      <section className="section">
        <div className="container two-col align-start">
          <div>
            <h2>Airports we cover</h2>
            <ul className="airport-list">
              {airports.map((a) => (
                <li key={a.code}><span className="code">{a.code}</span>{a.name}</li>
              ))}
            </ul>
          </div>
          <QuoteForm />
        </div>
      </section>
    </>
  );
}
