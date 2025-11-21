from .. import db

class Funcionario(db.Model):
    __tablename__ = 'funcionario'

    cpf_pk = db.Column(db.String(20), primary_key=True)
    sk_email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Funcionario {self.cpf_pk}>'
