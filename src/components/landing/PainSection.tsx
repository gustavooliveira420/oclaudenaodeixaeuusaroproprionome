import { motion } from "framer-motion";
import { AlertTriangle, TrendingDown, Eye, ShieldAlert } from "lucide-react";

const pains = [
  { icon: AlertTriangle, text: "Tributos pagos a maior sem revisão nos últimos anos" },
  { icon: Eye, text: "Falta de clareza sobre o regime tributário ideal" },
  { icon: TrendingDown, text: "Margem de lucro sendo reduzida silenciosamente" },
  { icon: ShieldAlert, text: "Risco de autuações por decisões fiscais incorretas" },
];

const PainSection = () => (
  <section className="py-24 px-6">
    <div className="max-w-5xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
        <div className="md:sticky md:top-32">
          <motion.span
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-accent text-sm font-semibold tracking-widest uppercase"
          >
            O problema
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="mt-4 text-2xl md:text-4xl font-bold text-foreground leading-tight"
          >
            Você pode estar pagando{" "}
            <span className="text-accent">mais impostos</span> do que deveria
          </motion.h2>
        </div>

        <div className="space-y-4">
          {pains.map((pain, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="flex items-start gap-4 bg-card rounded-2xl p-6 border border-border hover:border-accent/30 transition-colors group"
            >
              <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center shrink-0 group-hover:bg-accent/20 transition-colors">
                <pain.icon className="w-5 h-5 text-accent" />
              </div>
              <p className="text-foreground/80 text-sm md:text-base leading-relaxed">{pain.text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  </section>
);

export default PainSection;
