"""
    Primeiro programa de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM

"""
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class Cliente(Base):
    """
        Esta classe representa a tabela cliente dentro
        do SQlite.
    """
    __tablename__ = "cliente"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    address = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, cpf={self.cpf}, {self.address})"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(2))
    agencia = Column(Integer)
    numero = Column(Integer)
    saldo = Column(Float)

    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)

    def __repr__(self):
        return f"Account(id={self.id}, tipo={self.tipo}, saldo={self.balance})"


print(Cliente.__tablename__)
print(Conta.__tablename__)

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)


with Session(engine) as session:
    jose = Cliente(name='Jose Silva',
                  cpf = '1234567811',
                  address='Rua 98, numero 23'
                  )

    camila = Cliente(name='Camila braga',
                    cpf='12345678900',
                    address='Rua 45, numero 10'
                    )

    leonardo = Cliente(name='Leonardo Souto',
                      cpf='12345678945',
                      address='Rua 78, numero 34'
                      )

    account1 = Conta(client_id='1',
                       tipo='cc',
                       agency=1001,
                       number=10001,
                       balance=5000
                       )
    account2 = Conta(client_id='2',
                       tipo='cp',
                       agency=1001,
                       number=20001,
                       balance=15000
                       )
    account3 = Conta(client_id='3',
                       tipo='cc',
                       agency=1001,
                       number=10002,
                       balance=1000
                       )

    session.add_all(([jose, camila, leonardo]))
    session.add_all([account1, account2, account3])
    session.commit()


print("\nRecuperando clientes de maneira ordenada:")
stmt_order = select(Cliente).order_by(Cliente.name.desc())
for result in session.scalars(stmt_order):
    print(result)


print("\nRecuperando contas e clientes:")
stmt_join = select(Cliente.name, Conta.tipo, Conta.balance).join_from(Cliente, Conta)
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
for result in results:
    print(result)

session.close()

