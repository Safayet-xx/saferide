import { Link, useParams } from "react-router-dom";
import { useSite } from "../SiteContext.jsx";
import PageHeader from "../components/PageHeader.jsx";
import NotFound from "./NotFound.jsx";

export default function BlogPost() {
  const { slug } = useParams();
  const { blogs } = useSite();
  const post = blogs.find((b) => b.slug === slug);

  if (!post) return <NotFound />;

  return (
    <>
      <PageHeader title={post.title} intro={new Date(post.date).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })} />
      <article className="section">
        <div className="container narrow prose">
          {post.body.split("\n\n").map((para, i) => <p key={i}>{para}</p>)}
          <Link to="/blog">Back to all posts</Link>
        </div>
      </article>
    </>
  );
}
