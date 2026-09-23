import { useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import { SiteProvider } from "./SiteContext.jsx";
import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import Home from "./pages/Home.jsx";
import Book from "./pages/Book.jsx";
import Business from "./pages/Business.jsx";
import Vehicles from "./pages/Vehicles.jsx";
import Airport from "./pages/Airport.jsx";
import Location from "./pages/Location.jsx";
import WorkWithUs from "./pages/WorkWithUs.jsx";
import Blog from "./pages/Blog.jsx";
import BlogPost from "./pages/BlogPost.jsx";
import Contact from "./pages/Contact.jsx";
import Legal from "./pages/Legal.jsx";
import NotFound from "./pages/NotFound.jsx";

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}

export default function App() {
  return (
    <SiteProvider>
      <ScrollToTop />
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/book" element={<Book />} />
          <Route path="/business" element={<Business />} />
          <Route path="/vehicles" element={<Vehicles />} />
          <Route path="/airport-transfer" element={<Airport />} />
          <Route path="/locations/:slug" element={<Location />} />
          <Route path="/work-with-us" element={<WorkWithUs />} />
          <Route path="/blog" element={<Blog />} />
          <Route path="/blog/:slug" element={<BlogPost />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/terms" element={<Legal type="terms" />} />
          <Route path="/privacy" element={<Legal type="privacy" />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <Footer />
    </SiteProvider>
  );
}
