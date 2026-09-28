import { Link } from "react-router-dom";
import { useSite, telLink, mailLink } from "../SiteContext.jsx";

export default function Footer() {
  const { brand, locations } = useSite();

  return (
    <footer className="footer">
      <div className="road-line" aria-hidden="true" />
      <div className="container footer-grid">
        <div>
          <p className="logo">
            <img className="logo-mark" src="/logo.webp" alt="" />
            {brand.name}
          </p>
          <p><a href={mailLink(brand.email)}>{brand.email}</a></p>
          {brand.phone && <p><a href={telLink(brand.phone)}>Call {brand.phone}</a></p>}
          {brand.whatsapp && <p>WhatsApp {brand.whatsapp}</p>}
          {brand.address && <p>{brand.address}</p>}
        </div>

        <div>
          <h3>Information</h3>
          <Link to="/contact">Contact us</Link>
          <Link to="/terms">Terms and conditions</Link>
          <Link to="/privacy">Privacy policy</Link>
        </div>

        <div>
          <h3>Locations</h3>
          {locations.map((l) => (
            <Link key={l.slug} to={`/locations/${l.slug}`}>{l.name}</Link>
          ))}
        </div>

        {Object.keys(brand.socials).length > 0 && (
          <div>
            <h3>Follow us</h3>
            {Object.entries(brand.socials).map(([name, url]) => (
              <a key={name} href={url} target="_blank" rel="noreferrer">{name}</a>
            ))}
          </div>
        )}
      </div>
      <p className="container copyright">
        © {new Date().getFullYear()} {brand.legal_name}. All rights reserved.
      </p>
    </footer>
  );
}
