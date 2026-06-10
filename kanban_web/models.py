from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Conta(Base):
    __tablename__ = "contas"

    email = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)

    quadros = relationship("Quadro", back_populates="dono", cascade="all, delete-orphan")
    membros = relationship("QuadroMembro", back_populates="usuario", cascade="all, delete-orphan")


class Quadro(Base):
    __tablename__ = "quadros"

    codigo = Column(String(4), primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    limite_wip = Column(Integer, nullable=False, default=10)
    status = Column(String, nullable=False, default="A FAZER")
    email_dono = Column(String, ForeignKey("contas.email"), nullable=False)

    dono = relationship("Conta", back_populates="quadros")
    raias = relationship("Raia", back_populates="quadro", cascade="all, delete-orphan")
    cartoes = relationship("Cartao", back_populates="quadro", cascade="all, delete-orphan")
    membros = relationship("QuadroMembro", back_populates="quadro", cascade="all, delete-orphan")


class QuadroMembro(Base):
    __tablename__ = "quadro_membros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_quadro = Column(String(4), ForeignKey("quadros.codigo"), nullable=False)
    email_usuario = Column(String, ForeignKey("contas.email"), nullable=False)
    papel = Column(String, nullable=False, default="MEMBRO")  # DONO | MEMBRO

    __table_args__ = (UniqueConstraint("codigo_quadro", "email_usuario", name="uq_quadro_membro"),)

    quadro = relationship("Quadro", back_populates="membros")
    usuario = relationship("Conta", back_populates="membros")


class Raia(Base):
    __tablename__ = "raias"

    id_raia = Column(Integer, primary_key=True, autoincrement=True)
    codigo_quadro = Column(String(4), ForeignKey("quadros.codigo"), nullable=False, index=True)
    nome = Column(String, nullable=False)
    responsavel = Column(String, nullable=False)
    ordem_exibicao = Column(Integer, nullable=False, default=0)

    __table_args__ = (UniqueConstraint("codigo_quadro", "nome", name="uq_raia_nome_no_quadro"),)

    quadro = relationship("Quadro", back_populates="raias")
    cartoes = relationship("Cartao", back_populates="raia")


class Cartao(Base):
    __tablename__ = "cartoes"

    codigo = Column(String(4), nullable=False, index=True)
    codigo_quadro = Column(String(4), ForeignKey("quadros.codigo"), nullable=False)
    id_raia = Column(Integer, ForeignKey("raias.id_raia"), nullable=False)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    responsavel = Column(String, nullable=False)
    prioridade = Column(String, nullable=False, default="MEDIA")
    data_limite = Column(String, nullable=True)
    coluna = Column(String, nullable=False, default="A FAZER")
    criado_em = Column(DateTime, default=datetime.utcnow)
    iniciado_em = Column(DateTime, nullable=True)
    concluido_em = Column(DateTime, nullable=True)

    quadro = relationship("Quadro", back_populates="cartoes")
    raia = relationship("Raia", back_populates="cartoes")

    __table_args__ = (PrimaryKeyConstraint("codigo", "codigo_quadro"),)
