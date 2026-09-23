import PageHeader from "../components/PageHeader.jsx";
import QuoteForm from "../components/QuoteForm.jsx";

export default function Book() {
  return (
    <>
      <PageHeader title="Book a ride" intro="Send us your journey details and we'll reply with a fixed price." />
      <section className="section">
        <div className="container narrow">
          <QuoteForm />
        </div>
      </section>
    </>
  );
}
