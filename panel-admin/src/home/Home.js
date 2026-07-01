import Header from "./components/Header";
import Hero from "./components/Hero";
import Features from "./components/Features";
import ShiftCards from "./components/ShiftCards";
import CTA from "./components/CTA";
import Footer from "./components/Footer";

function Home() {
  return (
    <div className="bg-[#DCCFC0] min-h-screen">
      <Header />
      <Hero />
      <Features />
      <ShiftCards />
      <CTA />
      <Footer />
    </div>
  );
}

export default Home;