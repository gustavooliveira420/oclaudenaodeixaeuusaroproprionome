import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { ArrowRight, ArrowLeft } from "lucide-react";
import patternBg from "@/assets/pattern-bg.jpg";

const SETORES = [
  "Comércio Varejista (Postos, Farmácias, etc.)",
  "Indústria",
  "Serviços (TI, Saúde, Educação)",
  "Agronegócio",
  "Setor Financeiro",
];

const REGIMES = [
  "Simples Nacional",
  "Lucro Presumido",
  "Lucro Real",
  "Não tenho certeza",
];

const FAIXAS = [
  "Até R$ 100 mil",
  "De R$ 100 mil a R$ 500 mil",
  "De R$ 500 mil a R$ 2 Milhões",
  "Acima de R$ 2 Milhões",
];

const SITUACOES = [
  {
    id: "planejamento",
    label:
      "Nunca fizemos (ou faz mais de 2 anos) um estudo comparando se o Simples, Lucro Presumido ou Lucro Real é mais vantajoso.",
  },
  {
    id: "inss",
    label:
      "Temos uma folha de pagamento alta (acima de R$ 100k) e pagamos benefícios como PLR, aviso-prévio indenizado ou auxílios.",
  },
  {
    id: "pis_cofins",
    label:
      "Temos um alto volume de compras mensais de insumos, matérias-primas, energia elétrica ou fretes.",
  },
  {
    id: "icms_st",
    label:
      "Trabalhamos com revenda e pagamos ICMS-ST (Substituição Tributária) nas nossas compras.",
  },
  {
    id: "refis",
    label:
      "Possuímos débitos de impostos em aberto e buscamos opções de parcelamento com redução de multas.",
  },
  {
    id: "holding",
    label:
      "Os sócios possuem patrimônio relevante e pensam em proteção familiar ou sucessão.",
  },
];

