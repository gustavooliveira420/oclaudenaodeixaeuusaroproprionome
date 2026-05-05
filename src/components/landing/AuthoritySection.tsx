import { motion } from "framer-motion";
import { FileSpreadsheet, Search, Scale } from "lucide-react";

const pillars = [
  {
    icon: FileSpreadsheet,
    title: "Análise técnica profunda",
    desc: "SPED, ECF, EFD-Contribuições e DRE para identificar oportunidades reais.",
  },
  {
    icon: Search,
    title: "Diagnóstico baseado em dados",
    desc: "Cada recomendação sustentada por análise documental e legislação vigente.",
  },
  {
    icon: Scale,
    title: "Segurança jurídica",
    desc: "Estratégias fundamentadas legalmente, sem atalhos ou riscos desnecessários.",
  },
];

const AuthoritySection = () => (
  <section className="py-24 px-4 md:px-6 bg-prime-light">
    <div className="max-w-7xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-14 items-center">
        <div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="flex items-center gap-3 mb-4"
          >
            <span className="h-px w-10 bg-prime-green" />
            <span className="text-prime-green text-xs font-semibold tracking-[0.2em] uppercase">
              Nossa atuação
            </span>
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-2xl md:text-4xl font-black uppercase tracking-tight text-prime-dark leading-tight"
          >
            Atuação estratégica baseada em{" "}
            <span className="text-prime-green">dados</span>
          </motion.h2>
          <p className="mt-5 text-prime-black/70 leading-relaxed max-w-lg">
            Combinamos inteligência tributária, análise documental e estratégia
            comercial para entregar resultados mensuráveis. Sem promessas vazias —
            só números, fundamentação legal e execução.
          </p>

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
                <div className="w-11 h-11 rounded-xl bg-prime-dark flex items-center justify-center shrink-0">
                  <p.icon className="w-5 h-5 text-prime-gold" />
                </div>
                <div>
                  <h3 className="font-bold text-prime-dark uppercase tracking-tight text-sm">
                    {p.title}
                  </h3>
                  <p className="mt-1 text-sm text-prime-black/65 leading-relaxed">
                    {p.desc}
                  </p>
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
          className="relative aspect-[4/5] rounded-2xl overflow-hidden bg-prime-dark border border-prime-gold/20"
        >
          {/* Decoração — gráfico ascendente em SVG */}
          <div className="absolute inset-0 prime-grid opacity-30" />
          <svg
            viewBox="0 0 400 500"
            className="absolute inset-0 w-full h-full"
            aria-hidden="true"
          >
            <defs>
              <linearGradient id="gridFill" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stopColor="#16B98A" stopOpacity="0.4" />
                <stop offset="100%" stopColor="#16B98A" stopOpacity="0" />
              </linearGradient>
            </defs>
            <polygon
              points="40,440 100,400 160,360 220,300 280,220 340,140 400,80 400,500 40,500"
              fill="url(#gridFill)"
            />
            <polyline
              points="40,440 100,400 160,360 220,300 280,220 340,140 400,80"
              fill="none"
              stroke="#16B98A"
              strokeWidth="3"
              strokeLinecap="round"
            />
            <polyline
              points="40,470 100,450 160,420 220,380 280,330 340,260 400,180"
              fill="none"
              stroke="#D4AF37"
              strokeWidth="2"
              strokeLinecap="round"
              strokeDasharray="6 4"
              opacity="0.7"
            />
          </svg>
          <div className="absolute bottom-0 left-0 right-0 p-8 bg-gradient-to-t from-prime-dark via-prime-dark/80 to-transparent">
            <p className="text-prime-gold text-xs font-bold tracking-[0.2em] uppercase">
              Inteligência tributária
            </p>
            <p className="text-white text-2xl font-black mt-2 leading-tight uppercase">
              Que gera{" "}
              <span className="text-prime-green">caixa</span> para sua empresa
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  </section>
);

export default AuthoritySection;
