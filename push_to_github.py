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
        # Run command capturing output
        res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if res.returncode == 0:
            print(f"[+] Sucesso: {desc}")
            if res.stdout:
                print(f"    Saída: {res.stdout.strip()}")
            return True, res.stdout
        else:
            print(f"[-] Erro em '{desc}': {res.stderr.strip()}")
            return False, res.stderr
    except Exception as e:
        print(f"[!] Falha crítica ao rodar comando '{desc}': {str(e)}")
        return False, str(e)

def main():
    print_header("SCRIPT DE INTEGRAÇÃO GIT E PREPARAÇÃO VERCEL - MINICRIPT")
    
    # 1. Verificar se o Git está instalado
    git_installed, out = run_command("git --version", "Verificação do Git instalado")
    if not git_installed:
        print("\n[!] AVISO IMPORTANTE:")
        print("    O Git não foi detectado no PATH do seu sistema ou não está instalado.")
        print("    Por favor, instale o Git antes de prosseguir:")
        print("    Download oficial: https://git-scm.com/downloads")
        sys.exit(1)
        
    # Repo URL fornecido
    repo_url = "https://github.com/ScriptDev/Micripto.git"
    
    # 2. Verificar se repositório git local já existe
    if not os.path.exists(".git"):
        success, _ = run_command("git init", "Inicializar repositório Git local")
        if not success:
            sys.exit(1)
    else:
        print("\n[*] Repositório Git já está inicializado localmente.")

    # 3. Configurar remoto 'origin'
    # Vamos verificar se o origin já existe
    _, remotes = run_command("git remote -v", "Verificar remotos cadastrados")
    if "origin" in remotes:
        # Atualiza a URL do origin
        success, _ = run_command(f"git remote set-url origin {repo_url}", f"Atualizar URL do remoto origin para {repo_url}")
    else:
        # Adiciona o origin
        success, _ = run_command(f"git remote add origin {repo_url}", f"Adicionar remoto origin apontando para {repo_url}")
        
    if not success:
        print("[-] Erro ao configurar o controle remoto do Git. Verifique a URL.")
        sys.exit(1)

    # 4. Criar branch padrão 'main'
    run_command("git branch -M main", "Definir branch principal como 'main'")

    # 5. Adicionar arquivos ao Stage
    success, _ = run_command("git add .", "Adicionar arquivos ao controle de versão (.git)")
    if not success:
        sys.exit(1)

    # 6. Criar Commit Inicial
    success, _ = run_command('git commit -m "feat: configuração de deploy Vercel, README.md e estrutura de arquivos"', "Criar commit local")
    if not success:
        print("[*] Nota: Caso não haja arquivos modificados/novos para commitar, este passo pode ser pulado.")

    print("\n" + "=" * 70)
    print(" CONFIGURAÇÃO LOCAL CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print(f"\nSeu repositório local está conectado a: {repo_url}")
    print("\nPara enviar os arquivos para o GitHub, execute o comando abaixo no seu terminal:")
    print("\n    >>>  git push -u origin main  <<<")
    print("\nAlternativamente, gostaria que eu tente fazer o push agora mesmo?")
    
    decide = input("Deseja realizar o 'git push' agora? (S/N): ").strip().upper()
    if decide in ['S', 'SIM', 'Y', 'YES']:
        print("\n[*] Tentando realizar o upload dos arquivos para o GitHub...")
        print("[!] Nota: Se esta for a primeira vez que você envia para este repositório,")
        print("    o Git pode abrir uma janela para você fazer login no GitHub no navegador.")
        
        # Executa de forma interativa para permitir prompts do git
        try:
            res = subprocess.run("git push -u origin main", shell=True)
            if res.returncode == 0:
                print("\n[+] SUCESSO ABSOLUTO! Seus códigos foram enviados ao GitHub!")
                print("    Agora você pode acessar a dashboard do Vercel (https://vercel.com)")
                print("    e importar o repositório 'Micripto' para publicar o seu site instantaneamente.")
            else:
                print("\n[-] Ocorreu um erro ou o envio foi cancelado/requer autenticação manual.")
                print("    Tente executar manualmente no seu terminal:")
                print("    git push -u origin main")
        except Exception as e:
            print(f"\n[-] Erro ao tentar push automático: {str(e)}")
            print("    Por favor, execute manualmente: git push -u origin main")
    else:
        print("\n[*] Operação finalizada. Quando estiver pronto, execute manualmente:")
        print("    git push -u origin main")
        
    print("\n" + "=" * 70)
    print(" Ass: Samuel Mendes Cardoso - Software Factory Labs")
    print("=" * 70)

if __name__ == "__main__":
    main()
