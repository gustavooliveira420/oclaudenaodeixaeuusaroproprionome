import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const ClosingCtaSection = () => {
  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative py-20 px-4 md:px-6 bg-prime-light overflow-hidden">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="relative bg-gradient-to-br from-prime-dark via-[hsl(170_45%_10%)] to-prime-dark rounded-3xl p-10 md:p-16 overflow-hidden border border-prime-gold/20"
        >
          {/* Decoração: linhas douradas + R translúcido */}
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-prime-gold to-transparent" />
          <div className="absolute -right-12 top-1/2 -translate-y-1/2 pointer-events-none opacity-[0.06]">
            <svg viewBox="0 0 200 200" className="w-80 h-80">
              <path d="M 36 52 L 64 52 L 76 156 L 36 156 Z" fill="#D4AF37" />
              <path
                d="M 64 32 L 128 32 Q 164 32 164 72 Q 164 104 132 112 L 168 168 L 140 168 L 108 116 L 92 116 L 92 168 L 64 168 Z M 92 56 L 92 92 L 124 92 Q 140 92 140 74 Q 140 56 124 56 Z"
                fill="#FFFFFF"
              />
            </svg>
          </div>

          <div className="relative z-10 max-w-3xl">
            <div className="flex items-center gap-3 mb-4">
              <span className="h-px w-10 bg-prime-gold" />
              <span className="text-prime-gold text-xs font-semibold tracking-[0.2em] uppercase">
                Próximo passo
              </span>
            </div>
            <h2 className="text-2xl md:text-4xl font-black text-white uppercase tracking-tight leading-tight">
              Descubra quanto sua empresa pode{" "}
              <span className="text-prime-green">economizar</span> ou{" "}
              <span className="text-prime-gold">recuperar</span>
            </h2>
            <p className="mt-5 text-white/75 max-w-xl leading-relaxed">
              Solicite um diagnóstico gratuito e sem compromisso. Em 30 a 45 minutos
              mostramos com números as oportunidades concretas para o seu CNPJ.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row gap-4">
              <Button variant="prime" size="xl" onClick={scrollToForm} className="group">
                Falar com especialista
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button variant="primeOutline" size="xl" onClick={scrollToForm}>
                Diagnóstico gratuito
              </Button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default ClosingCtaSection;
