from config.database import SessionLocal
from services.departamento_service import DepartamentoService


session = SessionLocal()

try:
    departamentos = DepartamentoService.listar(session)

    print("Departamentos cadastrados:")

    for departamento in departamentos:
        print(
            f"{departamento.id} - {departamento.nome}"
        )

finally:
    session.close()