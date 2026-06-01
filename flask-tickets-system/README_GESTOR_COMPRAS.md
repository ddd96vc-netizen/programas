# Gestor de Compras
## Aplicación Web Full Stack para Registro y Análisis de Gastos

---

## 📋 Descripción Ejecutiva

**Gestor de Compras** es una aplicación web completa desarrollada con Flask que permite registrar, organizar y analizar gastos de compra en tiempo real. Proporciona un sistema robusto para gestionar tickets de múltiples tiendas, categorizar productos y generar reportes visuales detallados.

La aplicación demuestra competencias completas de **desarrollo full-stack**: autenticación segura, CRUD operativo, API REST documentada, visualización de datos interactiva y arquitectura modular.

### Características Diferenciadores
✅ **Autenticación avanzada** con protección por IP y bloqueo adaptativo  
✅ **Dashboard inteligente** con estadísticas en tiempo real  
✅ **API REST** completamente funcional y escalable  
✅ **Interfaz responsiva** optimizada para desktop y móvil  
✅ **Búsqueda poderosa** con edición inline de resultados  

---

## 🎯 Funcionalidades Principales

### Módulos Implementados

| Módulo | Funcionalidad | Características |
|--------|---------------|-----------------|
| **Autenticación** | Login seguro | Protección por IP, bloqueo 15 min tras 5 fallos |
| **Dashboard** | Vista general | KPIs en tiempo real, últimas compras |
| **CRUD Tickets** | Gestión completa | Crear, leer, editar, eliminar con validación |
| **Búsqueda** | Motor de búsqueda | Búsqueda global + edición inline de productos |
| **Categorías** | Organización | Gestión modal, estadísticas por categoría |
| **Estadísticas** | Análisis avanzado | 4 vistas especializadas con gráficos |
| **API REST** | Integración | 5+ endpoints documentados y funcionales |

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA PRESENTACIÓN (Frontend)                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │  Login   │ │Dashboard │ │ Tickets  │ │ Estadísticas 4x  │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────────────┘   │
│       └─────────────┴────────────┴──────────────┘                │
│              HTML5 + CSS3 + JavaScript ES6                       │
│              Chart.js | FontAwesome 6 | Responsive              │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ HTTP/JSON
┌────────────────────────────────▼─────────────────────────────────┐
│                  CAPA APLICACIÓN (Backend - Flask)               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              app.py (Controlador Principal)              │   │
│  │  ✓ Rutas HTTP (GET, POST, DELETE)                       │   │
│  │  ✓ Autenticación + Rate Limiting                         │   │
│  │  ✓ Protección de sesiones (before_request)              │   │
│  │  ✓ Endpoints API REST                                    │   │
│  └────┬─────────────────────────────────────────────────┬───┘   │
│       │                                                 │         │
│  ┌────▼──────────────────┐  ┌──────────────────────────▼───┐   │
│  │   models.py           │  │   templates/ (Jinja2)        │   │
│  │  ◆ ComprasMiasFlask   │  │  ◆ base.html (estructura)   │   │
│  │    - Gestión tickets  │  │  ◆ 10+ plantillas           │   │
│  │    - CRUD productos   │  │  ◆ Componentes reutilizables│   │
│  │  ◆ EstadisticasFlask  │  │                              │   │
│  │    - Análisis datos   │  └──────────────────────────────┘   │
│  │    - Cálculos avanzados                                     │
│  └────┬──────────────────┘                                      │
│       │                                                          │
│  ┌────▼──────────────────────────────────────────────────────┐  │
│  │          static/ (Recursos Frontend)                      │  │
│  │  ◆ css/style.css (diseño + responsive)                  │  │
│  │  ◆ js/script.js (interactividad + AJAX)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬────────────────────────────────┘
                                  │
