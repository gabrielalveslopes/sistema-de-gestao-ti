print("Sistema de Gestão TI iniciado.")

from sqlalchemy import text

from config.database import engine


try:
    with engine.connect() as connection:
        resultado = connection.execute(
            text("SELECT current_database();")
        )

        banco = resultado.scalar()

        print("Conexão realizada com sucesso!")
        print(f"Banco conectado: {banco}")

except Exception as erro:
    print("Erro ao conectar ao banco:")
    print(erro)