const ContactSection = () => {
  const { toast } = useToast();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    nome: "",
    email: "",
    telefone: "",
    empresa: "",
    setor: "",
    regime: "",
    faturamento: "",
    situacoes: [] as string[],
  });

  const toggleSituacao = (id: string) => {
    setForm((prev) => ({
      ...prev,
      situacoes: prev.situacoes.includes(id)
        ? prev.situacoes.filter((s) => s !== id)
        : [...prev.situacoes, id],
    }));
  };

  const validateStep = (s: number): boolean => {
    if (s === 1) {
      if (!form.nome.trim() || !form.email.trim() || !form.telefone.trim() || !form.empresa.trim()) {
        toast({ title: "Preencha todos os campos de contato", variant: "destructive" });
        return false;
      }
    }
    if (s === 2) {
      if (!form.setor || !form.regime || !form.faturamento) {
        toast({ title: "Preencha o perfil do negócio", variant: "destructive" });
        return false;
      }
    }
    return true;
  };

  const next = () => {
    if (validateStep(step)) setStep((s) => Math.min(s + 1, 3));
  };

  const prev = () => setStep((s) => Math.max(s - 1, 1));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.situacoes.length === 0) {
      toast({ title: "Selecione pelo menos uma situação", variant: "destructive" });
      return;
    }
    setLoading(true);
    try {
      const situacoesLabels = form.situacoes.map(id => {
        const sit = SITUACOES.find(s => s.id === id);
        return sit ? sit.label : id;
      });

      const payload = new URLSearchParams();
      payload.append("nome", form.nome);
      payload.append("email", form.email);
      payload.append("telefone", form.telefone);
      payload.append("empresa", form.empresa);
      payload.append("setor", form.setor);
      payload.append("regime", form.regime);
      payload.append("faturamento", form.faturamento);
      payload.append("situacoes", situacoesLabels.join(" | "));

      await fetch(
        "https://webhooks-mvp.algomaisacai.com.br/webhook/90229d83-2494-467d-8918-b342b50ed66d",
        {
          method: "POST",
          mode: "no-cors",
          body: payload,
        }
      );

      // Com mode: 'no-cors' não conseguimos ler a resposta, mas o dado é enviado
      toast({ title: "Solicitação enviada!", description: "Entraremos em contato em breve.", duration: 5000 });
      setForm({ nome: "", email: "", telefone: "", empresa: "", setor: "", regime: "", faturamento: "", situacoes: [] });
      setStep(1);
    } catch (err) {
      console.error("Webhook error:", err);
      toast({ title: "Erro ao enviar", description: "Tente novamente em instantes.", variant: "destructive", duration: 5000 });
    } finally {
      setLoading(false);
    }
  };

  const inputClass =
    "bg-primary-foreground/5 border-primary-foreground/15 text-primary-foreground placeholder:text-primary-foreground/40 h-13 rounded-xl focus:border-accent";

  const selectTriggerClass =
    "bg-primary-foreground/5 border-primary-foreground/15 text-primary-foreground h-13 rounded-xl focus:border-accent [&>span]:text-primary-foreground/60 data-[state=open]:border-accent";

  const stepIndicator = (num: number, label: string) => (
    <div className="flex flex-col items-center gap-1.5">
      <div
        className={`w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold transition-colors ${
          step >= num
            ? "bg-accent text-accent-foreground"
            : "bg-primary-foreground/10 text-primary-foreground/40"
        }`}
      >
        {num}
      </div>
      <span
        className={`text-[11px] font-medium transition-colors ${
          step >= num ? "text-accent" : "text-primary-foreground/30"
        }`}
      >
        {label}
      </span>
    </div>
  );

  return (
    <section id="contato" className="relative py-24 px-4 bg-primary overflow-hidden">
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

        {/* Step indicators */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.18 }}
          className="mt-8 flex items-center justify-center gap-6"
        >
          {stepIndicator(1, "Contato")}
          <div className={`h-px w-8 transition-colors ${step >= 2 ? "bg-accent" : "bg-primary-foreground/15"}`} />
          {stepIndicator(2, "Negócio")}
          <div className={`h-px w-8 transition-colors ${step >= 3 ? "bg-accent" : "bg-primary-foreground/15"}`} />
          {stepIndicator(3, "Oportunidades")}
        </motion.div>

        <form onSubmit={handleSubmit} className="mt-8">
          <AnimatePresence mode="wait">
            {step === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -30 }}
                transition={{ duration: 0.25 }}
                className="space-y-4"
              >
                <p className="text-primary-foreground/70 text-sm font-semibold mb-2 text-left">
                  Passo 1: Dados de Contato
                </p>
                <Input
                  placeholder="Nome completo"
                  value={form.nome}
                  onChange={(e) => setForm({ ...form, nome: e.target.value })}
                  className={inputClass}
                  maxLength={100}
                />
                <Input
                  type="email"
                  placeholder="E-mail corporativo"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className={inputClass}
                  maxLength={255}
                />
                <Input
                  type="tel"
                  placeholder="WhatsApp / Telefone"
                  value={form.telefone}
                  onChange={(e) => setForm({ ...form, telefone: e.target.value })}
                  className={inputClass}
                  maxLength={20}
                />
                <Input
                  placeholder="Nome da empresa"
                  value={form.empresa}
                  onChange={(e) => setForm({ ...form, empresa: e.target.value })}
                  className={inputClass}
                  maxLength={100}
                />
                <Button variant="hero" size="xl" className="w-full group mt-2" type="button" onClick={next}>
                  Próximo
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </motion.div>
            )}

            {step === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -30 }}
                transition={{ duration: 0.25 }}
                className="space-y-4"
              >
                <p className="text-primary-foreground/70 text-sm font-semibold mb-2 text-left">
                  Passo 2: Perfil do Negócio
                </p>

                <Select value={form.setor} onValueChange={(v) => setForm({ ...form, setor: v })}>
                  <SelectTrigger className={selectTriggerClass}>
                    <SelectValue placeholder="Setor de Atuação (CNAE Principal)" />
                  </SelectTrigger>
                  <SelectContent>
                    {SETORES.map((s) => (
                      <SelectItem key={s} value={s}>{s}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Select value={form.regime} onValueChange={(v) => setForm({ ...form, regime: v })}>
                  <SelectTrigger className={selectTriggerClass}>
                    <SelectValue placeholder="Regime Tributário atual" />
                  </SelectTrigger>
                  <SelectContent>
                    {REGIMES.map((r) => (
                      <SelectItem key={r} value={r}>{r}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Select value={form.faturamento} onValueChange={(v) => setForm({ ...form, faturamento: v })}>
                  <SelectTrigger className={selectTriggerClass}>
                    <SelectValue placeholder="Faixa de faturamento mensal" />
                  </SelectTrigger>
                  <SelectContent>
                    {FAIXAS.map((f) => (
                      <SelectItem key={f} value={f}>{f}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <div className="flex gap-3 mt-2">
                  <Button
                    variant="heroOutline"
                    size="xl"
                    className="flex-1 group border-primary-foreground/20 text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
                    type="button"
                    onClick={prev}
                  >
                    <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
                    Voltar
                  </Button>
                  <Button variant="hero" size="xl" className="flex-1 group" type="button" onClick={next}>
                    Próximo
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </motion.div>
            )}

            {step === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -30 }}
                transition={{ duration: 0.25 }}
                className="space-y-4"
              >
                <p className="text-primary-foreground/70 text-sm font-semibold mb-2 text-left">
                  Passo 3: Identificação de Oportunidades
                </p>
                <p className="text-primary-foreground/40 text-xs text-left mb-3">
                  Selecione todas as situações que se aplicam à sua empresa:
                </p>

                <div className="space-y-3 text-left">
                  {SITUACOES.map((sit) => (
                    <label
                      key={sit.id}
                      className="flex items-start gap-3 p-3 rounded-xl bg-primary-foreground/5 border border-primary-foreground/10 hover:border-accent/40 transition-colors cursor-pointer"
                    >
                      <Checkbox
                        checked={form.situacoes.includes(sit.id)}
                        onCheckedChange={() => toggleSituacao(sit.id)}
                        className="mt-0.5 border-primary-foreground/30 data-[state=checked]:bg-accent data-[state=checked]:border-accent"
                      />
                      <span className="text-primary-foreground/80 text-sm leading-snug">
                        {sit.label}
                      </span>
                    </label>
                  ))}
                </div>

                <div className="flex gap-3 mt-2">
                  <Button
                    variant="heroOutline"
                    size="xl"
                    className="flex-1 group border-primary-foreground/20 text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
                    type="button"
                    onClick={prev}
                  >
                    <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
                    Voltar
                  </Button>
                  <Button variant="hero" size="xl" className="flex-1 group" type="submit" disabled={loading}>
                    {loading ? "Enviando..." : "Agendar Diagnóstico"}
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </form>
      </div>
    </section>
  );
};

export default ContactSection;