┌─────────────────────────────────▼────────────────────────────────┐
│              CAPA PERSISTENCIA (Almacenamiento)                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            solocompras.json (Base de Datos)             │   │
│  │  {                                                       │   │
│  │    "tickets": [                                         │   │
│  │      {                                                  │   │
│  │        "id": "Mercadona_2025-01-15",                  │   │
│  │        "tienda": "Mercadona",                         │   │
│  │        "fecha": "2025-01-15T10:30",                  │   │
│  │        "total": 45.50,                               │   │
│  │        "productos": [...]                            │   │
│  │      }                                                │   │
│  │    ]                                                  │   │
│  │  }                                                    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ⚠️ Escalable a SQLite / PostgreSQL                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 💻 Tecnologías Utilizadas

### Backend
```
Python 3.10+          Lenguaje principal
Flask 2.3+            Framework web minimalista
Jinja2                Motor de templating
JSON                  Almacenamiento de datos
```

### Frontend
```
HTML5                 Estructura semántica
CSS3                  Diseño responsive (Mobile-first)
JavaScript ES6        Interactividad y AJAX
Chart.js              Gráficos interactivos
FontAwesome 6         Iconografía
```

### Herramientas & Librerías
```
pip                   Gestor de dependencias
virtualenv            Aislamiento del entorno
Git                   Control de versiones
```

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
```
- Python 3.8+
- pip (gestor de paquetes)
- 100 MB espacio disponible
- Navegador moderno (Chrome, Firefox, Safari, Edge)
```

### Paso a Paso

#### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/gestor-compras.git
cd gestor-compras
```

#### 2. Crear entorno virtual
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Instalar dependencias
```bash
pip install flask
```

#### 4. Configurar variables de entorno (Opcional)
```bash
# Linux / macOS
export SECRET_KEY="tu-clave-secreta-aqui"
export APP_PASSWORD="Compras2025!"

# Windows (PowerShell)
$env:SECRET_KEY="tu-clave-secreta-aqui"
$env:APP_PASSWORD="Compras2025!"
```

#### 5. Ejecutar la aplicación
```bash
python app.py
```

#### 6. Acceder a la aplicación
```
Abre en tu navegador: http://localhost:5000
Credencial por defecto: Compras2025!
```

### Primeros Pasos
```
1. Inicia sesión con la contraseña
2. Haz clic en "Nuevo Ticket" para agregar una compra
3. Navega a "Búsqueda" para consultar histórico
4. Explora "Estadísticas" para análisis detallados
```

---

## 📁 Estructura del Proyecto

```
gestor-compras/
│
├── 📄 app.py                          # Servidor Flask (150+ líneas)
│   ├── Rutas HTTP (GET, POST, DELETE)
│   ├── Autenticación y sesiones
│   ├── Protección de rutas
│   ├── Endpoints API REST
│   └── Manejo de errores (404, 500)
│
├── 📄 models.py                       # Lógica de negocio (250+ líneas)
│   ├── class ComprasMiasFlask
│   │   ├── add_ticket()
│   │   ├── get_ticket()
│   │   ├── delete_ticket()
│   │   ├── search_producto()
│   │   └── get_all_categorias()
│   │
│   └── class EstadisticasFlask
│       ├── total_gastado()
│       ├── tickets_count()
│       ├── tickets_por_tienda()
│       ├── productos_por_categoria()
│       ├── frecuencia_producto()
│       └── evoluccion_precios()
│
├── 📄 solocompras.json               # Base de datos (se crea automáticamente)
│
├── 📂 templates/                     # Plantillas Jinja2
│   ├── base.html                    # Plantilla base (navbar, footer)
│   ├── login.html                   # Pantalla de autenticación
│   ├── index.html                   # Dashboard principal (KPIs + gráfico)
│   ├── nuevo_ticket.html            # Formulario crear ticket
│   ├── editar_ticket.html           # Formulario editar ticket
│   ├── ver_tickets.html             # Listado completo
│   ├── ticket_detalle.html          # Vista detallada de un ticket
│   ├── buscar_producto.html         # Motor de búsqueda con edición inline
│   ├── categorias.html              # Gestión de categorías (modal)
│   ├── estadisticas.html            # Dashboard de estadísticas
│   ├── estadisticas_tiendas.html    # Análisis por tienda (gráfico donut)
│   ├── estadisticas_fechas.html     # Análisis por fechas (gráfico líneas)
│   ├── estadisticas_frecuencia.html # Frecuencia de productos
│   ├── 404.html                     # Error: página no encontrada
│   └── 500.html                     # Error: error interno del servidor
│
└── 📂 static/                       # Recursos estáticos
    ├── 📂 css/
    │   └── style.css                # Estilos globales (~500 líneas)
    │       ├── Variables CSS
    │       ├── Layout responsivo
    │       ├── Componentes (botones, tarjetas, modales)
    │       ├── Dark mode compatible
    │       └── Animaciones suaves
    │
    └── 📂 js/
        └── script.js                # Lógica frontend (~300 líneas)
            ├── Manejo de modales
            ├── Validación de formularios
            ├── Llamadas AJAX
            ├── Inicialización de gráficos Chart.js
            └── Event listeners
