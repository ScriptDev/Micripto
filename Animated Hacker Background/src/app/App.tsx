import { useState, useEffect } from "react";
import { HackerBackground } from "./components/HackerBackground";
import { Shield, Lock, Key, Cpu, Globe, Eye, EyeOff } from "lucide-react";

const TYPING_TEXTS = [
  "Protegendo dados com AES-256...",
  "Gerando par de chaves RSA-4096...",
  "Verificando assinatura ECDSA...",
  "Handshake TLS 1.3 completo...",
  "Hash SHA-256 validado...",
  "Criptografia end-to-end ativa...",
];

function TypingText() {
  const [displayText, setDisplayText] = useState("");
  const [phraseIndex, setPhraseIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const current = TYPING_TEXTS[phraseIndex];
    const timeout = setTimeout(
      () => {
        if (!deleting) {
          setDisplayText(current.slice(0, charIndex + 1));
          if (charIndex + 1 === current.length) {
            setTimeout(() => setDeleting(true), 1800);
          } else {
            setCharIndex((c) => c + 1);
          }
        } else {
          setDisplayText(current.slice(0, charIndex - 1));
          if (charIndex - 1 === 0) {
            setDeleting(false);
            setCharIndex(0);
            setPhraseIndex((p) => (p + 1) % TYPING_TEXTS.length);
          } else {
            setCharIndex((c) => c - 1);
          }
        }
      },
      deleting ? 40 : 70
    );
    return () => clearTimeout(timeout);
  }, [charIndex, deleting, phraseIndex]);

  return (
    <span
      className="font-mono"
      style={{ color: "#00ff41", textShadow: "0 0 10px #00ff41" }}
    >
      {displayText}
      <span
        style={{
          borderRight: "2px solid #00ff41",
          marginLeft: 2,
          animation: "blink 1s step-end infinite",
        }}
      />
    </span>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
}) {
  return (
    <div
      className="flex flex-col items-center gap-2 px-6 py-4 rounded-lg"
      style={{
        background: "rgba(0,255,65,0.04)",
        border: "1px solid rgba(0,255,65,0.2)",
        backdropFilter: "blur(8px)",
      }}
    >
      <Icon size={20} style={{ color: "#00ff41", filter: "drop-shadow(0 0 6px #00ff41)" }} />
      <span className="font-mono text-xs" style={{ color: "rgba(0,255,65,0.6)" }}>
        {label}
      </span>
      <span
        className="font-mono font-bold text-sm"
        style={{ color: "#00ff41", textShadow: "0 0 8px #00ff41" }}
      >
        {value}
      </span>
    </div>
  );
}

function LiveCounter() {
  const [count, setCount] = useState(8473921);
  useEffect(() => {
    const i = setInterval(
      () => setCount((c) => c + Math.floor(Math.random() * 3 + 1)),
      600
    );
    return () => clearInterval(i);
  }, []);
  return (
    <span style={{ color: "#00ff41", fontVariantNumeric: "tabular-nums" }}>
      {count.toLocaleString("pt-BR")}
    </span>
  );
}

