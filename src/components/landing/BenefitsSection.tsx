import { motion } from "framer-motion";
import { DollarSign, Percent, Landmark, CheckCircle2 } from "lucide-react";

const benefits = [
  { icon: DollarSign, text: "Recuperação de valores dos últimos 5 anos" },
  { icon: Percent, text: "Redução de 5% a 30% na carga tributária" },
  { icon: Landmark, text: "Economia sem novos empréstimos" },
  { icon: CheckCircle2, text: "Segurança jurídica e previsibilidade" },
];

const BenefitsSection = () => (
  <section className="py-20 px-5 bg-primary text-primary-foreground">
    <div className="max-w-3xl mx-auto text-center">
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-2xl md:text-3xl font-bold"
      >
        Resultados que impactam diretamente o caixa
      </motion.h2>

      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-6">
        {benefits.map((b, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="flex items-center gap-4 bg-primary-foreground/10 rounded-xl p-5"
          >
            <b.icon className="w-6 h-6 text-accent shrink-0" />
            <p className="text-sm md:text-base text-primary-foreground/90 text-left">{b.text}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default BenefitsSection;
