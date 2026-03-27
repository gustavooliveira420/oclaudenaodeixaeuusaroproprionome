import { motion } from "framer-motion";
import { RotateCcw, BarChart3, Building2, Shield } from "lucide-react";

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
    title: "Defesa e acompanhamento",
    desc: "Suporte contínuo para garantir segurança jurídica nas suas decisões fiscais.",
  },
];

const SolutionSection = () => (
  <section className="py-20 px-5">
    <div className="max-w-4xl mx-auto text-center">
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-2xl md:text-3xl font-bold text-foreground"
      >
        Inteligência tributária aplicada ao seu lucro
      </motion.h2>

      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-6">
        {solutions.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="bg-card rounded-2xl p-6 text-left shadow-sm border border-border hover:shadow-md transition-shadow"
          >
            <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mb-4">
              <s.icon className="w-6 h-6 text-accent" />
            </div>
            <h3 className="font-semibold text-foreground text-lg">{s.title}</h3>
            <p className="mt-2 text-muted-foreground text-sm">{s.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default SolutionSection;
