# -*- coding: utf-8 -*-
"""
Interfaz gráfica para "Turtle" - Versión 1.0
Autor: G. José Rodríguez
"""
import turtle
import tkinter as tk
import os
import time
import math

class PaginaDibujo:
    def __init__(self, numero):
        self.numero = numero
        self.comandos = []
        self.estado = None

class TurtleEngine:
    def __init__(self):
        self.turtle = None
        self.screen = None
        self.canvas = None
        
        # Configuración del lienzo (501x501)
        self.ancho = 501
        self.alto = 501
        self.limite_x = 250
        self.limite_y = 250
        
        # Gestión de páginas
        self.paginas = [PaginaDibujo(1)]
        self.pagina_actual = 0
        self.total_paginas = 1
        
        self.estado_turtle = None
        self.velocidad = 100
        self.pixeles_por_segundo = 0
        self.animando = False
        self.pausado = False
        
        # Colores por defecto
        self.color_linea = (0, 0, 0)
        self.color_relleno = (255, 255, 255)
        
        # Estado de relleno
        self.en_relleno = False
        
        # Callback para el mouse
        self.callback_mouse = None
        
        # Cursores
        self.cursores = {1: "turtle", 2: "classic", 3: "circle", 4: "square",
                        5: "triangle", 6: "arrow", 7: "turtle", 8: "classic",
                        9: "circle", 10: "square", 11: "triangle", 12: "arrow",
                        13: "turtle", 14: "classic", 15: "circle", 16: "square",
                        17: "triangle", 18: "arrow", 19: "turtle", 20: "classic",
                        21: "circle", 22: "square", 23: "triangle", 24: "arrow",
                        25: "turtle"}
        self.cursor_actual = 1
        self.imagenes_cursores = {}
        self.cargar_cursores_imagenes()
        
    def cargar_cursores_imagenes(self):
        try:
            if os.path.exists("cursores"):
                for archivo in os.listdir("cursores"):
                    if archivo.endswith(".gif"):
                        nombre = archivo[:-4]
                        ruta = os.path.join("cursores", archivo)
                        self.imagenes_cursores[nombre] = ruta
        except:
            pass
    
    def _rgb_a_hex(self, r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _verificar_limites(self, x, y):
        epsilon = 1e-9
        if abs(x) <= self.limite_x + epsilon and abs(y) <= self.limite_y + epsilon:
            return True
        return False
    
    def _distancia_hasta_borde(self, x, y, angulo):
        dx = math.cos(angulo)
        dy = math.sin(angulo)
        
        distancias = []
        if dx > 0:
            distancias.append((self.limite_x - x) / dx)
        elif dx < 0:
            distancias.append((-self.limite_x - x) / dx)
        else:
            distancias.append(float('inf'))
        
        if dy > 0:
            distancias.append((self.limite_y - y) / dy)
        elif dy < 0:
            distancias.append((-self.limite_y - y) / dy)
        else:
            distancias.append(float('inf'))
        
        distancias_positivas = [d for d in distancias if d > 0]
        if not distancias_positivas:
            return 0
        
        distancia_maxima = min(distancias_positivas)
        return distancia_maxima
    
    def _mover_con_velocidad(self, distancia, direccion):
        if self.pixeles_por_segundo == 0:
            if direccion == "adelante":
                self.turtle.forward(distancia)
            else:
                self.turtle.backward(distancia)
            self.screen.update()
            return
        
        tiempo_por_pixel = 1.0 / self.pixeles_por_segundo
        pasos = int(abs(distancia))
        if pasos == 0:
            return
        
        paso = 1 if distancia > 0 else -1
        for _ in range(pasos):
            if direccion == "adelante":
                self.turtle.forward(paso)
            else:
                self.turtle.backward(paso)
            time.sleep(tiempo_por_pixel)
    
    def get_canvas(self, parent):
        self.canvas = tk.Canvas(parent, width=self.ancho, height=self.alto, bg="white", highlightthickness=1, highlightbackground="#cccccc")
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("white")
        self.screen.colormode(255)
        
        for nombre, ruta in self.imagenes_cursores.items():
            try:
                self.screen.addshape(ruta)
            except:
                pass
        
        self.turtle = turtle.RawTurtle(self.screen)
        self.turtle.shape("turtle")
        self.turtle.speed(0)
        self.turtle.pensize(2)
        self.turtle.pendown()
        
        color_hex = self._rgb_a_hex(*self.color_linea)
        relleno_hex = self._rgb_a_hex(*self.color_relleno)
        self.turtle.color(color_hex, relleno_hex)
        
        self.guardar_estado()
        
        # Configurar eventos de mouse si ya hay un callback
        if hasattr(self, 'callback_mouse') and self.callback_mouse:
            self.configurar_eventos_mouse(self.callback_mouse)
        
        return self.canvas
    
    def guardar_estado(self):
        try:
            self.estado_turtle = {
                'posicion': self.turtle.position(),
                'angulo': self.turtle.heading(),
                'color_linea': self.turtle.pencolor(),
                'color_relleno': self.turtle.fillcolor(),
                'lapiz_abajo': self.turtle.isdown(),
                'cursor': self.turtle.shape()
            }
            return True
        except:
            return False
    
    def restaurar_estado(self, estado):
        try:
            self.turtle.penup()
            self.turtle.setposition(estado['posicion'][0], estado['posicion'][1])
            self.turtle.setheading(estado['angulo'])
            self.turtle.pencolor(estado['color_linea'])
            self.turtle.fillcolor(estado['color_relleno'])
            self.turtle.color(estado['color_linea'], estado['color_relleno'])
            self.turtle.shape(estado['cursor'])
            if estado['lapiz_abajo']:
                self.turtle.pendown()
            else:
                self.turtle.penup()
            return True
        except:
            return False
    
    def set_velocidad(self, porcentaje):
        self.velocidad = porcentaje
        
        if porcentaje == 25:
            self.pixeles_por_segundo = 20
        elif porcentaje == 50:
            self.pixeles_por_segundo = 100
        elif porcentaje == 75:
            self.pixeles_por_segundo = 200
        else:
            self.pixeles_por_segundo = 0
        
        if self.pixeles_por_segundo == 0:
            self.turtle.speed(0)
        else:
            self.turtle.speed(6)
        
        self.screen.update()
        return f"Velocidad ajustada a {porcentaje}% ({self.pixeles_por_segundo} px/s)"
    
    # --- Comandos de movimiento ---
    def adelante(self, pixeles):
        x, y = self.turtle.position()
        angulo = math.radians(self.turtle.heading())
        nuevo_x = x + pixeles * math.cos(angulo)
        nuevo_y = y + pixeles * math.sin(angulo)
        
        if self._verificar_limites(nuevo_x, nuevo_y):
            if self.pixeles_por_segundo == 0:
                self.turtle.forward(pixeles)
                self.screen.update()
                return f"Avanza {pixeles} píxeles (instantáneo)"
            else:
                self._mover_con_velocidad(pixeles, "adelante")
                return f"Avanza {pixeles} píxeles"
        else:
            distancia_maxima = self._distancia_hasta_borde(x, y, angulo)
            if distancia_maxima > 1:
                if self.pixeles_por_segundo == 0:
                    self.turtle.forward(distancia_maxima)
                    self.screen.update()
                    return f"⚠️ Límite alcanzado. Avanza solo {distancia_maxima:.1f} píxeles (instantáneo)"
                else:
                    self._mover_con_velocidad(distancia_maxima, "adelante")
                    return f"⚠️ Límite alcanzado. Avanza solo {distancia_maxima:.1f} píxeles."
            else:
                return f"⚠️ Ya estás en el borde. No se puede avanzar más."
    
    def atras(self, pixeles):
        x, y = self.turtle.position()
        angulo = math.radians(self.turtle.heading())
        nuevo_x = x - pixeles * math.cos(angulo)
        nuevo_y = y - pixeles * math.sin(angulo)
        
        if self._verificar_limites(nuevo_x, nuevo_y):
            if self.pixeles_por_segundo == 0:
                self.turtle.backward(pixeles)
                self.screen.update()
                return f"Retrocede {pixeles} píxeles (instantáneo)"
            else:
                self._mover_con_velocidad(pixeles, "atras")
                return f"Retrocede {pixeles} píxeles"
        else:
            angulo_opuesto = math.radians(self.turtle.heading() + 180)
            distancia_maxima = self._distancia_hasta_borde(x, y, angulo_opuesto)
            if distancia_maxima > 1:
                if self.pixeles_por_segundo == 0:
                    self.turtle.backward(distancia_maxima)
                    self.screen.update()
                    return f"⚠️ Límite alcanzado. Retrocede solo {distancia_maxima:.1f} píxeles (instantáneo)"
                else:
                    self._mover_con_velocidad(distancia_maxima, "atras")
                    return f"⚠️ Límite alcanzado. Retrocede solo {distancia_maxima:.1f} píxeles."
            else:
                return f"⚠️ Ya estás en el borde. No se puede retroceder más."
    
    def derecha(self, grados):
        self.turtle.right(grados)
        return f"Gira a la derecha {grados}°"
    
    def izquierda(self, grados):
        self.turtle.left(grados)
        return f"Gira a la izquierda {grados}°"
    
    def dibujar(self):
        self.turtle.pendown()
        return "Dibujo activado"
    
    def no_dibujar(self):
        self.turtle.penup()
        return "Dibujo desactivado"
    
    def subir_lapiz(self):
        self.turtle.penup()
        return "Lápiz levantado"
    
    def bajar_lapiz(self):
        self.turtle.pendown()
        return "Lápiz bajado"
    
    def set_color_linea(self, r, g, b):
        try:
            color_hex = self._rgb_a_hex(r, g, b)
            self.turtle.pencolor(color_hex)
            self.turtle.color(color_hex)
            self.color_linea = (r, g, b)
            return f"Color línea: RGB({r}, {g}, {b})"
        except Exception as e:
            return f"Error al cambiar color: {str(e)}"
    
    def set_color_relleno(self, r, g, b):
        try:
            color_hex = self._rgb_a_hex(r, g, b)
            self.turtle.fillcolor(color_hex)
            color_linea_hex = self._rgb_a_hex(*self.color_linea)
            self.turtle.color(color_linea_hex, color_hex)
            self.color_relleno = (r, g, b)
            return f"Color relleno: RGB({r}, {g}, {b})"
        except Exception as e:
            return f"Error al cambiar color de relleno: {str(e)}"
    
    def pintar_cursor(self, r, g, b):
        try:
            pos = self.turtle.position()
            color_hex = self._rgb_a_hex(r, g, b)
            color_original = self.turtle.pencolor()
            relleno_original = self.turtle.fillcolor()
            self.turtle.color(color_hex)
            self.turtle.stamp()
            self.turtle.color(color_original, relleno_original)
            return f"Cursor pintado en ({pos[0]:.0f}, {pos[1]:.0f})"
        except Exception as e:
            return f"Error al pintar cursor: {str(e)}"
    
    def cambiar_cursor(self, numero):
        nombre_cursor = f"cursor{numero}"
        if nombre_cursor in self.imagenes_cursores:
            try:
                self.turtle.shape(self.imagenes_cursores[nombre_cursor])
                self.cursor_actual = numero
                return f"Cursor cambiado a {nombre_cursor}"
            except:
                pass
        
        forma = self.cursores.get(numero, "turtle")
        try:
            self.turtle.shape(forma)
            self.cursor_actual = numero
            return f"Cursor cambiado a {forma}"
        except Exception as e:
            return f"Error al cambiar cursor: {str(e)}"
    
    def centrar_tortuga(self):
        self.turtle.penup()
        self.turtle.home()
        self.turtle.pendown()
        return "Tortuga centrada"
    
    def clear(self):
        self.turtle.clear()
        self.turtle.penup()
        self.turtle.home()
        self.turtle.pendown()
        color_hex = self._rgb_a_hex(*self.color_linea)
        relleno_hex = self._rgb_a_hex(*self.color_relleno)
        self.turtle.color(color_hex, relleno_hex)
        return "Lienzo limpiado"
    
    def get_position(self):
        return (self.turtle.xcor(), self.turtle.ycor())
    
    def get_angle(self):
        return self.turtle.heading()
    
    def ir_a(self, x, y):
        if not self._verificar_limites(x, y):
            return f"⚠️ Posición ({x}, {y}) fuera de los límites (±{self.limite_x}, ±{self.limite_y})"
        
        lapiz_abajo = self.turtle.isdown()
        self.turtle.penup()
        self.turtle.goto(x, y)
        if lapiz_abajo:
            self.turtle.pendown()
        
        self.screen.update()
        return f"📍 Movido a posición ({x}, {y})"
    
    # --- COMANDOS DE RELLENO ---
    def iniciar_relleno(self):
        self.turtle.begin_fill()
        self.en_relleno = True
        return "🔴 Relleno iniciado - dibuja la figura y luego usa TERMINAR_RELLENO"
    
    def terminar_relleno(self):
        if not self.en_relleno:
            return "⚠️ No hay un relleno activo. Usa INICIAR_RELLENO primero."
        self.turtle.end_fill()
        self.en_relleno = False
        return f"✅ Relleno aplicado con color RGB({int(self.color_relleno[0]*255)}, {int(self.color_relleno[1]*255)}, {int(self.color_relleno[2]*255)})"
    
    # --- EVENTOS DE MOUSE (CORREGIDOS) ---
    def configurar_eventos_mouse(self, callback_coordenadas):
        """
        Configura eventos de mouse para mostrar coordenadas.
        callback_coordenadas: función que recibe (x, y) cuando el mouse se mueve
        """
        self.callback_mouse = callback_coordenadas
        
        if self.canvas:
            # Bindear el movimiento del mouse directamente al canvas de Tkinter
            self.canvas.bind('<Motion>', self._on_mouse_move_wrapper)
            self.canvas.bind('<Leave>', self._on_mouse_leave_wrapper)

    def _on_mouse_move_wrapper(self, event):
        """Wrapper para el movimiento del mouse."""
        if hasattr(self, 'callback_mouse') and self.callback_mouse:
            x, y = self._canvas_to_turtle(event.x, event.y)
            if x is not None and y is not None:
                self.callback_mouse(x, y)
            else:
                self.callback_mouse(None, None)

    def _on_mouse_leave_wrapper(self, event):
        """Cuando el mouse sale del canvas."""
        if hasattr(self, 'callback_mouse') and self.callback_mouse:
            self.callback_mouse(None, None)

    def _canvas_to_turtle(self, canvas_x, canvas_y):
        """Convierte coordenadas de canvas a coordenadas de Turtle."""
        try:
            ancho = int(self.canvas.cget('width'))
            alto = int(self.canvas.cget('height'))
            
            if ancho == 0 or alto == 0:
                return None, None
            
            turtle_x = (canvas_x / ancho) * 500 - 250
            turtle_y = 250 - (canvas_y / alto) * 500
            
            # Redondear a enteros
            turtle_x = round(turtle_x)
            turtle_y = round(turtle_y)
            
            if -250 <= turtle_x <= 250 and -250 <= turtle_y <= 250:
                return turtle_x, turtle_y
            else:
                return None, None
        except Exception:
            return None, None
    
    # --- Funciones de páginas ---
    def nueva_pagina(self):
        self.guardar_estado()
        nueva = PaginaDibujo(self.total_paginas + 1)
        self.paginas.append(nueva)
        self.total_paginas += 1
        self.pagina_actual = len(self.paginas) - 1
        self.limpiar_pagina_actual()
        return self.pagina_actual
    
    def ir_a_pagina(self, indice):
        if 0 <= indice < len(self.paginas):
            self.guardar_estado()
            self.paginas[self.pagina_actual].comandos = self.comandos_actuales()
            self.pagina_actual = indice
            self.limpiar_pagina_actual()
            return True
        return False
    
    def comandos_actuales(self):
        return []
    
    def limpiar_pagina_actual(self):
        self.turtle.clear()
        self.turtle.penup()
        self.turtle.home()
        self.turtle.pendown()
        color_hex = self._rgb_a_hex(*self.color_linea)
        relleno_hex = self._rgb_a_hex(*self.color_relleno)
        self.turtle.color(color_hex, relleno_hex)
        if self.paginas[self.pagina_actual].estado:
            self.restaurar_estado(self.paginas[self.pagina_actual].estado)
    
    def eliminar_pagina(self, indice):
        if len(self.paginas) <= 1:
            return False
        if 0 <= indice < len(self.paginas):
            del self.paginas[indice]
            self.total_paginas -= 1
            if self.pagina_actual >= len(self.paginas):
                self.pagina_actual = len(self.paginas) - 1
            self.ir_a_pagina(self.pagina_actual)
            return True
        return False
    
    def esperar(self, milisegundos):
        time.sleep(milisegundos / 1000)
        return f"Espera de {milisegundos}ms"
    
    def guardar_proyecto(self, archivo):
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                for i, pagina in enumerate(self.paginas):
                    f.write(f"=== PAGINA {i+1} ===\n")
                    for comando in pagina.comandos:
                        f.write(comando + '\n')
                    f.write("\n")
            return True
        except Exception as e:
            return str(e)
    
    def cargar_proyecto(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            self.paginas = []
            self.total_paginas = 0
            
            bloques = contenido.split('=== PAGINA ')
            for bloque in bloques:
                if not bloque.strip():
                    continue
                lineas = bloque.strip().split('\n')
                if lineas and lineas[0].strip().endswith('==='):
                    pagina = PaginaDibujo(self.total_paginas + 1)
                    for linea in lineas[1:]:
                        if linea.strip():
                            pagina.comandos.append(linea.strip())
                    self.paginas.append(pagina)
                    self.total_paginas += 1
            
            if not self.paginas:
                self.paginas = [PaginaDibujo(1)]
                self.total_paginas = 1
            
            self.pagina_actual = 0
            self.limpiar_pagina_actual()
            self.set_velocidad(100)
            
            return True
        except Exception as e:
            return str(e)