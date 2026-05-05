import { motion } from "framer-motion";
import { DollarSign, Percent, Landmark, CheckCircle2 } from "lucide-react";

const benefits = [
  { icon: DollarSign, text: "Recuperação de valores dos últimos 5 anos" },
  { icon: Percent, text: "Redução de 5% a 30% na carga tributária" },
  { icon: Landmark, text: "Economia sem novos empréstimos" },
  { icon: CheckCircle2, text: "Segurança jurídica e previsibilidade" },
];

const BenefitsSection = () => (
  <section className="py-24 px-4 md:px-6 bg-prime-light">
    <div className="max-w-7xl mx-auto">
      <div className="text-center max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="flex items-center justify-center gap-3 mb-4"
        >
          <span className="h-px w-10 bg-prime-green" />
          <span className="text-prime-green text-xs font-semibold tracking-[0.2em] uppercase">
            Resultados
          </span>
          <span className="h-px w-10 bg-prime-green" />
        </motion.div>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-2xl md:text-4xl font-black uppercase tracking-tight text-prime-dark leading-tight"
        >
          Resultados que impactam diretamente o{" "}
          <span className="text-prime-green">caixa</span>
        </motion.h2>
      </div>

      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-5">
        {benefits.map((b, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1, duration: 0.4 }}
            className="flex items-center gap-5 bg-white rounded-2xl p-6 border border-prime-dark/10 hover:border-prime-gold/40 hover:shadow-md transition-all"
          >
            <div className="w-12 h-12 rounded-xl bg-prime-dark flex items-center justify-center shrink-0">
              <b.icon className="w-6 h-6 text-prime-gold" />
            </div>
            <p className="text-prime-dark text-sm md:text-base font-semibold">
              {b.text}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default BenefitsSection;
