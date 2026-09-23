export default function Stars({ rating }) {
  return (
    <span className="stars" aria-label={`${rating} out of 5 stars`}>
      {"★".repeat(Math.round(rating))}
      <span className="stars-empty">{"★".repeat(5 - Math.round(rating))}</span>
    </span>
  );
}
