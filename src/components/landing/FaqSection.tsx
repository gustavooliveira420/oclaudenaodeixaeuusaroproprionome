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
    a: "Não. Nosso trabalho é complementar ao da contabilidade. Atuamos na esfera estratégica e tributária, sem interferir na rotina contábil da sua empresa.",
  },
  {
    q: "Quanto tempo leva o processo?",
    a: "O diagnóstico inicial leva de 7 a 15 dias. A recuperação de créditos pode variar de 60 a 180 dias para vias administrativas e de 12 a 36 meses para vias judiciais, dependendo da tese e do volume de dados.",
  },
  {
    q: "Existe algum risco?",
    a: "Não. Todas as estratégias são baseadas em legislação vigente e jurisprudência consolidada (STF/STJ). Não utilizamos atalhos nem interpretações agressivas.",
  },
  {
    q: "Minha empresa se enquadra?",
    a: "Empresas em Lucro Presumido ou Lucro Real são as que mais se beneficiam. Empresas no Simples Nacional em crescimento também podem ter ganho com planejamento de regime. O diagnóstico gratuito confirma se há oportunidades específicas para o seu CNPJ.",
  },
];

const FaqSection = () => (
  <section className="py-24 px-4 md:px-6 bg-white">
    <div className="max-w-3xl mx-auto">
      <div className="text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="flex items-center justify-center gap-3 mb-4"
        >
          <span className="h-px w-10 bg-prime-green" />
          <span className="text-prime-green text-xs font-semibold tracking-[0.2em] uppercase">
            Dúvidas
          </span>
          <span className="h-px w-10 bg-prime-green" />
        </motion.div>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-2xl md:text-4xl font-black uppercase tracking-tight text-prime-dark"
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
              className="bg-prime-light rounded-2xl border border-prime-dark/10 px-6 data-[state=open]:border-prime-gold/50 data-[state=open]:bg-prime-light data-[state=open]:shadow-md transition-all"
            >
              <AccordionTrigger className="text-left text-sm md:text-base font-bold text-prime-dark hover:no-underline py-5">
                {f.q}
              </AccordionTrigger>
              <AccordionContent className="text-sm text-prime-black/70 pb-5 leading-relaxed">
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
