import { motion } from "framer-motion";
import { BadgeCheck, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const PricingSection = () => {
  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="py-24 px-6 bg-card">
      <div className="max-w-3xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="relative bg-background rounded-3xl p-8 md:p-14 border border-border overflow-hidden"
        >
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-accent via-accent/50 to-transparent" />
          
          <div className="text-center">
            <BadgeCheck className="w-14 h-14 text-accent mx-auto mb-6" />
            <h2 className="text-2xl md:text-4xl font-bold text-foreground">
              Você só paga se houver{" "}
              <span className="text-accent">resultado</span>
            </h2>
            <p className="mt-5 text-muted-foreground max-w-lg mx-auto leading-relaxed">
              Na maioria dos casos, trabalhamos com modelo de êxito — você só paga um percentual sobre o valor efetivamente recuperado. Sem custo inicial, sem risco.
            </p>
            <Button variant="hero" size="lg" className="mt-8 group" onClick={scrollToForm}>
              Quero saber mais
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default PricingSection;
