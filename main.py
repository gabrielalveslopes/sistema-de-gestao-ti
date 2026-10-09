from config.database import SessionLocal
from services.movimentacao_service import MovimentacaoService


def main():

    session = SessionLocal()

    try:
        movimentacao_id = MovimentacaoService.registrar_entrega(
            session=session,
            funcionario_id=1,
            equipamento_id=1
        )

        print("Entrega registrada com sucesso!")
        print(f"Movimentação ID: {movimentacao_id}")

    except ValueError as erro:
        print(f"Erro: {erro}")

    finally:
        session.close()


if __name__ == "__main__":
    main()