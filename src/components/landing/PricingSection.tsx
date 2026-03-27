import { motion } from "framer-motion";
import { BadgeCheck } from "lucide-react";

const PricingSection = () => (
  <section className="py-20 px-5 bg-secondary">
    <div className="max-w-2xl mx-auto text-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="bg-background rounded-2xl p-8 md:p-12 shadow-sm border border-border"
      >
        <BadgeCheck className="w-12 h-12 text-accent mx-auto mb-4" />
        <h2 className="text-2xl md:text-3xl font-bold text-foreground">
          Você só paga se houver resultado
        </h2>
        <p className="mt-4 text-muted-foreground text-sm md:text-base max-w-md mx-auto">
          Na maioria dos casos, trabalhamos com modelo de êxito — você só paga um percentual sobre o valor efetivamente recuperado. Sem custo inicial, sem risco.
        </p>
      </motion.div>
    </div>
  </section>
);

export default PricingSection;
