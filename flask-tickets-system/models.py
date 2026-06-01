"""
models.py - CLASES ADAPTADAS PARA FLASK
========================================
Aquí están tus clases ComprasMias y Estadisticas
adaptadas para trabajar con Flask (devuelven datos en lugar de imprimir)
"""

import json
import os
from datetime import datetime


class ComprasMiasFlask:
    """
    Versión adaptada de ComprasMias para Flask.
    
    Diferencias con la versión de consola:
    - Los métodos DEVUELVEN datos en lugar de print()
    - No usa input() (los datos vienen de formularios web)
    - Métodos adicionales para buscar/actualizar
    """
    
    def __init__(self):
        self.tickets = []
        self.archivo = 'solocompras.json'
        self.cargar_tickets()
    
    def cargar_tickets(self):
        """Carga los tickets desde el archivo JSON"""
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r', encoding='utf-8') as file:
                self.tickets = json.load(file)
            print(f"✅ {len(self.tickets)} tickets cargados")
        else:
            print("⚠️ Archivo no existe, se creará uno nuevo")
    
    def guardar_tickets(self):
        """Guarda los tickets en el archivo JSON"""
        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(self.tickets, file, ensure_ascii=False, indent=2)
    
    def obtener_categorias_existentes(self):
        """
        Obtiene todas las categorías existentes
        
        Retorna:
        --------
        set con las categorías únicas
        """
        categorias = set()
        for ticket in self.tickets:
            for producto in ticket.get('productos', []):
                cat = producto.get('categoria')
                if cat:
                    categorias.add(cat)
        return sorted(categorias)
    
    def obtener_productos_por_categoria(self, categoria):
        """
        Muestra productos de una categoría específica
        
        Parámetros:
        -----------
        categoria: str - categoría a buscar
        
        Retorna:
        --------
        list de dict con 'ticket' y 'producto' y precio, tienda, fecha, observacio
        """
        resultados = []
        categoria_lower = categoria.lower()
        
        for ticket in self.tickets:
            for producto in ticket.get('productos', []):
                if producto.get('categoria', '').lower() == categoria_lower:
                    resultados.append({
                        'nombre': producto['nombre'],
                        'ticket_id': ticket.get('id', ''),
                        
                        'fecha': ticket['fecha'],
                        'tienda': ticket['tienda'],
                        'observacion': producto.get('observacion', ''),
                        'precio': producto['precio'],
                    })

        return resultados 
    
    def crear_ticket_desde_dict(self, datos):
        """
        Crea un ticket desde un diccionario (datos del formulario web)
        
        Parámetros:
        -----------
        datos: dict con claves 'tienda', 'fecha', 'productos'
        
        Retorna:
        --------
        dict del ticket creado
        """
        # Calcular total
        total = sum(p['precio'] for p in datos['productos'])
        
        ticket = {
            'id': datos['tienda'] + "_" + datos['fecha'],
            'tienda': datos['tienda'],
            'fecha': datos['fecha'],
            'productos': datos['productos'],
            'total': round(total, 2)
        }
        
        self.tickets.append(ticket)
        self.guardar_tickets()
        
        return ticket
    
    def buscar_ticket_por_id(self, ticket_id):
        """
        Busca un ticket por su ID
        
        Parámetros:
        -----------
        ticket_id: str - ID del ticket
        
        Retorna:
        --------
        dict del ticket o None si no existe
        """
        for ticket in self.tickets:
            if ticket['id'] == ticket_id:
                return ticket
        return None
    
    def actualizar_ticket(self, ticket_id, nuevos_datos):
        """
        Actualiza un ticket existente
        
        Parámetros:
        -----------
        ticket_id: str - ID del ticket
        nuevos_datos: dict - Datos a actualizar
        
        Retorna:
        --------
        dict del ticket actualizado o None si no existe
        """
        ticket = self.buscar_ticket_por_id(ticket_id)
        if ticket:
            ticket.update(nuevos_datos)
            self.guardar_tickets()
            return ticket
        return None
    
    def buscar_productos_por_nombre(self, nombre):
        """
        Busca productos que contengan el nombre especificado
        
        Parámetros:
        -----------
        nombre: str - Nombre a buscar (búsqueda parcial)
        
        Retorna:
        --------
        list de dict con 'ticket' y 'producto'
        """
        resultados = []
        nombre_lower = nombre.lower()
        
        for ticket in self.tickets:
            for producto in ticket.get('productos', []):
                if nombre_lower in producto['nombre'].lower():
                    resultados.append({
                        'ticket': ticket,
                        'producto': producto
                    })
        
        return resultados


