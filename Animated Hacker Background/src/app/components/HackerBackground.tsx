import { useEffect, useRef, useState } from "react";

const CRYPTO_CHARS =
  "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF∑∏∫∂∇⊕⊗⊂⊃∈∉≡≈≠∧∨¬⊻";

const HEX_STRINGS = [
  "SHA-256: a3f8b2c1d4e9...",
  "AES-256-GCM",
  "RSA-4096",
  "0x7f3a9b2c4d1e",
  "ECDSA secp256k1",
  "PBKDF2-HMAC-SHA512",
  "0xdeadbeef",
  "TLS 1.3 handshake",
  "ChaCha20-Poly1305",
  "ED25519 keypair",
  "keccak256(data)",
  "secp384r1 curve",
  "blake2b-512",
  "argon2id hash",
  "x25519 DH",
];

interface FloatingTag {
  id: number;
  text: string;
  x: number;
  y: number;
  opacity: number;
  speed: number;
  color: string;
}

function MatrixCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    const fontSize = 14;
    let columns = Math.floor(canvas.width / fontSize);
    const drops: number[] = Array(columns).fill(1);

    let animId: number;

    const draw = () => {
      ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < drops.length; i++) {
        const char = CRYPTO_CHARS[Math.floor(Math.random() * CRYPTO_CHARS.length)];
        const x = i * fontSize;
        const y = drops[i] * fontSize;

        // Vary color: bright lead, medium body
        if (drops[i] * fontSize < canvas.height * 0.1 || Math.random() > 0.95) {
          ctx.fillStyle = "#ffffff";
          ctx.shadowColor = "#00ff41";
          ctx.shadowBlur = 8;
        } else if (Math.random() > 0.7) {
          ctx.fillStyle = "#00ff41";
          ctx.shadowColor = "#00ff41";
          ctx.shadowBlur = 4;
        } else {
          ctx.fillStyle = "#003b00";
          ctx.shadowBlur = 0;
        }

        ctx.font = `${fontSize}px monospace`;
        ctx.fillText(char, x, y);

        if (y > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }

      animId = requestAnimationFrame(draw);
    };

    draw();

    const handleResize = () => {
      resize();
      columns = Math.floor(canvas.width / fontSize);
      drops.length = 0;
      drops.push(...Array(columns).fill(1));
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full"
      style={{ display: "block" }}
    />
  );
}

