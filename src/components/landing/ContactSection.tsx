import { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";

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
    <section id="contato" className="py-20 px-5 bg-primary">
      <div className="max-w-lg mx-auto text-center">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-2xl md:text-3xl font-bold text-primary-foreground"
        >
          Descubra se sua empresa tem dinheiro parado
        </motion.h2>
        <p className="mt-3 text-primary-foreground/70 text-sm">Sem custo inicial</p>

        <motion.form
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.15 }}
          onSubmit={handleSubmit}
          className="mt-10 space-y-4"
        >
          <Input
            placeholder="Nome completo"
            value={form.nome}
            onChange={(e) => setForm({ ...form, nome: e.target.value })}
            className="bg-primary-foreground/10 border-primary-foreground/20 text-primary-foreground placeholder:text-primary-foreground/50 h-12"
            maxLength={100}
          />
          <Input
            type="email"
            placeholder="E-mail profissional"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            className="bg-primary-foreground/10 border-primary-foreground/20 text-primary-foreground placeholder:text-primary-foreground/50 h-12"
            maxLength={255}
          />
          <Input
            placeholder="Nome da empresa"
            value={form.empresa}
            onChange={(e) => setForm({ ...form, empresa: e.target.value })}
            className="bg-primary-foreground/10 border-primary-foreground/20 text-primary-foreground placeholder:text-primary-foreground/50 h-12"
            maxLength={100}
          />
          <Input
            type="tel"
            placeholder="Telefone / WhatsApp"
            value={form.telefone}
            onChange={(e) => setForm({ ...form, telefone: e.target.value })}
            className="bg-primary-foreground/10 border-primary-foreground/20 text-primary-foreground placeholder:text-primary-foreground/50 h-12"
            maxLength={20}
          />
          <Button variant="hero" size="xl" className="w-full" type="submit" disabled={loading}>
            {loading ? "Enviando..." : "Agendar diagnóstico gratuito"}
          </Button>
        </motion.form>
      </div>
    </section>
  );
};

export default ContactSection;
