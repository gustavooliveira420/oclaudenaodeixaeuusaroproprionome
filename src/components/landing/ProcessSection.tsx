import { motion } from "framer-motion";
import { Search, FileSearch, Target, Cog } from "lucide-react";

const steps = [
  {
    num: "01",
    icon: Search,
    title: "Diagnóstico Gratuito",
    desc: "Entendemos sua situação e identificamos potenciais oportunidades.",
  },
  {
    num: "02",
    icon: FileSearch,
    title: "Análise Técnica",
    desc: "Realizamos uma análise detalhada dos tributos, contratos e documentos.",
  },
  {
    num: "03",
    icon: Target,
    title: "Estratégia Personalizada",
    desc: "Desenvolvemos um plano estratégico para reduzir sua carga tributária.",
  },
  {
    num: "04",
    icon: Cog,
    title: "Execução e Acompanhamento",
    desc: "Cuidamos de todo o processo e acompanhamos cada etapa até o resultado final.",
  },
];

const ProcessSection = () => (
  <section
    id="como-funciona"
    className="relative py-24 px-4 md:px-6 bg-prime-dark text-white overflow-hidden"
  >
    {/* Linha dourada decorativa de fundo */}
    <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-prime-gold/40 to-transparent" />
    <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-prime-gold/40 to-transparent" />

    <div className="max-w-7xl mx-auto">
      <div className="text-center max-w-3xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="flex items-center justify-center gap-3 mb-4"
        >
          <span className="h-px w-10 bg-prime-green" />
          <span className="text-prime-green text-xs font-semibold tracking-[0.2em] uppercase">
            Como funciona
          </span>
          <span className="h-px w-10 bg-prime-green" />
        </motion.div>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-2xl md:text-4xl font-black uppercase tracking-tight leading-tight"
        >
          Um processo estratégico,
          <br />
          <span className="text-prime-green">transparente e seguro</span>
        </motion.h2>
      </div>

      <div className="mt-16 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-4 relative">
        {/* Linha conectora decorativa (desktop) */}
        <div className="hidden lg:block absolute top-12 left-[12%] right-[12%] h-px border-t border-dashed border-prime-gold/30 pointer-events-none" />

        {steps.map((s, i) => {
          const Icon = s.icon;
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.12, duration: 0.5 }}
              className="relative flex flex-col items-center text-center"
            >
              {/* Círculo numerado */}
              <div className="relative z-10 w-24 h-24 rounded-full bg-prime-dark border-2 border-prime-gold/60 flex items-center justify-center shadow-[0_0_0_6px_hsl(var(--prime-dark))]">
                <Icon className="w-9 h-9 text-prime-gold" />
                <span className="absolute -top-2 -right-2 w-9 h-9 rounded-full bg-prime-green text-prime-dark text-xs font-black flex items-center justify-center shadow-lg">
                  {s.num}
                </span>
              </div>

              <h3 className="mt-6 font-bold text-prime-green text-base uppercase tracking-wide">
                {s.title}
              </h3>
              <p className="mt-3 text-white/70 text-sm leading-relaxed max-w-[18rem]">
                {s.desc}
              </p>
            </motion.div>
          );
        })}
      </div>
    </div>
  </section>
);

export default ProcessSection;
