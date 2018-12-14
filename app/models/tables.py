from app import db

class User(db.Model):
	__tablename__ = "users"
		
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(80), nullable=False)
	sobrenome = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_anoanymous(self):
		return True

	@property
	def is_active(self):
		return True

	def get_id(self):
		return str(self.id)

	def __init__(self,primeiroNome, segundoNome, email):
		self.nome = nome
		self.sobrenome = sobrenome
		self.email = email
		self.password = password


	def __repr__(self):
		return '<Email %r>' % self.email