import { motion } from "framer-motion";

const steps = [
  { num: "01", title: "Agendamento", desc: "Reunião gratuita de 30-45 minutos para entender sua realidade." },
  { num: "02", title: "Diagnóstico", desc: "Qualificação inicial e levantamento das principais oportunidades." },
  { num: "03", title: "Análise de dados", desc: "Estudo técnico de SPED, DRE e documentação fiscal." },
  { num: "04", title: "Oportunidades", desc: "Apresentação detalhada com números e projeções concretas." },
];

const ProcessSection = () => (
  <section className="py-20 px-5">
    <div className="max-w-3xl mx-auto text-center">
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-2xl md:text-3xl font-bold text-foreground"
      >
        Como funciona na prática
      </motion.h2>

      <div className="mt-12 space-y-6">
        {steps.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="flex items-start gap-5 text-left"
          >
            <span className="text-3xl font-extrabold text-accent/30">{s.num}</span>
            <div>
              <h3 className="font-semibold text-foreground">{s.title}</h3>
              <p className="text-sm text-muted-foreground mt-1">{s.desc}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default ProcessSection;
