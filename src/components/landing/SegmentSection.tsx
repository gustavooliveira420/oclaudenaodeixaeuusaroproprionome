import { motion } from "framer-motion";
import { ShoppingCart, Factory, Briefcase, HeartPulse } from "lucide-react";

const segments = [
  {
    icon: ShoppingCart,
    title: "Varejo",
    subtitle: "Se você é do Varejo...",
    pains: [
      "Paga ICMS-ST sem acompanhamento de restituição",
      "PIS/COFINS não está sendo apurado corretamente",
    ],
    benefit: "Identificamos créditos não aproveitados e reduzimos sua carga tributária.",
    color: "from-accent/20 to-accent/5",
  },
  {
    icon: Factory,
    title: "Indústria",
    subtitle: "Se você tem uma Indústria...",
    pains: [
      "IPI e ICMS geram complexidade que consome margem",
      "Incentivos fiscais não estão sendo utilizados",
    ],
    benefit: "Revisamos toda a cadeia para encontrar oportunidades reais de economia.",
    color: "from-primary/10 to-primary/5",
  },
  {
    icon: Briefcase,
    title: "Serviços",
    subtitle: "Se você presta serviços...",
    pains: [
      "ISS e regime de tributação podem estar inadequados",
      "Crescimento sem planejamento aumenta a carga fiscal",
    ],
    benefit: "Enquadramos sua operação no regime mais vantajoso e seguro.",
    color: "from-accent/15 to-accent/5",
  },
  {
    icon: HeartPulse,
    title: "Saúde",
    subtitle: "Se você atua na Área de Saúde...",
    pains: [
      "Clínicas, hospitais ou laboratórios com tributação inadequada",
      "Insumos e medicamentos com créditos não aproveitados",
    ],
    benefit: "Revisamos o enquadramento e identificamos créditos específicos do setor.",
    color: "from-accent/20 to-accent/5",
  },
];

const SegmentSection = () => (
  <section className="py-24 px-4 md:px-6 bg-white">
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
            Segmentos
          </span>
          <span className="h-px w-10 bg-prime-green" />
        </motion.div>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-2xl md:text-4xl font-black uppercase tracking-tight text-prime-dark"
        >
          Para quem é{" "}
          <span className="text-prime-green">esse serviço?</span>
        </motion.h2>
      </div>

      <div className="mt-14 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {segments.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.12, duration: 0.5 }}
            className="group relative bg-prime-light rounded-2xl border border-prime-dark/10 overflow-hidden hover:shadow-xl hover:border-prime-gold/40 transition-all duration-300"
          >
            <div className="p-7">
              <div className="flex items-center gap-3 mb-5">
                <div className="w-11 h-11 rounded-xl bg-prime-dark flex items-center justify-center group-hover:bg-prime-green transition-colors">
                  <s.icon className="w-5 h-5 text-prime-gold group-hover:text-white transition-colors" />
                </div>
                <span className="text-xs font-bold tracking-[0.18em] uppercase text-prime-green">
                  {s.title}
                </span>
              </div>
              <h3 className="font-bold text-prime-dark text-lg uppercase tracking-tight">
                {s.subtitle}
              </h3>
              <ul className="mt-4 space-y-2.5">
                {s.pains.map((p, j) => (
                  <li
                    key={j}
                    className="text-sm text-prime-black/70 flex items-start gap-2.5"
                  >
                    <span className="w-1.5 h-1.5 bg-prime-gold rounded-full mt-2 shrink-0" />
                    {p}
                  </li>
                ))}
              </ul>
              <div className="mt-5 pt-5 border-t border-prime-dark/10">
                <p className="text-sm text-prime-green font-semibold">{s.benefit}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default SegmentSection;
