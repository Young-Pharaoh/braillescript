# BrailleScript

**BrailleScript** es una aplicación web full-stack que transcribe texto en español a escritura Braille, muestra las celdas Braille de forma visual e interactiva y permite exportar el resultado como imagen PNG o documento PDF.

El proyecto fue desarrollado con un backend en **Python/FastAPI** y un frontend en **React + Vite**, separando la lógica de transcripción, renderizado visual y consumo de API en módulos independientes.

---

## Objetivo del proyecto

El objetivo principal de BrailleScript es facilitar la conversión de texto escrito en español a una representación Braille clara, útil para señalización, material educativo o demostraciones académicas.

La aplicación permite:

- Ingresar texto en español desde una interfaz web.
- Convertir letras, números, signos y caracteres especiales al sistema Braille.
- Visualizar cada celda Braille con sus puntos activos.
- Mostrar u ocultar etiquetas debajo de las celdas.
- Exportar la transcripción como imagen PNG.
- Exportar la transcripción como documento PDF.

---

## Tecnologías utilizadas

| Capa | Tecnología | Descripción | Puerto |
|---|---|---|---|
| Backend | Python + FastAPI | API REST para transcripción y exportación | 8000 |
| Frontend | React + Vite | Interfaz web para entrada, visualización y descarga | 5173 |
| Renderizado | Pillow + ReportLab | Generación de imágenes PNG y documentos PDF | — |
| Contenedores | Docker + Docker Compose | Ejecución del proyecto completo | 3000 / 8000 |

---

## Arquitectura general

```text
BrailleScript/
├── backend/
│   ├── main.py                  # Endpoints principales de la API
│   ├── requirements.txt         # Dependencias del backend
│   └── braille/
│       ├── encoder.py           # Lógica de conversión Español → Braille
│       └── renderer.py          # Generación de PNG y PDF
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Componente principal
│   │   ├── api/
│   │   │   └── brailleApi.js    # Comunicación con la API
│   │   ├── components/
│   │   │   ├── BrailleCell.jsx
│   │   │   ├── BrailleDisplay.jsx
│   │   │   ├── ExportBar.jsx
│   │   │   ├── Header.jsx
│   │   │   └── TextInput.jsx
│   │   └── styles/
│   │       └── index.css
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
└── README.md
```

---

## Funcionamiento del sistema

1. El usuario escribe un texto en español desde el frontend.
2. React envía el texto al endpoint `/api/transcribe`.
3. FastAPI procesa el texto usando el módulo `encoder.py`.
4. El backend devuelve:
   - Texto original.
   - Lista de celdas con carácter, puntos activos y tipo.
   - Cadena Braille en Unicode.
5. El frontend renderiza visualmente cada celda Braille.
6. El usuario puede exportar el resultado a PNG o PDF.

---

## Sistema Braille implementado

El módulo de transcripción incluye soporte para:

- Alfabeto español completo: `a-z`.
- Vocales acentuadas: `á`, `é`, `í`, `ó`, `ú`.
- Caracteres especiales del español: `ñ`, `ü`.
- Letra `w` para palabras extranjeras.
- Signo de mayúscula para letras capitales.
- Signo numérico para secuencias de dígitos.
- Signos de puntuación básicos.
- Signos matemáticos simples como `+`, `-`, `=`, `×`, `÷`.
- Separadores decimales con coma o punto.

Ejemplo:

```text
Texto: Hola Mundo 123
Braille Unicode: ⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕ ⠼⠁⠃⠉
```

---

## Interfaz de usuario

La interfaz está compuesta por componentes reutilizables:

| Componente | Función |
|---|---|
| `Header` | Muestra el nombre y descripción del sistema |
| `TextInput` | Permite escribir el texto, activar etiquetas y transcribir |
| `BrailleDisplay` | Presenta el resultado en Unicode y en celdas visuales |
| `BrailleCell` | Dibuja cada celda Braille con SVG |
| `ExportBar` | Permite descargar el resultado como PNG o PDF |

También se agregó el atajo de teclado **Ctrl + Enter** para transcribir rápidamente el texto ingresado.

---

## Endpoints de la API

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/health` | Verifica que la API esté activa |
| `POST` | `/api/transcribe` | Convierte texto español a Braille |
| `GET` | `/api/export/image` | Genera y descarga la transcripción como PNG |
| `GET` | `/api/export/pdf` | Genera y descarga la transcripción como PDF |

### Ejemplo de solicitud

```http
POST /api/transcribe
Content-Type: application/json
```

```json
{
  "text": "Hola Mundo 123",
  "show_labels": true
}
```

### Ejemplo de respuesta

```json
{
  "original": "Hola Mundo 123",
  "cells": [
    {
      "char": "H",
      "dots": [1, 2, 5],
      "type": "letter"
    },
    {
      "char": "o",
      "dots": [1, 3, 5],
      "type": "letter"
    }
  ],
  "unicode_braille": "⠨⠓⠕⠇⠁ ⠨⠍⠥⠝⠙⠕ ⠼⠁⠃⠉"
}
```

---

## Instalación y ejecución local

### Requisitos previos

- Python 3.10 o superior.
- Node.js 18 o superior.
- npm.
- Docker, opcional para ejecución con contenedores.

---

### 1. Ejecutar el backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

Documentación automática de FastAPI:

```text
http://localhost:8000/docs
```

---

### 2. Ejecutar el frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

La aplicación estará disponible en:

```text
http://localhost:5173
```

Durante el desarrollo, Vite redirige las peticiones `/api` hacia el backend.

---

## Ejecución con Docker

También se puede levantar todo el sistema con Docker Compose:

```bash
docker compose up --build
```

| Servicio | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |

En este modo, el contenedor de frontend usa **nginx** para servir la aplicación y redirigir las peticiones `/api` al backend.

---

## Exportación de resultados

La aplicación permite generar archivos visuales de la transcripción:

### Exportar como PNG

```http
GET /api/export/image?text=Hola%20Mundo%20123&show_labels=true
```

Devuelve un archivo:

```text
braillescript.png
```

### Exportar como PDF

```http
GET /api/export/pdf?text=Hola%20Mundo%20123&show_labels=true
```

Devuelve un archivo:

```text
braillescript.pdf
```

---
## Licencia

Este proyecto se distribuye bajo licencia MIT.

---

## License

MIT
