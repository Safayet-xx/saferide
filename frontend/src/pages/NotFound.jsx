import { Link } from "react-router-dom";
import PageHeader from "../components/PageHeader.jsx";

export default function NotFound() {
  return (
    <>
      <PageHeader title="Page not found" intro="This page doesn't exist or has moved." />
      <section className="section">
        <div className="container narrow">
          <Link className="btn btn-amber" to="/">Go to the home page</Link>
        </div>
      </section>
    </>
  );
}
