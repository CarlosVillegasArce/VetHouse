from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Dueno(Base):
    __tablename__ = "duenos"

    id_dueno = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, index=True, nullable=False)
    telefono = Column(String(20))
    correo = Column(String(100), unique=True)
    direccion = Column(String(255))

    # Relación
    mascotas = relationship("Mascota", back_populates="dueno")

class Mascota(Base):
    __tablename__ = "mascotas"

    id_mascota = Column(Integer, primary_key=True, index=True)
    id_dueno = Column(Integer, ForeignKey("duenos.id_dueno"))
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(50))
    sexo = Column(String(20))
    fecha_nacimiento = Column(Date)
    peso_actual = Column(Float)
    estado_reproductivo = Column(String(50))
    observaciones = Column(String(255))

    # Relación
    dueno = relationship("Dueno", back_populates="mascotas")