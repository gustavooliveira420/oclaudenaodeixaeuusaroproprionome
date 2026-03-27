import { motion } from "framer-motion";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    q: "Preciso trocar de contador?",
    a: "Não. Nosso trabalho é complementar ao da contabilidade. Atuamos na esfera jurídica e estratégica, sem interferir na rotina contábil da sua empresa.",
  },
  {
    q: "Quanto tempo leva o processo?",
    a: "O diagnóstico inicial leva de 7 a 15 dias. A recuperação de créditos pode variar de 60 a 180 dias, dependendo da complexidade e do volume de dados.",
  },
  {
    q: "Existe algum risco?",
    a: "Não. Todas as estratégias são baseadas em legislação vigente e jurisprudência consolidada. Não utilizamos atalhos ou interpretações agressivas.",
  },
  {
    q: "Minha empresa se enquadra?",
    a: "Empresas no Lucro Presumido, Lucro Real ou Simples Nacional em crescimento podem se beneficiar. O diagnóstico gratuito confirma se há oportunidades para o seu caso.",
  },
];

const FaqSection = () => (
  <section className="py-24 px-6 bg-card">
    <div className="max-w-2xl mx-auto">
      <div className="text-center">
        <motion.span
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-accent text-sm font-semibold tracking-widest uppercase"
        >
          Dúvidas
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="mt-4 text-2xl md:text-4xl font-bold text-foreground"
        >
          Perguntas frequentes
        </motion.h2>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2 }}
        className="mt-12"
      >
        <Accordion type="single" collapsible className="space-y-3">
          {faqs.map((f, i) => (
            <AccordionItem
              key={i}
              value={`faq-${i}`}
              className="bg-background rounded-2xl border border-border px-6 data-[state=open]:border-accent/30 transition-colors"
            >
              <AccordionTrigger className="text-left text-sm md:text-base font-semibold text-foreground hover:no-underline py-5">
                {f.q}
              </AccordionTrigger>
              <AccordionContent className="text-sm text-muted-foreground pb-5 leading-relaxed">
                {f.a}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </motion.div>
    </div>
  </section>
);

export default FaqSection;
