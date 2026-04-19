from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MS1 - Mascotas", version="1.0.0")

# --- ESQUEMAS DE VALIDACIÓN (Pydantic) ---
class DuenoCreate(BaseModel):
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    # Exigimos exactamente 8 dígitos (Formato DNI) para evitar inyecciones
    documento: str = Field(..., pattern=r"^\d{8}$")
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None

class MascotaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    especie: str = Field(..., min_length=2, max_length=50)
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    peso_actual: Optional[float] = None
    estado_reproductivo: Optional[str] = None
    observaciones: Optional[str] = None

# --- MONITOREO (Para AWS Load Balancer) ---
@app.get("/health", tags=["Monitoreo"])
def health_check():
    return {"status": "ok", "service": "ms1-mascotas"}

# --- RUTAS DE DUEÑOS ---
@app.post("/duenos", status_code=201, tags=["Dueños"])
def crear_dueno(dueno: DuenoCreate, db: Session = Depends(get_db)):
    db_dueno = models.Dueno(**dueno.model_dump())
    db.add(db_dueno)
    try:
        db.commit()
        db.refresh(db_dueno)
        return db_dueno
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error: El documento ya existe.")

@app.get("/duenos", tags=["Dueños"])
def obtener_duenos(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    skip = (page - 1) * size
    # Solo traemos los activos (Soft Delete aplicado)
    query = db.query(models.Dueno).filter(models.Dueno.activo == True)
    
    total = query.count()
    duenos = query.offset(skip).limit(size).all()
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "paginas": (total // size) + (1 if total % size > 0 else 0),
        "items": duenos
    }

@app.delete("/duenos/{id_dueno}", tags=["Dueños"])
def eliminar_dueno_logicamente(id_dueno: int, db: Session = Depends(get_db)):
    dueno = db.query(models.Dueno).filter(models.Dueno.id_dueno == id_dueno).first()
    if not dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    
    dueno.activo = False # Eliminación Lógica
    db.commit()
    return {"mensaje": "Dueño eliminado correctamente"}

# --- RUTAS DE MASCOTAS ---
@app.post("/duenos/{id_dueno}/mascotas", status_code=201, tags=["Mascotas"])
def crear_mascota(id_dueno: int, mascota: MascotaCreate, db: Session = Depends(get_db)):
    dueno = db.query(models.Dueno).filter(models.Dueno.id_dueno == id_dueno, models.Dueno.activo == True).first()
    if not dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado o inactivo")
    
    db_mascota = models.Mascota(**mascota.model_dump(), id_dueno=id_dueno)
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota