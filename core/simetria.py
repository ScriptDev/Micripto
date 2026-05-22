class CifraSimetricaEducacional:
    @staticmethod
    def s_box(x: int) -> int:
        return (x * 9 + 13) % 256

    @staticmethod
    def derivar_chaves_rodada(chave_mestra: str) -> list[int]:
        if not chave_mestra:
            chave_mestra = "CHAVE_PADRAO"
            
        soma_chave = sum(ord(c) for c in chave_mestra)
        
        k0 = soma_chave % 256
        k1 = (soma_chave * 3 + 17) % 256
        k2 = (soma_chave * 7 + 43) % 256
        k3 = (soma_chave * 13 + 97) % 256
        
        return [k0, k1, k2, k3]

    @classmethod
    def cifrar(cls, texto_puro: str, chave_mestra: str) -> tuple[str, list[str]]:
        logs = []
        logs.append(f"1. Preparação da Cifra Feistel:")
        logs.append(f"   Chave Mestra: '{chave_mestra}'")
        
        chaves_rodada = cls.derivar_chaves_rodada(chave_mestra)
        logs.append(f"   Chaves de Rodada derivadas:")
        for r, k in enumerate(chaves_rodada):
            logs.append(f"     Subchave K{r} = {k} (0x{k:02X})")

        texto_ajustado = texto_puro
        if len(texto_puro) % 2 != 0:
            texto_ajustado += " "
            logs.append(f"   Preenchimento (Padding): Texto de entrada ímpar. Adicionado caractere de espaço. Texto final: '{texto_ajustado}'")
        else:
            logs.append(f"   Texto de entrada de tamanho par: '{texto_ajustado}'")

        bytes_cifrados = []
        logs.append("\n2. Processamento dos blocos de 2 bytes (16 bits):")

        for idx_bloco in range(0, len(texto_ajustado), 2):
            char_l = texto_ajustado[idx_bloco]
            char_r = texto_ajustado[idx_bloco + 1]
            
            L0 = ord(char_l)
            R0 = ord(char_r)
            
            logs.append(f"\n   Bloco [{idx_bloco // 2}]: '{char_l}{char_r}' -> ASCII: (L0: {L0}, R0: {R0})")
            
            F0 = cls.s_box(R0 ^ chaves_rodada[0])
            L1 = R0
            R1 = L0 ^ F0
            logs.append(f"     Rodada 0 (Subchave K0 = {chaves_rodada[0]}):")
            logs.append(f"       F(R0, K0) = S-Box(R0 ^ K0) = S-Box({R0} ^ {chaves_rodada[0]}) = S-Box({R0 ^ chaves_rodada[0]}) = {F0}")
            logs.append(f"       L1 = R0 = {L1}")
            logs.append(f"       R1 = L0 ^ F(R0, K0) = {L0} ^ {F0} = {R1}")
            
            F1 = cls.s_box(R1 ^ chaves_rodada[1])
            L2 = R1
            R2 = L1 ^ F1
            logs.append(f"     Rodada 1 (Subchave K1 = {chaves_rodada[1]}):")
            logs.append(f"       F(R1, K1) = {F1}")
            logs.append(f"       L2 = {L2} | R2 = {R2}")

            F2 = cls.s_box(R2 ^ chaves_rodada[2])
            L3 = R2
            R3 = L2 ^ F2
            logs.append(f"     Rodada 2 (Subchave K2 = {chaves_rodada[2]}):")
            logs.append(f"       F(R2, K2) = {F2}")
            logs.append(f"       L3 = {L3} | R3 = {R3}")

            F3 = cls.s_box(R3 ^ chaves_rodada[3])
            L4 = R3
            R4 = L3 ^ F3
            logs.append(f"     Rodada 3 (Subchave K3 = {chaves_rodada[3]}):")
            logs.append(f"       F(R3, K3) = {F3}")
            logs.append(f"       Resultado do Bloco -> L4: {L4}, R4: {R4}")
            
            bytes_cifrados.extend([L4, R4])

        texto_cifrado_hex = "".join(f"{b:02x}" for b in bytes_cifrados)
        logs.append(f"\n3. Resultado Cifrado Final (Hexadecimal):")
        logs.append(f"   {texto_cifrado_hex}")
        
        return texto_cifrado_hex, logs

    @classmethod
    def decifrar(cls, texto_cifrado_hex: str, chave_mestra: str) -> tuple[str, list[str]]:
        logs = []
        logs.append(f"1. Preparação da Decifragem Feistel:")
        logs.append(f"   Chave Mestra: '{chave_mestra}'")
        
        chaves_rodada = cls.derivar_chaves_rodada(chave_mestra)
        logs.append(f"   Chaves de Rodada (Ordem Inversa para Decifragem):")
        for r in range(3, -1, -1):
            logs.append(f"     Subchave K{r} = {chaves_rodada[r]} (0x{chaves_rodada[r]:02X})")

        try:
            bytes_cifrados = [int(texto_cifrado_hex[i:i+2], 16) for i in range(0, len(texto_cifrado_hex), 2)]
        except Exception:
            return "", ["Erro: Texto hexadecimal inválido para decifrar."]

        caracteres_decriptados = []
        logs.append("\n2. Processamento dos blocos cifrados (Ordem Inversa das Operações):")

        for idx_bloco in range(0, len(bytes_cifrados), 2):
            L4 = bytes_cifrados[idx_bloco]
            R4 = bytes_cifrados[idx_bloco + 1]
            
            logs.append(f"\n   Bloco [{idx_bloco // 2}]: Hex (L4: 0x{L4:02X}, R4: 0x{R4:02X}) -> Inteiros: ({L4}, {R4})")
            
            F3 = cls.s_box(L4 ^ chaves_rodada[3])
            R3 = L4
            L3 = R4 ^ F3
            logs.append(f"     Desfazendo Rodada 3 (K3 = {chaves_rodada[3]}):")
            logs.append(f"       F(L4, K3) = S-Box({L4} ^ {chaves_rodada[3]}) = {F3}")
            logs.append(f"       L3 = R4 ^ F(L4, K3) = {R4} ^ {F3} = {L3}")
            logs.append(f"       R3 = L4 = {R3}")

            F2 = cls.s_box(L3 ^ chaves_rodada[2])
            R2 = L3
            L2 = R3 ^ F2
            logs.append(f"     Desfazendo Rodada 2 (K2 = {chaves_rodada[2]}):")
            logs.append(f"       F(L3, K2) = {F2}")
            logs.append(f"       L2 = {L2} | R2 = {R2}")

            F1 = cls.s_box(L2 ^ chaves_rodada[1])
            R1 = L2
            L1 = R2 ^ F1
            logs.append(f"     Desfazendo Rodada 1 (K1 = {chaves_rodada[1]}):")
            logs.append(f"       F(L2, K1) = {F1}")
            logs.append(f"       L1 = {L1} | R1 = {R1}")

            F0 = cls.s_box(L1 ^ chaves_rodada[0])
            R0 = L1
            L0 = R1 ^ F0
            logs.append(f"     Desfazendo Rodada 0 (K0 = {chaves_rodada[0]}):")
            logs.append(f"       F(L1, K0) = {F0}")
            logs.append(f"       L0 (Original) = R1 ^ F(L1, K0) = {R1} ^ {F0} = {L0}")
            logs.append(f"       R0 (Original) = L1 = {R0}")

            caracteres_decriptados.extend([chr(L0), chr(R0)])

        texto_decifrado = "".join(caracteres_decriptados)
        logs.append(f"\n3. Resultado Decifrado Final:")
        logs.append(f"   '{texto_decifrado}'")
        
        return texto_decifrado, logs
