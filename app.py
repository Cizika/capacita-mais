from dotenv import load_dotenv
import oracledb
import os

from aluno_insert import insert_aluno
from aluno_select import list_alunos_by_grupo, search_by_email

# Carregando variáveis de ambiente ao projeto
load_dotenv()

# Lendo variáveis de ambiente
username: str = os.getenv("USERNAME")
password: str = os.getenv("PASSWORD")
host: str = os.getenv("HOST")
service_name: str = os.getenv("SERVICE_NAME")
port: str = os.getenv("PORT")


# Inicializando conexão com o banco
def connect_db() -> oracledb.Connection:
    # Configurando parâmetros de conexão do banco
    params = oracledb.ConnectParams(host=host, port=port, service_name=service_name)

    try:
        # Estabelecendo conexão com o banco
        connection = oracledb.connect(user=username, password=password, params=params)
        return connection
    except oracledb.OperationalError:
        print(
            "Não foi possível realizar a conexão com o banco (Verifique a VPN da USP)"
        )

def main():
    print("--------------------------------------------------")
    print("Seja bem vinde à versão beta do Capacita Mais!")

    print("Estabelecendo conexão com o Banco...")
    connection = connect_db()

    while True and connection:
        print("--------------------------------------------------")
        print("1. Cadastrar novo Aluno")
        print("2. Pesquisar alunos pelo E-mail")
        print("3. Listar alunos por Grupo")
        print("0. Finalizar programa")

        option = str(input("\nDigite a opção desejada: "))
        print("--------------------------------------------------")

        try:
            if option == "0":
                print("Encerrando conexão com o banco...")
                connection.close()
                print("Até mais!")
                break
            elif option == "1":
                # Criando novo Aluno na Base
                insert_aluno(connection)
            elif option == "2":
                # Procurando Aluno por e-mail
                search_by_email(connection)
            elif option == "3":
                # Listando alunos por grupo
                list_alunos_by_grupo(connection)
            else:
                print("\nOpção inválida! Digite um dos números presentes no menu.")
        except Exception as e:
            print("Erro inesperado. Encerrando conexão...")
            print(f"Mensagem do erro: {e}")
            connection.rollback()
            connection.close()
            break


if __name__ == "__main__":
    main()
