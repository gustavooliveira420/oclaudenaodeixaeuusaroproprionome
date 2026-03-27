import { motion } from "framer-motion";

const steps = [
  { num: "01", title: "Agendamento", desc: "Reunião gratuita de 30–45 min para entender sua realidade." },
  { num: "02", title: "Diagnóstico", desc: "Qualificação inicial e levantamento das principais oportunidades." },
  { num: "03", title: "Análise técnica", desc: "Estudo detalhado de SPED, DRE e documentação fiscal." },
  { num: "04", title: "Oportunidades", desc: "Apresentação com números e projeções concretas." },
];

const ProcessSection = () => (
  <section className="py-24 px-6 bg-primary text-primary-foreground overflow-hidden">
    <div className="max-w-5xl mx-auto">
      <motion.span
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-accent text-sm font-semibold tracking-widest uppercase"
      >
        Processo
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.1 }}
        className="mt-4 text-2xl md:text-4xl font-bold leading-tight max-w-md"
      >
        Como funciona na prática
      </motion.h2>

      <div className="mt-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
        {steps.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.12, duration: 0.5 }}
            className="relative"
          >
            <span className="text-6xl font-black text-accent/15">{s.num}</span>
            <h3 className="mt-2 font-bold text-primary-foreground text-lg">{s.title}</h3>
            <p className="mt-2 text-primary-foreground/60 text-sm leading-relaxed">{s.desc}</p>
            {i < steps.length - 1 && (
              <div className="hidden lg:block absolute top-8 right-0 translate-x-1/2 w-8 h-px bg-accent/30" />
            )}
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default ProcessSection;
