import { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { ArrowRight } from "lucide-react";
import patternBg from "@/assets/pattern-bg.jpg";

const ContactSection = () => {
  const { toast } = useToast();
  const [form, setForm] = useState({ nome: "", email: "", empresa: "", telefone: "" });
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nome.trim() || !form.email.trim() || !form.empresa.trim() || !form.telefone.trim()) {
      toast({ title: "Preencha todos os campos", variant: "destructive" });
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      toast({ title: "Solicitação enviada!", description: "Entraremos em contato em breve." });
      setForm({ nome: "", email: "", empresa: "", telefone: "" });
    }, 1000);
  };

  return (
    <section id="contato" className="relative py-24 px-6 bg-primary overflow-hidden">
      <div className="absolute inset-0 opacity-10">
        <img src={patternBg} alt="" className="w-full h-full object-cover" loading="lazy" />
      </div>

      <div className="relative z-10 max-w-lg mx-auto text-center">
        <motion.span
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-accent text-sm font-semibold tracking-widest uppercase"
        >
          Comece agora
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="mt-4 text-2xl md:text-4xl font-bold text-primary-foreground leading-tight"
        >
          Descubra se sua empresa tem{" "}
          <span className="text-accent">dinheiro parado</span>
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.15 }}
          className="mt-3 text-primary-foreground/50 text-sm"
        >
          Sem custo inicial · Diagnóstico gratuito
        </motion.p>

        <motion.form
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          onSubmit={handleSubmit}
          className="mt-10 space-y-4"
        >
          <Input
            placeholder="Nome completo"
            value={form.nome}
            onChange={(e) => setForm({ ...form, nome: e.target.value })}
            className="bg-primary-foreground/5 border-primary-foreground/15 text-primary-foreground placeholder:text-primary-foreground/40 h-13 rounded-xl focus:border-accent"
            maxLength={100}
          />
          <Input
            type="email"
            placeholder="E-mail profissional"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            className="bg-primary-foreground/5 border-primary-foreground/15 text-primary-foreground placeholder:text-primary-foreground/40 h-13 rounded-xl focus:border-accent"
            maxLength={255}
          />
          <Input
            placeholder="Nome da empresa"
            value={form.empresa}
            onChange={(e) => setForm({ ...form, empresa: e.target.value })}
            className="bg-primary-foreground/5 border-primary-foreground/15 text-primary-foreground placeholder:text-primary-foreground/40 h-13 rounded-xl focus:border-accent"
            maxLength={100}
          />
          <Input
            type="tel"
            placeholder="Telefone / WhatsApp"
            value={form.telefone}
            onChange={(e) => setForm({ ...form, telefone: e.target.value })}
            className="bg-primary-foreground/5 border-primary-foreground/15 text-primary-foreground placeholder:text-primary-foreground/40 h-13 rounded-xl focus:border-accent"
            maxLength={20}
          />
          <Button variant="hero" size="xl" className="w-full group" type="submit" disabled={loading}>
            {loading ? "Enviando..." : "Agendar diagnóstico gratuito"}
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </motion.form>
      </div>
    </section>
  );
};

export default ContactSection;
