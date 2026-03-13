# 🕷️ Web Scraping Tutorial with Python & Playwright

Este proyecto es una **herramienta educativa para aprender Web Scraping moderno** utilizando **Python + Playwright**.

El scraper extrae información de loadouts de armas desde:

🌐 https://wzstats.gg

El objetivo del proyecto es **mostrar cómo funcionan los scrapers dinámicos**, cómo interactuar con páginas que usan JavaScript y cómo almacenar datos estructurados.

---

# 📚 Contenido del proyecto

```
warzone_scrapper/
│
├── main.py
├── data.json
│
└── README.md
```

---

# 🚀 ¿Qué es Web Scraping?

Web Scraping es una técnica que permite **extraer información automáticamente desde páginas web**.

En lugar de copiar los datos manualmente, un script:

1. abre una página web  
2. localiza los elementos HTML  
3. extrae la información  
4. guarda los datos en un formato estructurado  

Usos comunes:

- análisis de datos
- scraping de precios
- monitoreo de información
- creación de datasets
- agregadores de contenido

---

# ⚙️ Tecnologías utilizadas

Este proyecto utiliza:

- **Python**
- **Playwright**
- **Chromium**
- **JSON**

Playwright permite **controlar navegadores reales**, lo que facilita scrapear páginas dinámicas con JavaScript.

---

# 🧰 Requisitos

Antes de comenzar necesitas:

- Python 3.8+
- pip
- conexión a internet
- Linux / Mac / Windows

---

# 🐍 Instalación de Python

Descargar Python desde:

https://www.python.org/downloads/

Verificar instalación:

```bash
python3 --version
```

---

# 📦 Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
```

Activar entorno:

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

# 📥 Instalar librerías

Instalar Playwright:

```bash
pip install playwright
```

---

# 🌐 Instalar navegadores de Playwright

Playwright necesita descargar navegadores.

```bash
playwright install
```

Esto instalará:

- Chromium
- Firefox
- WebKit

Si solo necesitas Chromium:

```bash
playwright install chromium
```

---

# 🖥️ Dependencias para VPS / Linux

Si ejecutas el scraper en **Ubuntu o VPS**, instala estas dependencias:

```bash
sudo apt update

sudo apt install -y \
libnss3 \
libatk1.0-0 \
libatk-bridge2.0-0 \
libxcomposite1 \
libxdamage1 \
libxrandr2 \
libgbm1 \
libasound2 \
libpangocairo-1.0-0 \
libgtk-3-0
```

---

# ▶️ Ejecutar el scraper

```bash
python3 main.py
```

Salida esperada:

```
Iniciando scraping dinámico...

ARMA #1
{
 "nombre": "Peacekeeper Mk1",
 "tier": "S Tier",
 "rank": "#1",
 "categoria": "Long Range",
 "tipo": "Assault Rifle"
}
```

---

# 🌐 Visualización en la página HTML

La página **index.html** carga los datos del scraper usando:

```javascript
fetch('data.json')
    .then(res => res.json())
    .then(data => {
        allData = data
        initFilters()
        render(allData)
    })
