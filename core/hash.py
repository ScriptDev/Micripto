import os
import random
import string

class HashEducacional:
    @staticmethod
    def gerar_sal(tamanho: int = 8) -> str:
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(tamanho))

    @staticmethod
    def hash_senha(senha: str, sal: str) -> tuple[str, list[str]]:
        logs = []
        senha_com_sal = senha + sal
        logs.append(f"1. Preparação: Senha original = '{senha}', Sal = '{sal}'")
        logs.append(f"2. Concatenação (Senha + Sal) = '{senha_com_sal}'")

        A = 0x67452301
        B = 0xEFCDAB89
        C = 0x98BADCFE
        D = 0x10325476
        
        logs.append(f"3. Inicialização do Estado de Registros:")
        logs.append(f"   A = 0x{A:08X} ({A})")
        logs.append(f"   B = 0x{B:08X} ({B})")
        logs.append(f"   C = 0x{C:08X} ({C})")
        logs.append(f"   D = 0x{D:08X} ({D})")

        logs.append("4. Processamento caractere por caractere:")
        
        for idx, caractere in enumerate(senha_com_sal):
            char_ascii = ord(caractere)
            A_anterior, B_anterior, C_anterior, D_anterior = A, B, C, D
            
            A = (A + (char_ascii * 31)) & 0xFFFFFFFF
            B = (B ^ ((A << 3) | (A >> 29))) & 0xFFFFFFFF
            C = (C + B - char_ascii) & 0xFFFFFFFF
            D = (D ^ (C >> 2)) & 0xFFFFFFFF
            
            log_etapa = (
                f"   [{idx + 1}] Caractere '{caractere}' (ASCII: {char_ascii}):\n"
                f"       A = (A_ant + {char_ascii}*31) mod 2^32 => 0x{A_anterior:08X} -> 0x{A:08X}\n"
                f"       B = (B_ant ^ rot(A, 3)) mod 2^32     => 0x{B_anterior:08X} -> 0x{B:08X}\n"
                f"       C = (C_ant + B - {char_ascii}) mod 2^32     => 0x{C_anterior:08X} -> 0x{C:08X}\n"
                f"       D = (D_ant ^ (C >> 2)) mod 2^32      => 0x{D_anterior:08X} -> 0x{D:08X}"
            )
            logs.append(log_etapa)

        hash_final = f"{A:08x}{B:08x}{C:08x}{D:08x}"
        logs.append(f"5. Finalização: Concatenação dos estados [A][B][C][D] para formar o Hash de 128 bits:")
        logs.append(f"   Resultado = {hash_final}")
        
        return hash_final, logs


class RepositorioUsuarios:
    def __init__(self):
        self._banco_dados = {}

    def cadastrar(self, usuario: str, senha: str) -> tuple[bool, str, list[str]]:
        if not usuario or not senha:
            return False, "Usuário ou senha não podem ser vazios.", []
            
        usuario = usuario.strip().lower()
        if usuario in self._banco_dados:
            return False, f"Usuário '{usuario}' já está cadastrado no sistema.", []

        sal = HashEducacional.gerar_sal()
        hash_valor, logs = HashEducacional.hash_senha(senha, sal)
        
        self._banco_dados[usuario] = {
            "sal": sal,
            "hash": hash_valor
        }
        
        return True, f"Usuário '{usuario}' cadastrado com sucesso!", logs

    def autenticar(self, usuario: str, senha: str) -> tuple[bool, str, list[str]]:
        if not usuario or not senha:
            return False, "Campos de usuário e senha são obrigatórios.", []

        usuario = usuario.strip().lower()
        if usuario not in self._banco_dados:
            return False, f"Usuário '{usuario}' não encontrado no banco de dados.", [
                f"Erro: Tentativa de login para usuário inexistente: '{usuario}'"
            ]

        registro_usuario = self._banco_dados[usuario]
        sal_armazenado = registro_usuario["sal"]
        hash_armazenado = registro_usuario["hash"]
        
        logs = []
        logs.append(f"1. Busca no Banco: Registro encontrado para o usuário '{usuario}'")
        logs.append(f"   Sal (Salt) recuperado: '{sal_armazenado}'")
        logs.append(f"   Hash de referência armazenado: {hash_armazenado}")
        
        logs.append("2. Processo de Recálculo do Hash:")
        hash_gerado, logs_hash = HashEducacional.hash_senha(senha, sal_armazenado)
        logs.extend(logs_hash)

        logs.append("3. Comparação de Hashes:")
        logs.append(f"   Hash recalculado: {hash_gerado}")
        logs.append(f"   Hash armazenado:  {hash_armazenado}")

        if hash_gerado == hash_armazenado:
            logs.append("   [SUCESSO] Hashes são IDENTICOS! Login autorizado.")
            return True, "Login realizado com sucesso! Acesso concedido.", logs
        else:
            logs.append("   [FALHA] Hashes NÃO conferem! Acesso negado.")
            return False, "Senha incorreta. Acesso negado.", logs

    def obter_lista_usuarios(self) -> list[dict]:
        return [
            {"username": k, "salt": v["sal"], "hash": v["hash"]} 
            for k, v in self._banco_dados.items()
        ]
