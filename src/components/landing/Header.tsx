import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";

const Header = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${
        scrolled
          ? "bg-primary/98 backdrop-blur-md shadow-lg"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-5xl mx-auto flex items-center justify-center gap-4 px-4 h-16 md:h-20 md:justify-between">
        <span className="text-primary-foreground font-bold text-lg tracking-tight">
          Renegocia<span className="text-accent">.</span>Tributário
        </span>
        <Button variant="hero" size="sm" onClick={scrollToForm}>
          Agendar diagnóstico
        </Button>
      </div>
    </header>
  );
};

export default Header;
