import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { Menu, X, ArrowRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import Logo from "./Logo";

const NAV_ITEMS = [
  { id: "sobre", label: "Sobre nós" },
  { id: "servicos", label: "Serviços" },
  { id: "resultados", label: "Resultados" },
  { id: "como-funciona", label: "Como funciona" },
  { id: "contato", label: "Contato" },
];

const Header = () => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollTo = (id: string) => {
    setMobileOpen(false);
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${
        scrolled
          ? "bg-prime-dark/95 backdrop-blur-md shadow-lg"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between px-4 md:px-6 h-16 md:h-20">
        <button
          onClick={() => scrollTo("topo")}
          className="focus:outline-none focus-visible:ring-2 focus-visible:ring-prime-green rounded"
          aria-label="Renegocia — voltar ao topo"
        >
          <Logo variant="light" showTagline={!scrolled} />
        </button>

        {/* Nav desktop */}
        <nav className="hidden lg:flex items-center gap-8">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.id}
              onClick={() => scrollTo(item.id)}
              className="text-sm font-semibold uppercase tracking-wide text-white/80 hover:text-prime-gold transition-colors"
            >
              {item.label}
            </button>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <Button
            variant="prime"
            size="sm"
            className="hidden md:inline-flex group rounded-lg"
            onClick={() => scrollTo("contato")}
          >
            Analisar meu caso
            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
          </Button>

          <button
            onClick={() => setMobileOpen((v) => !v)}
            className="lg:hidden text-white p-2 rounded-md hover:bg-white/10"
            aria-label={mobileOpen ? "Fechar menu" : "Abrir menu"}
          >
            {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Menu mobile */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="lg:hidden bg-prime-dark/98 backdrop-blur-md border-t border-white/10"
          >
            <nav className="flex flex-col px-4 py-4">
              {NAV_ITEMS.map((item) => (
                <button
                  key={item.id}
                  onClick={() => scrollTo(item.id)}
                  className="text-left py-3 text-white/85 font-semibold uppercase tracking-wide text-sm border-b border-white/5 hover:text-prime-gold transition-colors"
                >
                  {item.label}
                </button>
              ))}
              <Button
                variant="prime"
                size="sm"
                className="mt-4 group rounded-lg"
                onClick={() => scrollTo("contato")}
              >
                Analisar meu caso
                <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Button>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};

export default Header;
