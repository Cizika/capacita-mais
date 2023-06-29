import oracledb
from aluno_insert import validate_email

from scripts import SELECT_ALUNO_BY_EMAIL, LIST_ALUNOS_BY_GRUPO, SELECT_GRUPO_BY_EMAIL


# Função para encontrar alunos por e-mail
def search_by_email(connection: oracledb.Connection):
    email = validate_email()
    with connection.cursor() as cursor:
        # Executando query de SELECT com email
        result = cursor.execute(SELECT_ALUNO_BY_EMAIL, email=email)
        alunos = [row for row in result]

        if alunos:
            aluno = alunos[0]
            print(f"Dados do Aluno encontrado!")
            print(f"Nome: {aluno[1]}")
            print(f"CPF: {aluno[2]}")
            print(f"Data de Nascimento: {aluno[3]:%d/%m/%Y}")
            print(f"Telefone: {aluno[4]}")
            print(f"Logradouro: {aluno[5]}")
            print(f"Bairro: {aluno[6]}")
            print(f"Cidade: {aluno[7]}")
            print(f"CEP: {aluno[8]}")
            print(f"UF: {aluno[9]}")
            print(f"Complemento: {aluno[10]}")

            grupos_aluno = cursor.execute(SELECT_GRUPO_BY_EMAIL, email=email)
            grupos = ", ".join([grupo[0] for grupo in grupos_aluno])
            print(f"Grupos: {grupos}")

        else:
            print("Nenhum aluno cadastrado com esse e-mail!")


# Função para encontrar alunos por e-mail
def list_alunos_by_grupo(connection: oracledb.Connection):
    grupo = str(input("Digite o Grupo de interesse: ")).upper()
    with connection.cursor() as cursor:
        # Executando query de SELECT para coletar alunos de um certo grupo
        result = cursor.execute(LIST_ALUNOS_BY_GRUPO, grupo=grupo)
        alunos = [row for row in result]

        if alunos:
            print(f"{len(alunos)} alunos encontrados!")
            for aluno in alunos:
                print(f"Nome: {aluno[0]}")
                print(f"CPF: {aluno[1]}")
        else:
            print("Grupo vazio ou não cadastrado!")
