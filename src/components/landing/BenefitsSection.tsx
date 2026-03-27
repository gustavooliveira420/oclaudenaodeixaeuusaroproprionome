import { motion } from "framer-motion";
import { DollarSign, Percent, Landmark, CheckCircle2 } from "lucide-react";

const benefits = [
  { icon: DollarSign, text: "Recuperação de valores dos últimos 5 anos", highlight: "5 anos" },
  { icon: Percent, text: "Redução de 5% a 30% na carga tributária", highlight: "5% a 30%" },
  { icon: Landmark, text: "Economia sem novos empréstimos", highlight: "sem empréstimos" },
  { icon: CheckCircle2, text: "Segurança jurídica e previsibilidade", highlight: "previsibilidade" },
];

const BenefitsSection = () => (
  <section className="py-24 px-6 bg-card">
    <div className="max-w-5xl mx-auto">
      <div className="text-center max-w-2xl mx-auto">
        <motion.span
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-accent text-sm font-semibold tracking-widest uppercase"
        >
          Resultados
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="mt-4 text-2xl md:text-4xl font-bold text-foreground leading-tight"
        >
          Resultados que impactam diretamente o{" "}
          <span className="text-accent">caixa</span>
        </motion.h2>
      </div>

      <div className="mt-14 grid grid-cols-1 sm:grid-cols-2 gap-5">
        {benefits.map((b, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1, duration: 0.4 }}
            className="flex items-center gap-5 bg-background rounded-2xl p-6 border border-border hover:shadow-lg transition-shadow"
          >
            <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center shrink-0">
              <b.icon className="w-6 h-6 text-accent" />
            </div>
            <p className="text-foreground text-sm md:text-base font-medium">{b.text}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default BenefitsSection;
