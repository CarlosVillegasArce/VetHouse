# Usa una imagen oficial de Python ligera
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto
EXPOSE 3001

# Comando para iniciar Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]