# Ambiente de Desarrollo — BrailleScript

Documentación de las herramientas seleccionadas y el flujo de trabajo del proyecto BrailleScript, una aplicación web que transcribe texto en español al sistema Braille (estándar ONCE) y genera exportaciones visuales en PNG y PDF.

---

## Arquitectura general

```
braillescript/
├── backend/           ← API REST en Python (FastAPI)
├── frontend/          ← Interfaz web en React + Vite
└── docker-compose.yml ← Orquestación de contenedores
```

El sistema sigue una arquitectura **cliente–servidor desacoplada**:

- El **frontend** se comunica con el **backend** exclusivamente a través de la API REST (`/api/*`).
- En desarrollo, cada servicio corre en su propio proceso local con hot reload.
- En producción, ambos servicios se empaquetan en contenedores Docker.

```
Navegador
   │
   │  HTTP (localhost:5173 en desarrollo / :80 en producción)
   ▼
Frontend — React 19 + Vite
   │
   │  HTTP REST (localhost:8000 en desarrollo / /api/* en producción)
   ▼
Backend — FastAPI + Uvicorn (Python 3.12)
   ├── braille/encoder.py   ← Lógica de codificación Braille
   └── braille/renderer.py  ← Generación de PNG y PDF
```

---

## Herramientas seleccionadas

### Backend

| Herramienta | Versión | Rol |
|---|---|---|
| **Python** | 3.12 | Lenguaje principal del backend |
| **FastAPI** | última estable | Framework web asíncrono para la API REST |
| **Uvicorn** | última estable | Servidor ASGI para ejecutar FastAPI |
| **Pillow (PIL)** | última estable | Generación de imágenes PNG con las celdas Braille |
| **ReportLab** | última estable | Generación de documentos PDF con las celdas Braille |
| **python-multipart** | última estable | Soporte para formularios y uploads en FastAPI |
| **venv** | incluido en Python | Entorno virtual aislado para dependencias |

**¿Por qué FastAPI?**
Proporciona validación automática con Pydantic, documentación interactiva (Swagger UI) sin configuración adicional y soporte nativo para operaciones asíncronas. Es ideal para APIs de transcripción donde las respuestas son rápidas.

---

### Frontend

| Herramienta | Versión | Rol |
|---|---|---|
| **React** | 19.x | Librería de UI basada en componentes |
| **Vite** | 8.x | Bundler y servidor de desarrollo con hot reload |
| **ESLint** | 10.x | Análisis estático de código JavaScript |
| **eslint-plugin-react-hooks** | 7.x | Reglas de linting específicas para hooks de React |
| **Node.js** | 20.x | Runtime necesario para Vite y npm |
| **JavaScript (JSX)** | ES Modules | Lenguaje del frontend (sin TypeScript) |

**¿Por qué Vite?**
Hot Module Replacement (HMR) instantáneo, arranque en menos de 1 segundo y configuración mínima. Es el estándar moderno para proyectos React sin necesidad de Next.js.

---

### Documentación

| Herramienta | Versión | Rol |
|---|---|---|
| **Sphinx** | 9.x | Generador de sitio HTML desde docstrings Python |
| **Furo** | última estable | Tema visual moderno con modo claro/oscuro y búsqueda |
| **sphinx-autodoc-typehints** | última estable | Renderiza type hints de forma legible en los docs |
| **napoleon** (extensión Sphinx) | incluida en Sphinx | Soporte para docstrings estilo Google |

---

### Infraestructura y despliegue

| Herramienta | Versión | Rol |
|---|---|---|
| **Docker** | última estable | Contenerización de cada servicio |
| **Docker Compose** | v3 | Orquestación multi-contenedor |
| **Nginx (Alpine)** | última estable | Servidor web para el frontend en producción |

**Imágenes base Docker:**

| Servicio | Imagen |
|---|---|
| Backend | `python:3.12-slim` |
| Frontend (build) | `node:20-alpine` |
| Frontend (producción) | `nginx:alpine` |

---

## Estructura de archivos del proyecto

