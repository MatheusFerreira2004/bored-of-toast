import Header from "@/components/Header";
import Hero from "@/components/Hero";
import ValueProps from "@/components/ValueProps";
import FeatureShowcase from "@/components/FeatureShowcase";
import CTASection from "@/components/CTASection";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main>
      <Header />
      <Hero />
      <ValueProps />
      <FeatureShowcase />
      <CTASection />
      <Footer />
    </main>
  );
}