```

---

## 🔐 Seguridad Implementada

### Medidas de Protección

| Medida | Implementación | Beneficio |
|--------|---|---|
| **Rate Limiting por IP** | 5 intentos máx, bloqueo 15 min | Previene fuerza bruta |
| **Protección de rutas** | `before_request` valida sesión | Solo usuarios autenticados |
| **Sesiones seguras** | Duración 30 días, HttpOnly | Persistencia y prevención XSS |
| **Variables de entorno** | `SECRET_KEY` + `APP_PASSWORD` | Credenciales no en código |
| **Logging** | Registro de intentos fallidos | Auditoría y debugging |
| **Validación input** | Sanitización de datos | Previene inyección |

---

## 📊 Módulo de Estadísticas

La aplicación proporciona **4 vistas especializadas** de análisis:

### 1. Dashboard Principal
```
┌─────────────────────────────────────────┐
│  KPIs                                   │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ 3        │ │ 245.50€  │ │ 81.83€  │ │
│  │ Tickets  │ │ Gastado  │ │ Promedio│ │
│  └──────────┘ └──────────┘ └─────────┘ │
│                                         │
│  Gráfico: Distribución por tienda      │
│  (Gráfico circular - Chart.js)         │
└─────────────────────────────────────────┘
```

### 2. Por Tiendas
```
Ranking:
1. Mercadona    ███████ 156.20€ (63.7%)
2. Carrefour    ███     56.30€  (23.0%)
3. Día          ██      33.00€  (13.5%)

Gráfico: Donut chart con porcentajes
```

### 3. Por Fechas
```
Rango: [Calendario] - [Calendario]

Evolución temporal:
Ene: ████ 45.50€
Feb: ██████ 78.20€
Mar: ███████ 121.80€

Gráfico: Línea con puntos (tendencia)
```

### 4. Frecuencia de Productos
```
Selecciona producto: [Leche entera ▼]

┌─────────────────────────────┐
│ Análisis: Leche entera      │
├─────────────────────────────┤
│ Veces comprado:    12       │
│ Precio promedio:   1.23€    │
│ Mín:               1.15€    │
│ Máx:               1.35€    │
│ Tienda más barata: Día      │
│                             │
│ Evolución de precios:       │
│ [Gráfico de líneas]         │
└─────────────────────────────┘
```

---

## 🔌 API REST Documentada

### Endpoints Disponibles

#### 1. Obtener todos los tickets
```http
GET /api/tickets
```
**Respuesta (200 OK):**
```json
{
  "status": "success",
  "tickets": [
    {
      "id": "Mercadona_2025-01-15",
      "tienda": "Mercadona",
      "fecha": "2025-01-15T10:30",
      "total": 45.50,
      "productos": [ ... ]
    }
  ]
}
```

#### 2. Obtener ticket específico
```http
GET /api/tickets/{id}
```
**Parámetro:** `id` = ID del ticket (ej: `Mercadona_2025-01-15`)  
**Respuesta (200 OK):**
```json
{
  "status": "success",
  "ticket": { ... }
}
```

#### 3. Obtener productos por categoría
```http
GET /api/productos_categoria/{categoria}
```
**Parámetro:** `categoria` = Nombre de categoría (ej: `Lácteos`)  
**Respuesta (200 OK):**
```json
{
  "status": "success",
  "categoria": "Lácteos",
  "productos": [ ... ],
  "total": 3
}
```

#### 4. Obtener resumen de estadísticas
```http
GET /api/estadisticas/resumen
```
**Respuesta (200 OK):**
```json
{
  "status": "success",
  "total_gastado": 245.50,
  "num_tickets": 3,
  "promedio_ticket": 81.83,
  "tiendas": [
    { "nombre": "Mercadona", "gasto": 156.20 }
  ]
}
```

#### 5. Editar producto individual
```http
POST /api/editar_producto
Content-Type: application/json

