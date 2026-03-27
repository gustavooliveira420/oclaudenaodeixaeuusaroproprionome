import Header from "@/components/landing/Header";
import Hero from "@/components/landing/Hero";
import StatsSection from "@/components/landing/StatsSection";
import PainSection from "@/components/landing/PainSection";
import SolutionSection from "@/components/landing/SolutionSection";
import BenefitsSection from "@/components/landing/BenefitsSection";
import SegmentSection from "@/components/landing/SegmentSection";
import ProcessSection from "@/components/landing/ProcessSection";
import PricingSection from "@/components/landing/PricingSection";
import AuthoritySection from "@/components/landing/AuthoritySection";
import FaqSection from "@/components/landing/FaqSection";
import ContactSection from "@/components/landing/ContactSection";
import WhatsAppButton from "@/components/landing/WhatsAppButton";
import Footer from "@/components/landing/Footer";

const Index = () => (
  <>
    <Header />
    <main>
      <Hero />
      <StatsSection />
      <PainSection />
      <SolutionSection />
      <BenefitsSection />
      <SegmentSection />
      <ProcessSection />
      <PricingSection />
      <AuthoritySection />
      <FaqSection />
      <ContactSection />
    </main>
    <Footer />
    <WhatsAppButton />
  </>
);

export default Index;
