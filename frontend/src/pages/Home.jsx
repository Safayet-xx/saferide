import { Link } from "react-router-dom";
import { useSite, mailLink } from "../SiteContext.jsx";
import QuoteForm from "../components/QuoteForm.jsx";
import Stars from "../components/Stars.jsx";

export default function Home() {
  const site = useSite();
  const { brand, hero } = site;
  const hasApp = Boolean(brand.app_links.ios || brand.app_links.android);

  return (
    <>
      {/* Hero with the quote form */}
      <section className="hero">
        <div className="container hero-grid">
          <div className="hero-copy">
            <h1>{hero.title}</h1>
            <p className="lead">{hero.subtitle}</p>
            <p className="hero-call">
              Prefer email? <a href={mailLink(brand.email)}>{brand.email}</a>
            </p>
          </div>
          <QuoteForm />
        </div>
        <div className="road-line" aria-hidden="true" />
      </section>

      {/* Ways to book */}
      <section className="section">
        <div className="container two-col">
          {site.booking_options.map((opt) => (
            <article key={opt.title} className="panel">
              <h2>{opt.title}</h2>
              <p>{opt.text}</p>
              {opt.link_type === "email" ? (
                <a className="btn btn-navy" href={mailLink(brand.email)}>{opt.action}</a>
              ) : (
                <Link className="btn btn-navy" to="/book">{opt.action}</Link>
              )}
            </article>
          ))}
        </div>
      </section>

      {/* Why ride with us */}
      <section className="section section-paper">
        <div className="container">
          <h2 className="section-title">Why ride with {brand.name}</h2>
          <div className="feature-list">
            {site.features.map((f) => (
              <div key={f.title} className="feature">
                <h3>{f.title}</h3>
                <p>{f.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Accounts */}
      <section className="section">
        <div className="container">
          <h2 className="section-title">Accounts</h2>
          <div className="two-col">
            {site.accounts.map((a) => (
              <article key={a.title} className="panel panel-accent">
                <h3>{a.title}</h3>
                <p>{a.text}</p>
                <Link className="btn btn-navy" to={a.title.startsWith("Business") ? "/business" : "/contact"}>
                  Sign up
                </Link>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* App: only shown once APP_LINK_IOS or APP_LINK_ANDROID is set */}
      {hasApp && (
        <section className="section section-navy">
          <div className="container app-grid">
            <div>
              <h2 className="section-title">Get the app</h2>
              {site.app_features.map((f) => (
                <div key={f.title} className="app-feature">
                  <h3>{f.title}</h3>
                  <p>{f.text}</p>
                </div>
              ))}
              <div className="store-links">
                {brand.app_links.ios && <a className="btn btn-amber" href={brand.app_links.ios}>App Store</a>}
                {brand.app_links.android && <a className="btn btn-amber" href={brand.app_links.android}>Google Play</a>}
              </div>
            </div>
            {/* Replace this block with a phone mockup image later */}
            <div className="phone-placeholder" aria-hidden="true">
              <div className="phone-screen">
                <span>{brand.name}</span>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Reviews */}
      <section className="section">
        <div className="container">
          <div className="reviews-head">
            <h2 className="section-title">What riders say</h2>
            <p>
              <Stars rating={site.review_summary.rating} /> {site.review_summary.rating} on {site.review_summary.source}
            </p>
          </div>
          <div className="three-col">
            {site.reviews.map((r, i) => (
              <blockquote key={i} className="review">
                <Stars rating={r.rating} />
                <p>{r.text}</p>
                <footer>{r.name}</footer>
              </blockquote>
            ))}
          </div>
        </div>
      </section>

      {/* Blog preview */}
      <section className="section section-paper">
        <div className="container">
          <h2 className="section-title">From the blog</h2>
          <div className="three-col">
            {site.blogs.slice(0, 3).map((b) => (
              <Link key={b.slug} to={`/blog/${b.slug}`} className="post-card">
                <time dateTime={b.date}>{new Date(b.date).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}</time>
                <h3>{b.title}</h3>
                <p>{b.excerpt}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
