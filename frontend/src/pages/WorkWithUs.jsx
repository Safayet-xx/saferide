import PageHeader from "../components/PageHeader.jsx";
import ContactForm from "../components/ContactForm.jsx";

export default function WorkWithUs() {
  return (
    <>
      <PageHeader
        title="Drive with us"
        intro="Licensed private hire driver? Send us your details and we'll be in touch about current openings."
      />
      <section className="section">
        <div className="container narrow">
          <ContactForm defaultTopic="Driving for us" buttonText="Apply" />
        </div>
      </section>
    </>
  );
}
