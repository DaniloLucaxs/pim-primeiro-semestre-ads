import time # Importa o módulo time para medir o tempo de execução
import json # Importa o módulo json para manipulação de arquivos JSON
import re # Importa o módulo re para expressões regulares

from bcrypt import hashpw, checkpw, gensalt # Importa funções do bcrypt para hashing de senhas

from statistics import mean, median, mode, StatisticsError # Importa funções estatísticas
from pathlib import Path # Importa Path para manipulação de caminhos de arquivos

# Diretórios e arquivos JSON
BASE_DIR = Path(__file__).resolve().parent / "data"
USER_DATA_FILE = BASE_DIR / "users.json"
STATS_FILE = BASE_DIR / "statistics.json"
LOCATIONS_FILE = BASE_DIR / "locations.json"

def print_banner(text):
    """Imprime um banner centralizado no console."""
    print("\n" + "=" * 50)
    print(text.center(50))
    print("=" * 50)

def ensure_directory_exists(file_path):
    """Garante que o diretório do arquivo exista."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

def load_json(file_path, default_data):
    """Carrega dados de um arquivo JSON ou cria com dados padrão."""
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
    print(policies)
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
            role = "admin" if role == "sim" else "user"
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

def login():
    """Realiza o login do usuário."""
    print_banner("Login")
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    users_data = load_json(USER_DATA_FILE, {"users": []})
    for user in users_data["users"]:
        if user["username"] == username and checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
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
        print("\n" + question["question"])
        for option in question["options"]:
            print(option)
        answer = input("Sua resposta: ").strip().upper()
        while answer not in ["A", "B", "C", "D"]:
            print("❌ Opção inválida! Por favor, escolha entre A, B, C ou D.")
            answer = input("Sua resposta: ").strip().upper()
        if answer == question["correct"]:
            print("✅ Resposta correta!")
            correct_answers += 1
        else:
            print(f"❌ Resposta incorreta! A resposta correta era: {question['correct']}")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nVocê acertou {correct_answers} de {len(questions)} questões.")
    print(f"Tempo total: {elapsed_time:.2f} segundos.")

    stats = load_json(STATS_FILE, {})
    if username not in stats:
        stats[username] = {}
    if quiz_name not in stats[username]:
        stats[username][quiz_name] = {
            "total_time": 0,
            "attempts": 0,
            "correct_answers": 0,
            "average_time": 0
        }

    stats[username][quiz_name]["total_time"] += elapsed_time
    stats[username][quiz_name]["attempts"] += 1
    stats[username][quiz_name]["correct_answers"] += correct_answers
    stats[username][quiz_name]["average_time"] = stats[username][quiz_name]["total_time"] / stats[username][quiz_name]["attempts"]
    save_json(STATS_FILE, stats)

    print(f"Tempo médio para este quiz: {stats[username][quiz_name]['average_time']:.2f} segundos.")

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
    print("1. Pensamento Lógico Computacional")
    print("2. Segurança Digital e Cidadania Digital")
    print("3. Programação em Python")
    print("4. Fundamentos de Cibersegurança")
    print("5. Voltar ao menu principal")
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
            print("Voltando ao menu principal...\n")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

def calculate_statistics():
    """Calcula estatísticas de idade e localidades dos usuários."""
    users_data = load_json(USER_DATA_FILE, {"users": []})
    ages = [user["age"] for user in users_data["users"] if user["role"] == "user"]
    locations_data = load_json(LOCATIONS_FILE, {})

    if not ages:
        print("\nNenhum dado de idade disponível para cálculo.")
        return

    print_banner("Estatísticas de Idade dos Usuários")
    print(f"Média: {mean(ages):.2f} anos")
    print(f"Mediana: {median(ages):.2f} anos")
    try:
        print(f"Moda: {mode(ages)} anos")
    except StatisticsError:
        print("Moda: Não há uma moda única (valores repetidos).")

    print_banner("Levantamento de Localidades")
    for location, count in locations_data.items():
        print(f"{location}: {count} usuário(s)")

def show_user_menu(username):
    """Exibe o menu principal para usuários comuns."""
    while True:
        print_banner("Menu Principal")
        print("1. Escolher um curso")
        print("2. Ver estatísticas dos quizzes")
        print("3. Sair")
        choice = input("Escolha uma opção: ")
        if choice == "1":
            show_courses(username)
        elif choice == "2":
            stats = load_json(STATS_FILE, {})
            if username in stats:
                print_banner(f"Estatísticas dos Quizzes para {username}")
                for quiz, data in stats[username].items():
                    print(f"{quiz}:")
                    print(f"  - Tempo médio: {data['average_time']:.2f} segundos")
                    print(f"  - Tentativas: {data['attempts']}")
                    print(f"  - Respostas corretas: {data['correct_answers']}")
            else:
                print("\nNenhuma estatística disponível para este usuário.")
        elif choice == "3":
            print("Obrigado por usar a plataforma. Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

def show_admin_menu(username):
    """Exibe o menu principal para administradores."""
    while True:
        print_banner("Menu Principal (Administrador)")
        print("1. Escolher um curso")
        print("2. Ver estatísticas avançadas")
        print("3. Sair")
        choice = input("Escolha uma opção: ")
        if choice == "1":
            show_courses(username)
        elif choice == "2":
            calculate_statistics()
        elif choice == "3":
            print("Obrigado por usar a plataforma. Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

def main():
    """Função principal."""
    while True:
        print_banner("Bem-vindo à União Digital")
        print("1. Registrar-se")
        print("2. Login")
        print("3. Sair")
        choice = input("Escolha uma opção: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Obrigado por usar a plataforma. Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