{
  "ticket_id": "Mercadona_2025-01-15",
  "producto_id": 1,
  "nombre": "Leche desnatada",
  "precio": 1.10,
  "categoria": "Lácteos",
  "observacion": "Oferta"
}
```
**Respuesta (200 OK):**
```json
{
  "status": "success",
  "message": "Producto actualizado correctamente"
}
```

---

## 📱 Interfaz Responsiva

### Desktop (>1024px)
```
┌────────────────────────────────────────┐
│  [Logo] [Nav] [Buscar] [Usuario]      │
├────────────────────────────────────────┤
│ [Sidebar] │ [Contenido Principal]     │
│           │ (3 columnas flexible)     │
│           │                           │
│           │                           │
└────────────────────────────────────────┘
```

### Tablet (768px - 1023px)
```
┌───────────────────────────────────┐
│ [Logo] [Menu] [User]             │
├───────────────────────────────────┤
│     [Contenido Principal]         │
│     (2 columnas)                  │
│                                   │
└───────────────────────────────────┘
```

### Mobile (<768px)
```
┌──────────────────┐
│ ☰ [Logo] [User] │
├──────────────────┤
│                  │
│ [Contenido]      │
│  (1 columna)     │
│                  │
└──────────────────┘
```

---

## 📈 Estructura de Datos (JSON)

```json
{
  "tickets": [
    {
      "id": "Mercadona_2025-01-15_1",
      "tienda": "Mercadona",
      "fecha": "2025-01-15T10:30:00",
      "total": 45.50,
      "productos": [
        {
          "id": 1,
          "nombre": "Leche entera",
          "precio": 1.20,
          "categoria": "Lácteos",
          "observacion": "Marca propia"
        },
        {
          "id": 2,
          "nombre": "Pan integral",
          "precio": 2.40,
          "categoria": "Panificados",
          "observacion": ""
        }
      ]
    },
    {
      "id": "Carrefour_2025-01-16_1",
      "tienda": "Carrefour",
      "fecha": "2025-01-16T14:15:00",
      "total": 56.30,
      "productos": [ ... ]
    }
  ]
}
```

---

## ✨ Características Técnicas Destacadas

### Control de Intentos Fallidos
```python
# Implementación en app.py
@app.before_request
def verificar_bloqueo():
    ip = request.remote_addr
    intentos = session.get(f'intentos_{ip}', 0)
    
    if intentos >= 5:
        tiempo_bloqueo = session.get(f'bloqueo_{ip}', 0)
        if time.time() < tiempo_bloqueo:
            return "IP bloqueada temporalmente", 429
        else:
            session[f'intentos_{ip}'] = 0  # Desbloquear
```

### Búsqueda Global con Edición Inline
```javascript
// Búsqueda AJAX sin recargar página
fetch(`/api/buscar?q=${query}`)
    .then(r => r.json())
    .then(data => mostrar_resultados(data))
    
