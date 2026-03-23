# Usamos Python 3.11 para compatibilidad con yfinance
FROM python:3.11-slim

# Configuraciones de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Ejecutar el script del pipeline
CMD ["python", "pipeline.py"]
