import { motion } from "framer-motion";
import { AlertTriangle, TrendingDown, Eye, ShieldAlert } from "lucide-react";

const pains = [
  { icon: AlertTriangle, text: "Tributos pagos a maior sem revisão nos últimos anos" },
  { icon: Eye, text: "Falta de clareza sobre o regime tributário ideal" },
  { icon: TrendingDown, text: "Margem de lucro sendo reduzida silenciosamente" },
  { icon: ShieldAlert, text: "Risco de autuações por decisões fiscais incorretas" },
];

const PainSection = () => (
  <section className="py-20 px-5 bg-secondary">
    <div className="max-w-3xl mx-auto text-center">
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-2xl md:text-3xl font-bold text-foreground"
      >
        Você pode estar pagando mais impostos do que deveria
      </motion.h2>

      <div className="mt-10 space-y-5">
        {pains.map((pain, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="flex items-start gap-4 text-left bg-background rounded-xl p-5 shadow-sm"
          >
            <pain.icon className="w-6 h-6 text-accent shrink-0 mt-0.5" />
            <p className="text-foreground/80 text-sm md:text-base">{pain.text}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default PainSection;
