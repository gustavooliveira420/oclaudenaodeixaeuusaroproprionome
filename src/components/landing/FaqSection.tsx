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
  <section className="py-20 px-5 bg-secondary">
    <div className="max-w-2xl mx-auto">
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-2xl md:text-3xl font-bold text-foreground text-center"
      >
        Perguntas frequentes
      </motion.h2>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.1 }}
        className="mt-10"
      >
        <Accordion type="single" collapsible className="space-y-3">
          {faqs.map((f, i) => (
            <AccordionItem
              key={i}
              value={`faq-${i}`}
              className="bg-background rounded-xl border border-border px-5"
            >
              <AccordionTrigger className="text-left text-sm md:text-base font-medium text-foreground hover:no-underline">
                {f.q}
              </AccordionTrigger>
              <AccordionContent className="text-sm text-muted-foreground">
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
