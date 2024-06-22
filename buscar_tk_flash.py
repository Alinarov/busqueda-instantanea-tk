import tkinter as tk
import json

class TuClase:
    def __init__(self):
        self.nombres_empleados = []  # Lista para almacenar nombres de empleados desde el JSON
        self.leer_desde_json()  # Cargar datos desde el archivo JSON al inicializar la clase

    def leer_desde_json(self):
        try:
            with open('temp.json', 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                self.nombres_empleados = datos.get('empleados', [])  # Obtener lista de nombres de empleados
        except FileNotFoundError:
            print(f"El archivo 'empleados.json' no existe.")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON en 'empleados.json': {e}")
        except Exception as e:
            print(f"Error al leer desde 'empleados.json': {e}")

    def buscar_empleados(self, patron_busqueda):
        resultados = []

        # Convertir el patrón de búsqueda a minúsculas para hacer la comparación sin distinción de mayúsculas
        patron_busqueda = patron_busqueda.lower()

        # Buscar por nombre completo, DNI o últimos 8 dígitos del DNI
        for empleado in self.nombres_empleados:
            partes = empleado.split(':')
            if len(partes) == 2:
                nombre_completo = partes[0].strip().lower()
                dni_empleado = partes[1].strip()

                # Buscar coincidencias en nombre o DNI
                if patron_busqueda in nombre_completo or patron_busqueda in dni_empleado:
                    resultados.append(empleado)
            else:
                nombre_completo = empleado.strip().lower()
                if patron_busqueda in nombre_completo:
                    resultados.append(empleado)

        return resultados

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Búsqueda de Empleados")
        
        self.tu_clase = TuClase()

        self.frame = tk.Frame(self)
        self.frame.pack(padx=20, pady=20)

        # Vincular el rastreador al campo de búsqueda para actualizar los resultados mientras se escribe
        self.entry_busqueda_var = tk.StringVar()
        self.entry_busqueda_var.trace('w', self.actualizar_resultados)

        self.label_busqueda = tk.Label(self.frame, text="Buscar empleado:")
        self.label_busqueda.grid(row=0, column=0, padx=10, pady=10)

        self.entry_busqueda = tk.Entry(self.frame, textvariable=self.entry_busqueda_var)
        self.entry_busqueda.grid(row=0, column=1, padx=10, pady=10)
        self.entry_busqueda.focus()

        self.lista_resultados = tk.Listbox(self.frame, width=50, height=10)
        self.lista_resultados.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def actualizar_resultados(self, *args):
        patron_busqueda = self.entry_busqueda_var.get()
        resultados = self.tu_clase.buscar_empleados(patron_busqueda)

        self.lista_resultados.delete(0, tk.END)
        for resultado in resultados:
            self.lista_resultados.insert(tk.END, resultado)

# Iniciar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()
