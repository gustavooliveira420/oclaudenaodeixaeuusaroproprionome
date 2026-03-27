import { motion } from "framer-motion";
import { RotateCcw, BarChart3, Building2, Shield, ArrowUpRight } from "lucide-react";

const solutions = [
  {
    icon: RotateCcw,
    title: "Recuperação de créditos",
    desc: "Identificamos valores pagos indevidamente nos últimos 5 anos e recuperamos para sua empresa.",
  },
  {
    icon: BarChart3,
    title: "Planejamento tributário",
    desc: "Revisamos seu regime e encontramos formas legais de reduzir a carga fiscal.",
  },
  {
    icon: Building2,
    title: "Estruturação de holdings",
    desc: "Proteja seu patrimônio com estruturas societárias inteligentes.",
  },
  {
    icon: Shield,
    title: "Defesa fiscal",
    desc: "Suporte contínuo para garantir segurança jurídica nas suas decisões fiscais.",
  },
];

const SolutionSection = () => (
  <section className="py-24 px-6 bg-primary text-primary-foreground overflow-hidden">
    <div className="max-w-5xl mx-auto">
      <motion.span
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-accent text-sm font-semibold tracking-widest uppercase"
      >
        Nossos serviços
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.1 }}
        className="mt-4 text-2xl md:text-4xl font-bold leading-tight max-w-lg"
      >
        Inteligência tributária aplicada ao seu{" "}
        <span className="text-accent">lucro</span>
      </motion.h2>

      <div className="mt-14 grid grid-cols-1 sm:grid-cols-2 gap-6">
        {solutions.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1, duration: 0.5 }}
            className="group relative bg-primary-foreground/5 hover:bg-primary-foreground/10 border border-primary-foreground/10 hover:border-accent/30 rounded-2xl p-7 transition-all duration-300 cursor-default"
          >
            <div className="flex items-start justify-between mb-5">
              <div className="w-12 h-12 rounded-xl bg-accent/15 flex items-center justify-center">
                <s.icon className="w-6 h-6 text-accent" />
              </div>
              <ArrowUpRight className="w-5 h-5 text-primary-foreground/20 group-hover:text-accent transition-colors" />
            </div>
            <h3 className="font-bold text-primary-foreground text-lg">{s.title}</h3>
            <p className="mt-2 text-primary-foreground/60 text-sm leading-relaxed">{s.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default SolutionSection;
