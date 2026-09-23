import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { useSite, telLink } from "../SiteContext.jsx";

export default function Header() {
  const { brand, locations } = useSite();
  const [open, setOpen] = useState(false);
  const close = () => setOpen(false);

  return (
    <header className="header">
      <div className="container header-inner">
        <Link to="/" className="logo" onClick={close}>
          <img className="logo-mark" src="/logo.webp" alt="" />
          {brand.name}
        </Link>

        <button
          className="menu-toggle"
          aria-expanded={open}
          aria-controls="main-nav"
          onClick={() => setOpen(!open)}
        >
          {open ? "Close" : "Menu"}
        </button>

        <nav id="main-nav" className={`nav ${open ? "is-open" : ""}`}>
          <NavLink to="/book" onClick={close}>Book a ride</NavLink>
          <NavLink to="/business" onClick={close}>Business</NavLink>
          <details className="dropdown">
            <summary>Locations</summary>
            <div className="dropdown-menu">
              {locations.map((l) => (
                <NavLink key={l.slug} to={`/locations/${l.slug}`} onClick={close}>{l.name}</NavLink>
              ))}
            </div>
          </details>
          <NavLink to="/vehicles" onClick={close}>Vehicles</NavLink>
          <NavLink to="/airport-transfer" onClick={close}>Airport</NavLink>
          <NavLink to="/work-with-us" onClick={close}>Work with us</NavLink>
          <NavLink to="/blog" onClick={close}>Blog</NavLink>
          <a className="btn btn-amber nav-phone" href={telLink(brand.phone)}>{brand.phone}</a>
        </nav>
      </div>
    </header>
  );
}
