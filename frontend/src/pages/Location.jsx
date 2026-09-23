import { Link, useParams } from "react-router-dom";
import { useSite } from "../SiteContext.jsx";
import PageHeader from "../components/PageHeader.jsx";
import NotFound from "./NotFound.jsx";

export default function Location() {
  const { slug } = useParams();
  const { locations, brand } = useSite();
  const place = locations.find((l) => l.slug === slug);

  if (!place) return <NotFound />;

  return (
    <>
      <PageHeader title={`Taxis in ${place.name}`} intro={place.text} />
      <section className="section">
        <div className="container narrow">
          <p>{brand.name} covers {place.name} and the surrounding area, day and night.</p>
          <Link className="btn btn-amber" to="/book">Book a ride in {place.name}</Link>
        </div>
      </section>
    </>
  );
}
