🖥️ União Digital – Plataforma Educacional Interativa

União Digital é uma plataforma educacional desenvolvida em Python para console, que oferece quizzes e cursos interativos sobre:

- Pensamento Lógico Computacional
- Segurança Digital
- Programação em Python
- Fundamentos de Cibersegurança

O sistema permite registro de usuários, perfils diferenciados (usuário comum e administrador) e acompanhamento de estatísticas de desempenho, tornando o aprendizado interativo e seguro.

📂 Estrutura do Projeto
main.py                  → arquivo principal que roda o programa
README.md                → este arquivo
plataforma-digital/
└── fonte-src/
    └── data/
        ├── locations.json    → informações sobre localidades dos usuários
        ├── statistics.json   → desempenho dos quizzes
        └── users.json        → dados dos usuários cadastrados


Todos os dados são armazenados localmente em JSON, garantindo persistência e segurança.

⚙️ Funcionalidades
- Cadastro e Login de Usuários: com validação de senha forte usando bcrypt
- Quizzes Interativos: sobre lógica computacional, segurança digital, Python e cibersegurança
- Estatísticas de Desempenho: acompanhe resultados dos quizzes e dados demográficos (idade, localização)
- Perfis Diferenciados: menus e permissões distintos para usuários comuns e administradores
- Políticas de Privacidade e Segurança: exibidas ao usuário após o login

🏃 Como Executar – Passo a Passo

Siga estas instruções para rodar a plataforma em qualquer máquina.

1️⃣ Instalar Python
Caso não tenha, Baixe e instale Python 3.10 ou superior: https://www.python.org/downloads/
Durante a instalação, marque “Add Python to PATH”

2️⃣ Clonar o Repositório
Abra Git Bash ou PowerShell e digite:

git clone https://github.com/DaniloLucaxs/pim-primeiro-semestre-ads.git
cd pim-primeiro-semestre-ads

Isso baixa os arquivos do projeto e entra na pasta correta.

3️⃣ Criar e Ativar o Ambiente Virtual

Git Bash:

python -m venv .venv
source .venv/Scripts/activate

PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Você verá (.venv) no início do terminal se estiver ativo.

4️⃣ Instalar Dependências
pip install bcrypt

Este pacote protege senhas dos usuários com hashing seguro.

5️⃣ Executar a Plataforma
python main.py

O programa será executado no terminal/console.
Siga as instruções para cadastrar usuários, jogar quizzes e acessar estatísticas.

🗃️ Observações Importantes
- Os dados são armazenados localmente em arquivos JSON: users.json, statistics.json, locations.json
- Senhas são protegidas com hashing (bcrypt)
- Administradores têm acesso a menus e estatísticas avançadas
- Todos os quizzes e interações são 100% no modo console, não requer navegador ou GUI

📌 Dicas
- Sempre rode o ambiente virtual antes de executar o programa
- Não apague os arquivos JSON para não perder dados dos usuários
- Ideal para estudantes, professores e iniciantes em programação

📄 Licença

Este projeto é de uso acadêmico e educacional.

Desenvolvido por Danilo – União Digital
