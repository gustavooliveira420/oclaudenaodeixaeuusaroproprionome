import { MessageCircle } from "lucide-react";

const WhatsAppButton = () => (
  <a
    href="https://wa.me/5511986539933"
    target="_blank"
    rel="noopener noreferrer"
    className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-[#25D366] hover:bg-[#20BA5A] rounded-full flex items-center justify-center shadow-lg hover:shadow-xl transition-all hover:-translate-y-0.5 ring-2 ring-prime-gold/0 hover:ring-prime-gold/40"
    aria-label="Falar pelo WhatsApp"
  >
    <MessageCircle className="w-7 h-7 text-white" />
  </a>
);

export default WhatsAppButton;
