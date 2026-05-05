import { motion } from "framer-motion";
import { BadgeCheck, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const PricingSection = () => {
  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="py-24 px-4 md:px-6 bg-white">
      <div className="max-w-3xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="relative bg-prime-light rounded-3xl p-10 md:p-14 border border-prime-gold/30 overflow-hidden text-center"
        >
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-prime-green via-prime-gold to-prime-green" />

          <div className="w-16 h-16 rounded-full bg-prime-dark flex items-center justify-center mx-auto mb-6">
            <BadgeCheck className="w-8 h-8 text-prime-gold" />
          </div>
          <h2 className="text-2xl md:text-4xl font-black uppercase tracking-tight text-prime-dark">
            Você só paga se houver{" "}
            <span className="text-prime-green">resultado</span>
          </h2>
          <p className="mt-5 text-prime-black/70 max-w-lg mx-auto leading-relaxed">
            Na maioria dos casos, trabalhamos com modelo de êxito — você só paga um
            percentual sobre o valor efetivamente recuperado.{" "}
            <span className="text-prime-dark font-semibold">
              Sem custo inicial, sem risco.
            </span>
          </p>
          <Button
            variant="prime"
            size="lg"
            className="mt-8 group"
            onClick={scrollToForm}
          >
            Quero saber mais
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default PricingSection;
