import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import officeImg from "@/assets/office-team.jpg";

const stats = [
  { label: "Anos de atuação", value: 5, suffix: "+", prefix: "" },
  { label: "Regimes analisados", value: 3, suffix: "", prefix: "" },
  { label: "Setores atendidos", value: 12, suffix: "+", prefix: "" },
];

function useCountUp(target: number, duration = 2000, inView: boolean) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!inView) return;
    let start = 0;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) {
        setCount(target);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, 16);
    return () => clearInterval(timer);
  }, [target, duration, inView]);
  return count;
}

const StatsSection = () => {
  const ref = useRef<HTMLDivElement>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setInView(true); },
      { threshold: 0.3 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <section ref={ref} className="relative py-20 px-6 bg-card overflow-hidden">
      <div className="max-w-5xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* Image */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            className="relative rounded-2xl overflow-hidden aspect-[4/5] md:aspect-[3/4]"
          >
            <img
              src={officeImg}
              alt="Equipe em consultoria"
              className="w-full h-full object-cover"
              loading="lazy"
              width={800}
              height={1000}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-primary/40 to-transparent" />
          </motion.div>

          {/* Stats */}
          <div>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-accent text-sm font-semibold tracking-widest uppercase mb-4"
            >
              Números
            </motion.p>
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-2xl md:text-4xl font-bold text-foreground leading-tight"
            >
              Atuação focada em{" "}
              <span className="text-accent">resultados reais</span>
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="mt-4 text-muted-foreground"
            >
              Trabalhamos todos os dias para potencializar empresas brasileiras, transformando impostos em resultado.
            </motion.p>

            <div className="mt-10 space-y-8">
              {stats.map((stat, i) => {
                const count = useCountUp(stat.value, 1500, inView);
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: 20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.2 + i * 0.15 }}
                    className="flex items-baseline gap-4"
                  >
                    <span className="text-4xl md:text-5xl font-black text-foreground">
                      {stat.prefix}{count}{stat.suffix}
                    </span>
                    <span className="text-muted-foreground text-sm">{stat.label}</span>
                  </motion.div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default StatsSection;
