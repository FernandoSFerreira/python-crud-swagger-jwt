from models.user import User, db
from datetime import datetime

def create_user():
    # Verificar se já existe um usuário no banco de dados
    existing_user = User.query.filter_by(username='Ferreira').first()
    if existing_user:
        print("Usuário já existe no banco de dados.")
        return

    # Criar um novo usuário
    username = "Ferreira"
    password = "q1w2e3r4"
    user = User(username=username, password=password, created_at=datetime.now())

    # Adicionar o usuário ao banco de dados
    db.session.add(user)
    db.session.commit()

    print("Usuário criado com sucesso.")
