import { cn } from "@/lib/utils";

type LogoVariant = "light" | "dark" | "mono-light" | "mono-dark";

interface LogoProps {
  variant?: LogoVariant;
  showWordmark?: boolean;
  showTagline?: boolean;
  className?: string;
}

/**
 * Logo Renegocia Consultoria Prime — reconstruído em SVG inline a partir
 * do manual de marca. Substituir por SVG oficial do designer quando disponível.
 *
 * Mark: "R" estilizada com perna formada por trapézio dourado (alude a prédio
 * em ascensão). Wordmark: RENEGOCIA + "Consultoria Prime" + "Tributário".
 */
const Logo = ({
  variant = "light",
  showWordmark = true,
  showTagline = true,
  className,
}: LogoProps) => {
  // Cores conforme o variant
  const isLight = variant === "light" || variant === "mono-light";
  const isMono = variant === "mono-light" || variant === "mono-dark";

  const rColor = isLight ? "#FFFFFF" : "#0F2F2A";
  const goldColor = isMono ? rColor : "#D4AF37";
  const wordmarkColor = isLight ? "#FFFFFF" : "#0F2F2A";
  const primeColor = isMono ? wordmarkColor : "#D4AF37";
  const taglineColor = isMono ? wordmarkColor : "#16B98A";

  return (
    <div className={cn("flex items-center gap-3", className)}>
      {/* Mark — "R" + prédio dourado */}
      <svg
        viewBox="0 0 100 100"
        className="h-10 w-10 shrink-0 md:h-12 md:w-12"
        aria-hidden="true"
      >
        {/* Trapézio dourado (perna esquerda do R, alusão a prédio) */}
        <path
          d="M 18 26 L 32 26 L 38 78 L 18 78 Z"
          fill={goldColor}
        />
        {/* Letra R principal */}
        <path
          d="M 32 16 L 64 16 Q 82 16 82 36 Q 82 52 66 56 L 84 84 L 70 84 L 54 58 L 46 58 L 46 84 L 32 84 Z M 46 28 L 46 46 L 62 46 Q 70 46 70 37 Q 70 28 62 28 Z"
          fill={rColor}
        />
      </svg>

      {showWordmark && (
        <div className="flex flex-col leading-none">
          <span
            className="font-bold tracking-tight text-lg md:text-xl"
            style={{ color: wordmarkColor }}
          >
            RENEGOCIA
          </span>
          <span
            className="text-[10px] md:text-xs font-semibold tracking-[0.18em] mt-0.5"
            style={{ color: wordmarkColor }}
          >
            CONSULTORIA{" "}
            <span style={{ color: primeColor }}>PRIME</span>
          </span>
          {showTagline && (
            <span
              className="text-[9px] md:text-[10px] font-semibold tracking-[0.2em] mt-0.5"
              style={{ color: taglineColor }}
            >
              TRIBUTÁRIO
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default Logo;
