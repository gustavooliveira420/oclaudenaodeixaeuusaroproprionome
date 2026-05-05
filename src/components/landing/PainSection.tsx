import { motion } from "framer-motion";
import { Calculator, FileX, ShieldOff, AlertTriangle } from "lucide-react";

const pains = [
  { icon: Calculator, text: "Erros de cálculo nas apurações" },
  { icon: FileX, text: "Tributação indevida sobre operações específicas" },
  { icon: ShieldOff, text: "Benefícios fiscais não aplicados" },
  { icon: AlertTriangle, text: "Pagamentos a maior pulverizados em cinco anos" },
];

const PainSection = () => (
  <section id="sobre" className="py-24 px-4 md:px-6 bg-prime-light">
    <div className="max-w-7xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-start">
        <div className="lg:sticky lg:top-32">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="flex items-center gap-3 mb-4"
          >
            <span className="h-px w-10 bg-prime-green" />
            <span className="text-prime-green text-xs font-semibold tracking-[0.2em] uppercase">
              O problema
            </span>
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-2xl md:text-4xl font-black uppercase tracking-tight text-prime-dark leading-tight"
          >
            Você pode estar pagando{" "}
            <span className="text-prime-green">impostos indevidos</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="mt-5 text-prime-black/70 leading-relaxed"
          >
            A maioria das empresas paga mais do que deveria — sem perceber. Erros de
            apuração, ausência de revisão técnica e benefícios fiscais não aplicados
            geram passivos silenciosos.{" "}
            <span className="text-prime-gold font-semibold">
              Dinheiro que sai do caixa e poderia estar no seu negócio.
            </span>
          </motion.p>
        </div>

        <div className="space-y-3">
          {pains.map((pain, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="flex items-center gap-4 bg-white rounded-xl p-5 border border-prime-dark/10 hover:border-prime-gold/40 hover:shadow-md transition-all"
            >
              <div className="w-11 h-11 rounded-lg bg-prime-dark flex items-center justify-center shrink-0">
                <pain.icon className="w-5 h-5 text-prime-gold" />
              </div>
              <p className="text-prime-dark text-base font-medium">{pain.text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  </section>
);

export default PainSection;
