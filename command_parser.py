# -*- coding: utf-8 -*-
"""
Interfaz gráfica para "Turtle" - Versión 1.0
Autor: G. José Rodríguez
"""
import re

class CommandParser:
    def __init__(self, turtle_engine):
        self.engine = turtle_engine
        
    def ejecutar(self, comando):
        """Ejecuta un comando y devuelve un mensaje de resultado."""
        comando = comando.upper().strip()
        
        if not comando:
            return ""
        
        if comando.startswith("#"):
            return ""
        
        # Comandos de movimiento
        if comando.startswith("AD "):
            return self._ejecutar_adelante(comando)
        elif comando.startswith("AT "):
            return self._ejecutar_atras(comando)
        elif comando.startswith("DE "):
            return self._ejecutar_derecha(comando)
        elif comando.startswith("IZ "):
            return self._ejecutar_izquierda(comando)
        
        # Control de dibujo
        elif comando == "DIB":
            return self.engine.dibujar()
        elif comando == "NODIB":
            return self.engine.no_dibujar()
        elif comando == "SUBIR":
            return self.engine.subir_lapiz()
        elif comando == "BAJAR":
            return self.engine.bajar_lapiz()
        
        # Colores
        elif comando.startswith("LCOLOR "):
            return self._ejecutar_color_linea(comando)
        elif comando.startswith("FCOLOR "):
            return self._ejecutar_color_relleno(comando)
        elif comando.startswith("FCURSOR "):
            return self._ejecutar_pintar_cursor(comando)
        
        # Cursor
        elif comando.startswith("CCURSOR "):
            return self._ejecutar_cambiar_cursor(comando)
        
        # Velocidad
        elif comando.startswith("VEL "):
            return self._ejecutar_vel(comando)
        elif comando.startswith("VELOCIDAD "):
            return self._ejecutar_velocidad(comando)
        
        # Esperar
        elif comando.startswith("ESPERAR "):
            return self._ejecutar_esperar(comando)
        
        # Repetir
        elif comando.startswith("REPETIR "):
            return self._ejecutar_repetir(comando)
        
        # Páginas
        elif comando.startswith("PAGINA "):
            return self._ejecutar_pagina(comando)
        elif comando == "NUEVA_PAGINA":
            return self._ejecutar_nueva_pagina()
        elif comando == "SIGUIENTE_PAGINA":
            return self._ejecutar_siguiente_pagina()
        elif comando == "ANTERIOR_PAGINA":
            return self._ejecutar_anterior_pagina()
        
        # Relleno
        elif comando == "INICIAR_RELLENO":
            return self.engine.iniciar_relleno()
        elif comando == "TERMINAR_RELLENO":
            return self.engine.terminar_relleno()
        elif comando.startswith("RELLENAR"):
            return self._ejecutar_rellenar(comando)

        elif comando.startswith("GOTO "):
            return self._ejecutar_goto(comando)
        elif comando.startswith("IR "):
            return self._ejecutar_goto(comando.replace("IR ", "GOTO "))

        # Utilidades
        elif comando == "BORRAR":
            return self.engine.clear()
        else:
            raise ValueError(f"Comando no reconocido: {comando}")
    
    # --- Métodos existentes ---
    def _ejecutar_adelante(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: AD [pixeles]")
        try:
            pixeles = int(partes[1])
            return self.engine.adelante(pixeles)
        except ValueError:
            raise ValueError("AD requiere un número entero")
    
    def _ejecutar_atras(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: AT [pixeles]")
        try:
            pixeles = int(partes[1])
            return self.engine.atras(pixeles)
        except ValueError:
            raise ValueError("AT requiere un número entero")
    
    def _ejecutar_derecha(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: DE [grados]")
        try:
            grados = int(partes[1])
            return self.engine.derecha(grados)
        except ValueError:
            raise ValueError("DE requiere un número entero")
    
    def _ejecutar_izquierda(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: IZ [grados]")
        try:
            grados = int(partes[1])
            return self.engine.izquierda(grados)
        except ValueError:
            raise ValueError("IZ requiere un número entero")
    
    def _ejecutar_color_linea(self, comando):
        partes = comando.split()
        if len(partes) != 4:
            raise ValueError("Formato: LCOLOR [r] [g] [b]")
        try:
            r, g, b = int(partes[1]), int(partes[2]), int(partes[3])
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError("Valores RGB deben estar entre 0 y 255")
            return self.engine.set_color_linea(r, g, b)
        except ValueError:
            raise ValueError("LCOLOR requiere tres números enteros entre 0 y 255")
    
    def _ejecutar_color_relleno(self, comando):
        partes = comando.split()
        if len(partes) != 4:
            raise ValueError("Formato: FCOLOR [r] [g] [b]")
        try:
            r, g, b = int(partes[1]), int(partes[2]), int(partes[3])
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError("Valores RGB deben estar entre 0 y 255")
            return self.engine.set_color_relleno(r, g, b)
        except ValueError:
            raise ValueError("FCOLOR requiere tres números enteros entre 0 y 255")
    
    def _ejecutar_pintar_cursor(self, comando):
        partes = comando.split()
        if len(partes) != 4:
            raise ValueError("Formato: FCURSOR [r] [g] [b]")
        try:
            r, g, b = int(partes[1]), int(partes[2]), int(partes[3])
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError("Valores RGB deben estar entre 0 y 255")
            return self.engine.pintar_cursor(r, g, b)
        except ValueError:
            raise ValueError("FCURSOR requiere tres números enteros entre 0 y 255")
    
    def _ejecutar_cambiar_cursor(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: CCURSOR [número]")
        try:
            numero = int(partes[1])
            if not (1 <= numero <= 25):
                raise ValueError("Número de cursor debe estar entre 1 y 25")
            return self.engine.cambiar_cursor(numero)
        except ValueError:
            raise ValueError("CCURSOR requiere un número entero entre 1 y 25")
    
    def _ejecutar_vel(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: VEL [25|50|75|100]")
        try:
            valor = int(partes[1])
            if valor not in [25, 50, 75, 100]:
                raise ValueError("Velocidad debe ser 25, 50, 75 o 100")
            return self.engine.set_velocidad(valor)
        except ValueError:
            raise ValueError("VEL requiere un número entero: 25, 50, 75 o 100")
    
    def _ejecutar_velocidad(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: VELOCIDAD [porcentaje]")
        try:
            porcentaje = int(partes[1])
            if not (0 <= porcentaje <= 100):
                raise ValueError("Porcentaje debe estar entre 0 y 100")
            return self.engine.set_velocidad(porcentaje)
        except ValueError:
            raise ValueError("VELOCIDAD requiere un número entero entre 0 y 100")
    
    def _ejecutar_esperar(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: ESPERAR [milisegundos]")
        try:
            ms = int(partes[1])
            if ms < 0:
                raise ValueError("Milisegundos debe ser un número positivo")
            return self.engine.esperar(ms)
        except ValueError:
            raise ValueError("ESPERAR requiere un número entero")
    
    def _ejecutar_repetir(self, comando):
        partes = comando.split()
        if len(partes) < 3:
            raise ValueError("Formato: REPETIR [n] [comando(s)]")
        
        try:
            n = int(partes[1])
            if n <= 0:
                raise ValueError("El número de repeticiones debe ser positivo")
            
            texto_comandos = ' '.join(partes[2:])
            
            comandos_conocidos = ['AD', 'AT', 'DE', 'IZ', 'LCOLOR', 'FCOLOR', 'FCURSOR', 
                                 'CCURSOR', 'VEL', 'VELOCIDAD', 'ESPERAR', 'DIB', 'NODIB', 
                                 'SUBIR', 'BAJAR', 'BORRAR', 'PAGINA', 'RELLENAR',
                                 'INICIAR_RELLENO', 'TERMINAR_RELLENO']
            
            comandos_a_repetir = []
            i = 0
            texto = texto_comandos.split()
            
            while i < len(texto):
                encontrado = False
                for cmd in comandos_conocidos:
                    if texto[i].upper() == cmd:
                        if cmd in ['LCOLOR', 'FCOLOR', 'FCURSOR']:
                            if i + 3 < len(texto):
                                comando_completo = ' '.join(texto[i:i+4])
                                comandos_a_repetir.append(comando_completo)
                                i += 4
                                encontrado = True
                                break
                        elif cmd in ['VEL', 'VELOCIDAD', 'ESPERAR']:
                            if i + 1 < len(texto):
                                comando_completo = ' '.join(texto[i:i+2])
                                comandos_a_repetir.append(comando_completo)
                                i += 2
                                encontrado = True
                                break
                        elif cmd in ['AD', 'AT', 'DE', 'IZ', 'CCURSOR', 'PAGINA']:
                            if i + 1 < len(texto):
                                comando_completo = ' '.join(texto[i:i+2])
                                comandos_a_repetir.append(comando_completo)
                                i += 2
                                encontrado = True
                                break
                        elif cmd in ['INICIAR_RELLENO', 'TERMINAR_RELLENO']:
                            comandos_a_repetir.append(texto[i])
                            i += 1
                            encontrado = True
                            break
                        elif cmd == 'RELLENAR':
                            if i + 3 < len(texto) and texto[i+1].isdigit() and texto[i+2].isdigit() and texto[i+3].isdigit():
                                comando_completo = ' '.join(texto[i:i+4])
                                comandos_a_repetir.append(comando_completo)
                                i += 4
                                encontrado = True
                                break
                            else:
                                comandos_a_repetir.append(texto[i])
                                i += 1
                                encontrado = True
                                break
                        else:
                            comandos_a_repetir.append(texto[i])
                            i += 1
                            encontrado = True
                            break
                
                if not encontrado:
                    i += 1
            
            if not comandos_a_repetir:
                comandos_a_repetir = [texto_comandos]
            
            for i in range(n):
                for cmd in comandos_a_repetir:
                    try:
                        self.ejecutar(cmd)
                    except Exception as e:
                        raise ValueError(f"Error en repetición {i+1}, comando '{cmd}': {str(e)}")
            
            return f"Repetido {n} veces: {', '.join(comandos_a_repetir)}"
        
        except ValueError as e:
            raise ValueError(f"REPETIR requiere un número entero positivo: {str(e)}")
    
    def _ejecutar_rellenar(self, comando):
        """Rellena el área cerrada donde está el cursor."""
        return self.engine.rellenar()
    
    def _ejecutar_pagina(self, comando):
        partes = comando.split()
        if len(partes) != 2:
            raise ValueError("Formato: PAGINA [número]")
        try:
            numero = int(partes[1])
            if numero < 1:
                raise ValueError("Número de página debe ser mayor que 0")
            if self.engine.ir_a_pagina(numero - 1):
                return f"Cambiado a página {numero}"
            else:
                raise ValueError(f"La página {numero} no existe")
        except ValueError:
            raise ValueError("PAGINA requiere un número entero positivo")

    def _ejecutar_goto(self, comando):
        """
        Mueve la tortuga a una posición específica.
        Formato: GOTO [x] [y]
        Ejemplo: GOTO -200 100
        """
        partes = comando.split()
        if len(partes) != 3:
            raise ValueError("Formato: GOTO [x] [y]")
        try:
            x = int(partes[1])
            y = int(partes[2])
            return self.engine.ir_a(x, y)
        except ValueError:
            raise ValueError("GOTO requiere dos números enteros")
    
    def _ejecutar_nueva_pagina(self):
        indice = self.engine.nueva_pagina()
        return f"Página {indice + 1} creada"
    
    def _ejecutar_siguiente_pagina(self):
        indice = self.engine.pagina_actual + 1
        if indice < len(self.engine.paginas):
            self.engine.ir_a_pagina(indice)
            return f"Página {indice + 1}"
        else:
            raise ValueError("Ya estás en la última página")
    
    def _ejecutar_anterior_pagina(self):
        indice = self.engine.pagina_actual - 1
        if indice >= 0:
            self.engine.ir_a_pagina(indice)
            return f"Página {indice - 1}"
        else:
            raise ValueError("Ya estás en la primera página")