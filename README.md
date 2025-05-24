# União Digital

Este projeto é uma plataforma educacional interativa focada em cursos e quizzes sobre Pensamento Lógico Computacional, Segurança Digital, Programação em Python e Fundamentos de Cibersegurança.

## Estrutura do Projeto

```
main.py
README.md
├───plataforma-digital
│   └───fonte-src
│       └───data
│           ├── locations.json
│           ├── statistics.json
│           └── users.json

## Funcionalidades

- **Cadastro e Login de Usuários:** Com validação de senha forte e armazenamento seguro utilizando bcrypt.
- **Quizzes Interativos:** Sobre lógica computacional, segurança digital, Python e cibersegurança.
- **Estatísticas:** Geração de estatísticas de desempenho dos quizzes e dados dos usuários (idade, localização).
- **Perfis de Usuário:** Diferenciação entre usuários comuns e administradores, com menus e permissões distintas.
- **Políticas de Privacidade e Segurança:** Exibição das políticas ao usuário após o login.

## Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Instale as dependências necessárias:
   ```sh
   pip install bcrypt
   ```
3. Execute o arquivo principal:
   ```sh
   python main.py
   ```

## Sobre os Arquivos de Dados

- `users.json`: Armazena os dados dos usuários cadastrados.
- `statistics.json`: Guarda as estatísticas de desempenho nos quizzes.
- `locations.json`: Mantém o levantamento das localidades dos usuários.

## Observações

- Os dados são armazenados localmente em arquivos JSON.
- Senhas são protegidas por hashing (bcrypt).
- Administradores têm acesso a estatísticas avançadas.

## Licença

Este projeto é de uso acadêmico e educacional.

---
Desenvolvido por  Danilo e União Digital.