function EncryptDemo() {
  const [visible, setVisible] = useState(false);
  const plain = "mensagem secreta 🔐";
  const encrypted = "U2FsdGVkX1/3mK9xQv7zBpW+L4nRJc0iE8hTdAyFqG==";

  return (
    <div
      className="w-full max-w-md rounded-lg overflow-hidden"
      style={{
        border: "1px solid rgba(0,255,65,0.25)",
        background: "rgba(0,0,0,0.7)",
        backdropFilter: "blur(12px)",
      }}
    >
      <div
        className="flex items-center gap-2 px-4 py-2"
        style={{ background: "rgba(0,255,65,0.08)", borderBottom: "1px solid rgba(0,255,65,0.15)" }}
      >
        <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ff5f56" }} />
        <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ffbd2e" }} />
        <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#27c93f" }} />
        <span className="font-mono text-xs ml-2" style={{ color: "rgba(0,255,65,0.5)" }}>
          crypto-terminal
        </span>
      </div>
      <div className="p-4 space-y-3">
        <div className="space-y-1">
          <span className="font-mono text-xs" style={{ color: "rgba(0,255,65,0.5)" }}>
            $ plaintext:
          </span>
          <div
            className="font-mono text-sm px-3 py-2 rounded"
            style={{
              background: "rgba(0,255,65,0.06)",
              color: visible ? "#00ff41" : "transparent",
              textShadow: visible ? "0 0 8px #00ff41" : "none",
              userSelect: "none",
              transition: "all 0.3s",
              border: "1px solid rgba(0,255,65,0.1)",
              filter: visible ? "none" : "blur(6px)",
            }}
          >
            {plain}
          </div>
        </div>
        <div className="space-y-1">
          <span className="font-mono text-xs" style={{ color: "rgba(0,255,65,0.5)" }}>
            $ AES-256-GCM(plaintext):
          </span>
          <div
            className="font-mono text-xs px-3 py-2 rounded break-all"
            style={{
              background: "rgba(0,255,65,0.06)",
              color: "#00cc33",
              border: "1px solid rgba(0,255,65,0.1)",
              letterSpacing: "0.05em",
            }}
          >
            {encrypted}
          </div>
        </div>
        <button
          onClick={() => setVisible((v) => !v)}
          className="w-full flex items-center justify-center gap-2 py-2 rounded font-mono text-xs transition-all"
          style={{
            background: "rgba(0,255,65,0.1)",
            border: "1px solid rgba(0,255,65,0.3)",
            color: "#00ff41",
            cursor: "pointer",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.background = "rgba(0,255,65,0.2)")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.background = "rgba(0,255,65,0.1)")
          }
        >
          {visible ? <EyeOff size={14} /> : <Eye size={14} />}
          {visible ? "ocultar mensagem" : "revelar mensagem"}
        </button>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <div className="w-screen h-screen">
      <style>{`
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(24px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .fade-in-up { animation: fade-in-up 0.8s ease forwards; }
        .delay-1 { animation-delay: 0.2s; opacity: 0; }
        .delay-2 { animation-delay: 0.5s; opacity: 0; }
        .delay-3 { animation-delay: 0.8s; opacity: 0; }
        .delay-4 { animation-delay: 1.1s; opacity: 0; }
      `}</style>

      <HackerBackground>
        <div className="flex flex-col items-center text-center px-6 gap-8 max-w-3xl w-full">
          {/* Logo / ícone */}
          <div
            className="fade-in-up flex items-center justify-center w-20 h-20 rounded-full"
            style={{
              background: "rgba(0,255,65,0.07)",
              border: "2px solid rgba(0,255,65,0.4)",
              boxShadow: "0 0 40px rgba(0,255,65,0.2), inset 0 0 20px rgba(0,255,65,0.05)",
            }}
          >
            <Shield
              size={36}
              style={{ color: "#00ff41", filter: "drop-shadow(0 0 12px #00ff41)" }}
            />
          </div>

          {/* Título */}
          <div className="fade-in-up delay-1 space-y-3">
            <h1
              className="font-mono tracking-widest uppercase"
              style={{
                fontSize: "clamp(1.8rem, 5vw, 3.2rem)",
                color: "#00ff41",
                textShadow: "0 0 20px rgba(0,255,65,0.8), 0 0 60px rgba(0,255,65,0.3)",
                letterSpacing: "0.15em",
              }}
            >
              CryptoShield
            </h1>
            <p
              className="font-mono text-sm tracking-wider"
              style={{ color: "rgba(0,255,65,0.55)", letterSpacing: "0.2em" }}
            >
              SEGURANÇA. PRIVACIDADE. CRIPTOGRAFIA.
            </p>
          </div>

          {/* Typing text */}
          <div className="fade-in-up delay-2 font-mono text-sm min-h-6">
            <TypingText />
          </div>

          {/* Demo interativo */}
          <div className="fade-in-up delay-3 w-full flex justify-center">
            <EncryptDemo />
          </div>

          {/* Stats */}
          <div className="fade-in-up delay-4 grid grid-cols-2 sm:grid-cols-4 gap-3 w-full">
            <StatCard icon={Lock} label="Algoritmos" value="AES · RSA · ECC" />
            <StatCard icon={Key} label="Chaves geradas" value="∞" />
            <StatCard
              icon={Cpu}
              label="Operações"
              value={<LiveCounter /> as unknown as string}
            />
            <StatCard icon={Globe} label="Padrão" value="FIPS 140-3" />
          </div>
        </div>
      </HackerBackground>
    </div>
  );
}
