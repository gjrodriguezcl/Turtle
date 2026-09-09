# -*- coding: utf-8 -*-
"""
Interfaz gráfica para "Turtle" - Versión 1.0
Autor: G. José Rodríguez
"""
import sys
import os
from interface import DibujaConCodigo
import tkinter as tk

def main():
    """Función principal que inicia la aplicación."""
    # Verificar que existe la carpeta de cursores
    if not os.path.exists("cursores"):
        os.makedirs("cursores")
        print("📁 Carpeta 'cursores' creada. Añade aquí tus imágenes de cursores.")
    
    if not os.path.exists("ejemplos"):
        os.makedirs("ejemplos")
        print("📁 Carpeta 'ejemplos' creada. Aquí se guardarán los dibujos de ejemplo.")
    
    # Crear la ventana principal
    root = tk.Tk()
    app = DibujaConCodigo(root)
    root.mainloop()

if __name__ == "__main__":
    main()