import { useSite } from "../SiteContext.jsx";
import PageHeader from "../components/PageHeader.jsx";

export default function Legal({ type }) {
  const { legal } = useSite();
  const title = type === "terms" ? "Terms and conditions" : "Privacy policy";
  return (
    <>
      <PageHeader title={title} />
      <section className="section">
        <div className="container narrow prose">
          {legal[type].split("\n\n").map((para, i) => <p key={i}>{para}</p>)}
        </div>
      </section>
    </>
  );
}
