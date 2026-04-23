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
  <section className="py-24 px-6">
    <div className="max-w-5xl mx-auto">
      <div className="text-center max-w-2xl mx-auto">
        <motion.span
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-accent text-sm font-semibold tracking-widest uppercase"
        >
          Segmentos
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="mt-4 text-2xl md:text-4xl font-bold text-foreground"
        >
          Para quem é esse serviço?
        </motion.h2>
      </div>

      <div className="mt-14 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {segments.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.15, duration: 0.5 }}
            className="group relative bg-background rounded-2xl border border-border overflow-hidden hover:shadow-xl transition-all duration-500"
          >
            <div className={`absolute inset-0 bg-gradient-to-b ${s.color} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
            <div className="relative p-7">
              <div className="flex items-center gap-3 mb-5">
                <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center group-hover:bg-accent/20 transition-colors">
                  <s.icon className="w-5 h-5 text-accent" />
                </div>
                <span className="text-xs font-semibold tracking-wider uppercase text-muted-foreground">{s.title}</span>
              </div>
              <h3 className="font-bold text-foreground text-lg">{s.subtitle}</h3>
              <ul className="mt-4 space-y-3">
                {s.pains.map((p, j) => (
                  <li key={j} className="text-sm text-muted-foreground flex items-start gap-2.5">
                    <span className="w-1.5 h-1.5 bg-accent rounded-full mt-2 shrink-0" />
                    {p}
                  </li>
                ))}
              </ul>
              <div className="mt-5 pt-5 border-t border-border">
                <p className="text-sm text-accent font-semibold">{s.benefit}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default SegmentSection;
