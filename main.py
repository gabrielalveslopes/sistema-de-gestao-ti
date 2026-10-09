from config.database import SessionLocal
from services.movimentacao_service import MovimentacaoService


def main():
    session = SessionLocal()

    try:
        equipamento_id = 1

        historico = MovimentacaoService.consultar_historico(
            session=session,
            equipamento_id=equipamento_id
        )

        print("\n=== HISTÓRICO DO EQUIPAMENTO ===")

        if not historico:
            print("Nenhuma movimentação encontrada.")

        for registro in historico:
            print(f"\nMovimentação: {registro['movimentacao_id']}")
            print(f"Equipamento: {registro['equipamento']}")
            print(f"Funcionário: {registro['funcionario']}")
            print(f"Departamento: {registro['departamento']}")
            print(f"Entrega: {registro['data_entrega']}")
            print(f"Devolução: {registro['data_devolucao'] or 'Pendente'}")
            print(f"Situação: {registro['situacao']}")

        print("\n=== RESPONSÁVEIS ATUAIS ===")

        responsaveis = MovimentacaoService.consultar_responsaveis_atuais(
            session=session
        )

        for registro in responsaveis:
            print(f"\nEquipamento: {registro['equipamento']}")
            print(f"Série: {registro['numero_serie']}")
            print(f"Responsável: {registro['responsavel']}")
            print(f"Departamento: {registro['departamento']}")
            print(f"Status: {registro['status']}")

    except ValueError as erro:
        print(f"Erro: {erro}")

    finally:
        session.close()


if __name__ == "__main__":
    main()