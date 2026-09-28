import { useSite, telLink, mailLink } from "../SiteContext.jsx";
import PageHeader from "../components/PageHeader.jsx";
import ContactForm from "../components/ContactForm.jsx";

export default function Contact() {
  const { brand } = useSite();
  return (
    <>
      <PageHeader title="Contact us" intro="Questions, lost property or account sign-ups. Email us or use the form and we'll reply by email." />
      <section className="section">
        <div className="container two-col align-start">
          <div className="contact-details">
            <h2>Reach us directly</h2>
            <p><strong>Email</strong><br /><a href={mailLink(brand.email)}>{brand.email}</a></p>
            {brand.phone && <p><strong>Phone</strong><br /><a href={telLink(brand.phone)}>{brand.phone}</a></p>}
            {brand.whatsapp && <p><strong>WhatsApp</strong><br />{brand.whatsapp}</p>}
            {brand.address && <p><strong>Office</strong><br />{brand.address}</p>}
          </div>
          <ContactForm />
        </div>
      </section>
    </>
  );
}
