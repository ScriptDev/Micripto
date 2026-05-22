# 🔐 MiniCript - Criptografia Aplicada ao Desenvolvimento

> Uma aplicação educacional interativa de alto impacto visual e arquitetura robusta, focada no ensino e demonstração prática de conceitos criptográficos fundamentais: Criptografia Simétrica (Rede de Feistel), Criptografia Assimétrica (RSA) e funções de Hash/Autenticação segura.

---

## 🚀 Demonstração & Deploy no Vercel

Esta aplicação está totalmente preparada para deploy na plataforma **Vercel** usando Serverless Functions do Python (`@vercel/python`).

### Arquivos de Configuração de Deploy incluídos:
* `vercel.json` - Define as rotas serverless mapeando todas as requisições HTTP para a aplicação Flask (`app.py`).
* `requirements.txt` - Gerencia as dependências requeridas (`Flask>=3.0.0`) para execução em ambiente de produção da nuvem.

---

## 🛠️ Tecnologias Utilizadas

* **Backend**: Python 3.x com framework **Flask** para construção das APIs de criptografia e roteamento de servidor.
* **Frontend**: HTML5, Vanilla CSS3 (Custom Properties/Design System Premium, animações de alta performance, layout responsivo) e JavaScript moderno (ES6+) para renderização reativa e interações em tempo real.
* **Estilização e Ícones**: Google Fonts (JetBrains Mono & Outfit) e Lucide Icons (via CDN).
* **Segurança e Algoritmos**: Implementação limpa de hashing com salting dinâmico, cifragem de Feistel e chaves RSA customizáveis.

---

## ⚙️ Funcionalidades Principais

1. **Autenticação com Hashing Educacional**:
   * Simulação visual de banco de dados em memória.
   * Visualização em tempo real de salt gerado e o hash resultante (demonstrando a resistência a ataques de dicionário).
   
2. **Criptografia Simétrica (Feistel)**:
   * Cifragem e decifragem de mensagens em texto com chaves personalizadas.
   * Logs detalhados de cada rodada da Rede de Feistel para fins educacionais.

3. **Criptografia Assimétrica (RSA)**:
   * Geração interativa de chaves públicas $(e, n)$ e privadas $(d, n)$ a partir de números primos $p$ e $q$.
   * Cifragem e decifragem de blocos numéricos RSA passo a passo.

4. **Painel de Logs (Live Terminal)**:
   * Um terminal estilizado que exibe o rastreamento técnico detalhado de todas as operações aritméticas executadas no backend.

---

## 💻 Como Executar Localmente

### Pré-requisitos:
* Python 3.8 ou superior instalado.
* Git instalado.

### Passo a Passo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/ScriptDev/Micripto.git
   cd Micripto
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicie o servidor local:
   ```bash
   python app.py
   ```

4. Acesse em seu navegador:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Estrutura do Projeto

```text
minicript/
│
├── core/                       # Regras de negócio e algoritmos criptográficos
│   ├── assimetria.py          # Implementação do algoritmo RSA
│   ├── hash.py                # Repositório de usuários, salting e hashing
│   └── simetria.py            # Estrutura da Rede de Feistel
│
├── templates/                  # Camada de apresentação (UI/UX)
│   └── index.html             # Interface gráfica moderna de alta fidelidade
│
├── app.py                      # Roteamento Flask e Endpoints de API
├── requirements.txt            # Dependências de execução
├── vercel.json                 # Configuração de infraestrutura Vercel
├── .gitignore                  # Arquivos ignorados pelo controle de versão
└── README.md                   # Documentação técnica oficial
```

---

## 💎 Excelência Arquitetural

* **SOLID & Clean Architecture**: Estrita separação de preocupações. A lógica criptográfica no diretório `core/` é 100% independente do framework HTTP Flask, facilitando testes unitários e manutenibilidade.
* **Premium UX/UI**: Tema escuro com design premium "cyberpunk/hacker", gradientes dinâmicos, micro-animações interativas e responsividade total para dispositivos móveis ou desktop.

---
Ass: Samuel Mendes Cardoso - Software Factory Labs
