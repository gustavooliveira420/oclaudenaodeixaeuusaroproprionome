import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { Calendar } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const Header = () => {
  // "edges" = topo ou fim da página (botão completo, logo centralizado)
  // "middle" = navegando (botão compacto com ícone, logo deslocada à direita)
  const [position, setPosition] = useState<"edges" | "middle">("edges");
  const [scrolled, setScrolled] = useState(false);

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
        scrolled
          ? "bg-primary/95 backdrop-blur-md shadow-lg"
          : "bg-transparent"
      }`}
    >
      <div className="relative max-w-5xl mx-auto flex items-center px-4 h-16 md:h-20">
        {/* Logo com efeito invertido conforme fundo */}
        <motion.div
          layout
          transition={{ type: "spring", stiffness: 260, damping: 26 }}
          className={`flex-1 flex ${
            position === "edges" ? "justify-center md:justify-start" : "justify-start"
          }`}
        >
          <span
            className={`font-bold text-lg tracking-tight px-3 py-1 rounded-md transition-colors duration-500 ${
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

        {/* Botão à direita: animação entre completo e ícone */}
        <div className="flex items-center justify-end">
          <AnimatePresence mode="wait" initial={false}>
            {position === "edges" ? (
              <motion.div
                key="full"
                initial={{ opacity: 0, scale: 0.9, width: 0 }}
                animate={{ opacity: 1, scale: 1, width: "auto" }}
                exit={{ opacity: 0, scale: 0.9, width: 0 }}
                transition={{ duration: 0.25 }}
              >
                <Button variant="hero" size="sm" onClick={scrollToForm}>
                  Agendar diagnóstico
                </Button>
              </motion.div>
            ) : (
              <motion.div
                key="icon"
                initial={{ opacity: 0, scale: 0.6 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.6 }}
                transition={{ duration: 0.25 }}
              >
                <Button
                  variant="hero"
                  size="icon"
                  onClick={scrollToForm}
                  aria-label="Agendar diagnóstico"
                  className="h-10 w-10 rounded-full shadow-lg"
                >
                  <Calendar className="w-4 h-4" />
                </Button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </header>
  );
};

export default Header;
