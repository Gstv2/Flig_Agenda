# models/estabelecimentos.py
from config import supabase

class Estabelecimento(db.Model):
    __tablename__ = 'estabelecimentos'

    id = Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    @staticmethod
    def listar_todos():
        return Estabelecimento.query.all()