```
braillescript/
│
├── backend/
│   ├── braille/
│   │   ├── __init__.py       ← Docstring del paquete
│   │   ├── encoder.py        ← Codificación Braille español (ONCE)
│   │   └── renderer.py       ← Exportación PNG y PDF
│   ├── docs/
│   │   ├── source/           ← Fuentes RST y conf.py de Sphinx
│   │   └── build/html/       ← Sitio HTML generado (no versionar)
│   ├── main.py               ← Endpoints FastAPI
│   ├── requirements.txt      ← Dependencias de producción
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── api/              ← Clientes HTTP hacia el backend
│   │   ├── components/       ← Componentes React (JSX)
│   │   ├── styles/           ← CSS vanilla
│   │   ├── App.jsx           ← Componente raíz
│   │   └── main.jsx          ← Punto de entrada de React
│   ├── vite.config.js        ← Configuración de Vite y proxy
│   ├── eslint.config.js      ← Reglas de ESLint
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Flujo de trabajo

### 1. Configuración inicial del entorno (primera vez)

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd braillescript

# ----- Backend -----
cd backend
python3 -m venv .venv                              # Crear entorno virtual
source .venv/bin/activate                          # Activar (Linux/macOS)
# .venv\Scripts\activate                           # Activar (Windows)
pip install -r requirements.txt                    # Dependencias de producción
pip install sphinx furo sphinx-autodoc-typehints   # Dependencias de documentación

# ----- Frontend -----
cd ../frontend
npm install                                        # Instalar dependencias Node
```

---

### 2. Desarrollo local (modo hot reload)

Abrir **dos terminales** en paralelo:

**Terminal 1 — Backend:**

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**

```bash
cd frontend
npm run dev
```

| URL | Servicio |
|-----|---------|
| `http://localhost:5173` | Aplicación web (Vite dev server) |
| `http://localhost:8000/docs` | Swagger UI — documentación interactiva de la API |
| `http://localhost:8000/redoc` | ReDoc — vista alternativa de la API |
| `http://localhost:8000/api/health` | Health check del backend |

---

### 3. Análisis estático (linting)

```bash
# Frontend
cd frontend
npm run lint

# Backend — verificar que los módulos compilan sin errores de sintaxis
cd backend
source .venv/bin/activate
python -m py_compile braille/encoder.py braille/renderer.py main.py
```

---

### 4. Generación y actualización de la documentación

```bash
cd backend
source .venv/bin/activate

# Reconstruir el sitio Sphinx completo desde cero
python -m sphinx docs/source docs/build/html -b html -E

# Abrir el resultado en el navegador
xdg-open docs/build/html/index.html    # Linux
open docs/build/html/index.html        # macOS
```

> [!TIP]
> Ejecutar este comando cada vez que se modifiquen docstrings o se añadan nuevos módulos al proyecto.

---

### 5. Construcción del bundle de producción (frontend)

```bash
cd frontend
npm run build
# Los archivos optimizados quedan en frontend/dist/
```

---

### 6. Despliegue completo con Docker Compose

```bash
# Desde la raíz del proyecto
cd braillescript

# Construir imágenes y levantar todos los servicios
docker compose up --build

# Modo segundo plano (detached)
docker compose up --build -d

# Ver logs en tiempo real
docker compose logs -f

# Detener todos los servicios
docker compose down
```

| URL | Servicio en producción |
|-----|------------------------|
| `http://localhost:3000` | Aplicación web (Nginx) |
| `http://localhost:8000` | API REST (backend) |

---

## Puertos utilizados

| Puerto | Servicio | Modo |
|--------|---------|------|
| `5173` | Frontend (Vite dev server) | Desarrollo |
| `8000` | Backend (Uvicorn) | Desarrollo y producción |
| `3000` | Frontend (Nginx) | Producción Docker |
| `80` | Frontend dentro del contenedor | Producción Docker (interno) |

---

## Variables de entorno

| Variable | Valor | Descripción |
|---|---|---|
| `VITE_API_BASE_URL` | `/api` (en producción) | URL base del backend accedida desde el frontend |

> [!NOTE]
> En desarrollo local, Vite utiliza el proxy configurado en `vite.config.js` para redirigir automáticamente las peticiones `/api/*` al backend en `http://localhost:8000`, evitando problemas de CORS.

---

## Dependencias de sistema requeridas (Linux, sin Docker)

El Dockerfile del backend instala automáticamente en el contenedor las librerías del sistema necesarias para Pillow. En un entorno de desarrollo local sin Docker, instalarlas manualmente con:

```bash
sudo apt install \
  libfreetype6-dev \      # Renderizado de fuentes TrueType en PNG
  libjpeg-turbo8-dev \   # Compresión JPEG
  zlib1g-dev \           # Compresión PNG
  fonts-dejavu-core      # Fuentes tipográficas para etiquetas en las exportaciones
```
