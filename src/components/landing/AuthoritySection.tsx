import { motion } from "framer-motion";
import { FileSpreadsheet, Search, Scale } from "lucide-react";
import dataImg from "@/assets/data-analysis.jpg";

const pillars = [
  { icon: FileSpreadsheet, title: "Análise técnica profunda", desc: "SPED, ECF, EFD-Contribuições e DRE para identificar oportunidades reais." },
  { icon: Search, title: "Diagnóstico baseado em dados", desc: "Cada recomendação sustentada por análise documental e legislação vigente." },
  { icon: Scale, title: "Segurança jurídica", desc: "Estratégias fundamentadas legalmente, sem atalhos ou riscos desnecessários." },
];

const AuthoritySection = () => (
  <section className="py-24 px-6 overflow-hidden">
    <div className="max-w-5xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-14 items-center">
        <div>
          <motion.span
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-accent text-sm font-semibold tracking-widest uppercase"
          >
            Nossa atuação
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="mt-4 text-2xl md:text-4xl font-bold text-foreground leading-tight"
          >
            Atuação estratégica baseada em{" "}
            <span className="text-accent">dados</span>
          </motion.h2>

          <div className="mt-10 space-y-6">
            {pillars.map((p, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 + i * 0.1 }}
                className="flex items-start gap-4"
              >
                <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center shrink-0">
                  <p.icon className="w-5 h-5 text-accent" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">{p.title}</h3>
                  <p className="mt-1 text-sm text-muted-foreground leading-relaxed">{p.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, x: 40 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="relative rounded-2xl overflow-hidden aspect-video"
        >
          <img
            src={dataImg}
            alt="Análise de dados tributários"
            className="w-full h-full object-cover"
            loading="lazy"
            width={1280}
            height={720}
          />
          <div className="absolute inset-0 bg-gradient-to-tr from-primary/30 to-transparent" />
        </motion.div>
      </div>
    </div>
  </section>
);

export default AuthoritySection;