class EstadisticasFlask:
    """
    Versión adaptada de EstadisticasCompras para Flask.
    
    Diferencias:
    - Métodos DEVUELVEN datos (dict/list) en lugar de print()
    - Los datos se usan en templates HTML o como JSON para gráficos
    """
    
    def __init__(self, compras_instance):
        """
        Constructor
        
        Parámetros:
        -----------
        compras_instance: ComprasMiasFlask - instancia de ComprasMias
        """
        self.compras = compras_instance
        self.tickets = compras_instance.tickets
    
    def tienda_mas_gasto_datos(self):
        """
        Calcula el gasto por tienda
        
        Retorna:
        --------
        dict con:
        - 'tiendas': list de dict {'nombre', 'total', 'porcentaje'}
        - 'tienda_top': dict con la tienda donde más se ha gastado
        """
        diccionario_tiendas = {}
        
        # Sumar por tienda
        for ticket in self.tickets:
            tienda = ticket['tienda']
            total = ticket['total']
            
            if tienda not in diccionario_tiendas:
                diccionario_tiendas[tienda] = 0
            
            diccionario_tiendas[tienda] += total
        
        # Ordenar de mayor a menor
        tiendas_ordenadas = sorted(
            diccionario_tiendas.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Calcular total general para porcentajes
        total_general = sum(total for _, total in tiendas_ordenadas)
        
        # Preparar datos para devolver
        tiendas_lista = []
        for tienda, total in tiendas_ordenadas:
            porcentaje = (total / total_general * 100) if total_general > 0 else 0
            tiendas_lista.append({
                'nombre': tienda,
                'total': round(total, 2),
                'porcentaje': round(porcentaje, 1)
            })
        
        return {
            'tiendas': tiendas_lista,
            'tienda_top': tiendas_lista[0] if tiendas_lista else None,
            'total_general': round(total_general, 2)
        }
    
    def total_gastado_general_datos(self):
        """
        Calcula estadísticas generales de gasto
        
        Retorna:
        --------
        dict con:
        - 'total': float - Total gastado
        - 'num_tickets': int - Número de tickets
        - 'num_productos': int - Número de productos
        - 'promedio_ticket': float - Gasto promedio por ticket
        - 'promedio_producto': float - Gasto promedio por producto
        - 'ticket_mas_caro': dict - Ticket con mayor gasto
        - 'ticket_mas_barato': dict - Ticket con menor gasto
        """
        if not self.tickets:
            return {
                'total': 0,
                'num_tickets': 0,
                'num_productos': 0,
                'promedio_ticket': 0,
                'promedio_producto': 0,
                'ticket_mas_caro': None,
                'ticket_mas_barato': None
            }
        
        # Calcular totales
        total = sum(ticket['total'] for ticket in self.tickets)
        num_tickets = len(self.tickets)
        num_productos = sum(len(ticket['productos']) for ticket in self.tickets)
        
        promedio_ticket = total / num_tickets if num_tickets > 0 else 0
        promedio_producto = total / num_productos if num_productos > 0 else 0
        
        # Encontrar extremos
        ticket_mas_caro = max(self.tickets, key=lambda t: t['total'])
        ticket_mas_barato = min(self.tickets, key=lambda t: t['total'])
        
        return {
            'total': round(total, 2),
            'num_tickets': num_tickets,
            'num_productos': num_productos,
            'promedio_ticket': round(promedio_ticket, 2),
            'promedio_producto': round(promedio_producto, 2),
            'ticket_mas_caro': {
                'tienda': ticket_mas_caro['tienda'],
                'fecha': ticket_mas_caro['fecha'],
                'total': round(ticket_mas_caro['total'], 2)
            },
            'ticket_mas_barato': {
                'tienda': ticket_mas_barato['tienda'],
                'fecha': ticket_mas_barato['fecha'],
                'total': round(ticket_mas_barato['total'], 2)
            }
        }
    
    def gastos_por_rango_fechas_datos(self, fecha_inicio_str, fecha_fin_str):
        """
        Calcula gastos en un rango de fechas
        
        Parámetros:
        -----------
        fecha_inicio_str: str - Fecha inicio (YYYY-MM-DD)
        fecha_fin_str: str - Fecha fin (YYYY-MM-DD)
        
        Retorna:
        --------
        dict con:
        - 'fecha_inicio': str
        - 'fecha_fin': str
        - 'tickets': list - Tickets en el rango
        - 'total': float - Total gastado
        - 'num_tickets': int
        - 'promedio': float
        """
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
        except ValueError:
            return {
                'error': 'Formato de fecha inválido',
                'fecha_inicio': fecha_inicio_str,
                'fecha_fin': fecha_fin_str,
                'tickets': [],
                'total': 0,
                'num_tickets': 0,
                'promedio': 0
            }
        
        tickets_en_rango = []
        total = 0
        
        for ticket in self.tickets:
            try:
                # Extraer fecha del ticket (primeros 10 caracteres)
                fecha_ticket_str = ticket['fecha'][:10]
                fecha_ticket = datetime.strptime(fecha_ticket_str, "%Y-%m-%d")
                
                # Verificar si está en el rango
                if fecha_inicio <= fecha_ticket <= fecha_fin:
                    tickets_en_rango.append(ticket)
                    total += ticket['total']
            except (ValueError, IndexError):
                continue
        
        num_tickets = len(tickets_en_rango)
        promedio = total / num_tickets if num_tickets > 0 else 0
        
        return {
            'fecha_inicio': fecha_inicio_str,
            'fecha_fin': fecha_fin_str,
            'tickets': tickets_en_rango,
            'total': round(total, 2),
            'num_tickets': num_tickets,
            'promedio': round(promedio, 2)
        }
    
    def frecuencia_producto_datos(self, nombre_producto):
        """
        Analiza la frecuencia de compra de un producto
        
        Parámetros:
        -----------
        nombre_producto: str - Nombre del producto a buscar
        
        Retorna:
        --------
        dict con:
        - 'nombre_busqueda': str
        - 'compras': list - Lista de compras encontradas
        - 'frecuencia': int - Número de veces comprado
        - 'precio_promedio': float
        - 'precio_minimo': float
        - 'precio_maximo': float
        - 'tiendas_distintas': list - Tiendas donde se compró
        - 'tienda_mas_barata': dict
        """
        nombre_lower = nombre_producto.lower()
        compras = []
        
        # Buscar todas las compras del producto
        for ticket in self.tickets:
            for producto in ticket.get('productos', []):
                if nombre_lower in producto['nombre'].lower():
                    compras.append({
                        'fecha': ticket['fecha'],
                        'tienda': ticket['tienda'],
                        'precio': producto['precio'],
                        'nombre_completo': producto['nombre'],
                        'categoria': producto.get('categoria', 'Sin categoría'),
                        'observacion': producto.get('observacion', '')
                    })
        
        if not compras:
            return {
                'nombre_busqueda': nombre_producto,
                'compras': [],
                'frecuencia': 0,
                'precio_promedio': 0,
                'precio_minimo': 0,
                'precio_maximo': 0,
                'tiendas_distintas': [],
                'tienda_mas_barata': None
            }
        
        # Calcular estadísticas
        precios = [c['precio'] for c in compras]
        precio_promedio = sum(precios) / len(precios)
        precio_minimo = min(precios)
        precio_maximo = max(precios)
        
        # Tiendas distintas
        tiendas_set = set(c['tienda'] for c in compras)
        
        # Promedio por tienda
        precios_por_tienda = {}
        for compra in compras:
            tienda = compra['tienda']
            if tienda not in precios_por_tienda:
                precios_por_tienda[tienda] = []
            precios_por_tienda[tienda].append(compra['precio'])
        
        # Calcular promedio de cada tienda
        promedios_tiendas = {
            tienda: sum(precios) / len(precios)
            for tienda, precios in precios_por_tienda.items()
        }
        
        # Tienda más barata
        tienda_mas_barata = min(promedios_tiendas.items(), key=lambda x: x[1])
        
        # Ordenar compras por fecha (más reciente primero)
        compras_ordenadas = sorted(compras, key=lambda x: x['fecha'], reverse=True)
        
        return {
            'nombre_busqueda': nombre_producto,
            'compras': compras_ordenadas,
            'frecuencia': len(compras),
            'precio_promedio': round(precio_promedio, 2),
            'precio_minimo': round(precio_minimo, 2),
            'precio_maximo': round(precio_maximo, 2),
            'diferencia': round(precio_maximo - precio_minimo, 2),
            'tiendas_distintas': sorted(tiendas_set),
            'tienda_mas_barata': {
                'nombre': tienda_mas_barata[0],
                'promedio': round(tienda_mas_barata[1], 2)
            },
            'promedios_tiendas': {
                tienda: round(promedio, 2)
                for tienda, promedio in promedios_tiendas.items()
            }
        }
