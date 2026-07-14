#Copyright (c) 2026 Daniel Alejandro Ramirez Palma. Todos los derechos reservados.
#Este software es propiedad intelectual privada. Prohibida su copia, distribución o ingeniería inversa sin autorización expresa del autor.
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import DateEntry  
import threading
# Importamos nuestros propios módulos
from database import BaseDatosContable
from logic import LibroDiario

class InterfazContable:
    def __init__(self, root):
        self.bd = BaseDatosContable()
        self.diario = LibroDiario(self.bd)
        self.root = root
        
        # --- PALETA MODO OSCURO ---
        self.colores = {
            "bg_base": "#1e1e1e",      # Fondo principal
            "bg_secundario": "#2d2d2d",# Fondo frames/paneles
            "texto": "#ffffff",        # Texto blanco
            "acento": "#007acc",       # Azul Visual Studio Code
            "btn_bg": "#333333",       # Botones oscuros
            "tree_bg": "#252526"       # Fondo tablas
        } 
        
        self._configurar_estilos()
        self.configurar_ventana(self.root, "Sistema Contable - Libro Diario", "500x350")
        
        # Etiqueta de título
        tk.Label(root, text="Menú Principal", font=("Arial", 16, "bold"), 
                 bg=self.colores["bg_base"], fg=self.colores["texto"]).pack(pady=20)

        # Botones Principales (Con diseño oscuro)
        btn_width = 30
        opciones = [
            ("1. Registrar Nuevo Asiento", self.abrir_ventana_registro),
            ("2. Visualizar Libro Diario", self.abrir_ventana_diario),
            ("3. Ver Totales", self.mostrar_totales),
            ("4. Exportar a Excel", self.ejecutar_exportacion), # Asumiendo la exportación del paso anterior
            ("5. Salir", self.salir)
        ]

        for texto, comando in opciones:
            tk.Button(root, text=texto, width=btn_width, command=comando,
                      bg=self.colores["btn_bg"], fg=self.colores["texto"], 
                      activebackground=self.colores["acento"], activeforeground="white",
                      relief="flat", pady=5).pack(pady=5)

    def _configurar_estilos(self):
        """Aplica el tema oscuro a los componentes ttk (Tablas y Scrollbars)"""
        style = ttk.Style()
        style.theme_use("clam") # 'clam' permite modificar colores fácilmente
        style.configure("Treeview", 
                        background=self.colores["tree_bg"], 
                        foreground=self.colores["texto"], 
                        fieldbackground=self.colores["tree_bg"],
                        rowheight=25)
        style.configure("Treeview.Heading", 
                        background=self.colores["bg_secundario"], 
                        foreground=self.colores["texto"], 
                        font=('Arial', 10, 'bold'))
        style.map("Treeview", background=[("selected", self.colores["acento"])])

    def configurar_ventana(self, ventana, titulo, geometria="800x500"):
        """Estandariza todas las pantallas del sistema."""
        ventana.title(titulo)
        ventana.geometry(geometria)
        ventana.configure(bg=self.colores["bg_base"])
        # Centrar ventana en la pantalla
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    def abrir_ventana_registro(self):
        ventana = tk.Toplevel(self.root)
        # Aplicamos la configuración de ventana uniforme que creamos antes
        self.configurar_ventana(ventana, "Nuevo Asiento", "550x650")
        ventana.grab_set() 

        lineas = []

        # Estilos para los Entry (para no repetir código)
        estilo_entry = {
            "bg": self.colores["bg_secundario"],
            "fg": self.colores["texto"],
            "insertbackground": self.colores["texto"], # Color del cursor al escribir
            "relief": "flat"
        }

        # Frame Cabecera - Añadimos 'foreground' al LabelFrame para el título del cuadro
        frame_cabecera = tk.LabelFrame(ventana, text="Datos del Asiento", padx=10, pady=10, 
                                       bg=self.colores["bg_base"], fg=self.colores["acento"], 
                                       font=("Arial", 10, "bold"))
        frame_cabecera.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_cabecera, text="Fecha:", bg=self.colores["bg_base"], 
                 fg=self.colores["texto"]).grid(row=0, column=0, sticky="e", padx=5)
        
        ent_fecha = DateEntry(frame_cabecera, width=12, background=self.colores["acento"],
                              foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        ent_fecha.grid(row=0, column=1, pady=5, sticky="w")

        tk.Label(frame_cabecera, text="Descripción:", bg=self.colores["bg_base"], 
                 fg=self.colores["texto"]).grid(row=1, column=0, sticky="e", padx=5)
        ent_desc = tk.Entry(frame_cabecera, **estilo_entry) # Aplicamos estilo oscuro
        ent_desc.grid(row=1, column=1, pady=5, sticky="we")
        frame_cabecera.columnconfigure(1, weight=1)

        # Frame Líneas
        frame_lineas = tk.LabelFrame(ventana, text="Agregar Cuentas", padx=10, pady=10, 
                                     bg=self.colores["bg_base"], fg=self.colores["acento"],
                                     font=("Arial", 10, "bold"))
        frame_lineas.pack(fill="x", padx=20, pady=10)

        # Etiquetas y Campos con estilo oscuro
        labels = [("Código:", 0, 0), ("Nombre:", 0, 2), ("Debe:", 1, 0), ("Haber:", 1, 2)]
        for texto, r, c in labels:
            tk.Label(frame_lineas, text=texto, bg=self.colores["bg_base"], 
                     fg=self.colores["texto"]).grid(row=r, column=c, padx=5, pady=5, sticky="e")

        ent_cod = tk.Entry(frame_lineas, width=10, **estilo_entry)
        ent_cod.grid(row=0, column=1, sticky="w")

        ent_nom = tk.Entry(frame_lineas, width=20, **estilo_entry)
        ent_nom.grid(row=0, column=3, sticky="we")

        ent_debe = tk.Entry(frame_lineas, width=10, **estilo_entry)
        ent_debe.grid(row=1, column=1, sticky="w")

        ent_haber = tk.Entry(frame_lineas, width=10, **estilo_entry)
        ent_haber.grid(row=1, column=3, sticky="w")

        # El Treeview ya debería tomar el estilo oscuro del __init__ gracias a 'style.theme_use("clam")'
        columnas = ("codigo", "nombre", "debe", "haber")
        tree = ttk.Treeview(ventana, columns=columnas, show="headings", height=6)
        tree.heading("codigo", text="Código")
        tree.heading("nombre", text="Nombre")
        tree.heading("debe", text="Debe")
        tree.heading("haber", text="Haber")
        tree.column("codigo", width=80, anchor="center")
        tree.column("nombre", width=150)
        tree.column("debe", width=80, anchor="e")
        tree.column("haber", width=80, anchor="e")
        tree.pack(padx=20, pady=10, fill="both", expand=True)

        # --- FUNCIONES INTERNAS (Sin cambios en lógica, solo limpieza) ---
        def agregar_linea():
            try:
                cod, nom = ent_cod.get().strip(), ent_nom.get().strip()
                debe = float(ent_debe.get().strip() or 0.0)
                haber = float(ent_haber.get().strip() or 0.0)

                if not cod or not nom:
                    messagebox.showwarning("Faltan datos", "Código y Nombre son obligatorios.")
                    return

                lineas.append({'codigo': cod, 'nombre': nom, 'debe': debe, 'haber': haber})
                tree.insert("", "end", values=(cod, nom, f"{debe:.2f}", f"{haber:.2f}"))
                
                # Limpiar campos
                for e in [ent_cod, ent_nom, ent_debe, ent_haber]: e.delete(0, tk.END)
                ent_cod.focus()
            except ValueError:
                messagebox.showerror("Error", "Los montos deben ser numéricos.")

        def guardar_asiento():
            fecha, desc = ent_fecha.get().strip(), ent_desc.get().strip()
            if not desc or len(lineas) < 2:
                messagebox.showwarning("Incompleto", "Verifique la descripción y las cuentas.")
                return
            try:
                self.diario.registrar_asiento(fecha, desc, lineas)
                messagebox.showinfo("Éxito", "Asiento registrado.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Botones con estilo oscuro
        tk.Button(frame_lineas, text="➕ Añadir Línea", command=agregar_linea,
                  bg=self.colores["btn_bg"], fg=self.colores["texto"], relief="flat").grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Button(ventana, text="💾 Guardar Asiento Completo", command=guardar_asiento, 
                  bg=self.colores["acento"], fg="white", font=("Arial", 10, "bold"), relief="flat").pack(pady=20)

    def abrir_ventana_diario(self):
        # Usamos el generador estándar de ventanas
        ventana = tk.Toplevel(self.root)
        self.configurar_ventana(ventana, "Libro Diario - Vista de Datos", "900x500")

        # --- BARRA SUPERIOR (FILTRADO) ---
        frame_filtros = tk.Frame(ventana, bg=self.colores["bg_base"])
        frame_filtros.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_filtros, text="Filtro de Tiempo:", bg=self.colores["bg_base"], 
                 fg=self.colores["texto"], font=("Arial", 11, "bold")).pack(side="left", padx=5)

        opciones_filtro = {
            "Últimos 7 Días": "7 days",
            "Últimos 7 Meses": "7 months",
            "Últimos 7 Años": "7 years"
        }
        
        combo_filtro = ttk.Combobox(frame_filtros, values=list(opciones_filtro.keys()), state="readonly", width=20)
        combo_filtro.current(0) # Por defecto: 7 días
        combo_filtro.pack(side="left", padx=5)

        # --- TABLA DE DATOS (TREEVIEW) ---
        columnas = ("fecha", "asiento", "codigo", "nombre", "desc", "debe", "haber")
        tree = ttk.Treeview(ventana, columns=columnas, show="headings")
        
        # Configurar cabeceras
        for col in columnas:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100)
        
        tree.column("desc", width=200)
        tree.column("nombre", width=150)

        scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=10, pady=5)

        # --- LÓGICA DE ACTUALIZACIÓN EN SEGUNDO PLANO ---
        def mostrar_en_tabla(registros):
            """Esta función corre en el hilo principal y actualiza la pantalla"""
            # 1. Borramos el mensaje de "Cargando..."
            for item in tree.get_children():
                tree.delete(item)

            # 2. Si no hay datos, mostramos el aviso
            if not registros:
                tree.insert("", "end", values=("Sin datos", "-", "-", "No hay registros", "en este periodo", "-", "-"))
                return

            # 3. Insertamos los datos reales
            for r in registros:
                fecha, as_id, desc, cod, nom, debe, haber = r
                debe_str = f"{debe:,.2f}" if debe > 0 else ""
                haber_str = f"{haber:,.2f}" if haber > 0 else ""
                tree.insert("", "end", values=(fecha, as_id, cod, nom, desc, debe_str, haber_str))

        def consultar_base_datos(valor_sql):
            """Esta función corre en segundo plano para no congelar la pantalla"""
            try:
                registros = self.diario.obtener_registros(filtro_tiempo=valor_sql)
                # Una vez traemos los datos, le decimos a Tkinter que los dibuje de forma segura
                ventana.after(0, mostrar_en_tabla, registros)
            except Exception as e:
                # 1. Convertimos el error a texto INMEDIATAMENTE antes de que Python lo borre
                error_texto = str(e)
                # 2. Usamos 'msg=error_texto' para pasar el valor de forma segura a la lambda
                ventana.after(0, lambda msg=error_texto: messagebox.showerror("Error", f"No se pudo cargar: {msg}"))

        def cargar_datos(event=None):
            """Inicia el proceso cuando el usuario cambia el filtro"""
            # 1. Limpiar tabla y poner aviso de carga temporal
            for item in tree.get_children():
                tree.delete(item)
            tree.insert("", "end", values=("Cargando...", "-", "-", "Buscando datos...", "Por favor espera...", "-", "-"))
            
            # 2. Obtener el filtro seleccionado
            seleccion = combo_filtro.get()
            valor_sql = opciones_filtro[seleccion]
            
            # 3. Lanzar el hilo en segundo plano (daemon=True hace que el hilo muera si cierras la app)
            hilo = threading.Thread(target=consultar_base_datos, args=(valor_sql,), daemon=True)
            hilo.start()

        # Enlazar el evento: cuando cambie el desplegable, se actualiza la tabla
        combo_filtro.bind("<<ComboboxSelected>>", cargar_datos)
        
        # Carga inicial de datos (Últimos 7 días)
        cargar_datos()

    def mostrar_totales(self):
        debe, haber = self.diario.obtener_saldos()
        estado = "✅ Cuadrado perfectamente." if round(debe, 2) == round(haber, 2) else "❌ Descuadre detectado."
        
        mensaje = f"--- BALANCE DE COMPROBACIÓN ---\n\n"
        mensaje += f"Total DEBE:  $ {debe:,.2f}\n"
        mensaje += f"Total HABER: $ {haber:,.2f}\n\n"
        mensaje += f"Estado: {estado}"
        
        messagebox.showinfo("Totales del Diario", mensaje)

    def salir(self):
        self.bd.cerrar()
        self.root.quit()

    def ejecutar_exportacion(self):
        # 1. Preguntar al usuario dónde quiere guardar el archivo
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            title="Guardar Libro Diario"
        )
        
        if ruta:
            try:
                # 2. Llamar a la lógica de exportación
                self.diario.exportar_a_excel(ruta)
                messagebox.showinfo("Exportación Exitosa", f"El archivo ha sido guardado en:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error de Exportación", f"No se pudo generar el archivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazContable(root)
    root.mainloop()
    