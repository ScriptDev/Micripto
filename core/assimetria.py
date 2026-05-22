class CifraAssimetricaEducacional:
    @staticmethod
    def e_primo(numero: int) -> bool:
        if numero < 2:
            return False
        for i in range(2, int(numero ** 0.5) + 1):
            if numero % i == 0:
                return False
        return True

    @staticmethod
    def mdc(a: int, b: int) -> int:
        while b != 0:
            a, b = b, a % b
        return a

    @classmethod
    def euclides_estendido(cls, a: int, b: int) -> tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        g, x1, y1 = cls.euclides_estendido(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

    @classmethod
    def inverso_modular(cls, e: int, phi: int) -> int:
        g, x, y = cls.euclides_estendido(e, phi)
        if g != 1:
            raise ValueError("O inverso modular não existe pois e e phi não são coprimos.")
        else:
            return x % phi

    @classmethod
    def gerar_chaves(cls, p: int, q: int) -> tuple[dict, list[str]]:
        logs = []
        logs.append(f"1. Geração de Chaves RSA:")
        logs.append(f"   Primos escolhidos: p = {p}, q = {q}")
        
        if not cls.e_primo(p):
            raise ValueError(f"O número p ({p}) não é primo!")
        if not cls.e_primo(q):
            raise ValueError(f"O número q ({q}) não é primo!")
        if p == q:
            raise ValueError("Os números p e q devem ser diferentes para segurança!")

        n = p * q
        logs.append(f"   [Módulo n] n = p * q = {p} * {q} = {n}")
        
        phi = (p - 1) * (q - 1)
        logs.append(f"   [Totiente de Euler] phi(n) = (p-1)*(q-1) = {p-1} * {q-1} = {phi}")

        common_es = [3, 5, 7, 11, 13, 17, 257, 65537]
        e = None
        for candidate in common_es:
            if candidate < phi and cls.mdc(candidate, phi) == 1:
                e = candidate
                break
        
        if e is None:
            for candidate in range(3, phi, 2):
                if cls.mdc(candidate, phi) == 1:
                    e = candidate
                    break
        
        if e is None:
            raise ValueError("Não foi possível encontrar um expoente público 'e' válido.")
            
        logs.append(f"   [Expoente Público e] Escolhido e = {e} (MDC({e}, {phi}) == 1)")

        d = cls.inverso_modular(e, phi)
        logs.append(f"   [Expoente Privado d] d = e^-1 mod phi(n) = {e}^-1 mod {phi} = {d}")
        logs.append(f"   [Verificação] (d * e) % phi(n) => ({d} * {e}) % {phi} = {(d*e)%phi}")
        
        chaves = {
            "p": p,
            "q": q,
            "n": n,
            "phi": phi,
            "e": e,
            "d": d,
            "public_key": (e, n),
            "private_key": (d, n)
        }
        
        logs.append("\n2. Chaves Geradas com Sucesso:")
        logs.append(f"   CHAVE PÚBLICA (e, n)  = ({e}, {n})")
        logs.append(f"   CHAVE PRIVADA (d, n) = ({d}, {n})")
        
        return chaves, logs

    @staticmethod
    def cifrar(mensagem: str, e: int, n: int) -> tuple[list[int], list[str]]:
        logs = []
        logs.append(f"1. Cifragem RSA da mensagem: '{mensagem}'")
        logs.append(f"   Usando Chave Pública: e = {e}, n = {n}")
        logs.append("   Fórmula: C = M^e mod n\n")
        
        texto_cifrado = []
        for idx, char in enumerate(mensagem):
            m = ord(char)
            if m >= n:
                logs.append(f"   [AVISO] Caractere '{char}' (ASCII {m}) é maior ou igual ao módulo n ({n}).")
                logs.append(f"   Isso pode causar perdas na decodificação. Recomenda-se usar primos maiores.")
            
            c = pow(m, e, n)
            texto_cifrado.append(c)
            logs.append(f"   Caractere [{idx}]: '{char}' (ASCII: {m})")
            logs.append(f"     C = {m}^{e} mod {n} = {c}")
            
        logs.append(f"\n2. Cifragem Concluída!")
        logs.append(f"   Vetor de Inteiros Cifrados: {texto_cifrado}")
        return texto_cifrado, logs

    @staticmethod
    def decifrar(texto_cifrado: list[int], d: int, n: int) -> tuple[str, list[str]]:
        logs = []
        logs.append(f"1. Decifragem RSA do vetor: {texto_cifrado}")
        logs.append(f"   Usando Chave Privada: d = {d}, n = {n}")
        logs.append("   Fórmula: M = C^d mod n\n")
        
        caracteres_decifrados = []
        for idx, c in enumerate(texto_cifrado):
            m = pow(c, d, n)
            char = chr(m) if m < 1114112 else '?'
            caracteres_decifrados.append(char)
            logs.append(f"   Valor Cifrado [{idx}]: {c}")
            logs.append(f"     M = {c}^{d} mod {n} = {m} -> Caractere: '{char}'")
            
        mensagem_decifrada = "".join(caracteres_decifrados)
        logs.append(f"\n2. Decifragem Concluída!")
        logs.append(f"   Mensagem Recuperada: '{mensagem_decifrada}'")
        return mensagem_decifrada, logs
