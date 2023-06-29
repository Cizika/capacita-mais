from typing import Any, Dict
import oracledb
from datetime import datetime, timedelta
import re

from scripts import INSERT_PESSOA, INSERT_ALUNO, INSERT_FUNCAO, INSERT_ALUNO_GRUPO


# Função para validar o CPF do Aluno
def validate_cpf() -> str:
    while True:
        cpf = str(input("CPF (000.000.000-00): "))
        result = re.findall(r"^\d{3}\.\d{3}\.\d{3}\-\d{2}$", cpf)
        if not result:
            print("Digite um CPF válido!")
        else:
            return "".join(list(map(str, re.findall(r"\d+", result[0]))))


# Função para validar o E-mail do Aluno
def validate_email() -> str:
    while True:
        email = str(input("E-mail: "))
        result = re.findall(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email
        )
        if not result:
            print("Digite um e-mail válido!")
        else:
            return result[0]


# Função para validar data de nascimento no formato DD/MM/YYYY digitado
def validate_date() -> str:
    while True:
        date = str(input("Data de Nascimento (DD/MM/YYYY): "))
        result = re.findall(r"\d{1,2}\/\d{1,2}\/\d{2,4}", date)
        if not result:
            print("Digite a data no formato correto (DD/MM/YYYY)!")
        else:
            # Verificando se o aluno tem mais de 16 anos
            try:
                birthday = datetime.strptime(result[0], "%d/%m/%Y")
                if datetime.today() - birthday > timedelta(days=5845):
                    return result[0]
                else:
                    print("Aluno com idade inválida! (Mínimo de 16 anos)")
            except Exception as e:
                print("Digite a data no formato correto (DD/MM/YYYY)!")


# Função para coletar grupos que o Aluno pertence
def collect_grupos() -> list:
    while True:
        print(
            "O aluno se encaixa em quais desses grupos? (Selecione ao menos um grupo)"
        )
        print("- Mulheres\n- Idosos\n- LGBTQIAP\n- Refugiados")
        grupos = list(
            map(
                str,
                input("\nSeparado por espaços, digite os grupos correspondentes: ")
                .upper()
                .strip()
                .split(),
            )
        )
        if len(grupos) > 0:
            return grupos


# Função para coletar dados pessoais do aluno
def collect_aluno_data() -> Dict[str, Any]:
    print("Insira os seguintes dados do aluno: ")
    aluno_data = {}

    aluno_data["nome"] = str(input("Nome Completo: "))

    # Validando E-mail
    aluno_data["email"] = validate_email()

    # Validando CPF
    aluno_data["cpf"] = validate_cpf()

    # Validando Data de Nascimento
    aluno_data["data_nasc"] = validate_date()

    aluno_data["telefone"] = str(input("Telefone: "))
    aluno_data["logradouro"] = str(input("Logradouro (Rua, Avenida, Número...): "))
    aluno_data["bairro"] = str(input("Bairro: "))
    aluno_data["cidade"] = str(input("Cidade: "))
    aluno_data["cep"] = str(input("CEP: "))
    aluno_data["uf"] = str(input("UF: ")).upper()
    aluno_data["complemento"] = str(input("Complemento: "))
    aluno_data["escolaridade"] = str(input("Nível de Escolaridade: "))
    aluno_data["experiencia"] = str(input("Experiência Profissional: "))

    # Tratando Valores null
    for k in aluno_data.keys():
        if not aluno_data[k]:
            aluno_data[k] = None

    return aluno_data


# Função para inserir um Aluno no banco de dados
def insert_aluno(connection: oracledb.Connection):
    # Coletando dados do Aluno
    aluno_data: dict = collect_aluno_data()

    # Coletando informação dos grupos do Aluno
    grupos = collect_grupos()

    # Inicializando cursor
    try:
        with connection.cursor() as cursor:
            # Executando query de Insert na Tabela PESSOA
            cursor.execute(
                INSERT_PESSOA,
                cpf=aluno_data["cpf"],
                email=aluno_data["email"],
                nome=aluno_data["nome"],
                data_nasc=aluno_data["data_nasc"],
                telefone=aluno_data["telefone"],
                logradouro=aluno_data["logradouro"],
                bairro=aluno_data["bairro"],
                cidade=aluno_data["cidade"],
                cep=aluno_data["cep"],
                uf=aluno_data["uf"],
                complemento=aluno_data["complemento"],
            )

            # Executando query de Insert na Tabela ALUNO
            cursor.execute(
                INSERT_ALUNO,
                cpf=aluno_data["cpf"],
                escolaridade=aluno_data["escolaridade"],
                experiencia=aluno_data["experiencia"],
            )

            # Executando query de Insert na Tabela FUNCAO
            cursor.execute(INSERT_FUNCAO, cpf=aluno_data["cpf"])

            # Executando query de Insert na Tabela ALUNO_GRUPO
            for grupo in grupos:
                cursor.execute(INSERT_ALUNO_GRUPO, cpf=aluno_data["cpf"], grupo=grupo)

            # Commmitando mudanças
            connection.commit()
    except oracledb.IntegrityError as e:
        print("Erro de Integridade: ", e)
        connection.rollback()

    except Exception as e:
        print("Erro na inserção. Executando roll back!")
        print(f"Mensagem retornada: {e}")
        connection.rollback()
