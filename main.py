from config.database import SessionLocal
from models.departamento import Departamento

session = SessionLocal()

departamentos = session.query(Departamento).all()

for departamento in departamentos:
    print(departamento.id, departamento.nome)

session.close()