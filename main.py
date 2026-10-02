from config.database import engine
from models.base import Base
import models


Base.metadata.create_all(bind=engine)

print("Estrutura do banco verificada com sucesso.")