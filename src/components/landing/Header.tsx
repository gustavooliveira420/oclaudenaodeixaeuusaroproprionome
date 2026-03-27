import { Button } from "@/components/ui/button";

const Header = () => {
  const scrollToForm = () => {
    document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-40 bg-primary/95 backdrop-blur-sm border-b border-primary-foreground/10">
      <div className="max-w-5xl mx-auto flex items-center justify-between px-5 h-16">
        <span className="text-primary-foreground font-bold text-lg tracking-tight">
          Henrique Melo
        </span>
        <Button variant="hero" size="sm" onClick={scrollToForm}>
          Agendar diagnóstico
        </Button>
      </div>
    </header>
  );
};

export default Header;
