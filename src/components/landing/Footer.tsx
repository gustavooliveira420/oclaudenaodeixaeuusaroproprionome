const Footer = () => (
  <footer className="py-10 px-6 bg-primary border-t border-primary-foreground/10">
    <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
      <span className="text-primary-foreground font-bold text-lg tracking-tight">
        Renegocia<span className="text-accent">.</span>Tributário
      </span>
      <p className="text-primary-foreground/40 text-xs">
        © {new Date().getFullYear()} Renegocia Consultoria. Todos os direitos reservados.
      </p>
    </div>
  </footer>
);

export default Footer;