function FloatingTags() {
  const [tags, setTags] = useState<FloatingTag[]>([]);

  useEffect(() => {
    const colors = ["#00ff41", "#00cc33", "#39ff14", "#7fff00", "#adff2f"];

    const initial: FloatingTag[] = Array.from({ length: 12 }, (_, i) => ({
      id: i,
      text: HEX_STRINGS[i % HEX_STRINGS.length],
      x: Math.random() * 90,
      y: Math.random() * 90,
      opacity: 0.3 + Math.random() * 0.5,
      speed: 0.01 + Math.random() * 0.02,
      color: colors[Math.floor(Math.random() * colors.length)],
    }));
    setTags(initial);

    let frame: number;
    let tick = 0;

    const animate = () => {
      tick++;
      if (tick % 2 === 0) {
        setTags((prev) =>
          prev.map((tag) => ({
            ...tag,
            y: tag.y - tag.speed > -5 ? tag.y - tag.speed : 105,
            opacity:
              Math.sin(tick * 0.02 + tag.id) * 0.25 + 0.5,
            text:
              tick % 180 === tag.id * 15
                ? HEX_STRINGS[Math.floor(Math.random() * HEX_STRINGS.length)]
                : tag.text,
          }))
        );
      }
      frame = requestAnimationFrame(animate);
    };

    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, []);

  return (
    <>
      {tags.map((tag) => (
        <div
          key={tag.id}
          className="absolute font-mono text-xs whitespace-nowrap pointer-events-none select-none"
          style={{
            left: `${tag.x}%`,
            top: `${tag.y}%`,
            color: tag.color,
            opacity: tag.opacity,
            textShadow: `0 0 8px ${tag.color}`,
            fontSize: "11px",
            letterSpacing: "0.05em",
          }}
        >
          {tag.text}
        </div>
      ))}
    </>
  );
}

function HexGrid() {
  return (
    <svg
      className="absolute inset-0 w-full h-full pointer-events-none"
      style={{ opacity: 0.04 }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <pattern
          id="hexPattern"
          x="0"
          y="0"
          width="60"
          height="52"
          patternUnits="userSpaceOnUse"
        >
          <polygon
            points="30,2 58,17 58,47 30,62 2,47 2,17"
            fill="none"
            stroke="#00ff41"
            strokeWidth="0.8"
          />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#hexPattern)" />
    </svg>
  );
}

function ScanLine() {
  return (
    <div
      className="absolute inset-0 pointer-events-none"
      style={{
        background:
          "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,65,0.015) 2px, rgba(0,255,65,0.015) 4px)",
      }}
    />
  );
}

function GlowOrbs() {
  return (
    <>
      <div
        className="absolute rounded-full pointer-events-none"
        style={{
          width: 600,
          height: 600,
          top: "-10%",
          left: "-10%",
          background: "radial-gradient(circle, rgba(0,255,65,0.06) 0%, transparent 70%)",
          animation: "pulse-orb 6s ease-in-out infinite",
        }}
      />
      <div
        className="absolute rounded-full pointer-events-none"
        style={{
          width: 500,
          height: 500,
          bottom: "-5%",
          right: "-5%",
          background: "radial-gradient(circle, rgba(0,204,51,0.07) 0%, transparent 70%)",
          animation: "pulse-orb 8s ease-in-out infinite reverse",
        }}
      />
      <div
        className="absolute rounded-full pointer-events-none"
        style={{
          width: 400,
          height: 400,
          top: "40%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          background: "radial-gradient(circle, rgba(57,255,20,0.04) 0%, transparent 70%)",
          animation: "pulse-orb 10s ease-in-out infinite",
        }}
      />
    </>
  );
}

function CryptoHashDisplay() {
  const [hashes, setHashes] = useState<string[]>([]);

  useEffect(() => {
    const generateHash = () =>
      Array.from({ length: 64 }, () =>
        "0123456789abcdef"[Math.floor(Math.random() * 16)]
      ).join("");

    setHashes(Array.from({ length: 6 }, generateHash));

    const interval = setInterval(() => {
      setHashes((prev) => {
        const next = [...prev];
        const idx = Math.floor(Math.random() * next.length);
        next[idx] = generateHash();
        return next;
      });
    }, 800);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-6 left-6 pointer-events-none select-none">
      {hashes.map((hash, i) => (
        <div
          key={i}
          className="font-mono text-xs mb-1"
          style={{
            color: "rgba(0,255,65,0.35)",
            fontSize: "10px",
            letterSpacing: "0.08em",
            textShadow: "0 0 4px rgba(0,255,65,0.3)",
            transition: "all 0.3s ease",
          }}
        >
          {hash}
        </div>
      ))}
    </div>
  );
}

function CircuitLines() {
  return (
    <svg
      className="absolute inset-0 w-full h-full pointer-events-none"
      style={{ opacity: 0.07 }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <line x1="0" y1="30%" x2="15%" y2="30%" stroke="#00ff41" strokeWidth="1" />
      <line x1="15%" y1="30%" x2="15%" y2="60%" stroke="#00ff41" strokeWidth="1" />
      <line x1="15%" y1="60%" x2="35%" y2="60%" stroke="#00ff41" strokeWidth="1" />
      <circle cx="15%" cy="30%" r="3" fill="#00ff41" />
      <circle cx="35%" cy="60%" r="3" fill="#00ff41" />

      <line x1="100%" y1="20%" x2="85%" y2="20%" stroke="#00ff41" strokeWidth="1" />
      <line x1="85%" y1="20%" x2="85%" y2="45%" stroke="#00ff41" strokeWidth="1" />
      <line x1="85%" y1="45%" x2="65%" y2="45%" stroke="#00ff41" strokeWidth="1" />
      <circle cx="85%" cy="20%" r="3" fill="#00ff41" />
      <circle cx="65%" cy="45%" r="3" fill="#00ff41" />

      <line x1="0" y1="75%" x2="20%" y2="75%" stroke="#00ff41" strokeWidth="1" />
      <line x1="20%" y1="75%" x2="20%" y2="85%" stroke="#00ff41" strokeWidth="1" />
      <line x1="20%" y1="85%" x2="50%" y2="85%" stroke="#00ff41" strokeWidth="1" />
      <circle cx="20%" cy="75%" r="3" fill="#00ff41" />
      <circle cx="50%" cy="85%" r="3" fill="#00ff41" />

      <line x1="100%" y1="70%" x2="80%" y2="70%" stroke="#00ff41" strokeWidth="1" />
      <line x1="80%" y1="70%" x2="80%" y2="90%" stroke="#00ff41" strokeWidth="1" />
      <circle cx="80%" cy="70%" r="3" fill="#00ff41" />
    </svg>
  );
}

export function HackerBackground({ children }: { children?: React.ReactNode }) {
  return (
    <div
      className="relative w-full h-full overflow-hidden"
      style={{ background: "#000000" }}
    >
      <style>{`
        @keyframes pulse-orb {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.15); opacity: 0.7; }
        }
      `}</style>

      <MatrixCanvas />
      <HexGrid />
      <GlowOrbs />
      <CircuitLines />
      <ScanLine />
      <FloatingTags />
      <CryptoHashDisplay />

      {children && (
        <div className="relative z-10 w-full h-full flex items-center justify-center">
          {children}
        </div>
      )}
    </div>
  );
}
