export default function PageHeader({ title, intro }) {
  return (
    <section className="page-header">
      <div className="container">
        <h1>{title}</h1>
        {intro && <p>{intro}</p>}
      </div>
      <div className="road-line" aria-hidden="true" />
    </section>
  );
}
