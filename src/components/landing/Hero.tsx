import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const Hero = () => {
  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };
  const scrollToServicos = () => {
    document.getElementById("servicos")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section
      id="topo"
      className="relative min-h-screen flex items-center overflow-hidden bg-prime-dark"
    >
      {/* Fundo: gradient + grid sutil + skyline em SVG abstrato */}
      <div className="absolute inset-0">
        {/* Gradient base verde escuro */}
        <div className="absolute inset-0 bg-gradient-to-br from-prime-dark via-[hsl(170_45%_8%)] to-prime-dark" />

        {/* Grid técnico sutil */}
        <div className="absolute inset-0 prime-grid opacity-40" />

        {/* Skyline + chart ascendente abstrato em SVG (decorativo) */}
        <svg
          viewBox="0 0 1200 800"
          preserveAspectRatio="xMidYMax slice"
          className="absolute inset-0 w-full h-full opacity-50"
          aria-hidden="true"
        >
          {/* Silhuetas de prédios */}
          <g fill="#0F2F2A" opacity="0.95">
            <rect x="60" y="500" width="60" height="300" />
            <rect x="130" y="430" width="80" height="370" />
            <rect x="220" y="460" width="50" height="340" />
            <rect x="280" y="380" width="90" height="420" />
            <rect x="380" y="420" width="65" height="380" />
            <rect x="455" y="350" width="100" height="450" />
            <rect x="565" y="420" width="55" height="380" />
            <rect x="630" y="300" width="110" height="500" />
            <rect x="750" y="380" width="70" height="420" />
            <rect x="830" y="440" width="55" height="360" />
            <rect x="895" y="320" width="120" height="480" />
            <rect x="1025" y="410" width="70" height="390" />
            <rect x="1105" y="470" width="60" height="330" />
          </g>
          {/* Linhas de janelas (verde claro) */}
          <g stroke="#16B98A" strokeWidth="1" opacity="0.18">
            {Array.from({ length: 20 }).map((_, i) => (
              <line key={i} x1="60" x2="1170" y1={520 + i * 14} y2={520 + i * 14} />
            ))}
          </g>
          {/* Linha de gráfico ascendente em verde ação */}
          <polyline
            points="60,650 200,620 340,560 480,540 620,470 760,420 900,360 1040,300 1170,240"
            fill="none"
            stroke="#16B98A"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
            opacity="0.85"
          />
          {/* Linha dourada secundária */}
          <polyline
            points="60,700 200,680 340,640 480,610 620,560 760,510 900,450 1040,390 1170,320"
            fill="none"
            stroke="#D4AF37"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            opacity="0.55"
            strokeDasharray="6 4"
          />
        </svg>

        {/* Vinheta */}
        <div className="absolute inset-0 bg-gradient-to-t from-prime-dark via-prime-dark/40 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-r from-prime-dark via-prime-dark/70 to-transparent md:to-prime-dark/30" />
      </div>

      {/* "R" gigante decorativo no fundo direito */}
      <div className="absolute right-0 md:right-[8%] top-1/2 -translate-y-1/2 pointer-events-none select-none hidden md:block">
        <svg
          viewBox="0 0 200 200"
          className="w-[28rem] h-[28rem] lg:w-[36rem] lg:h-[36rem] opacity-[0.08]"
          aria-hidden="true"
        >
          <path d="M 36 52 L 64 52 L 76 156 L 36 156 Z" fill="#D4AF37" />
          <path
            d="M 64 32 L 128 32 Q 164 32 164 72 Q 164 104 132 112 L 168 168 L 140 168 L 108 116 L 92 116 L 92 168 L 64 168 Z M 92 56 L 92 92 L 124 92 Q 140 92 140 74 Q 140 56 124 56 Z"
            fill="#FFFFFF"
          />
        </svg>
      </div>

      {/* Conteúdo */}
      <div className="relative z-10 w-full px-4 md:px-6 pb-16 pt-32 md:py-32 max-w-7xl mx-auto">
        <div className="max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="flex items-center gap-3 mb-6"
          >
            <span className="h-px w-10 bg-prime-gold" />
            <span className="text-prime-gold text-xs font-semibold tracking-[0.2em] uppercase">
              Consultoria Tributária Estratégica
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="text-3xl md:text-5xl lg:text-6xl font-black text-white leading-[1.05] tracking-tight uppercase"
          >
            Inteligência tributária
            <br />
            para transformar
            <br />
            impostos em{" "}
            <span className="text-prime-green">oportunidades financeiras</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="mt-6 text-base md:text-lg text-white/75 leading-relaxed max-w-lg"
          >
            Consultoria tributária estratégica para revisão de tributos, recuperação de
            valores e redução legal da carga fiscal. Mostramos, com números, onde sua
            empresa pode economizar ou recuperar valores dos últimos 5 anos.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.35 }}
            className="mt-10 flex flex-col sm:flex-row gap-4"
          >
            <Button variant="prime" size="xl" onClick={scrollToForm} className="group">
              Analisar meu caso
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="primeOutline" size="xl" onClick={scrollToServicos}>
              Diagnóstico gratuito
            </Button>
          </motion.div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.7, delay: 0.6 }}
            className="mt-8 text-prime-green text-sm font-semibold tracking-wide"
          >
            Menos carga, mais caixa, mais crescimento.
          </motion.p>
        </div>
      </div>

      {/* Linha dourada inferior */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-prime-gold/60 to-transparent" />
    </section>
  );
};

export default Hero;
