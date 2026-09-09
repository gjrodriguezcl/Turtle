# -*- coding: utf-8 -*-
"""
Interfaz gráfica para "Turtle" - Versión 1.0
Autor: G. José Rodríguez
"""
import tkinter as tk
from tkinter import ttk, scrolledtext

def mostrar_ayuda(parent):
    """Muestra la ventana de ayuda con todos los comandos."""
    ventana_ayuda = tk.Toplevel(parent)
    ventana_ayuda.title("🐢 Ayuda - Dibuja con Código")
    ventana_ayuda.geometry("720x650")
    ventana_ayuda.resizable(True, True)
    ventana_ayuda.configure(bg="#f0f3f5")
    
    # Frame principal
    frame = tk.Frame(ventana_ayuda, bg="#f0f3f5", padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    titulo = tk.Label(frame, text="🐢 Guía de comandos", 
                     font=("Segoe UI", 18, "bold"), bg="#f0f3f5", fg="#2c3e50")
    titulo.pack(pady=(0, 5))
    
    subtitulo = tk.Label(frame, text="¡Dibuja, colorea y crea animaciones con código!", 
                        font=("Segoe UI", 11), bg="#f0f3f5", fg="#7f8c8d")
    subtitulo.pack(pady=(0, 15))
    
    # Área de texto con scroll
    texto_ayuda = scrolledtext.ScrolledText(frame, font=("Courier", 10), 
                                            wrap=tk.WORD, height=22)
    texto_ayuda.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Contenido de la ayuda
    contenido = """
=== 🎯 COMANDOS DE MOVIMIENTO ===

AD [n]       → Avanza n píxeles en la dirección actual.
AT [n]       → Retrocede n píxeles en la dirección actual.
DE [n]       → Gira a la derecha n grados.
IZ [n]       → Gira a la izquierda n grados.


=== 🖊️ CONTROL DE DIBUJO ===

DIB          → Activa el dibujo (baja el lápiz).
NODIB        → Desactiva el dibujo (sube el lápiz, no dibuja al moverse).
SUBIR        → Sube el lápiz (igual que NODIB).
BAJAR        → Baja el lápiz (igual que DIB).


=== 🎨 COLORES ===

LCOLOR r g b → Cambia el color de la línea (RGB: 0-255).
FCOLOR r g b → Cambia el color de relleno (RGB: 0-255).
FCURSOR r g b → Pinta el cursor en la posición actual (RGB: 0-255).


=== 🖌️ RELLENO DE FIGURAS ===

INICIAR_RELLENO  → Comienza el modo de relleno (usar antes de dibujar).
TERMINAR_RELLENO → Aplica el color de relleno a la figura cerrada.

¡IMPORTANTE! Para rellenar una figura:
1. Usa FCOLOR para elegir el color.
2. Usa INICIAR_RELLENO antes de dibujar.
3. Dibuja la figura (debe estar cerrada).
4. Usa TERMINAR_RELLENO para aplicar el color.

Ejemplo:
  FCOLOR 255 255 0
  INICIAR_RELLENO
  REPETIR 36 AD 10 DE 10
  TERMINAR_RELLENO

=== 🧭 POSICIONAMIENTO ===

GOTO x y    → Mueve la tortuga a la posición (x, y) sin dibujar.
IR x y      → Lo mismo que GOTO (en español).

Ejemplo:
  GOTO -200 100  → Mueve la tortuga a la posición (-200, 100)

=== 🐢 CURSOR ===

CCURSOR n   → Cambia el cursor al número n (1-25).


=== ⚡ ANIMACIÓN Y VELOCIDAD ===

VELOCIDAD n  → Ajusta la velocidad de dibujo (0-100%).
ESPERAR ms   → Pausa la ejecución durante milisegundos.


=== 📄 PÁGINAS ===

PAGINA n     → Cambia a la página n.
NUEVA_PAGINA → Crea una nueva página en blanco.
SIGUIENTE    → Avanza a la siguiente página.
ANTERIOR     → Retrocede a la página anterior.


=== 🔄 REPETICIÓN ===

REPETIR n [comando] → Repite el comando n veces.
REPETIR n [comando1] [comando2] ... → Repite varios comandos n veces.

Ejemplos:
  REPETIR 4 AD 100 DE 90        → Dibuja un cuadrado
  REPETIR 36 AD 10 DE 10        → Dibuja un círculo
  REPETIR 3 AD 50 DE 120        → Dibuja un triángulo


=== 🧹 UTILIDADES ===

BORRAR       → Limpia el lienzo actual.


=== 📚 EJEMPLOS COMPLETOS ===

1. Cuadrado rojo relleno:
  FCOLOR 255 0 0
  INICIAR_RELLENO
  REPETIR 4 AD 100 DE 90
  TERMINAR_RELLENO

2. Círculo amarillo:
  FCOLOR 255 255 0
  INICIAR_RELLENO
  REPETIR 36 AD 10 DE 10
  TERMINAR_RELLENO

3. Estrella azul:
  FCOLOR 0 0 255
  INICIAR_RELLENO
  REPETIR 5 AD 100 DE 144
  TERMINAR_RELLENO

4. Casa con colores:
  FCOLOR 150 75 0
  INICIAR_RELLENO
  REPETIR 4 AD 100 DE 90
  TERMINAR_RELLENO
  
  FCOLOR 200 50 50
  INICIAR_RELLENO
  DE 45
  AD 70
  DE 90
  AD 70
  DE 135
  AD 100
  TERMINAR_RELLENO

¡Experimenta y diviértete creando tus propios dibujos!
    """
    
    texto_ayuda.insert(tk.END, contenido)
    texto_ayuda.config(state='disabled')  # Hacerlo de solo lectura
    
    # Botón de cerrar
    btn_cerrar = tk.Button(frame, text="Cerrar", command=ventana_ayuda.destroy,
                         bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"),
                         relief=tk.RAISED, bd=2, padx=20, pady=8)
    btn_cerrar.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mostrar_ayuda(root)
    root.mainloop()