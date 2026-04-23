import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import heroImg from "@/assets/hero-meeting.jpg";

const Hero = () => {
  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative min-h-screen flex items-end md:items-center overflow-hidden">
      {/* Background image */}
      <div className="absolute inset-0">
        <img
          src={heroImg}
          alt="Consultoria tributária estratégica"
          className="w-full h-full object-cover"
          width={1920}
          height={1080}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-primary via-primary/80 to-primary/40 md:bg-gradient-to-r md:from-primary md:via-primary/85 md:to-transparent" />
      </div>

      {/* Content */}
      <div className="relative z-10 w-full px-4 pb-16 pt-32 md:py-32 max-w-5xl mx-auto">
        <div className="max-w-xl">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
          >
            <span className="inline-block text-accent text-sm font-semibold tracking-widest uppercase mb-6">
              Consultoria Tributária Estratégica
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="text-3xl md:text-5xl lg:text-6xl font-black text-primary-foreground leading-[1.1] tracking-tight"
          >
            Descubra quanto sua empresa pode{" "}
            <span className="text-accent">recuperar</span> em impostos
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="mt-6 text-base md:text-lg text-primary-foreground/70 leading-relaxed max-w-md"
          >
            Análise tributária completa. Mostramos, com números, onde sua empresa pode economizar ou recuperar valores dos últimos 5 anos.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.35 }}
            className="mt-10 flex flex-col sm:flex-row gap-4"
          >
            <Button variant="hero" size="xl" onClick={scrollToForm} className="group">
              Agendar diagnóstico gratuito
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button
              variant="hero"
              size="xl"
              className="bg-primary-foreground text-primary hover:bg-primary-foreground/90 group"
              onClick={() => window.open("https://wa.me/5500000000000", "_blank")}
            >
              Falar com especialista
            </Button>
          </motion.div>
        </div>
      </div>

      {/* Accent line decoration */}
      <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-accent via-accent/50 to-transparent" />
    </section>
  );
};

export default Hero;
