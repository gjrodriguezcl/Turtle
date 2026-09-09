# -*- coding: utf-8 -*-
"""
Interfaz gráfica para "Turtle" - Versión 1.0
Autor: G. José Rodríguez
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import sys
import threading
import time

from turtle_engine import TurtleEngine
from command_parser import CommandParser
from help_menu import mostrar_ayuda

class DibujaConCodigo:
    def __init__(self, root):
        self.root = root
        self.root.title("🐢 Turtle")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Variables de estado
        self.comandos_actuales = {}
        self.pagina_actual = 1
        self.total_paginas = 1
        self.archivo_actual = None
        
        # Variables de animación
        self.animando = False
        self.velocidad_animacion = 100
        
        # Inicializar motor y parser
        self.turtle_engine = TurtleEngine()
        self.parser = CommandParser(self.turtle_engine)
        
        # Crear la interfaz
        self.crear_menu_principal()
        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        self.crear_barra_estado()
        
        # Configurar grid (18%-82%)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=18)
        self.root.grid_columnconfigure(1, weight=82)
        
        # Inicializar página 1
        self.comandos_actuales[1] = []
        self.actualizar_lista_comandos()
        self.actualizar_info_paginas()
        
        # Aplicar velocidad inicial 100%
        self.turtle_engine.set_velocidad(100)
        self.label_velocidad.config(text="100%")
        self._actualizar_botones_velocidad(100)
    
    def crear_menu_principal(self):
        """Crea la barra de menú superior."""
        frame_menu = tk.Frame(self.root, bg="#2c3e50", relief=tk.RAISED, bd=2)
        frame_menu.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        estilo_boton = {"bg": "#34495e", "fg": "white", "font": ("Segoe UI", 9), 
                       "relief": tk.RAISED, "bd": 1, "padx": 8, "pady": 3}
        
        # Grupo: Archivo
        btn_nuevo = tk.Button(frame_menu, text="📄 Nuevo", command=self.nuevo_proyecto, **estilo_boton)
        btn_nuevo.pack(side=tk.LEFT, padx=2)
        
        btn_abrir = tk.Button(frame_menu, text="📂 Abrir", command=self.abrir_proyecto, **estilo_boton)
        btn_abrir.pack(side=tk.LEFT, padx=2)
        
        btn_guardar = tk.Button(frame_menu, text="💾 Guardar", command=self.guardar_proyecto, **estilo_boton)
        btn_guardar.pack(side=tk.LEFT, padx=2)
        
        tk.Frame(frame_menu, width=2, bg="#7f8c8d").pack(side=tk.LEFT, padx=8, fill=tk.Y)
        
        # Grupo: Ejecución
        btn_ejecutar = tk.Button(frame_menu, text="▶️ Ejecutar", command=self.ejecutar_pagina, 
                               bg="#27ae60", fg="white", font=("Segoe UI", 9, "bold"),
                               relief=tk.RAISED, bd=1, padx=8, pady=3)
        btn_ejecutar.pack(side=tk.LEFT, padx=2)
        
        btn_paso = tk.Button(frame_menu, text="⏭️ Paso", command=self.ejecutar_paso_a_paso,
                           bg="#8e44ad", fg="white", font=("Segoe UI", 9),
                           relief=tk.RAISED, bd=1, padx=8, pady=3)
        btn_paso.pack(side=tk.LEFT, padx=2)
        
        btn_animar = tk.Button(frame_menu, text="🎬 Animar", command=self.animar_proyecto,
                             bg="#e67e22", fg="white", font=("Segoe UI", 9, "bold"),
                             relief=tk.RAISED, bd=1, padx=8, pady=3)
        btn_animar.pack(side=tk.LEFT, padx=2)
        
        btn_detener = tk.Button(frame_menu, text="⏹️ Detener", command=self.detener_animacion,
                              bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"),
                              relief=tk.RAISED, bd=1, padx=8, pady=3)
        btn_detener.pack(side=tk.LEFT, padx=2)
        
        tk.Frame(frame_menu, width=2, bg="#7f8c8d").pack(side=tk.LEFT, padx=8, fill=tk.Y)
        
        # Grupo: Limpiar
        btn_limpiar_todo = tk.Button(frame_menu, text="🧹 Todo", command=self.limpiar_todo,
                                   bg="#c0392b", fg="white", font=("Segoe UI", 9, "bold"),
                                   relief=tk.RAISED, bd=1, padx=8, pady=3)
        btn_limpiar_todo.pack(side=tk.LEFT, padx=2)
        
        btn_limpiar_lienzo = tk.Button(frame_menu, text="🧹 Lienzo", command=self.limpiar_lienzo,
                                     bg="#95a5a6", fg="white", font=("Segoe UI", 9),
                                     relief=tk.RAISED, bd=1, padx=8, pady=3)
        btn_limpiar_lienzo.pack(side=tk.LEFT, padx=2)
        
        btn_centrar = tk.Button(frame_menu, text="🎯 Centrar", command=self.centrar_tortuga,
                              bg="#3498db", fg="white", font=("Segoe UI", 9, "bold"),
                              relief=tk.RAISED, bd=1, padx=8, pady=3)
        btn_centrar.pack(side=tk.LEFT, padx=2)
        
        btn_ayuda = tk.Button(frame_menu, text="❓ Ayuda", command=self.mostrar_ayuda,
                            bg="#f39c12", fg="white", font=("Segoe UI", 9),
                            relief=tk.RAISED, bd=1, padx=8, pady=3)
        btn_ayuda.pack(side=tk.RIGHT, padx=2)
    
    def crear_panel_izquierdo(self):
        """Crea el panel izquierdo con comandos (18% del ancho)."""
        frame_izquierdo = tk.Frame(self.root, bg="#ecf0f1", relief=tk.SUNKEN, bd=2)
        frame_izquierdo.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        frame_izquierdo.grid_rowconfigure(3, weight=1)
        frame_izquierdo.grid_columnconfigure(0, weight=1)
        
        # Título
        tk.Label(frame_izquierdo, text="📝 Comandos", font=("Segoe UI", 12, "bold"),
                bg="#ecf0f1", fg="#2c3e50").grid(row=0, column=0, pady=6)
        
        # Campo de entrada
        frame_entrada = tk.Frame(frame_izquierdo, bg="#ecf0f1")
        frame_entrada.grid(row=1, column=0, sticky="ew", padx=5, pady=4)
        
        self.entry_comando = tk.Entry(frame_entrada, font=("Courier", 11),
                                     relief=tk.SUNKEN, bd=2)
        self.entry_comando.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        self.entry_comando.bind("<Return>", self.enviar_comando)
        
        btn_enviar = tk.Button(frame_entrada, text="▶ Enviar", command=self.enviar_comando,
                              bg="#3498db", fg="white", font=("Segoe UI", 9, "bold"),
                              relief=tk.RAISED, bd=2, padx=10, pady=4)
        btn_enviar.pack(side=tk.RIGHT)
        
        # Controles de página
        frame_paginas = tk.Frame(frame_izquierdo, bg="#ecf0f1", relief=tk.RAISED, bd=1)
        frame_paginas.grid(row=2, column=0, sticky="ew", padx=5, pady=4)
        
        tk.Label(frame_paginas, text="📄 Página", font=("Segoe UI", 9),
                bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=4)
        
        btn_anterior = tk.Button(frame_paginas, text="◄", command=self.pagina_anterior,
                               bg="#95a5a6", fg="white", font=("Segoe UI", 9, "bold"),
                               relief=tk.RAISED, bd=1, padx=8, pady=2)
        btn_anterior.pack(side=tk.LEFT, padx=2)
        
        self.label_pagina = tk.Label(frame_paginas, text="1/1", font=("Segoe UI", 10, "bold"),
                                   bg="#ecf0f1", fg="#2c3e50", width=5)
        self.label_pagina.pack(side=tk.LEFT, padx=6)
        
        btn_siguiente = tk.Button(frame_paginas, text="►", command=self.pagina_siguiente,
                               bg="#95a5a6", fg="white", font=("Segoe UI", 9, "bold"),
                               relief=tk.RAISED, bd=1, padx=8, pady=2)
        btn_siguiente.pack(side=tk.LEFT, padx=2)
        
        btn_nueva = tk.Button(frame_paginas, text="➕ Nueva", command=self.nueva_pagina,
                            bg="#27ae60", fg="white", font=("Segoe UI", 8),
                            relief=tk.RAISED, bd=1, padx=6, pady=2)
        btn_nueva.pack(side=tk.LEFT, padx=2)
        
        btn_eliminar = tk.Button(frame_paginas, text="✖", command=self.eliminar_pagina,
                               bg="#e74c3c", fg="white", font=("Segoe UI", 8),
                               relief=tk.RAISED, bd=1, padx=6, pady=2)
        btn_eliminar.pack(side=tk.LEFT, padx=2)
        
        # Lista de comandos
        self.text_comandos = scrolledtext.ScrolledText(frame_izquierdo, font=("Courier", 9),
                                                      bg="#ffffff", fg="#2c3e50",
                                                      relief=tk.SUNKEN, bd=2,
                                                      height=10, state='disabled')
        self.text_comandos.grid(row=3, column=0, sticky="nsew", padx=5, pady=4)
        
        # Botones de control de lista
        frame_botones_lista = tk.Frame(frame_izquierdo, bg="#ecf0f1")
        frame_botones_lista.grid(row=4, column=0, sticky="ew", padx=5, pady=3)
        
        btn_eliminar_ultimo = tk.Button(frame_botones_lista, text="🗑️ Eliminar último",
                                      command=self.eliminar_ultimo_comando,
                                      bg="#e67e22", fg="white", font=("Segoe UI", 8),
                                      relief=tk.RAISED, bd=1, padx=6, pady=2)
        btn_eliminar_ultimo.pack(side=tk.LEFT, padx=2)
        
        btn_limpiar_lista = tk.Button(frame_botones_lista, text="🧹 Limpiar lista",
                                    command=self.limpiar_lista_comandos,
                                    bg="#95a5a6", fg="white", font=("Segoe UI", 8),
                                    relief=tk.RAISED, bd=1, padx=6, pady=2)
        btn_limpiar_lista.pack(side=tk.LEFT, padx=2)
        
        # Control de velocidad
        frame_velocidad = tk.Frame(frame_izquierdo, bg="#ecf0f1")
        frame_velocidad.grid(row=5, column=0, sticky="ew", padx=5, pady=4)
        
        tk.Label(frame_velocidad, text="🐢 Velocidad", font=("Segoe UI", 9, "bold"),
                bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=4)
        
        velocidades = [("25%", 25), ("50%", 50), ("75%", 75), ("100%", 100)]
        for texto, valor in velocidades:
            btn = tk.Button(frame_velocidad, text=texto, 
                           command=lambda v=valor: self.cambiar_velocidad_fija(v),
                           bg="#3498db" if valor == 100 else "#95a5a6",
                           fg="white", font=("Segoe UI", 8, "bold"),
                           relief=tk.RAISED, bd=1, padx=6, pady=2,
                           width=4)
            btn.pack(side=tk.LEFT, padx=2)
        
        self.label_velocidad = tk.Label(frame_velocidad, text="100%", 
                                      font=("Segoe UI", 9, "bold"),
                                      bg="#ecf0f1", fg="#2c3e50", width=5)
        self.label_velocidad.pack(side=tk.LEFT, padx=4)
    
    def crear_panel_derecho(self):
        """Crea el panel derecho con el lienzo de dibujo centrado."""
        frame_derecho = tk.Frame(self.root, bg="#d0d0d0", relief=tk.SUNKEN, bd=3)
        frame_derecho.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_derecho.grid_rowconfigure(0, weight=1)
        frame_derecho.grid_columnconfigure(0, weight=1)
        
        # Frame interno para centrar el canvas
        frame_interno = tk.Frame(frame_derecho, bg="#d0d0d0")
        frame_interno.grid(row=0, column=0, sticky="nsew")
        frame_interno.grid_rowconfigure(0, weight=1)
        frame_interno.grid_columnconfigure(0, weight=1)
        
        # Canvas centrado
        self.canvas_turtle = self.turtle_engine.get_canvas(frame_interno)
        self.canvas_turtle.pack(expand=True)
        self.canvas_turtle.config(relief=tk.SUNKEN, bd=2)
    
    def crear_barra_estado(self):
        """Crea la barra de estado en la parte inferior."""
        frame_estado = tk.Frame(self.root, bg="#ecf0f1", relief=tk.SUNKEN, bd=1)
        frame_estado.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Estado general (izquierda)
        self.label_estado = tk.Label(frame_estado, text="✅ Listo", font=("Segoe UI", 9),
                                bg="#ecf0f1", fg="#2c3e50")
        self.label_estado.pack(side=tk.LEFT, padx=10)
        
        # Posición de la tortuga (enteros)
        self.label_posicion = tk.Label(frame_estado, text="📌 Tortuga: (0, 0) | Ángulo: 0°",
                                    font=("Segoe UI", 9), bg="#ecf0f1", fg="#2c3e50")
        self.label_posicion.pack(side=tk.LEFT, padx=20)
        
        # Coordenadas del mouse (derecha)
        self.label_coordenadas_mouse = tk.Label(frame_estado, text="🖱️ Mouse: (---, ---)",
                                            font=("Segoe UI", 9), bg="#ecf0f1", fg="#e67e22")
        self.label_coordenadas_mouse.pack(side=tk.RIGHT, padx=10)
        
        # Función para actualizar coordenadas del mouse (con enteros)
        def actualizar_coordenadas_mouse(x, y):
            if self.label_coordenadas_mouse:
                if x is not None and y is not None:
                    self.label_coordenadas_mouse.config(text=f"🖱️ Mouse: ({int(x)}, {int(y)})")
                else:
                    self.label_coordenadas_mouse.config(text="🖱️ Mouse: (---, ---)")
        
        # Configurar eventos del mouse en el motor
        if hasattr(self.turtle_engine, 'configurar_eventos_mouse'):
            self.turtle_engine.configurar_eventos_mouse(actualizar_coordenadas_mouse)
        
        # Iniciar actualización de posición de la tortuga
        self.actualizar_estado()
    
    def actualizar_estado(self):
        """Actualiza la barra de estado con la posición de la tortuga."""
        try:
            pos = self.turtle_engine.get_position()
            angulo = self.turtle_engine.get_angle()
            self.label_posicion.config(text=f"📌 Tortuga: ({pos[0]:.0f}, {pos[1]:.0f}) | Ángulo: {angulo:.0f}°")
        except:
            pass
        self.root.after(500, self.actualizar_estado)
    
    def actualizar_info_paginas(self):
        self.label_pagina.config(text=f"{self.pagina_actual}/{self.total_paginas}")
        self.root.title(f"🐢 Dibuja con Código - Página {self.pagina_actual} de {self.total_paginas}")
    
    def actualizar_lista_comandos(self):
        self.text_comandos.config(state='normal')
        self.text_comandos.delete(1.0, tk.END)
        if self.pagina_actual in self.comandos_actuales:
            for comando in self.comandos_actuales[self.pagina_actual]:
                self.text_comandos.insert(tk.END, f"> {comando}\n")
        self.text_comandos.see(tk.END)
        self.text_comandos.config(state='disabled')
    
    # --- Funciones de comandos ---
    def _dividir_comandos(self, linea):
        """Divide una línea con múltiples comandos."""
        comandos_conocidos = [
            'AD', 'AT', 'DE', 'IZ', 'LCOLOR', 'FCOLOR', 'FCURSOR',
            'CCURSOR', 'VEL', 'VELOCIDAD', 'ESPERAR', 'DIB', 'NODIB',
            'SUBIR', 'BAJAR', 'BORRAR', 'PAGINA', 'NUEVA_PAGINA',
            'SIGUIENTE_PAGINA', 'ANTERIOR_PAGINA', 'REPETIR', 'GOTO', 'IR'
        ]
        
        if not linea:
            return []
        
        # Si la línea comienza con REPETIR, GOTO o IR, no la dividimos
        if linea.upper().startswith("REPETIR ") or linea.upper().startswith("GOTO ") or linea.upper().startswith("IR "):
            return [linea.upper()]
        
        if ' ' not in linea:
            return [linea]
        
        resultado = []
        partes = linea.split()
        i = 0
        
        while i < len(partes):
            encontrado = False
            for cmd in comandos_conocidos:
                if partes[i].upper() == cmd:
                    if cmd in ['LCOLOR', 'FCOLOR', 'FCURSOR']:
                        if i + 3 < len(partes):
                            resultado.append(' '.join(partes[i:i+4]))
                            i += 4
                            encontrado = True
                            break
                    elif cmd in ['VEL', 'VELOCIDAD', 'ESPERAR']:
                        if i + 1 < len(partes):
                            resultado.append(' '.join(partes[i:i+2]))
                            i += 2
                            encontrado = True
                            break
                    elif cmd in ['AD', 'AT', 'DE', 'IZ', 'CCURSOR', 'PAGINA']:
                        if i + 1 < len(partes):
                            resultado.append(' '.join(partes[i:i+2]))
                            i += 2
                            encontrado = True
                            break
                    elif cmd in ['REPETIR', 'GOTO', 'IR']:
                        comando_completo = ' '.join(partes[i:])
                        resultado.append(comando_completo.upper())
                        i = len(partes)
                        encontrado = True
                        break
                    else:
                        resultado.append(partes[i])
                        i += 1
                        encontrado = True
                        break
            
            if not encontrado:
                i += 1
        
        return resultado if resultado else [linea]
    
    def enviar_comando(self, event=None):
        comando = self.entry_comando.get().strip()
        if not comando:
            return
        
        comandos = self._dividir_comandos(comando)
        
        for cmd in comandos:
            if self.pagina_actual not in self.comandos_actuales:
                self.comandos_actuales[self.pagina_actual] = []
            self.comandos_actuales[self.pagina_actual].append(cmd)
            self.ejecutar_comando_individual(cmd)
        
        self.entry_comando.delete(0, tk.END)
        self.actualizar_lista_comandos()
    
    def ejecutar_comando_individual(self, comando):
        try:
            resultado = self.parser.ejecutar(comando)
            self.label_estado.config(text=f"✅ {resultado}")
        except Exception as e:
            self.label_estado.config(text=f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Error en el comando:\n{comando}\n\n{str(e)}")
    
    def ejecutar_pagina(self):
        if self.pagina_actual not in self.comandos_actuales or not self.comandos_actuales[self.pagina_actual]:
            messagebox.showinfo("Información", "No hay comandos en esta página.")
            return
        
        self.turtle_engine.set_velocidad(self.velocidad_animacion)
        self.turtle_engine.clear()
        self.label_estado.config(text="🔄 Ejecutando página...")
        errores = []
        
        for i, comando in enumerate(self.comandos_actuales[self.pagina_actual]):
            try:
                self.parser.ejecutar(comando)
                self.root.update()
            except Exception as e:
                errores.append(f"Línea {i+1}: {comando} → Error: {str(e)}")
        
        if errores:
            messagebox.showerror("Errores", "\n".join(errores))
            self.label_estado.config(text="❌ Error en algunos comandos")
        else:
            self.label_estado.config(text="✅ Página ejecutada correctamente")
    
    def ejecutar_paso_a_paso(self):
        if self.pagina_actual not in self.comandos_actuales or not self.comandos_actuales[self.pagina_actual]:
            messagebox.showinfo("Información", "No hay comandos en esta página.")
            return
        
        self.turtle_engine.set_velocidad(self.velocidad_animacion)
        self.turtle_engine.clear()
        self.label_estado.config(text="🔄 Ejecutando paso a paso...")
        
        for i, comando in enumerate(self.comandos_actuales[self.pagina_actual]):
            try:
                self.parser.ejecutar(comando)
                self.root.update()
                time.sleep(0.5)
            except Exception as e:
                messagebox.showerror("Error", f"Error en comando {i+1}: {comando}\n\n{str(e)}")
                break
        
        self.label_estado.config(text="✅ Paso a paso completado")
    
    # --- Funciones de velocidad ---
    def cambiar_velocidad_fija(self, porcentaje):
        self.velocidad_animacion = porcentaje
        self.label_velocidad.config(text=f"{porcentaje}%")
        resultado = self.turtle_engine.set_velocidad(porcentaje)
        self.label_estado.config(text=f"🐢 {resultado}")
        self._actualizar_botones_velocidad(porcentaje)
    
    def _actualizar_botones_velocidad(self, porcentaje):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for frame_child in widget.winfo_children():
                    if isinstance(frame_child, tk.Frame):
                        for btn in frame_child.winfo_children():
                            if isinstance(btn, tk.Button) and btn.cget('text') in ["25%", "50%", "75%", "100%"]:
                                if btn.cget('text') == f"{porcentaje}%":
                                    btn.config(bg="#3498db")
                                else:
                                    btn.config(bg="#95a5a6")
    
    # --- Funciones de animación ---
    def detener_animacion(self):
        if self.animando:
            self.animando = False
            self.label_estado.config(text="⏹️ Animación detenida")
            messagebox.showinfo("Animación", "La animación ha sido detenida correctamente.")
        else:
            messagebox.showinfo("Información", "No hay ninguna animación en curso.")
    
    def animar_proyecto(self):
        if len(self.comandos_actuales) <= 1:
            messagebox.showinfo("Información", "Solo hay una página. Añade más páginas para animar.")
            return
        
        if self.animando:
            messagebox.showinfo("Información", "Ya hay una animación en curso.")
            return
        
        self.animando = True
        self.label_estado.config(text="🎬 Reproduciendo animación en bucle...")
        pagina_original = self.pagina_actual
        
        def hilo_animacion():
            try:
                while self.animando:
                    paginas_ordenadas = sorted(self.comandos_actuales.keys())
                    total_paginas = len(paginas_ordenadas)
                    
                    for idx, pagina in enumerate(paginas_ordenadas):
                        if not self.animando:
                            break
                        
                        self.pagina_actual = pagina
                        self.actualizar_info_paginas()
                        self.actualizar_lista_comandos()
                        self.turtle_engine.clear()
                        
                        velocidad_pagina = self._obtener_velocidad_pagina(pagina)
                        if velocidad_pagina is not None:
                            self.turtle_engine.set_velocidad(velocidad_pagina)
                            self.velocidad_animacion = velocidad_pagina
                            self.label_velocidad.config(text=f"{velocidad_pagina}%")
                            self._actualizar_botones_velocidad(velocidad_pagina)
                        else:
                            self.turtle_engine.set_velocidad(self.velocidad_animacion)
                        
                        for comando in self.comandos_actuales[pagina]:
                            if not self.animando:
                                break
                            try:
                                self.parser.ejecutar(comando)
                                self.root.update()
                                time.sleep(0.01)
                            except Exception as e:
                                print(f"Error en animación: {e}")
                        
                        if idx < total_paginas - 1 and self.animando:
                            time.sleep(0.3)
                    
                    if self.animando:
                        time.sleep(0.5)
                
                self.pagina_actual = pagina_original
                self.actualizar_info_paginas()
                self.actualizar_lista_comandos()
                self.turtle_engine.clear()
                self.turtle_engine.set_velocidad(self.velocidad_animacion)
                for comando in self.comandos_actuales.get(pagina_original, []):
                    try:
                        if not comando.upper().startswith("VEL "):
                            self.parser.ejecutar(comando)
                    except:
                        pass
                
                if not self.animando:
                    self.label_estado.config(text="⏹️ Animación detenida")
                self.animando = False
                
            except Exception as e:
                self.label_estado.config(text=f"❌ Error en animación: {str(e)}")
                self.animando = False
        
        thread = threading.Thread(target=hilo_animacion)
        thread.daemon = True
        thread.start()
    
    def _obtener_velocidad_pagina(self, pagina):
        if pagina not in self.comandos_actuales:
            return None
        
        for comando in self.comandos_actuales[pagina]:
            comando_upper = comando.upper().strip()
            if comando_upper.startswith("VEL "):
                try:
                    partes = comando_upper.split()
                    if len(partes) >= 2:
                        valor = int(partes[1])
                        if valor in [25, 50, 75, 100]:
                            return valor
                except:
                    pass
        return None
    
    # --- Funciones de páginas ---
    def nueva_pagina(self):
        self.total_paginas += 1
        self.pagina_actual = self.total_paginas
        self.comandos_actuales[self.pagina_actual] = []
        self.actualizar_info_paginas()
        self.actualizar_lista_comandos()
        self.turtle_engine.clear()
        self.label_estado.config(text=f"📄 Página {self.pagina_actual} creada")
    
    def eliminar_pagina(self):
        if self.total_paginas <= 1:
            messagebox.showinfo("Información", "No se puede eliminar la única página.")
            return
        if messagebox.askyesno("Eliminar página", f"¿Eliminar la página {self.pagina_actual}?"):
            del self.comandos_actuales[self.pagina_actual]
            self.total_paginas -= 1
            nuevos_comandos = {}
            i = 1
            for pagina in sorted(self.comandos_actuales.keys()):
                nuevos_comandos[i] = self.comandos_actuales[pagina]
                i += 1
            self.comandos_actuales = nuevos_comandos
            if self.pagina_actual > self.total_paginas:
                self.pagina_actual = self.total_paginas
            self.actualizar_info_paginas()
            self.actualizar_lista_comandos()
            self.turtle_engine.clear()
            self.label_estado.config(text=f"🗑️ Página eliminada")
    
    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.actualizar_info_paginas()
            self.actualizar_lista_comandos()
            self.turtle_engine.clear()
            self.ejecutar_pagina()
    
    def pagina_siguiente(self):
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.actualizar_info_paginas()
            self.actualizar_lista_comandos()
            self.turtle_engine.clear()
            self.ejecutar_pagina()
    
    # --- Funciones de limpieza ---
    def centrar_tortuga(self):
        self.turtle_engine.centrar_tortuga()
        self.label_estado.config(text="🎯 Tortuga centrada")
        messagebox.showinfo("Centrar", "La tortuga ha sido centrada en el lienzo.")
    
    def limpiar_todo(self):
        if messagebox.askyesno("Limpiar Todo", 
                              "¿Estás seguro de que quieres limpiar el lienzo y todos los comandos?\n\n"
                              "Esta acción no se puede deshacer."):
            if self.pagina_actual in self.comandos_actuales:
                self.comandos_actuales[self.pagina_actual] = []
            self.actualizar_lista_comandos()
            self.turtle_engine.clear()
            self.label_estado.config(text="🧹 Todo limpiado correctamente")
    
    def limpiar_lienzo(self):
        self.turtle_engine.clear()
        self.label_estado.config(text="🧹 Lienzo limpio")
    
    def eliminar_ultimo_comando(self):
        if self.pagina_actual in self.comandos_actuales and self.comandos_actuales[self.pagina_actual]:
            self.comandos_actuales[self.pagina_actual].pop()
            self.actualizar_lista_comandos()
            self.label_estado.config(text="🗑️ Último comando eliminado")
    
    def limpiar_lista_comandos(self):
        if self.pagina_actual in self.comandos_actuales:
            self.comandos_actuales[self.pagina_actual] = []
            self.actualizar_lista_comandos()
            self.label_estado.config(text="🧹 Lista de comandos limpiada")
    
    # --- Funciones de archivo ---
    def nuevo_proyecto(self):
        if any(self.comandos_actuales.values()) and not messagebox.askyesno("Nuevo", "¿Perder los cambios actuales?"):
            return
        
        self.comandos_actuales = {1: []}
        self.pagina_actual = 1
        self.total_paginas = 1
        self.archivo_actual = None
        
        self.velocidad_animacion = 100
        self.turtle_engine.set_velocidad(100)
        self.label_velocidad.config(text="100%")
        self._actualizar_botones_velocidad(100)
        
        self.actualizar_info_paginas()
        self.actualizar_lista_comandos()
        self.turtle_engine.clear()
        self.label_estado.config(text="📄 Nuevo proyecto (Vel: 100%)")
    
    def abrir_proyecto(self):
        archivo = filedialog.askopenfilename(
            title="Abrir proyecto",
            filetypes=[("Proyectos de dibujo", "*.dib"), ("Todos los archivos", "*.*")]
        )
        if not archivo:
            return
        
        try:
            resultado = self.turtle_engine.cargar_proyecto(archivo)
            if resultado is not True:
                raise Exception(resultado)
            
            self.comandos_actuales = {}
            velocidad_encontrada = None
            
            for i, pagina in enumerate(self.turtle_engine.paginas):
                self.comandos_actuales[i+1] = pagina.comandos.copy()
                if i == 0 and pagina.comandos:
                    primer_comando = pagina.comandos[0].upper().strip()
                    if primer_comando.startswith("VEL "):
                        try:
                            valor = int(primer_comando.split()[1])
                            if valor in [25, 50, 75, 100]:
                                velocidad_encontrada = valor
                        except:
                            pass
            
            self.total_paginas = len(self.comandos_actuales)
            self.pagina_actual = 1
            self.archivo_actual = archivo
            self.actualizar_info_paginas()
            self.actualizar_lista_comandos()
            self.turtle_engine.clear()
            
            if velocidad_encontrada is not None:
                self.velocidad_animacion = velocidad_encontrada
                self.turtle_engine.set_velocidad(velocidad_encontrada)
                self.label_velocidad.config(text=f"{velocidad_encontrada}%")
                self._actualizar_botones_velocidad(velocidad_encontrada)
                self.label_estado.config(text=f"📂 Abierto: {os.path.basename(archivo)} (Vel: {velocidad_encontrada}%)")
            else:
                self.velocidad_animacion = 100
                self.turtle_engine.set_velocidad(100)
                self.label_velocidad.config(text="100%")
                self._actualizar_botones_velocidad(100)
                self.label_estado.config(text=f"📂 Abierto: {os.path.basename(archivo)} (Vel: 100% por defecto)")
            
            if messagebox.askyesno("Ejecutar", "¿Quieres ejecutar los comandos del proyecto?"):
                self.ejecutar_pagina()
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")
    
    def guardar_proyecto(self):
        if not self.comandos_actuales:
            messagebox.showinfo("Información", "No hay comandos para guardar.")
            return
        
        archivo = filedialog.asksaveasfilename(
            title="Guardar proyecto",
            defaultextension=".dib",
            filetypes=[("Proyectos de dibujo", "*.dib"), ("Todos los archivos", "*.*")]
        )
        
        if not archivo:
            return
        
        try:
            for i, pagina in enumerate(self.turtle_engine.paginas):
                if i+1 in self.comandos_actuales:
                    pagina.comandos = self.comandos_actuales[i+1].copy()
            
            resultado = self.turtle_engine.guardar_proyecto(archivo)
            if resultado is not True:
                raise Exception(resultado)
            
            self.archivo_actual = archivo
            self.label_estado.config(text=f"💾 Guardado: {os.path.basename(archivo)}")
            messagebox.showinfo("Éxito", "Proyecto guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    def mostrar_ayuda(self):
        mostrar_ayuda(self.root)

def main():
    root = tk.Tk()
    app = DibujaConCodigo(root)
    root.mainloop()

if __name__ == "__main__":
    main()