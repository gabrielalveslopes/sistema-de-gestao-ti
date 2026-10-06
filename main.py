from config.database import SessionLocal
from models.funcionario import Funcionario


session = SessionLocal()

try:
    funcionarios = session.query(Funcionario).all()

    print("FUNCIONÁRIOS CADASTRADOS")
    print("------------------------")

    for funcionario in funcionarios:
        print(f"ID: {funcionario.id}")
        print(f"Nome: {funcionario.nome}")
        print(f"E-mail: {funcionario.email_institucional}")
        print(f"Departamento: {funcionario.departamento.nome}")
        print(f"Ativo: {funcionario.ativo}")
        print("------------------------")

finally:
    session.close()