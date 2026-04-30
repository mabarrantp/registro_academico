#!/bin/bash
set -e

echo "🚀 Deploy Registro Académico"

# Variables de entorno
export ENV=production
export PYTHONUNBUFFERED=1

# Activar entorno virtual
source venv/bin/activate

# Dependencias
pip install -r requirements.txt

# Migraciones
alembic upgrade head

# Arranque (ajustar workers según servidor)
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4