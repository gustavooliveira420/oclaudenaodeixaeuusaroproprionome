import { motion } from "framer-motion";
import { ShoppingCart, Factory, Briefcase } from "lucide-react";

const segments = [
  {
    icon: ShoppingCart,
    title: "Se você é do Varejo...",
    pains: [
      "Paga ICMS-ST sem acompanhamento de restituição",
      "Não sabe se PIS/COFINS está sendo apurado corretamente",
    ],
    benefit: "Podemos identificar créditos não aproveitados e reduzir sua carga tributária.",
  },
  {
    icon: Factory,
    title: "Se você tem uma Indústria...",
    pains: [
      "IPI e ICMS geram complexidade que consome margem",
      "Incentivos fiscais não estão sendo utilizados",
    ],
    benefit: "Revisamos toda a cadeia para encontrar oportunidades reais de economia.",
  },
  {
    icon: Briefcase,
    title: "Se você presta serviços...",
    pains: [
      "ISS e regime de tributação podem estar inadequados",
      "Crescimento sem planejamento aumenta a carga fiscal",
    ],
    benefit: "Enquadramos sua operação no regime mais vantajoso e seguro.",
  },
];

const SegmentSection = () => (
  <section className="py-20 px-5 bg-secondary">
    <div className="max-w-4xl mx-auto text-center">
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-2xl md:text-3xl font-bold text-foreground"
      >
        Para quem é esse serviço?
      </motion.h2>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        {segments.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="bg-background rounded-2xl p-6 text-left shadow-sm border border-border"
          >
            <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center mb-4">
              <s.icon className="w-5 h-5 text-accent" />
            </div>
            <h3 className="font-semibold text-foreground">{s.title}</h3>
            <ul className="mt-3 space-y-2">
              {s.pains.map((p, j) => (
                <li key={j} className="text-sm text-muted-foreground flex items-start gap-2">
                  <span className="w-1.5 h-1.5 bg-accent rounded-full mt-1.5 shrink-0" />
                  {p}
                </li>
              ))}
            </ul>
            <p className="mt-4 text-sm text-accent font-medium">{s.benefit}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default SegmentSection;
