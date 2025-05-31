import os  # Adicionado para limpeza de tela e centralização
import time # Importa o módulo time para medir o tempo de execução
import json # Importa o módulo json para manipulação de arquivos JSON
import re # Importa o módulo re para expressões regulares

from bcrypt import hashpw, checkpw, gensalt # Importa funções do bcrypt para hashing de senhas

from statistics import mean, median, mode, StatisticsError # Importa funções estatísticas
from pathlib import Path # Importa Path para manipulação de caminhos de arquivos

# Senha secreta para cadastro de administradores
ADMIN_SECRET = "02plataforma!"  # Altere para a senha desejada

# Diretórios e arquivos JSON
BASE_DIR = Path(__file__).resolve().parent / "data"
USER_DATA_FILE = BASE_DIR / "users.json"
STATS_FILE = BASE_DIR / "statistics.json"
LOCATIONS_FILE = BASE_DIR / "locations.json"
BASE_DIR.mkdir(parents=True, exist_ok=True)

def clear_screen():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(text):
    """Imprime um banner centralizado no console (horizontal e vertical)."""
    clear_screen()
    try:
        size = os.get_terminal_size()
        columns = size.columns
        lines = size.lines
    except OSError:
        columns = 80
        lines = 24

    banner_lines = [
        "",
        "=" * 50,
        text.center(50),
        "=" * 50
    ]
    total_banner_lines = len(banner_lines)
    empty_lines = max((lines - total_banner_lines) // 2, 0)
    print("\n" * empty_lines)
    for line in banner_lines:
        print(line.center(columns))

def ensure_directory_exists(file_path):
    """Garante que o diretório do arquivo exista."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

def load_json(file_path, default_data):
    """Carrega dados de um arquivo JSON ou cria com dados padrão."""
    print(f"[DEBUG] Carregando: {file_path}")  # Debug para ver onde está lendo
    ensure_directory_exists(file_path)
    if not file_path.exists():
        with file_path.open('w') as file:
            json.dump(default_data, file)
    with file_path.open('r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return default_data

def save_json(file_path, data):
    """Salva dados em um arquivo JSON."""
    print(f"[DEBUG] Salvando: {file_path}")  # Debug para ver onde está salvando
    with file_path.open('w') as file:
        json.dump(data, file, indent=4)

def is_valid_password(password):
    """Valida se a senha atende aos requisitos de segurança."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def show_policies():
    """Exibe as políticas do sistema no console."""
    print_banner("Políticas do Sistema")
    policies = """
=== Políticas do Sistema ===

1. **Política de Privacidade - União Digital**
   - Os dados coletados são utilizados exclusivamente para autenticação e personalização da experiência do usuário.
   - Coletamos apenas os dados necessários para o funcionamento da plataforma, como nome de usuário, senha, idade e localização.
   - Implementamos medidas técnicas para proteger os dados contra acessos não autorizados, incluindo criptografia e hashing de senhas.
   - Você pode solicitar acesso, correção ou exclusão de seus dados pessoais a qualquer momento.
   - Os dados serão armazenados apenas pelo tempo necessário para cumprir as finalidades declaradas.
   - Para dúvidas ou solicitações, entre em contato com nosso encarregado de proteção de dados (DPO) pelo e-mail: dpo@uniaodigital.com.

2. **Políticas de Segurança**
   - Senhas seguras são obrigatórias.
   - Dados são armazenados de forma segura e protegidos contra acessos não autorizados.
   - Todas as entradas do usuário são validadas para evitar erros e comportamentos inesperados.

3. **Políticas de Uso**
   - Ao usar o sistema, o usuário concorda com os termos de uso.
   - O uso indevido do sistema pode resultar em suspensão da conta.

4. **Termos de Uso**
   - Seus dados serão armazenados de forma segura e usados apenas para fins estatísticos.
   - Você é responsável por manter sua senha segura.
   - Administradores têm acesso a estatísticas gerais, mas não a dados pessoais.
   - O uso indevido do sistema pode resultar em suspensão da conta.
"""
    # Centraliza o texto das políticas horizontalmente
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    for line in policies.strip().split('\n'):
        print(line.center(columns))
    input("\nPressione Enter para continuar.")

def register():
    """Registra um novo usuário."""
    print_banner("Registro de Usuário")
    username = input("Escolha um nome de usuário: ")

    while True:
        password = input("Escolha uma senha (mínimo 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais): ")
        if is_valid_password(password):
            hashed_password = hashpw(password.encode('utf-8'), gensalt())
            break
        print("❌ Erro: A senha não atende aos requisitos de segurança. Tente novamente.\n")

    while True:
        try:
            age = int(input("Digite sua idade: "))
            if age <= 0:
                raise ValueError
            break
        except ValueError:
            print("❌ Erro: Idade inválida. Digite um número inteiro positivo.")

    location = input("Digite sua cidade/estado: ")

    while True:
        role = input("Você é um administrador? (sim/não): ").strip().lower()
        if role in ["sim", "não"]:
            if role == "sim":
                admin_pass = input("Digite a senha secreta de administrador: ")
                if admin_pass == ADMIN_SECRET:
                    role = "admin"
                else:
                    print("❌ Senha de administrador incorreta! Registrando como usuário comum.")
                    role = "user"
            else:
                role = "user"
            break
        print("❌ Opção inválida! Digite 'sim' ou 'não'.")

    users_data = load_json(USER_DATA_FILE, {"users": []})
    for user in users_data["users"]:
        if user["username"] == username:
            print("❌ Erro: Nome de usuário já existe. Tente novamente.\n")
            return

    users_data["users"].append({
        "username": username,
        "password": hashed_password.decode('utf-8'),
        "age": age,
        "location": location,
        "role": role
    })
    save_json(USER_DATA_FILE, users_data)

    locations_data = load_json(LOCATIONS_FILE, {})
    if location not in locations_data:
        locations_data[location] = 0
    locations_data[location] += 1
    save_json(LOCATIONS_FILE, locations_data)

    print(f"✅ Usuário {username} registrado com sucesso!\n")

def reset_password():
    """Permite ao usuário redefinir a senha caso esqueça."""
    print_banner("Recuperação de Senha")
    username = input("Digite seu nome de usuário: ")
    users_data = load_json(USER_DATA_FILE, {"users": []})
    for user in users_data["users"]:
        if user["username"] == username:
            # Pergunta a localização e idade como verificação simples
            location = input("Digite sua cidade/estado cadastrada: ")
            try:
                age = int(input("Digite sua idade cadastrada: "))
            except ValueError:
                print("❌ Idade inválida.")
                return
            if user["location"] == location and user["age"] == age:
                while True:
                    new_password = input("Digite a nova senha: ")
                    if is_valid_password(new_password):
                        user["password"] = hashpw(new_password.encode('utf-8'), gensalt()).decode('utf-8')
                        save_json(USER_DATA_FILE, users_data)
                        print("✅ Senha redefinida com sucesso!\n")
                        return
                    else:
                        print("❌ A senha não atende aos requisitos de segurança. Tente novamente.")
            else:
                print("❌ Dados de verificação incorretos. Não foi possível redefinir a senha.")
            return
    print("❌ Usuário não encontrado.")

def login():
    """Realiza o login do usuário."""
    print_banner("Login")
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    users_data = load_json(USER_DATA_FILE, {"users": []})
    for user in users_data["users"]:
        if user["username"] == username and checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            # Verificação extra para admin: pede senha secreta
            if user["role"] == "admin":
                admin_pass = input("Digite a senha secreta de administrador para acessar o painel admin: ")
                if admin_pass != ADMIN_SECRET:
                    print("❌ Senha de administrador incorreta! Acesso como usuário comum.")
                    show_user_menu(username)
                    return
            print(f"✅ Bem-vindo(a), {username}! Login realizado com sucesso.\n")
            show_policies()  # Exibe as políticas após o login
            if user["role"] == "admin":
                show_admin_menu(username)
            else:
                show_user_menu(username)
            return
    print("❌ Erro: Nome de usuário ou senha incorretos. Tente novamente.\n")

def run_quiz(questions, quiz_name, username):
    """Executa um quiz genérico."""
    correct_answers = 0
    start_time = time.time()

    for question in questions:
        print()
        try:
            columns = os.get_terminal_size().columns
        except OSError:
            columns = 80
        print(question["question"].center(columns))
        for option in question["options"]:
            print(option.center(columns))
        answer = input("Sua resposta: ").strip().upper()
        while answer not in ["A", "B", "C", "D"]:
            print("❌ Opção inválida! Por favor, escolha entre A, B, C ou D.".center(columns))
            answer = input("Sua resposta: ").strip().upper()
        if answer == question["correct"]:
            print("✅ Resposta correta!".center(columns))
            correct_answers += 1
        else:
            print(f"❌ Resposta incorreta! A resposta correta era: {question['correct']}".center(columns))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nVocê acertou {correct_answers} de {len(questions)} questões.".center(columns))
    print(f"Tempo total: {elapsed_time:.2f} segundos.".center(columns))

    # --- DEBUG: Mostra onde está salvando as estatísticas ---
    print(f"[DEBUG] Salvando estatísticas em: {STATS_FILE}")

    stats = load_json(STATS_FILE, {})
    username_key = username.strip()
    if username_key not in stats:
        stats[username_key] = {}
    if quiz_name not in stats[username_key]:
        stats[username_key][quiz_name] = {
            "total_time": 0,
            "attempts": 0,
            "correct_answers": 0,
            "average_time": 0
        }

    stats[username_key][quiz_name]["total_time"] += elapsed_time
    stats[username_key][quiz_name]["attempts"] += 1
    stats[username_key][quiz_name]["correct_answers"] += correct_answers
    stats[username_key][quiz_name]["average_time"] = (
        stats[username_key][quiz_name]["total_time"] / stats[username_key][quiz_name]["attempts"]
    )
    save_json(STATS_FILE, stats)

    print(f"Tempo médio para este quiz: {stats[username_key][quiz_name]['average_time']:.2f} segundos.".center(columns))

def logic_quiz(username):
    """Quiz de Pensamento Lógico Computacional."""
    questions = [
        {
            "question": "1️⃣ O que é o pensamento computacional?",
            "options": [
                "A) Um conjunto de regras para programar computadores.",
                "B) Uma estratégia para resolver problemas de forma eficiente, criando soluções genéricas.",
                "C) Uma técnica exclusiva para engenheiros de software.",
                "D) Um método para aprender apenas matemática avançada."
            ],
            "correct": "B"
        },
        {
            "question": "2️⃣ Quando o pensamento computacional deveria ser desenvolvido?",
            "options": [
                "A) Apenas na fase adulta, quando se aprende programação.",
                "B) Apenas por profissionais de tecnologia.",
                "C) Desde a infância, assim como outras disciplinas.",
                "D) Somente em cursos de ciência da computação."
            ],
            "correct": "C"
        },
        {
            "question": "3️⃣ O pensamento computacional está obrigatoriamente ligado ao ensino da programação?",
            "options": [
                "A) Sim, pois só pode ser aprendido escrevendo códigos.",
                "B) Não, pois é uma habilidade que pode ser desenvolvida sem programação.",
                "C) Sim, pois todas as soluções computacionais precisam de código.",
                "D) Não, pois só é útil em jogos e inteligência artificial."
            ],
            "correct": "B"
        }
    ]
    run_quiz(questions, "logic_quiz", username)

def digital_security_quiz(username):
    """Quiz de Segurança Digital e Cidadania Digital."""
    questions = [
        {
            "question": "1️⃣ O que é uma senha forte?",
            "options": [
                "A) Uma senha curta e fácil de lembrar.",
                "B) Uma senha longa, com letras, números e caracteres especiais.",
                "C) Uma senha que contém apenas números.",
                "D) Uma senha que é o nome do usuário."
            ],
            "correct": "B"
        },
        {
            "question": "2️⃣ Qual é a melhor prática para proteger suas contas online?",
            "options": [
                "A) Usar a mesma senha para todas as contas.",
                "B) Compartilhar sua senha com amigos de confiança.",
                "C) Ativar a autenticação de dois fatores.",
                "D) Escrever sua senha em um papel e deixá-lo visível."
            ],
            "correct": "C"
        },
        {
            "question": "3️⃣ O que é phishing?",
            "options": [
                "A) Um ataque que tenta enganar pessoas para obter informações confidenciais.",
                "B) Um software antivírus.",
                "C) Um método de criptografia.",
                "D) Um tipo de firewall."
            ],
            "correct": "A"
        }
    ]
    run_quiz(questions, "digital_security_quiz", username)

def python_programming_quiz(username):
    """Quiz de Programação em Python."""
    questions = [
        {
            "question": "1️⃣ Qual é a função usada para imprimir algo na tela em Python?",
            "options": [
                "A) print()",
                "B) echo()",
                "C) printf()",
                "D) output()"
            ],
            "correct": "A"
        },
        {
            "question": "2️⃣ Qual é o operador usado para exponenciação em Python?",
            "options": [
                "A) ^",
                "B) **",
                "C) //",
                "D) %%"
            ],
            "correct": "B"
        },
        {
            "question": "3️⃣ Qual é o tipo de dado retornado pela função input()?",
            "options": [
                "A) int",
                "B) str",
                "C) float",
                "D) bool"
            ],
            "correct": "B"
        }
    ]
    run_quiz(questions, "python_programming_quiz", username)

def cyber_quiz(username):
    """Quiz de Fundamentos de Cibersegurança."""
    questions = [
        {
            "question": "1️⃣ O que é um firewall?",
            "options": [
                "A) Um dispositivo que protege redes contra acessos não autorizados.",
                "B) Um software para editar imagens.",
                "C) Um tipo de vírus de computador.",
                "D) Uma ferramenta para criar senhas."
            ],
            "correct": "A"
        },
        {
            "question": "2️⃣ Qual é a prática de enganar pessoas para obter informações confidenciais?",
            "options": [
                "A) Phishing",
                "B) Malware",
                "C) Firewall",
                "D) Criptografia"
            ],
            "correct": "A"
        },
        {
            "question": "3️⃣ O que significa HTTPS?",
            "options": [
                "A) Protocolo de Transferência de Hipertexto Seguro",
                "B) Protocolo de Transferência de Arquivos",
                "C) Sistema de Proteção de Dados",
                "D) Rede de Segurança Avançada"
            ],
            "correct": "A"
        }
    ]
    run_quiz(questions, "cyber_quiz", username)

def show_courses(username):
    """Exibe as opções de cursos disponíveis."""
    print_banner("Cursos Disponíveis")
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    print("1. Pensamento Lógico Computacional".center(columns))
    print("2. Segurança Digital e Cidadania Digital".center(columns))
    print("3. Programação em Python".center(columns))
    print("4. Fundamentos de Cibersegurança".center(columns))
    print("5. Voltar ao menu principal".center(columns))
    while True:
        choice = input("Escolha um curso entre 1, 2, 3, 4 ou digite 5 para voltar: ")
        if choice == "1":
            logic_quiz(username)
        elif choice == "2":
            digital_security_quiz(username)
        elif choice == "3":
            python_programming_quiz(username)
        elif choice == "4":
            cyber_quiz(username)
        elif choice == "5":
            print("Voltando ao menu principal...\n".center(columns))
            break
        else:
            print("❌ Opção inválida! Tente novamente.".center(columns))

def show_all_quiz_statistics():
    """Exibe estatísticas de quizzes de todos os usuários para o administrador."""
    stats = load_json(STATS_FILE, {})
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    print_banner("Estatísticas dos Quizzes (Todos os Usuários)")
    if not stats:
        print("Nenhuma estatística de quiz disponível.".center(columns))
    else:
        for user, quizzes in stats.items():
            print(f"Usuário: {user}".center(columns))
            for quiz, data in quizzes.items():
                print(f"  {quiz}:".center(columns))
                print(f"    - Tempo médio: {data['average_time']:.2f} segundos".center(columns))
                print(f"    - Tentativas: {data['attempts']}".center(columns))
                print(f"    - Respostas corretas: {data['correct_answers']}".center(columns))
            print("-" * 40)
    input("\nPressione Enter para voltar ao menu.")

def show_all_users():
    """Exibe todos os usuários cadastrados (exceto senhas) para o administrador."""
    users_data = load_json(USER_DATA_FILE, {"users": []})
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    print_banner("Usuários Cadastrados")
    if not users_data["users"]:
        print("Nenhum usuário cadastrado.".center(columns))
    else:
        for user in users_data["users"]:
            print(f"Usuário: {user['username']}".center(columns))
            print(f"  Idade: {user['age']}".center(columns))
            print(f"  Localidade: {user['location']}".center(columns))
            print(f"  Perfil: {user['role']}".center(columns))
            print("-" * 40)
    input("\nPressione Enter para voltar ao menu.")

def show_locations():
    """Exibe levantamento de localidades dos usuários."""
    locations_data = load_json(LOCATIONS_FILE, {})
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    print_banner("Levantamento de Localidades")
    if not locations_data:
        print("Nenhuma localidade cadastrada.".center(columns))
    else:
        for location, count in locations_data.items():
            print(f"{location}: {count} usuário(s)".center(columns))
    input("\nPressione Enter para voltar ao menu.")

def show_admin_menu(username):
    """Exibe o menu principal para administradores."""
    while True:
        print_banner("Menu Principal (Administrador)")
        try:
            columns = os.get_terminal_size().columns
        except OSError:
            columns = 80
        print("1. Escolher um curso".center(columns))
        print("2. Estatísticas dos quizzes (todos os usuários)".center(columns))
        print("3. Estatísticas de usuários cadastrados".center(columns))
        print("4. Levantamento de localidades".center(columns))
        print("5. Sair".center(columns))
        choice = input("Escolha uma opção: ")
        if choice == "1":
            show_courses(username)
        elif choice == "2":
            show_all_quiz_statistics()
        elif choice == "3":
            show_all_users()
        elif choice == "4":
            show_locations()
        elif choice == "5":
            print("Obrigado por usar a plataforma. Até logo!".center(columns))
            break
        else:
            print("❌ Opção inválida! Tente novamente.".center(columns))

def show_user_menu(username):
    """Exibe o menu principal para usuários comuns."""
    while True:
        print_banner("Menu Principal")
        try:
            columns = os.get_terminal_size().columns
        except OSError:
            columns = 80
        print("1. Escolher um curso".center(columns))
        print("2. Ver estatísticas dos quizzes".center(columns))
        print("3. Sair".center(columns))
        choice = input("Escolha uma opção: ")
        if choice == "1":
            show_courses(username)
        elif choice == "2":
            stats = load_json(STATS_FILE, {})
            username_key = username.strip()
            if username_key in stats and stats[username_key]:
                print_banner(f"Estatísticas dos Quizzes para {username_key}")
                for quiz, data in stats[username_key].items():
                    print(f"{quiz}:".center(columns))
                    print(f"  - Tempo médio: {data['average_time']:.2f} segundos".center(columns))
                    print(f"  - Tentativas: {data['attempts']}".center(columns))
                    print(f"  - Respostas corretas: {data['correct_answers']}".center(columns))
                input("\nPressione Enter para voltar ao menu.")
            else:
                print("\nNenhuma estatística disponível para este usuário.".center(columns))
                input("\nPressione Enter para voltar ao menu.")
        elif choice == "3":
            print("Obrigado por usar a plataforma. Até logo!".center(columns))
            break
        else:
            print("❌ Opção inválida! Tente novamente.".center(columns))

def main():
    """Função principal."""
    while True:
        print_banner("Bem-vindo à União Digital")
        try:
            columns = os.get_terminal_size().columns
        except OSError:
            columns = 80
        print("1. Registrar-se".center(columns))
        print("2. Login".center(columns))
        print("3. Recuperar senha".center(columns))
        print("4. Sair".center(columns))
        choice = input("Escolha uma opção: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            reset_password()
        elif choice == "4":
            print("Obrigado por usar a plataforma. Até logo!".center(columns))
            break
        else:
            print("❌ Opção inválida! Tente novamente.".center(columns))

if __name__ == "__main__":
    main()
