import os
import sys
import subprocess

def print_header(title):
    print("=" * 70)
    print(f" {title:^68}")
    print("=" * 70)

def run_command(cmd, desc):
    print(f"\n[*] Executando: {desc}...")
    try:
        res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if res.returncode == 0:
            print(f"[+] Sucesso: {desc}")
            return True, res.stdout
        else:
            print(f"[-] Status do comando '{desc}': {res.stderr.strip() or res.stdout.strip()}")
            return False, res.stderr or res.stdout
    except Exception as e:
        print(f"[!] Falha crítica ao rodar comando '{desc}': {str(e)}")
        return False, str(e)

def main():
    print_header("SCRIPT DE AUTOMACÃO GIT & DEPLOY VERCEL - MINICRIPT")
    
    # 1. Verificar se o Git está instalado
    git_installed, _ = run_command("git --version", "Verificação do Git")
    if not git_installed:
        print("\n[!] AVISO IMPORTANTE:")
        print("    O Git não foi detectado no PATH do seu sistema.")
        print("    Por favor, instale o Git: https://git-scm.com/downloads")
        sys.exit(1)
        
    # Copiar o favicon gerado do diretório da IA para o projeto do usuário
    src_favicon = r"C:\Users\Usuario\.gemini\antigravity\brain\5477bb17-6572-4c44-90f7-4ccb8fafcace\favicon_1779410231613.png"
    dest_favicon = os.path.join("uniateneulogo", "favicon.png")
    
    if os.path.exists(src_favicon):
        print(f"\n[*] Copiando favicon gerado de {src_favicon} para {dest_favicon}...")
        try:
            import shutil
            os.makedirs(os.path.dirname(dest_favicon), exist_ok=True)
            shutil.copy2(src_favicon, dest_favicon)
            print("[+] Favicon copiado com sucesso!")
        except Exception as e:
            print(f"[-] Erro ao copiar o favicon: {str(e)}")
            
    repo_url = "https://github.com/ScriptDev/Micripto.git"
    
    # 2. Inicializar repositório local se necessário
    if not os.path.exists(".git"):
        success, _ = run_command("git init", "Inicializar repositório Git local")
        if not success:
            sys.exit(1)
    else:
        print("\n[*] Repositório Git já está inicializado.")

    # 3. Configurar controle remoto (origin)
    _, remotes = run_command("git remote -v", "Verificar remotos cadastrados")
    if "origin" in remotes:
        success, _ = run_command(f"git remote set-url origin {repo_url}", f"Atualizar URL do remoto para {repo_url}")
    else:
        success, _ = run_command(f"git remote add origin {repo_url}", f"Adicionar remoto origin como {repo_url}")
        
    if not success:
        print("[-] Erro ao configurar remoto. Prosseguindo...")

    # 4. Ajustar branch para 'main'
    run_command("git branch -M main", "Configurar branch principal para 'main'")

    # 5. Adicionar arquivos modificados/novos
    run_command("git add .", "Adicionar arquivos modificados ao Stage (git add .)")

    # 6. Detectar modificações para Commitar
    _, status_out = run_command("git status --porcelain", "Verificar modificações pendentes")
    if not status_out.strip():
        print("\n[+] Nenhuma modificação pendente detectada no momento.")
    else:
        print("\n[!] Modificações detectadas prontas para commit.")
        print("--- Status dos arquivos ---")
        print(status_out.strip())
        print("---------------------------")
        
        # Define mensagem padrão de commit dependendo do estado do repo
        default_message = "fix: ajuste visual dos tooltips e otimização do card"
        print(f"\nMensagem de commit padrão: '{default_message}'")
        custom_message = input("Digite uma mensagem de commit personalizada (ou aperte ENTER para usar a padrão): ").strip()
        
        commit_msg = custom_message if custom_message else default_message
        success, _ = run_command(f'git commit -m "{commit_msg}"', f"Criar commit com mensagem: '{commit_msg}'")

    print("\n" + "=" * 70)
    print(" SINCRO E PREPARAÇÃO DO REPOSITÓRIO FINALIZADA")
    print("=" * 70)
    print(f"\nRepositório remoto: {repo_url}")
    print("Branch: main")
    print("\nComando recomendado de terminal para upload:")
    print("    >>>  git push -u origin main  <<<")
    
    # 7. Solicitar execução automática do Git Push
    decide = input("\nDeseja realizar o 'git push' agora? (S/N): ").strip().upper()
    if decide in ['S', 'SIM', 'Y', 'YES']:
        print("\n[*] Iniciando envio (push) para o GitHub...")
        print("[!] Nota: O Git pode solicitar login caso suas credenciais não estejam salvas.")
        
        try:
            # Executa com processo interativo herdando stdin/stdout para permitir prompts do terminal do usuário
            res = subprocess.run("git push -u origin main", shell=True)
            if res.returncode == 0:
                print("\n[+] PARABÉNS! Código enviado com sucesso ao repositório GitHub!")
                print("    Seu Vercel será atualizado automaticamente se o deploy contínuo estiver ativo.")
            else:
                print("\n[-] Falha ou cancelamento no git push. Tente rodar manualmente no terminal:")
                print("    git push -u origin main")
        except Exception as e:
            print(f"\n[-] Erro ao executar push automático: {str(e)}")
            print("    Por favor, execute manualmente: git push -u origin main")
    else:
        print("\n[*] Operação finalizada. Quando estiver pronto, execute no seu terminal:")
        print("    git push -u origin main")
        
    print("\n" + "=" * 70)
    print(" Ass: Samuel Mendes Cardoso - Software Factory Labs")
    print("=" * 70)

if __name__ == "__main__":
    main()
