import { Button } from "@/components/ui/button";
import { useEffect, useRef, useState } from "react";
import { Calendar } from "lucide-react";
import { motion } from "framer-motion";

const Header = () => {
  // "edges" = topo ou fim da página (botão completo, logo centralizado)
  // "middle" = navegando (botão compacto com ícone, logo deslocada à direita)
  const [position, setPosition] = useState<"edges" | "middle">("edges");
  const [scrolled, setScrolled] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const logoRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLDivElement>(null);
  const [centerOffset, setCenterOffset] = useState(0);
  const [logoMaxWidth, setLogoMaxWidth] = useState<number | undefined>(undefined);
  const [logoScale, setLogoScale] = useState(1);

  const isEdges = position === "edges";

  useEffect(() => {
    const measure = () => {
      const c = containerRef.current;
      const l = logoRef.current;
      const b = buttonRef.current;
      if (!c || !l || !b) return;
      const cw = c.clientWidth;
      const bw = b.clientWidth;
      const sidePad = 16; // px-4
      const gap = 36; // espaço mínimo entre logo e botão
      const maxLogo = cw - sidePad * 2 - bw - gap;
      setLogoMaxWidth(Math.max(80, maxLogo));
      const rawLogoWidth = l.scrollWidth;
      const nextScale = Math.min(1, Math.max(0.78, maxLogo / rawLogoWidth));
      setLogoScale(nextScale);
      const lw = Math.min(rawLogoWidth * nextScale, maxLogo);
      const target = (cw - bw - gap - lw) / 2 - sidePad;
      setCenterOffset(Math.max(0, target));
    };
    measure();
    window.addEventListener("resize", measure);
    return () => window.removeEventListener("resize", measure);
  }, [isEdges]);

  useEffect(() => {
    const handleScroll = () => {
      const y = window.scrollY;
      const docH = document.documentElement.scrollHeight - window.innerHeight;
      const nearTop = y < 120;
      const nearBottom = docH - y < 200;
      setPosition(nearTop || nearBottom ? "edges" : "middle");
      setScrolled(y > 50);
    };
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };

  // Detecta fundo claro/escuro: nas bordas (hero/footer) o fundo é escuro;
  // no meio com header transparente o fundo é claro.
  const onDarkBg = scrolled || position === "edges";

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-500 ${
        scrolled ? "bg-primary/95 backdrop-blur-md shadow-lg" : "bg-transparent"
      }`}
    >
      <div ref={containerRef} className="relative max-w-5xl mx-auto h-16 md:h-20 px-4">
        {/* Logo: posicionada à esquerda; ao rolar, desliza suavemente para o centro */}
        <motion.div
          ref={logoRef}
          className="absolute top-1/2 left-4"
          style={{ willChange: "transform", y: "-50%", maxWidth: logoMaxWidth }}
          animate={{ x: isEdges ? 0 : centerOffset, y: "-50%", scale: isEdges ? logoScale : 1 }}
          transition={{ type: "tween", ease: [0.22, 1, 0.36, 1], duration: 0.45 }}
        >
          <span
            className={`inline-block font-bold text-lg tracking-tight px-3 py-1 rounded-md transition-colors duration-500 whitespace-nowrap ${
              onDarkBg
                ? "text-primary-foreground"
                : "text-primary border border-primary/40 bg-background/70 backdrop-blur-sm shadow-sm"
            }`}
          >
            Renegocia
            <span className="text-accent">.</span>
            Tributário
          </span>
        </motion.div>

        {/* Botão à direita: morfa entre completo e ícone via animação de largura, sem unmount */}
        <div ref={buttonRef} className="absolute top-1/2 right-4 -translate-y-1/2">
          <motion.div
            animate={{ scale: isEdges ? 1 : 0.95 }}
            transition={{ duration: 0.3 }}
          >
            {isEdges ? (
              <Button variant="hero" size="sm" onClick={scrollToForm}>
                Agendar diagnóstico
              </Button>
            ) : (
              <Button
                variant="hero"
                size="icon"
                onClick={scrollToForm}
                aria-label="Agendar diagnóstico"
                className="h-10 w-10 rounded-full shadow-lg"
              >
                <Calendar className="w-4 h-4" />
              </Button>
            )}
          </motion.div>
        </div>
      </div>
    </header>
  );
};

export default Header;