```

Esto significa que:

- el scraper genera **data.json**
- el frontend usa **data0.json**

Puedes:

### Opción 1

Renombrar automáticamente:

```
data.json → data0.json
```

### Opción 2

Modificar el HTML:

```javascript
fetch('data.json')
```

---

# 🧩 Funcionamiento de la página HTML

La página muestra los datos en **cards visuales**.

Cada arma muestra:

- imagen
- nombre
- tier
- primeros accesorios

Código:

```javascript
function render(data) {
    grid.innerHTML = ''

    data.forEach((arma) => {

        const card = document.createElement('div')

        card.innerHTML = `
        <img data-src="${arma.imagen}">
        <h3>${arma.nombre}</h3>
        <p>${arma.tier}</p>
        `
        
        grid.appendChild(card)
    })
}
```

---

# 🔎 Sistema de búsqueda

El buscador permite filtrar armas:

```javascript
searchInput.addEventListener('input', applyFilters)
```

Filtra por:

- nombre del arma
- tier seleccionado

---

# 🎛 Sistema de filtros

El filtro de tier se genera automáticamente:

```javascript
const tiers = [...new Set(allData.map(a => a.tier || 'N/A'))]
```

Esto crea opciones como:

```
S TIER
A TIER
B TIER
```

---

# 🖼 Lazy Loading de imágenes

Las imágenes se cargan solo cuando aparecen en pantalla.

```javascript
const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target
            img.src = img.dataset.src
        }
    })
})
```

Esto mejora el rendimiento.

---

# 🧾 Modal de detalles

Al hacer click en una card se abre un **modal con información completa**.

```javascript
card.onclick = () => openModal(arma)
```

El modal muestra:

- imagen grande
- accesorios completos
- código de build
- fecha de actualización

---

# 🚀 Cómo usar el sistema completo

Paso 1

Ejecutar scraper

```
python3 main.py
```

Paso 2

Verificar que existe:

```
data.json
```

Paso 3

Mover o copiar:

```
data.json → data0.json
```

Paso 4

Abrir la página:

```
index.html
```

---

# 📊 Resultado

La página mostrará:

- grid de armas
- buscador
- filtro por tier
- modal con accesorios
- lazy loading de imágenes

---

# 🧠 Cómo funciona el scraper

El scraper sigue estos pasos:

1️⃣ Abre un navegador Chromium  
2️⃣ Carga la página web  
3️⃣ Espera a que aparezcan los elementos  
4️⃣ Recorre cada arma encontrada  
5️⃣ Extrae datos relevantes  
6️⃣ Hace scroll para cargar más contenido  
7️⃣ Guarda los resultados en JSON  

---

# 📦 Librerías utilizadas

```python
from playwright.sync_api import sync_playwright
import json
import time
import os
from datetime import datetime
```

### Explicación

| Librería | Uso |
|--------|------|
| playwright | control del navegador |
| json | guardar datos |
| time | pausas para evitar errores |
| os | manejo de archivos |
| datetime | crear backups |

---

# 🔍 Selectores CSS utilizados

Los selectores permiten localizar elementos dentro del HTML.

Ejemplos:

```
.loadout-container
.loadout-content-name
.attachment-name-no-image
.weapon-build-code
.loadout-tag
```

---

# 🧪 Ejemplo de extracción

```python
items = page.query_selector_all(".loadout-container")

for item in items:
    nombre = item.query_selector(".loadout-content-name").inner_text()
```

---

# 🔄 Scroll infinito

Muchas páginas cargan contenido dinámicamente cuando se hace scroll.

```python
page.evaluate("window.scrollBy(0,1500)")
```

Esto permite **cargar nuevos elementos dinámicamente**.

---

# 💾 Guardar datos en JSON

```python
with open("data.json","w",encoding="utf-8") as f:
    json.dump(data,f,indent=4,ensure_ascii=False)
```

Resultado:

```json
[
 {
  "nombre": "Peacekeeper Mk1",
  "tier": "S Tier",
  "rank": "#1"
 }
]
```

---

# 🔁 Sistema de backup automático

Antes de guardar nuevos datos, el script crea una copia del JSON anterior.

Ejemplo:

```
backup/data_2026-03-12_21-10-22.json
```

Esto evita perder datos anteriores.

---

# ⚠️ Buenas prácticas de scraping

✔ agregar pausas entre requests  
✔ evitar saturar servidores  
✔ respetar robots.txt cuando sea necesario  
✔ usar user-agents realistas  
✔ manejar errores  

---

# 🚀 Posibles mejoras

Este proyecto puede evolucionar agregando:

- proxies
- rotación de user agents
- multithreading
- scraping distribuido
- guardado en base de datos
- APIs REST
- dashboard de visualización

---

# 📊 Aplicaciones reales

El scraping se usa en:

- análisis financiero
- monitorización de precios
- investigación académica
- agregadores de noticias
- inteligencia de mercado

---

# ⚖️ Consideraciones legales

Siempre verifica:

- términos de uso del sitio
- robots.txt
- leyes de datos locales

Evita scrapear:

- datos personales
- contenido protegido
- información privada

---

# 📜 Licencia

Proyecto educativo para aprendizaje de **Web Scraping con Python**.

---

# 👨‍💻 Natanael Sanchez (nsmdeveloper)

Proyecto creado como **ejemplo educativo de scraping dinámico con Playwright**.
