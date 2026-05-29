# 📖 Manual de Instalación — BrailleScript

> Convierte texto en español a escritura Braille y exporta el resultado como imagen PNG o PDF.

---

## ¿Qué necesitas antes de empezar?

Asegúrate de tener instalado lo siguiente en tu computadora:

###Instalación manual:
- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)

###Instalación automatica (Recomendado):
- [Docker](https://www.docker.com/products/docker-desktop/) — si prefieres no instalar nada manualmente

---

## Opción A — Instalación Manual (paso a paso)

### Paso 1 — Descarga el proyecto

Clona el repositorio o descarga el ZIP desde GitHub y accede a la carpeta:

```bash
cd braillescript
```

---

### Paso 2 — Inicia el Backend (Python / FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

✅ El servidor estará corriendo en: **http://localhost:8000**

---

### Paso 3 — Inicia el Frontend (React / Vite)

Abre **otra terminal** (sin cerrar la del backend) y ejecuta:

```bash
cd frontend
npm install
npm run dev
```

✅ La aplicación estará disponible en: **http://localhost:5173**

---

### Paso 4 — Abre la aplicación

Ve a tu navegador y entra a:

```
http://localhost:5173
```

¡Listo! Ya puedes empezar a convertir texto a Braille. 🎉

---

## Opción B — Instalación con Docker (más rápido)

Primero se tiene que clonar el repositorio
```bash
git clone https://github.com/Young-Pharaoh/braillescript.git
cd braillescript
```
Y de ahi, con un solo comando tendrás acceso al sistema
```bash
docker compose up --build
```

| Servicio   | URL                      |
|------------|--------------------------|
| Aplicación | http://localhost:3000    |
| API        | http://localhost:8000    |

> 💡 No necesitas instalar Python ni Node.js por separado. Docker lo maneja todo.

---

## ¿Qué hace la aplicación?

Una vez abierta, puedes:

- ✏️ **Escribir texto en español** y ver su equivalente en Braille
- 🔤 Soporte completo para letras con tilde (á, é, í, ó, ú), ñ, ü y signos de puntuación
- 🔢 Conversión de números con prefijo de signo numeral
- 📸 **Exportar como imagen PNG**
- 📄 **Exportar como PDF**

---

## Solución de problemas comunes

| Problema | Solución |
|---|---|
| `pip` no se reconoce | Usa `pip3` en su lugar |
| `npm` no se reconoce | Verifica que Node.js esté instalado correctamente |
| El frontend no conecta con el backend | Asegúrate de que ambos servidores estén corriendo al mismo tiempo |
| Puerto 8000 ocupado | Cambia el puerto con `uvicorn main:app --reload --port 8001` |

---

## Resumen rápido

```
# Terminal 1 — Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend && npm install && npm run dev

# O con Docker (una sola terminal)
docker compose up --build
```

---

*BrailleScript — Licencia MIT*
