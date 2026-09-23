import { useSite, telLink } from "../SiteContext.jsx";
import PageHeader from "../components/PageHeader.jsx";
import ContactForm from "../components/ContactForm.jsx";

export default function Contact() {
  const { brand } = useSite();
  return (
    <>
      <PageHeader title="Contact us" intro="Questions, lost property or account sign-ups. We usually reply within a day." />
      <section className="section">
        <div className="container two-col align-start">
          <div className="contact-details">
            <h2>Reach us directly</h2>
            <p><strong>Phone</strong><br /><a href={telLink(brand.phone)}>{brand.phone}</a></p>
            <p><strong>WhatsApp</strong><br />{brand.whatsapp}</p>
            <p><strong>Email</strong><br /><a href={`mailto:${brand.email}`}>{brand.email}</a></p>
            <p><strong>Office</strong><br />{brand.address}</p>
          </div>
          <ContactForm />
        </div>
      </section>
    </>
  );
}
