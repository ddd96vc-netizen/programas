"""
app.py - SERVIDOR FLASK PRINCIPAL
==================================
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from datetime import datetime, timedelta
import json
import os
import logging
from functools import wraps

from models import ComprasMiasFlask, EstadisticasFlask

# ============================================================
# CONFIGURACIÓN
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-cambiar-en-produccion')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

PASSWORD_ACCESO = os.environ.get('APP_PASSWORD', 'Compras2025!')

# ============================================================
# CONTROL DE INTENTOS DE LOGIN
# ============================================================

intentosLogin = {}
MAX_INTENTOS = 5
BLOQUEO_MINUTOS = 15

def verificar_intentos(ip):
    """Devuelve (permitido: bool, bloqueado_hasta: datetime|None)"""
    if ip not in intentosLogin:
        return True, None

    datos = intentosLogin[ip]
    if datos['intentos'] > MAX_INTENTOS:
        bloqueado_hasta = datos['bloqueado_hasta']
        if datetime.now() < bloqueado_hasta:
            return False, bloqueado_hasta
        else:
            del intentosLogin[ip]
    return True, None

def registrar_intento_fallido(ip):
    """Registra un intento fallido. Devuelve intentos restantes (0 si bloqueado)."""
    if ip not in intentosLogin:
        intentosLogin[ip] = {'intentos': 0, 'bloqueado_hasta': None}

    intentosLogin[ip]['intentos'] += 1

    if intentosLogin[ip]['intentos'] > MAX_INTENTOS:
        intentosLogin[ip]['bloqueado_hasta'] = datetime.now() + timedelta(minutes=BLOQUEO_MINUTOS)
        logger.warning(f"IP {ip} bloqueada por {BLOQUEO_MINUTOS} minutos")
        return 0

    return MAX_INTENTOS - intentosLogin[ip]['intentos']

def resetear_intentos(ip):
    if ip in intentosLogin:
        del intentosLogin[ip]

# ============================================================
# PROTECCIÓN DE RUTAS (before_request en lugar de decorador)
# ============================================================

RUTAS_PUBLICAS = {'login', 'static'}

@app.before_request
def verificar_sesion():
    if request.endpoint in RUTAS_PUBLICAS:
        return None
    if not session.get('logueado'):
        flash('Debes iniciar sesion para acceder a esta pagina', 'error')
        return redirect(url_for('login'))

# ============================================================
# INSTANCIA GLOBAL
# ============================================================

compras = ComprasMiasFlask()

# ============================================================
# AUTENTICACIÓN
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logueado'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        ip = request.remote_addr
        password = request.form.get('password', '').strip()

        permitido, bloqueado_hasta = verificar_intentos(ip)
        if not permitido:
            minutos = int((bloqueado_hasta - datetime.now()).total_seconds() / 60) + 1
            flash(f'Demasiados intentos fallidos. Espera {minutos} minuto(s).', 'error')
            return redirect(url_for('login'))

        if password == PASSWORD_ACCESO:
            session['logueado'] = True
            session.permanent = True
            resetear_intentos(ip)
            logger.info(f"Login correcto desde {ip}")
            flash('Bienvenido al Gestor de Compras', 'success')
            return redirect(url_for('index'))
        else:
            restantes = registrar_intento_fallido(ip)
            logger.warning(f"Login fallido desde {ip} - intentos restantes: {restantes}")
            if restantes == 0:
                flash(f'Cuenta bloqueada {BLOQUEO_MINUTOS} minutos por exceso de intentos.', 'error')
            else:
                flash(f'Contrasena incorrecta. Te quedan {restantes} intentos.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesion correctamente', 'success')
    return redirect(url_for('login'))


# ============================================================
# PAGINA PRINCIPAL
# ============================================================

@app.route('/')
def index():
    tickets = compras.tickets
    total_tickets = len(tickets)
    total_gastado = sum(ticket['total'] for ticket in tickets)
    promedio_ticket = total_gastado / total_tickets if total_tickets > 0 else 0

    ultimos_tickets = list(reversed(tickets[-5:] if len(tickets) >= 5 else tickets[:]))

    return render_template('index.html',
                           tickets=ultimos_tickets,
                           total_tickets=total_tickets,
                           total_gastado=round(total_gastado, 2),
                           promedio_ticket=round(promedio_ticket, 2))


# ============================================================
# TICKETS - CRUD
# ============================================================

@app.route('/nuevo_ticket', methods=['GET', 'POST'])
def nuevo_ticket():
    if request.method == 'GET':
        categorias = compras.obtener_categorias_existentes()
        return render_template('nuevo_ticket.html', categorias=categorias)

    try:
        tienda = request.form.get('tienda')
        fecha = request.form.get('fecha')
        nombres = request.form.getlist('producto_nombre[]')
        precios = request.form.getlist('producto_precio[]')
        categorias = request.form.getlist('producto_categoria[]')
        observaciones = request.form.getlist('producto_observacion[]')

        if not tienda or not fecha:
            flash('Tienda y fecha son obligatorios', 'error')
            return redirect(url_for('nuevo_ticket'))

        if not nombres:
            flash('Debes agregar al menos un producto', 'error')
            return redirect(url_for('nuevo_ticket'))

        productos = []
        for i, nombre in enumerate(nombres):
            if nombre.strip():
                productos.append({
                    'id': i + 1,
                    'nombre': nombre.strip(),
                    'precio': float(precios[i]) if i < len(precios) and precios[i] else 0.0,
                    'categoria': categorias[i].strip() if i < len(categorias) and categorias[i] else None,
                    'observacion': observaciones[i].strip() if i < len(observaciones) and observaciones[i] else None
                })

        ticket_creado = compras.crear_ticket_desde_dict({'tienda': tienda, 'fecha': fecha, 'productos': productos})
        logger.info(f"Ticket creado: {tienda} - {len(productos)} productos")
        flash(f'Ticket creado: {tienda} - {len(productos)} productos - {ticket_creado["total"]:.2f}euro', 'success')
        return redirect(url_for('ver_tickets'))

    except Exception as e:
        logger.error(f"Error al crear ticket: {e}")
        flash(f'Error al crear ticket: {str(e)}', 'error')
        return redirect(url_for('nuevo_ticket'))


@app.route('/ver_tickets')
def ver_tickets():
    tickets = list(reversed(compras.tickets.copy()))
    return render_template('ver_tickets.html', tickets=tickets)


@app.route('/ticket/<ticket_id>')
def ver_ticket_detalle(ticket_id):
    ticket = compras.buscar_ticket_por_id(ticket_id)
    if not ticket:
        flash('Ticket no encontrado', 'error')
        return redirect(url_for('ver_tickets'))
    return render_template('ticket_detalle.html', ticket=ticket)


@app.route('/editar_ticket/<ticket_id>', methods=['GET', 'POST'])
def editar_ticket(ticket_id):
    ticket = compras.buscar_ticket_por_id(ticket_id)
    if not ticket:
        flash('Ticket no encontrado', 'error')
        return redirect(url_for('ver_tickets'))

    if request.method == 'GET':
        categorias = compras.obtener_categorias_existentes()
        return render_template('editar_ticket.html', ticket=ticket, categorias=categorias)

    try:
        ticket['tienda'] = request.form.get('tienda')
        ticket['fecha'] = request.form.get('fecha')

        nombres = request.form.getlist('producto_nombre[]')
        precios = request.form.getlist('producto_precio[]')
        categorias = request.form.getlist('producto_categoria[]')
        observaciones = request.form.getlist('producto_observacion[]')

        productos = []
        for i, nombre in enumerate(nombres):
            if nombre.strip():
                productos.append({
                    'id': i + 1,
                    'nombre': nombre.strip(),
                    'precio': float(precios[i]) if i < len(precios) else 0.0,
                    'categoria': categorias[i].strip() if i < len(categorias) and categorias[i] else None,
                    'observacion': observaciones[i].strip() if i < len(observaciones) and observaciones[i] else None
                })

        ticket['productos'] = productos
        ticket['total'] = round(sum(p['precio'] for p in productos), 2)
        compras.guardar_tickets()

        logger.info(f"Ticket editado: {ticket_id}")
        flash(f'Ticket actualizado: {ticket["tienda"]}', 'success')
        return redirect(url_for('ver_ticket_detalle', ticket_id=ticket_id))

    except Exception as e:
        logger.error(f"Error al editar ticket {ticket_id}: {e}")
        flash(f'Error al actualizar: {str(e)}', 'error')
        return redirect(url_for('editar_ticket', ticket_id=ticket_id))


@app.route('/eliminar_ticket/<ticket_id>', methods=['POST'])
def eliminar_ticket(ticket_id):
    ticket = compras.buscar_ticket_por_id(ticket_id)
    if not ticket:
        flash('Ticket no encontrado', 'error')
        return redirect(url_for('ver_tickets'))

    for i, t in enumerate(compras.tickets):
        if t['id'] == ticket_id:
            eliminado = compras.tickets.pop(i)
            compras.guardar_tickets()
            logger.info(f"Ticket eliminado: {ticket_id}")
            flash(f'Ticket eliminado: {eliminado["tienda"]}', 'success')
            break

    return redirect(url_for('ver_tickets'))


# ============================================================
# BUSQUEDA Y CATEGORIAS
# ============================================================

@app.route('/buscar_producto', methods=['GET', 'POST'])
def buscar_producto():
    if request.method == 'GET':
        return render_template('buscar_producto.html', resultados=None)

    nombre_busqueda = request.form.get('nombre_producto', '').strip().lower()
    if not nombre_busqueda:
        flash('Debes ingresar un nombre para buscar', 'error')
        return render_template('buscar_producto.html', resultados=None)

    resultados = []
    for ticket in compras.tickets:
        for producto in ticket.get('productos', []):
            if nombre_busqueda in producto['nombre'].lower():
                resultados.append({'ticket': ticket, 'producto': producto})

    return render_template('buscar_producto.html',
                           resultados=resultados,
                           nombre_busqueda=nombre_busqueda)


@app.route('/categorias')
def gestionar_categorias():
    categorias = compras.obtener_categorias_existentes()
    stats_categorias = {}

    for ticket in compras.tickets:
        for producto in ticket.get('productos', []):
            cat = producto.get('categoria') or 'Sin categoria'
            if cat not in stats_categorias:
                stats_categorias[cat] = {'cantidad': 0, 'total': 0.0}
            stats_categorias[cat]['cantidad'] += 1
            stats_categorias[cat]['total'] += producto['precio']

    return render_template('categorias.html', categorias=categorias, stats=stats_categorias)


# ============================================================
# ESTADISTICAS
# ============================================================

@app.route('/estadisticas')
def estadisticas_dashboard():
    estadisticas = EstadisticasFlask(compras)
    datos_tiendas = estadisticas.tienda_mas_gasto_datos()
    datos_generales = estadisticas.total_gastado_general_datos()
    return render_template('estadisticas.html',
                           datos_tiendas=datos_tiendas,
                           datos_generales=datos_generales)


@app.route('/estadisticas/tiendas')
def estadisticas_tiendas():
    estadisticas = EstadisticasFlask(compras)
    datos = estadisticas.tienda_mas_gasto_datos()
    return render_template('estadisticas_tiendas.html', datos=datos)


@app.route('/estadisticas/fechas', methods=['GET', 'POST'])
def estadisticas_fechas():
    if request.method == 'GET':
        return render_template('estadisticas_fechas.html', datos=None)

    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        flash('Debes especificar ambas fechas', 'error')
        return render_template('estadisticas_fechas.html', datos=None)

    estadisticas = EstadisticasFlask(compras)
    datos = estadisticas.gastos_por_rango_fechas_datos(fecha_inicio, fecha_fin)
    return render_template('estadisticas_fechas.html', datos=datos)


@app.route('/estadisticas/frecuencia', methods=['GET', 'POST'])
def estadisticas_frecuencia():
    if request.method == 'GET':
        return render_template('estadisticas_frecuencia.html', datos=None)

    nombre_producto = request.form.get('nombre_producto', '').strip()
    if not nombre_producto:
        flash('Debes ingresar un nombre de producto', 'error')
        return render_template('estadisticas_frecuencia.html', datos=None)

    estadisticas = EstadisticasFlask(compras)
    datos = estadisticas.frecuencia_producto_datos(nombre_producto)

    if not datos['compras']:
        flash(f'No se encontraron compras de "{nombre_producto}"', 'warning')

    return render_template('estadisticas_frecuencia.html', datos=datos)


# ============================================================
# API REST
# ============================================================

@app.route('/api/tickets')
def api_tickets():
    return jsonify(compras.tickets)


@app.route('/api/tickets/<ticket_id>')
def api_ticket(ticket_id):
    ticket = compras.buscar_ticket_por_id(ticket_id)
    if ticket:
        return jsonify(ticket)
    return jsonify({'error': 'Ticket no encontrado'}), 404


@app.route('/api/productos_categoria/<categoria>')
def api_productos_categoria(categoria):
    try:
        productos = compras.obtener_productos_por_categoria(categoria)
        return jsonify({'success': True, 'categoria': categoria, 'productos': productos, 'total': len(productos)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/estadisticas/resumen')
def api_estadisticas_resumen():
    estadisticas = EstadisticasFlask(compras)
    return jsonify({
        'total_gastado': estadisticas.total_gastado_general_datos(),
        'tiendas': estadisticas.tienda_mas_gasto_datos(),
    })


@app.route('/api/editar_producto', methods=['POST'])
def editar_producto_api():
    try:
        data = request.json
        required_fields = ['producto_id', 'ticket_id', 'nombre', 'precio', 'tienda', 'fecha']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Campo {field} es requerido'}), 400

        encontrado = False
        for ticket in compras.tickets:
            if ticket['id'] == data['ticket_id']:
                ticket['tienda'] = data['tienda']
                ticket['fecha'] = data['fecha']
                for producto in ticket['productos']:
                    if str(producto['id']) == str(data['producto_id']):
                        producto['nombre'] = data['nombre']
                        producto['precio'] = float(data['precio'])
                        if 'observacion' in data:
                            producto['observacion'] = data['observacion']
                        encontrado = True
                        break
                ticket['total'] = round(sum(p['precio'] for p in ticket['productos']), 2)
                break

        if not encontrado:
            return jsonify({'success': False, 'message': 'Producto o ticket no encontrado'})

        compras.guardar_tickets()
        logger.info(f"Producto {data['producto_id']} del ticket {data['ticket_id']} actualizado")
        return jsonify({'success': True, 'message': 'Producto actualizado correctamente'})

    except Exception as e:
        logger.error(f"Error en editar_producto_api: {e}")
        return jsonify({'success': False, 'message': f'Error del servidor: {str(e)}'}), 500


# ============================================================
# MANEJO DE ERRORES
# ============================================================

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_servidor(e):
    logger.error(f"Error 500: {e}")
    return render_template('500.html'), 500


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