// Edición inline con guardar automático
$('.producto').on('click', () => {
    entrada.contentEditable = true;
    entrada.focus();
})
```

### Gráficos Interactivos
```javascript
// Chart.js con actualizaciones en tiempo real
const ctx = document.getElementById('chart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'doughnut',
    data: { labels: tiendas, datasets: [{ data: gastos }] },
    options: { responsive: true, maintainAspectRatio: false }
});
```

---

## 🎯 Casos de Uso Reales

| Caso | Funcionalidad | Beneficio |
|------|---|---|
| **Usuario diario** | Registra compra → Accede a dashboard | Seguimiento en tiempo real |
| **Análisis mensual** | Filtra por fechas → Ve tendencias | Identifica patrones |
| **Comparativa tiendas** | Visualiza gastos por tienda | Optimiza compras futuras |
| **Búsqueda histórica** | Consulta precio de producto → Edita inline | Correcciones rápidas |
| **Reportes** | Exporta estadísticas (futura) | Comparte con familia |

---

## 🔜 Mejoras Futuras

### Corto Plazo (v1.1)
- [ ] Exportar datos a CSV/Excel
- [ ] Gráficos de gasto por mes/año
- [ ] Modo oscuro automático
- [ ] Notificaciones push

### Mediano Plazo (v2.0)
- [ ] Base de datos SQLite (reemplazar JSON)
- [ ] Presupuestos mensuales por categoría
- [ ] Alertas de sobregasto
- [ ] Sistema multiusuario

### Largo Plazo (v3.0)
- [ ] Aplicación móvil nativa (React Native)
- [ ] Sincronización en la nube
- [ ] Machine Learning para recomendaciones
- [ ] Integración con APIs de tiendas

---

## 📊 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código (Backend)** | ~400 |
| **Líneas de código (Frontend)** | ~800 |
| **Plantillas HTML** | 12 |
| **Endpoints API** | 5+ |
| **Funciones principales** | 25+ |
| **Tiempo de carga** | <1s (local) |
| **Compatibilidad** | Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ |

---

## 💡 Competencias Demostradas

### Desarrollo Backend
✅ Flask (routing, blueprints, sesiones)  
✅ Autenticación y control de acceso  
✅ Gestión de estado con JSON  
✅ API REST RESTful  
✅ Manejo de errores y logging  

### Desarrollo Frontend
✅ HTML5 semántico  
✅ CSS3 responsivo (Mobile-first)  
✅ JavaScript ES6 (vanilla, sin frameworks)  
✅ AJAX/Fetch API  
✅ Chart.js (visualización de datos)  

### Arquitectura & Diseño
✅ MVC (Models, Views, Controllers)  
✅ Separación de responsabilidades  
✅ Componentes reutilizables  
✅ Escalabilidad a BD relacional  

### Seguridad
✅ Protección contra ataques (Rate Limiting)  
✅ Validación y sanitización de inputs  
✅ Gestión segura de credenciales  
✅ Logging y auditoría  

---

## 🚀 Despliegue

### En Railway.app (Recomendado para portafolio)
```bash
# 1. Instalar Railway CLI
npm i -g @railway/cli

# 2. Conectar repositorio
railway link

# 3. Configurar variables de entorno
railway variables set APP_PASSWORD="Compras2025!"

# 4. Desplegar
railway up

# La app estará en: https://[proyecto].railway.app
```

### En Render.com
```bash
# Similar a Railway, con interfaz gráfica
# https://render.com → New Web Service
```

---

## 📚 Tecnologías Aprendidas

- Flask 2.3+
- Jinja2 Templating
- Flask Sessions
- Chart.js
- CSS Grid/Flexbox
- JavaScript Fetch API
- JSON manipulation
- Git/GitHub

---

## 👤 Autor

**Desarrollador:** [Tu nombre]  
**Portafolio:** Junior Full Stack Developer  
📧 Email: [tu-email@example.com]  
🔗 LinkedIn: [Tu perfil]  
💻 GitHub: [Tu usuario]  

---

## 📜 Licencia

MIT License - Libre para uso educativo y comercial

---

## 🙏 Agradecimientos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

---

**Última actualización:** Junio 2026  
**Versión:** 1.0.0  
**Estado:** ✅ Funcional y desplegable  
**Navegadores soportados:** Modernos (2020+)

