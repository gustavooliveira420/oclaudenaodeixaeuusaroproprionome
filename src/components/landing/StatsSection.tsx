import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { Coins, Percent, Users, BadgeCheck } from "lucide-react";

const stats = [
  {
    icon: Coins,
    value: 1000000,
    prefix: "+ R$ ",
    suffix: "",
    formatter: (n: number) =>
      "+ R$ " + n.toLocaleString("pt-BR", { maximumFractionDigits: 0 }),
    label: "recuperados para nossos clientes",
    accent: "text-prime-gold",
  },
  {
    icon: Percent,
    value: 62,
    prefix: "- ",
    suffix: "%",
    formatter: (n: number) => "- " + n + "%",
    label: "redução média de carga tributária",
    accent: "text-prime-green",
  },
  {
    icon: Users,
    value: 120,
    prefix: "+ ",
    suffix: "",
    formatter: (n: number) => "+ " + n,
    label: "empresas atendidas em todo o Brasil",
    accent: "text-prime-gold",
  },
  {
    icon: BadgeCheck,
    value: 15,
    prefix: "+ ",
    suffix: " anos",
    formatter: (n: number) => "+ " + n + " anos",
    label: "de experiência em consultoria tributária",
    accent: "text-prime-green",
  },
];

function useCountUp(target: number, duration = 1500, inView: boolean) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!inView) return;
    let start = 0;
    const step = Math.max(1, target / (duration / 16));
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
      ([entry]) => entry.isIntersecting && setInView(true),
      { threshold: 0.25 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <section
      id="resultados"
      ref={ref}
      className="relative bg-prime-dark text-white border-y border-white/5"
    >
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-12 md:py-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-6">
          {stats.map((stat, i) => {
            const count = useCountUp(stat.value, 1500, inView);
            const Icon = stat.icon;
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.4 }}
                className="flex items-start gap-4"
              >
                <div className="shrink-0 w-12 h-12 rounded-xl bg-white/5 border border-prime-gold/30 flex items-center justify-center">
                  <Icon className="w-6 h-6 text-prime-gold" />
                </div>
                <div>
                  <div className={`text-2xl md:text-3xl font-black tracking-tight ${stat.accent}`}>
                    {stat.formatter(count)}
                  </div>
                  <p className="mt-1 text-white/70 text-sm leading-snug max-w-[15rem]">
                    {stat.label}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;
