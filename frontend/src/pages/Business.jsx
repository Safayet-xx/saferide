import PageHeader from "../components/PageHeader.jsx";
import ContactForm from "../components/ContactForm.jsx";

export default function Business() {
  return (
    <>
      <PageHeader
        title="Business accounts"
        intro="Priority bookings, monthly invoices and team discounts. Tell us about your company and we'll set you up."
      />
      <section className="section">
        <div className="container narrow">
          <ContactForm defaultTopic="Business account" buttonText="Request an account" />
        </div>
      </section>
    </>
  );
}
