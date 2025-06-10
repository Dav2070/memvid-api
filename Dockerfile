FROM debian:bookworm-slim

# Install Python and pip
RUN apt-get update && apt-get install -y \
	python3.11 \
	python3-pip \
	python3.11-venv \
	libgl1 \
	libgl1-mesa-dri \
	mesa-utils \
	libglib2.0-0 \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Use python3 and pip3 as default
RUN ln -sf /usr/bin/python3.11 /usr/local/bin/python && \
	ln -sf /usr/bin/pip3 /usr/local/bin/pip

# Vermeide interaktive Dialoge
ENV DEBIAN_FRONTEND=noninteractive

# Setze Arbeitsverzeichnis
WORKDIR /app

# Virtual Environment erstellen
RUN python3 -m venv venv
# Aktiviere das Virtual Environment
#RUN . venv/bin/activate

# Kopiere Requirements und installiere Python-Abhängigkeiten
COPY requirements.txt .
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# Kopiere restlichen Code
COPY . .

# Port für Gunicorn
EXPOSE 8080

# Startbefehl
CMD ["venv/bin/gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
