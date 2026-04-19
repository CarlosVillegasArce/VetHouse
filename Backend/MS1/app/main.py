from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from . import models
from .database import engine, get_db

# Crea las tablas en la BD automáticamente al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MS1 - Mascotas",
    description="Microservicio para la gestión de dueños y mascotas",
    version="1.0.0"
)

# --- Esquemas Pydantic para validar datos de entrada y salida ---
class MascotaCreate(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    peso_actual: Optional[float] = None
    estado_reproductivo: Optional[str] = None
    observaciones: Optional[str] = None

class DuenoCreate(BaseModel):
    nombres: str
    apellidos: str
    documento: str
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None

# --- Rutas (Endpoints) ---

@app.post("/duenos", status_code=201)
def crear_dueno(dueno: DuenoCreate, db: Session = Depends(get_db)):
    db_dueno = models.Dueno(**dueno.model_dump())
    db.add(db_dueno)
    try:
        db.commit()
        db.refresh(db_dueno)
        return db_dueno
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el dueño. Verifica que el documento no exista.")

@app.post("/duenos/{id_dueno}/mascotas", status_code=201)
def crear_mascota_para_dueno(id_dueno: int, mascota: MascotaCreate, db: Session = Depends(get_db)):
    # Verificar si el dueño existe
    dueno = db.query(models.Dueno).filter(models.Dueno.id_dueno == id_dueno).first()
    if not dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    
    db_mascota = models.Mascota(**mascota.model_dump(), id_dueno=id_dueno)
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@app.get("/duenos/{id_dueno}")
def obtener_dueno_con_mascotas(id_dueno: int, db: Session = Depends(get_db)):
    dueno = db.query(models.Dueno).filter(models.Dueno.id_dueno == id_dueno).first()
    if not dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    
    return {
        "dueño": dueno,
        "mascotas": dueno.mascotas
    }