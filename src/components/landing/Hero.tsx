import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import heroBg from "@/assets/hero-bg.jpg";

const Hero = () => {
  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative min-h-[90vh] flex items-center overflow-hidden">
      <div className="absolute inset-0">
        <img src={heroBg} alt="" className="w-full h-full object-cover opacity-20" />
        <div className="absolute inset-0 bg-gradient-to-b from-primary/95 via-primary/90 to-primary/80" />
      </div>

      <div className="relative z-10 w-full px-5 py-20 md:py-32 max-w-3xl mx-auto text-center">
        <motion.h1
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-3xl md:text-5xl font-extrabold text-primary-foreground leading-tight text-balance"
        >
          Descubra quanto sua empresa pode recuperar em impostos pagos indevidamente
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15 }}
          className="mt-6 text-base md:text-lg text-primary-foreground/80 max-w-xl mx-auto text-balance"
        >
          Fazemos uma análise tributária completa e mostramos, com números, onde sua empresa pode economizar ou recuperar valores dos últimos 5 anos.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-10 flex flex-col sm:flex-row gap-4 justify-center"
        >
          <Button variant="hero" size="xl" onClick={scrollToForm}>
            Agendar diagnóstico gratuito
          </Button>
          <Button
            variant="heroOutline"
            size="xl"
            className="border-primary-foreground/30 text-primary-foreground hover:bg-primary-foreground hover:text-primary"
            onClick={() => window.open("https://wa.me/5500000000000", "_blank")}
          >
            Falar com especialista
          </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;
