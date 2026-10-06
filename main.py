from config.database import SessionLocal
from services.equipamento_service import EquipamentoService


session = SessionLocal()

try:
    equipamento = EquipamentoService.criar(
        session=session,
        numero_serie="SN-002",
        nome_maquina="NOTE-TI-002",
        fabricante="Lenovo",
        modelo="ThinkPad E14",
        tipo_aquisicao="ALUGADO",
        fornecedor="Simpress"
    )

    print("Equipamento cadastrado com sucesso!")
    print(f"ID: {equipamento.id}")
    print(f"Número de série: {equipamento.numero_serie}")
    print(f"Nome da máquina: {equipamento.nome_maquina}")
    print(f"Fabricante: {equipamento.fabricante}")
    print(f"Modelo: {equipamento.modelo}")
    print(f"Tipo: {equipamento.tipo_aquisicao}")

    if equipamento.tipo_aquisicao == "ALUGADO":
        print(f"Fornecedor: {equipamento.fornecedor}")
    else:
        print("Origem: Equipamento próprio")

    print(f"Status: {equipamento.status}")
    print(f"Ativo: {equipamento.ativo}")

except ValueError as erro:
    print(f"Erro: {erro}")

finally:
    session.close()