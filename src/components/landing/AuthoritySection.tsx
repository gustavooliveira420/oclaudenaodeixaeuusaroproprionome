import { motion } from "framer-motion";
import { FileSpreadsheet, Search, Scale } from "lucide-react";

const pillars = [
  { icon: FileSpreadsheet, title: "Análise técnica profunda", desc: "Trabalhamos com SPED, ECF, EFD-Contribuições e DRE para identificar oportunidades reais." },
  { icon: Search, title: "Diagnóstico baseado em dados", desc: "Cada recomendação é sustentada por análise documental e legislação vigente." },
  { icon: Scale, title: "Segurança jurídica", desc: "Todas as estratégias são fundamentadas legalmente, sem atalhos ou riscos desnecessários." },
];

const AuthoritySection = () => (
  <section className="py-20 px-5">
    <div className="max-w-4xl mx-auto text-center">
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-2xl md:text-3xl font-bold text-foreground"
      >
        Atuação estratégica baseada em dados
      </motion.h2>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        {pillars.map((p, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="text-center p-6"
          >
            <div className="w-14 h-14 rounded-2xl bg-accent/10 flex items-center justify-center mx-auto mb-4">
              <p.icon className="w-7 h-7 text-accent" />
            </div>
            <h3 className="font-semibold text-foreground">{p.title}</h3>
            <p className="mt-2 text-sm text-muted-foreground">{p.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default AuthoritySection;
