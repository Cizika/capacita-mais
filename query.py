from dotenv import load_dotenv
import oracledb
import os

# Carregando variáveis de ambiente ao projeto
load_dotenv()

# Lendo variáveis de ambiente
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
service_name = os.getenv("SERVICE_NAME")
port = os.getenv("PORT")

# Parâmetros da conexão
params = oracledb.ConnectParams(host=host, port=port, service_name=service_name)

# Inicializando conexão
with oracledb.connect(user=username, password=password, params=params) as connection:
    # Inicializando cursor
    with connection.cursor() as cursor:

        # SQL select Query (DML)
        sql = """select * from Diretor"""
        for row in cursor.execute(sql):
            print(row)