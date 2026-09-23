import { Link } from "react-router-dom";
import { useSite } from "../SiteContext.jsx";
import PageHeader from "../components/PageHeader.jsx";

export default function Blog() {
  const { blogs } = useSite();
  return (
    <>
      <PageHeader title="Blog" intro="News, travel tips and updates." />
      <section className="section">
        <div className="container three-col">
          {blogs.map((b) => (
            <Link key={b.slug} to={`/blog/${b.slug}`} className="post-card">
              <time dateTime={b.date}>{new Date(b.date).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}</time>
              <h3>{b.title}</h3>
              <p>{b.excerpt}</p>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
