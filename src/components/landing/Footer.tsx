import Logo from "./Logo";

const Footer = () => (
  <footer className="bg-prime-dark border-t border-prime-gold/20">
    <div className="max-w-7xl mx-auto px-4 md:px-6 py-12">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
        <div>
          <Logo variant="light" />
          <p className="mt-4 text-prime-green text-sm font-semibold">
            você livre, das dívidas!
          </p>
          <p className="mt-2 text-white/50 text-xs leading-relaxed max-w-xs">
            Inteligência tributária para transformar impostos em oportunidades
            financeiras.
          </p>
        </div>

        <div className="text-white/70 text-sm space-y-2">
          <h4 className="text-prime-gold text-xs font-bold tracking-[0.2em] uppercase mb-3">
            Soluções
          </h4>
          <p>Revisão Tributária</p>
          <p>Recuperação de Créditos</p>
          <p>Renegociação Estratégica</p>
          <p>Assessoria Mensal (Retainer)</p>
        </div>

        <div className="text-white/70 text-sm space-y-2">
          <h4 className="text-prime-gold text-xs font-bold tracking-[0.2em] uppercase mb-3">
            Contato
          </h4>
          <p>Atendimento em todo o Brasil</p>
          <button
            type="button"
            onClick={() =>
              document.getElementById("contato")?.scrollIntoView({ behavior: "smooth" })
            }
            className="block text-left hover:text-prime-green transition-colors"
          >
            Agendar diagnóstico
          </button>
        </div>
      </div>

      <div className="mt-12 pt-6 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-3">
        <p className="text-white/40 text-xs">
          © {new Date().getFullYear()} Renegocia Consultoria Prime. Todos os direitos
          reservados.
        </p>
        <p className="text-prime-green/70 text-xs font-semibold tracking-wide">
          Menos carga · mais caixa · mais crescimento
        </p>
      </div>
    </div>
  </footer>
);

export default Footer;
