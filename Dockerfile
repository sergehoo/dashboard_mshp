
FROM python:3.9-slim
LABEL authors="ogahserge"

#ENV DJANGO_SETTINGS_MODULE=epidemietrackr.settings

WORKDIR /dashboardmshp-app
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY requirements.txt /dashboardmshp-app/requirements.txt

# Installer les dépendances système nécessaires pour GDAL et PostgreSQL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    gcc \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir la variable d'environnement pour GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so
# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . /dashboardmshp-app/

RUN apt-get update && apt-get install -y postgresql-client
# Exposer le port sur lequel l'application Django sera accessible
EXPOSE 8000

# Démarrer l'application
#CMD ["gunicorn", "epidemietrackr.wsgi:application", "--bind=0.0.0.0:8000"]
CMD ["gunicorn", "dashboard_mshp.wsgi:application", "--bind=0.0.0.0:8000", "--workers=4", "--timeout=180", "--log-level=debug"]
#CMD ["gunicorn", "epidemietrackr.wsgi:application", "--bind=0.0.0.0:8000", "--timeout=180", "--log-level=debug"]