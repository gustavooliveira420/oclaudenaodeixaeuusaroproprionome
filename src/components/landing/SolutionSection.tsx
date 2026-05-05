import { motion } from "framer-motion";
import { ClipboardList, RefreshCcw, Scale } from "lucide-react";

const solutions = [
  {
    icon: ClipboardList,
    title: "Revisão Tributária",
    desc: "Análise detalhada de tributos federais, estaduais e municipais para identificar pagamentos indevidos ou a maior.",
  },
  {
    icon: RefreshCcw,
    title: "Recuperação de Créditos",
    desc: "Levantamento e restituição de valores pagos indevidamente nos últimos 5 anos com segurança e agilidade.",
  },
  {
    icon: Scale,
    title: "Renegociação Estratégica",
    desc: "Negociação de dívidas tributárias e bancárias com foco em redução de passivos e melhores condições de pagamento.",
  },
];

const SolutionSection = () => (
  <section id="servicos" className="py-24 px-4 md:px-6 bg-prime-light">
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
            Nossas soluções
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
          Estratégia tributária completa
          <br />
          para gerar{" "}
          <span className="text-prime-green">resultados reais</span>
        </motion.h2>
      </div>

      <div className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-6">
        {solutions.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.12, duration: 0.5 }}
            className="group relative bg-prime-dark rounded-2xl p-8 border border-prime-gold/20 hover:border-prime-gold/60 transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl"
          >
            <div className="w-14 h-14 rounded-full bg-prime-light/10 border border-prime-gold/40 flex items-center justify-center mb-6 group-hover:bg-prime-gold/15 group-hover:border-prime-gold transition-colors">
              <s.icon className="w-7 h-7 text-prime-gold" />
            </div>
            <h3 className="font-bold text-white text-xl uppercase tracking-tight">
              {s.title}
            </h3>
            <p className="mt-3 text-white/70 text-sm leading-relaxed">
              {s.desc}
            </p>
            <div className="mt-6 h-px w-12 bg-prime-green group-hover:w-full transition-all duration-500" />
          </motion.div>
        ))}
      </div>

      {/* Sub-CTA bar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2 }}
        className="mt-12 bg-prime-dark text-white rounded-2xl p-6 md:p-8 flex flex-col md:flex-row items-start md:items-center gap-4 md:gap-6"
      >
        <div className="w-12 h-12 rounded-xl bg-prime-gold/15 border border-prime-gold/40 flex items-center justify-center shrink-0">
          <svg viewBox="0 0 24 24" className="w-6 h-6 text-prime-gold" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="9" />
            <circle cx="12" cy="12" r="4" />
            <circle cx="12" cy="12" r="1" fill="currentColor" />
          </svg>
        </div>
        <div className="flex-1">
          <p className="text-white font-bold uppercase tracking-tight">
            Consultoria tributária especializada. Resultados comprovados.
          </p>
          <p className="text-white/70 text-sm mt-1">
            Menos carga, mais caixa, mais crescimento.
          </p>
        </div>
      </motion.div>
    </div>
  </section>
);

export default SolutionSection;
