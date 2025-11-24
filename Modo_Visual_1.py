"""
fabricante_lentes.py
Aplicación Tkinter + ttk (estética profesional) para el rol: Fabricante de lentes.
Incluye: registro/edición/búsqueda/eliminación de órdenes, inventario, fabricación simulada,
control de calidad, alertas, export/import CSV, dashboard (matplotlib opcional) y reportes simples.

Autor: Generado por ChatGPT
Ejecutar: python fabricante_lentes.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import threading
import time
import csv
import os
import sqlite3
from datetime import datetime

# Intentar importar matplotlib para dashboard (opcional)
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False

# ---------------------------------------------------------------------
# Persistencia simple con SQLite (incluye tablas: ordenes, materiales, produccion, qc)
# ---------------------------------------------------------------------
DB_PATH = "fabricante_lentes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS ordenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        graduacion TEXT,
        tipo TEXT,
        estado TEXT,
        fecha TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS materiales (
        nombre TEXT PRIMARY KEY,
        cantidad INTEGER,
        umbral INTEGER
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS produccion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orden_id INTEGER,
        resultado TEXT,
        fecha TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS qc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orden_id INTEGER,
        resultado TEXT,
        observaciones TEXT,
        fecha TEXT
    )""")
    # Inventario por defecto si no existe
    c.execute("SELECT COUNT(*) FROM materiales")
    if c.fetchone()[0] == 0:
        defaults = [("Micas", 50, 5), ("Armazones", 40, 5), ("Tornillos", 200, 10), ("Barniz", 30, 5)]
        c.executemany("INSERT INTO materiales (nombre, cantidad, umbral) VALUES (?, ?, ?)", defaults)
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------------------
# Utilidades DB
# ---------------------------------------------------------------------
def fetch_orders(search_term=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if search_term:
        q = f"%{search_term}%"
        c.execute("SELECT id, cliente, graduacion, tipo, estado, fecha FROM ordenes WHERE cliente LIKE ? OR tipo LIKE ? OR graduacion LIKE ? ORDER BY id DESC", (q, q, q))
    else:
        c.execute("SELECT id, cliente, graduacion, tipo, estado, fecha FROM ordenes ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def add_order_db(cliente, graduacion, tipo):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fecha = datetime.now().isoformat(sep=' ', timespec='seconds')
    c.execute("INSERT INTO ordenes (cliente, graduacion, tipo, estado, fecha) VALUES (?, ?, ?, ?, ?)",
              (cliente, graduacion, tipo, "Pendiente", fecha))
    conn.commit()
    conn.close()

def update_order_db(order_id, cliente, graduacion, tipo, estado):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE ordenes SET cliente=?, graduacion=?, tipo=?, estado=? WHERE id=?", (cliente, graduacion, tipo, estado, order_id))
    conn.commit()
    conn.close()

def delete_order_db(order_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM ordenes WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

def fetch_materials():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nombre, cantidad, umbral FROM materiales")
    rows = c.fetchall()
    conn.close()
    return rows

def update_material(nombre, cantidad):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE materiales SET cantidad=? WHERE nombre=?", (cantidad, nombre))
    conn.commit()
    conn.close()

def record_production(orden_id, resultado):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fecha = datetime.now().isoformat(sep=' ', timespec='seconds')
    c.execute("INSERT INTO produccion (orden_id, resultado, fecha) VALUES (?, ?, ?)", (orden_id, resultado, fecha))
    conn.commit()
    conn.close()

def record_qc(orden_id, resultado, observaciones):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fecha = datetime.now().isoformat(sep=' ', timespec='seconds')
    c.execute("INSERT INTO qc (orden_id, resultado, observaciones, fecha) VALUES (?, ?, ?, ?)", (orden_id, resultado, observaciones, fecha))
    conn.commit()
    conn.close()

# ---------------------------------------------------------------------
# Lógica del fabricante
# ---------------------------------------------------------------------
def check_materials_needed(tipo):
    """Retorna dict de materiales requeridos según tipo de lente (simulado)."""
    # reglas simples de consumo por tipo
    base = {"Micas": 1, "Armazones": 1, "Tornillos": 4, "Barniz": 1}
    if tipo == "Progresivos":
        base["Micas"] = 2
        base["Tornillos"] = 6
    elif tipo == "Bifocales":
        base["Micas"] = 1
        base["Tornillos"] = 5
    return base

def materials_available_for(tipo):
    required = check_materials_needed(tipo)
    current = {row[0]: row[1] for row in fetch_materials()}
    for k, v in required.items():
        if current.get(k, 0) < v:
            return False, k
    return True, None

def consume_materials(tipo):
    required = check_materials_needed(tipo)
    mats = fetch_materials()
    mats_dict = {row[0]: row[1] for row in mats}
    for k, v in required.items():
        new_q = mats_dict.get(k, 0) - v
        update_material(k, new_q)

# ---------------------------------------------------------------------
# GUI: estilo ttk profesional (tema personalizado)
# ---------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Panel Profesional - Fabricante de Lentes")
        self.geometry("1000x650")
        self.minsize(900, 600)

        # Estilo ttk
        self.style = ttk.Style(self)
        # Estilo base limpio: usar tema nativo o 'clam' si disponible
        try:
            self.style.theme_use('clam')
        except:
            pass
        self.style.configure("TFrame", background="#f5f7fa")
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background="#f5f7fa")
        self.style.configure("TButton", padding=6)
        self.style.configure("Accent.TButton", foreground="white", background="#2b7cff")
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        self.style.map("Accent.TButton", background=[('active', '#1a5fe0')])

        # Layout principal: sidebar + content
        self.sidebar = ttk.Frame(self, width=220)
        self.content = ttk.Frame(self)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self._build_sidebar()
        self._build_content()
        self.refresh_all()

    # ---------------- Sidebar ----------------
    def _build_sidebar(self):
        ttk.Label(self.sidebar, text="Fabricante - Menú", style="Header.TLabel").pack(pady=(0,10))
        ttk.Button(self.sidebar, text="Registrar Orden", command=self.show_register, width=20).pack(pady=4)
        ttk.Button(self.sidebar, text="Órdenes / Buscar", command=self.show_orders, width=20).pack(pady=4)
        ttk.Button(self.sidebar, text="Producción", command=self.show_production, width=20).pack(pady=4)
        ttk.Button(self.sidebar, text="Materiales", command=self.show_materials, width=20).pack(pady=4)
        ttk.Button(self.sidebar, text="Control de Calidad", command=self.show_qc, width=20).pack(pady=4)
        ttk.Button(self.sidebar, text="Dashboard", command=self.show_dashboard, width=20).pack(pady=4)
        ttk.Separator(self.sidebar).pack(fill="x", pady=8)
        ttk.Button(self.sidebar, text="Importar CSV", command=self.import_csv, width=20).pack(pady=4)
        ttk.Button(self.sidebar, text="Exportar CSV (Órdenes)", command=self.export_orders_csv, width=20).pack(pady=4)
        ttk.Button(self.sidebar, text="Exportar inventario", command=self.export_materials_csv, width=20).pack(pady=4)
        ttk.Button(self.sidebar, text="Salir", command=self.quit, width=20).pack(side="bottom", pady=10)

    # ---------------- Content (paneles) ----------------
    def _build_content(self):
        # Frames para cada vista
        self.frames = {}
        for name in ("register", "orders", "production", "materials", "qc", "dashboard"):
            frame = ttk.Frame(self.content)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.frames[name] = frame

        self._build_register(self.frames["register"])
        self._build_orders(self.frames["orders"])
        self._build_production(self.frames["production"])
        self._build_materials(self.frames["materials"])
        self._build_qc(self.frames["qc"])
        self._build_dashboard(self.frames["dashboard"])

        self.show_register()

    # ---------------- Register view ----------------
    def _build_register(self, parent):
        ttk.Label(parent, text="Registrar Nueva Orden", style="Header.TLabel").pack(anchor="w", pady=8)
        frm = ttk.Frame(parent)
        frm.pack(anchor="nw", padx=6, pady=4)

        ttk.Label(frm, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.reg_cliente = ttk.Entry(frm, width=30)
        self.reg_cliente.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(frm, text="Graduación:").grid(row=1, column=0, sticky="w")
        self.reg_graduacion = ttk.Entry(frm, width=30)
        self.reg_graduacion.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(frm, text="Tipo de lente:").grid(row=2, column=0, sticky="w")
        self.reg_tipo = ttk.Combobox(frm, values=["Visión Sencilla", "Bifocales", "Progresivos"], state="readonly", width=28)
        self.reg_tipo.current(0)
        self.reg_tipo.grid(row=2, column=1, padx=6, pady=4)

        ttk.Button(frm, text="Agregar orden", style="Accent.TButton", command=self.add_order).grid(row=3, column=1, sticky="e", pady=8)

    # ---------------- Orders view ----------------
    def _build_orders(self, parent):
        top = ttk.Frame(parent)
        top.pack(fill="x", pady=6)
        ttk.Label(top, text="Órdenes registradas", style="Header.TLabel").pack(side="left", padx=4)
        search_f = ttk.Frame(top)
        search_f.pack(side="right", padx=4)
        self.search_var = tk.StringVar()
        ttk.Entry(search_f, textvariable=self.search_var, width=30).pack(side="left", padx=4)
        ttk.Button(search_f, text="Buscar", command=self.search_orders).pack(side="left", padx=2)
        ttk.Button(search_f, text="Refrescar", command=self.refresh_orders).pack(side="left", padx=2)

        # Treeview
        cols = ("id", "cliente", "graduacion", "tipo", "estado", "fecha")
        self.tree_orders = ttk.Treeview(parent, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree_orders.heading(c, text=c.capitalize())
            self.tree_orders.column(c, anchor="center")
        self.tree_orders.pack(fill="both", expand=True, pady=6)
        # Buttons
        btns = ttk.Frame(parent)
        btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="Editar orden", command=self.edit_order).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar orden", command=self.delete_order).pack(side="left", padx=4)
        ttk.Button(btns, text="Marcar como en producción", command=lambda: self.change_state_selected("En producción")).pack(side="left", padx=4)
        ttk.Button(btns, text="Marcar como completada", command=lambda: self.change_state_selected("Completada")).pack(side="left", padx=4)
        ttk.Button(btns, text="Iniciar fabricación (simulada)", command=self.start_fabrication_selected).pack(side="right", padx=4)

    # ---------------- Production view ----------------
    def _build_production(self, parent):
        ttk.Label(parent, text="Producción y simulación", style="Header.TLabel").pack(anchor="w", pady=8)
        frm = ttk.Frame(parent)
        frm.pack(fill="x", padx=6, pady=4)
        ttk.Button(frm, text="Mostrar inventario", command=self.show_inventory).pack(side="left", padx=2)
        ttk.Button(frm, text="Ver registro de producción", command=self.show_production_log).pack(side="left", padx=2)
        ttk.Button(frm, text="Simular producción masiva", command=self.simulate_bulk_production).pack(side="left", padx=2)

        # Progress area
        self.progress = ttk.Progressbar(parent, orient="horizontal", length=600, mode="determinate")
        self.progress.pack(pady=10)
        ttk.Label(parent, text="Estado de la simulación:").pack()
        self.lbl_prog = ttk.Label(parent, text="Idle")
        self.lbl_prog.pack()

    # ---------------- Materials view ----------------
    def _build_materials(self, parent):
        ttk.Label(parent, text="Gestión de materiales", style="Header.TLabel").pack(anchor="w", pady=8)
        frm = ttk.Frame(parent)
        frm.pack(fill="x", padx=6, pady=4)
        self.tree_mats = ttk.Treeview(frm, columns=("nombre", "cantidad", "umbral"), show="headings")
        for c in ("nombre", "cantidad", "umbral"):
            self.tree_mats.heading(c, text=c.capitalize())
            self.tree_mats.column(c, anchor="center")
        self.tree_mats.pack(side="left", fill="both", expand=True)
        ops = ttk.Frame(frm)
        ops.pack(side="right", fill="y", padx=6)
        ttk.Button(ops, text="Ajustar cantidad", command=self.adjust_material).pack(pady=4)
        ttk.Button(ops, text="Agregar material", command=self.add_material).pack(pady=4)
        ttk.Button(ops, text="Eliminar material", command=self.remove_material).pack(pady=4)
        ttk.Button(ops, text="Ver alertas", command=self.check_low_stock_alerts).pack(pady=4)

    # ---------------- QC view ----------------
    def _build_qc(self, parent):
        ttk.Label(parent, text="Control de Calidad (QC)", style="Header.TLabel").pack(anchor="w", pady=8)
        frm = ttk.Frame(parent)
        frm.pack(fill="x", padx=6, pady=4)
        ttk.Button(frm, text="Realizar QC sobre orden seleccionada", command=self.perform_qc).pack(side="left", padx=4)
        ttk.Button(frm, text="Ver historial QC", command=self.view_qc_history).pack(side="left", padx=4)

    # ---------------- Dashboard view ----------------
    def _build_dashboard(self, parent):
        ttk.Label(parent, text="Dashboard", style="Header.TLabel").pack(anchor="w", pady=8)
        btns = ttk.Frame(parent)
        btns.pack(fill="x", padx=6, pady=4)
        ttk.Button(btns, text="Gráfica: Producción vs Tiempo", command=self.plot_production_chart).pack(side="left", padx=4)
        ttk.Button(btns, text="Gráfica: Inventario actual", command=self.plot_inventory_chart).pack(side="left", padx=4)
        ttk.Button(btns, text="Resumen rápido", command=self.quick_summary).pack(side="left", padx=4)
        self.txt_dashboard = tk.Text(parent, height=15, wrap="word")
        self.txt_dashboard.pack(fill="both", expand=True, padx=6, pady=6)

    # ---------------- Navegación ----------------
    def show_frame(self, name):
        for n, f in self.frames.items():
            if n == name:
                f.lift()
        self.current_frame = name
        if name == "orders":
            self.refresh_orders()
        elif name == "materials":
            self.refresh_materials()
        elif name == "dashboard":
            self.refresh_dashboard()

    def show_register(self):
        self.show_frame("register")

    def show_orders(self):
        self.show_frame("orders")

    def show_production(self):
        self.show_frame("production")

    def show_materials(self):
        self.show_frame("materials")

    def show_qc(self):
        self.show_frame("qc")

    def show_dashboard(self):
        self.show_frame("dashboard")

    # ---------------- Funciones de órdenes ----------------
    def add_order(self):
        cliente = self.reg_cliente.get().strip()
        graduacion = self.reg_graduacion.get().strip()
        tipo = self.reg_tipo.get()
        if not cliente or not graduacion:
            messagebox.showwarning("Datos incompletos", "Rellena cliente y graduación.")
            return
        add_order_db(cliente, graduacion, tipo)
        messagebox.showinfo("Orden agregada", "Orden registrada correctamente.")
        self.reg_cliente.delete(0, tk.END)
        self.reg_graduacion.delete(0, tk.END)
        self.refresh_orders()

    def refresh_orders(self):
        for i in self.tree_orders.get_children():
            self.tree_orders.delete(i)
        for row in fetch_orders():
            self.tree_orders.insert("", "end", values=row)

    def search_orders(self):
        term = self.search_var.get().strip()
        for i in self.tree_orders.get_children():
            self.tree_orders.delete(i)
        for row in fetch_orders(search_term=term):
            self.tree_orders.insert("", "end", values=row)

    def get_selected_order(self):
        sel = self.tree_orders.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona una orden primero.")
            return None
        item = self.tree_orders.item(sel[0])['values']
        return item  # tuple (id, cliente, graduacion, tipo, estado, fecha)

    def edit_order(self):
        sel = self.get_selected_order()
        if not sel:
            return
        order_id = sel[0]
        cliente = simpledialog.askstring("Editar", "Cliente:", initialvalue=sel[1], parent=self)
        if cliente is None: return
        graduacion = simpledialog.askstring("Editar", "Graduación:", initialvalue=sel[2], parent=self)
        if graduacion is None: return
        tipo = simpledialog.askstring("Editar", "Tipo:", initialvalue=sel[3], parent=self)
        if tipo is None: return
        estados = ["Pendiente", "En producción", "Completada", "Rechazada"]
        estado = simpledialog.askstring("Estado", "Estado (Pendiente/En producción/Completada/Rechazada):", initialvalue=sel[4], parent=self)
        if estado is None: return
        update_order_db(order_id, cliente, graduacion, tipo, estado)
        messagebox.showinfo("Editada", "Orden actualizada.")
        self.refresh_orders()

    def delete_order(self):
        sel = self.get_selected_order()
        if not sel:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar la orden seleccionada?"):
            delete_order_db(sel[0])
            messagebox.showinfo("Eliminada", "Orden eliminada.")
            self.refresh_orders()

    def change_state_selected(self, new_state):
        sel = self.get_selected_order()
        if not sel:
            return
        update_order_db(sel[0], sel[1], sel[2], sel[3], new_state)
        self.refresh_orders()

    # ---------------- Fabricación (simulación) ----------------
    def start_fabrication_selected(self):
        sel = self.get_selected_order()
        if not sel:
            return
        order_id, cliente, graduacion, tipo, estado, fecha = sel
        available, missing = materials_available_for(tipo)
        if not available:
            messagebox.showerror("Materiales insuficientes", f"Falta material: {missing}. Revisa inventario.")
            return
        # Confirm
        if not messagebox.askyesno("Fabricar", f"Iniciar fabricación para {cliente} (Tipo: {tipo})?"):
            return
        # Lanzar thread para no bloquear GUI
        t = threading.Thread(target=self._fabrication_process, args=(order_id, tipo))
        t.daemon = True
        t.start()

    def _fabrication_process(self, order_id, tipo):
        # Simulación paso a paso con progreso
        steps = ["Corte de micas", "Pulido", "Tratamiento antirreflejante", "Montaje en armazón", "Control final"]
        total = len(steps)
        self.progress['maximum'] = total
        self.progress['value'] = 0
        for i, step in enumerate(steps, 1):
            self.lbl_prog.config(text=f"{step} ({i}/{total})")
            time.sleep(1.2)  # simulación (ajustable)
            self.progress['value'] = i
            # opcional: en cada paso verificar QC simulado
        # Consumir materiales y completar
        consume_materials(tipo)
        record_production(order_id, f"Fabricado: {tipo}")
        update_order_db(order_id, *self._get_order_data_for_update(order_id))
        # cambiar estado a completada
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE ordenes SET estado=? WHERE id=?", ("Completada", order_id))
        conn.commit()
        conn.close()
        self.lbl_prog.config(text="Completado")
        messagebox.showinfo("Fabricación", "Fabricación completada y materiales actualizados.")
        self.refresh_all()
        self.progress['value'] = 0

    def _get_order_data_for_update(self, order_id):
        # helper que devuelve cliente, graduacion, tipo, estado (se usa para update_order_db)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT cliente, graduacion, tipo, estado FROM ordenes WHERE id=?", (order_id,))
        r = c.fetchone()
        conn.close()
        if r:
            return (r[0], r[1], r[2], r[3])
        return ("", "", "", "")

    # ---------------- Bulk production simulation ----------------
    def simulate_bulk_production(self):
        count = simpledialog.askinteger("Simulación masiva", "¿Cuántas unidades simular?", minvalue=1, maxvalue=100, parent=self)
        if not count:
            return
        t = threading.Thread(target=self._simulate_bulk_thread, args=(count,))
        t.daemon = True
        t.start()

    def _simulate_bulk_thread(self, count):
        self.progress['maximum'] = count
        self.progress['value'] = 0
        self.lbl_prog.config(text="Simulación masiva iniciada")
        mats = fetch_materials()
        mat_dict = {m[0]: m[1] for m in mats}
        produced = 0
        for i in range(count):
            time.sleep(0.4)
            # intentar fabricar lente "Visión Sencilla"
            can, missing = materials_available_for("Visión Sencilla")
            if not can:
                self.lbl_prog.config(text=f"Detenido: falta {missing}")
                messagebox.showwarning("Simulación", f"Detenido en {i} unidades — falta {missing}")
                break
            consume_materials("Visión Sencilla")
            produced += 1
            self.progress['value'] = i+1
        record_production(0, f"Producción masiva: {produced} unidades")
        self.lbl_prog.config(text=f"Simulación finalizada ({produced} unidades)")
        self.progress['value'] = 0
        self.refresh_all()

    # ---------------- Inventario ----------------
    def refresh_materials(self):
        for i in self.tree_mats.get_children():
            self.tree_mats.delete(i)
        for nombre, cantidad, umbral in fetch_materials():
            self.tree_mats.insert("", "end", values=(nombre, cantidad, umbral))

    def show_inventory(self):
        rows = fetch_materials()
        texto = "\n".join([f"{r[0]}: {r[1]} unidades (Umbral: {r[2]})" for r in rows])
        messagebox.showinfo("Inventario", texto)

    def adjust_material(self):
        sel = self.tree_mats.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un material en la lista.")
            return
        item = self.tree_mats.item(sel[0])['values']
        nombre = item[0]
        cantidad_actual = item[1]
        nuevo = simpledialog.askinteger("Ajustar", f"Nuevo stock para {nombre}:", initialvalue=cantidad_actual, minvalue=0, parent=self)
        if nuevo is None:
            return
        update_material(nombre, nuevo)
        messagebox.showinfo("Actualizado", f"{nombre} ahora tiene {nuevo} unidades.")
        self.refresh_materials()

    def add_material(self):
        nombre = simpledialog.askstring("Nuevo material", "Nombre del material:", parent=self)
        if not nombre:
            return
        cantidad = simpledialog.askinteger("Cantidad", "Cantidad inicial:", minvalue=0, parent=self)
        if cantidad is None:
            return
        umbral = simpledialog.askinteger("Umbral", "Umbral de alerta:", minvalue=0, parent=self)
        if umbral is None:
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO materiales (nombre, cantidad, umbral) VALUES (?, ?, ?)", (nombre, cantidad, umbral))
            conn.commit()
            messagebox.showinfo("Agregado", f"Material {nombre} agregado.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ese material ya existe.")
        conn.close()
        self.refresh_materials()

    def remove_material(self):
        sel = self.tree_mats.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un material.")
            return
        item = self.tree_mats.item(sel[0])['values']
        nombre = item[0]
        if messagebox.askyesno("Confirmar", f"Eliminar material {nombre}?"):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM materiales WHERE nombre=?", (nombre,))
            conn.commit()
            conn.close()
            self.refresh_materials()

    def check_low_stock_alerts(self):
        low = []
        for nombre, cantidad, umbral in fetch_materials():
            if cantidad <= umbral:
                low.append(f"{nombre}: {cantidad} (umbral {umbral})")
        if not low:
            messagebox.showinfo("Alertas", "No hay materiales por debajo del umbral.")
        else:
            messagebox.showwarning("Alertas de inventario", "Materiales críticos:\n" + "\n".join(low))

    # ---------------- Control de calidad (QC) ----------------
    def perform_qc(self):
        sel = self.get_selected_order()
        if not sel:
            return
        order_id = sel[0]
        resultado = simpledialog.askstring("QC", "Resultado (Aprobado/Rechazado):", initialvalue="Aprobado", parent=self)
        if not resultado:
            return
        observaciones = simpledialog.askstring("Observaciones", "Observaciones (opcional):", parent=self)
        record_qc(order_id, resultado, observaciones or "")
        if resultado.lower().startswith("r"):
            # si rechazado, marcar orden como Rechazada
            update_order_db(order_id, sel[1], sel[2], sel[3], "Rechazada")
        messagebox.showinfo("QC", "Registro QC guardado.")
        self.refresh_all()

    def view_qc_history(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, orden_id, resultado, observaciones, fecha FROM qc ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        if not rows:
            messagebox.showinfo("QC", "No hay historial QC.")
            return
        txt = "\n".join([f"#{r[0]} - Orden {r[1]} - {r[2]} - {r[4]}\nObs: {r[3]}" for r in rows])
        # mostrar en ventana grande
        win = tk.Toplevel(self)
        win.title("Historial QC")
        text = tk.Text(win, wrap="word", width=80, height=30)
        text.pack(fill="both", expand=True)
        text.insert("1.0", txt)

    # ---------------- Producción log ----------------
    def show_production_log(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, orden_id, resultado, fecha FROM produccion ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        if not rows:
            messagebox.showinfo("Producción", "Aún no hay registros de producción.")
            return
        txt = "\n".join([f"#{r[0]} - Orden {r[1]} - {r[2]} - {r[3]}" for r in rows])
        win = tk.Toplevel(self)
        win.title("Registro de Producción")
        text = tk.Text(win, wrap="word", width=80, height=30)
        text.pack(fill="both", expand=True)
        text.insert("1.0", txt)

    # ---------------- Export / Import CSV ----------------
    def export_orders_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Exportar órdenes a CSV")
        if not path:
            return
        rows = fetch_orders()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id","cliente","graduacion","tipo","estado","fecha"])
            w.writerows(rows)
        messagebox.showinfo("Exportado", f"Órdenes exportadas a {path}")

    def export_materials_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Exportar inventario a CSV")
        if not path:
            return
        rows = fetch_materials()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["nombre","cantidad","umbral"])
            w.writerows(rows)
        messagebox.showinfo("Exportado", f"Inventario exportado a {path}")

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")], title="Importar órdenes desde CSV")
        if not path:
            return
        with open(path, newline="", encoding="utf-8") as f:
            r = csv.reader(f)
            headers = next(r, [])
            # Espera columnas: cliente, graduacion, tipo (si hay id/estado/fecha se ignoran)
            count = 0
            for row in r:
                if not row:
                    continue
                # intentar mapear por longitud
                if len(row) >= 3:
                    cliente, graduacion, tipo = row[0], row[1], row[2]
                    add_order_db(cliente, graduacion, tipo)
                    count += 1
            messagebox.showinfo("Importado", f"Importadas {count} órdenes desde {os.path.basename(path)}")
            self.refresh_orders()

    # ---------------- Dashboard / Charts ----------------
    def refresh_dashboard(self):
        # resumen simple
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM ordenes")
        total_ordenes = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM ordenes WHERE estado='Completada'")
        completadas = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM produccion")
        producida = c.fetchone()[0]
        conn.close()
        txt = f"Resumen rápido:\n- Órdenes totales: {total_ordenes}\n- Órdenes completadas: {completadas}\n- Registros de producción: {producida}\n\nPara ver gráficas, pulsa las opciones de la derecha."
        self.txt_dashboard.delete("1.0", "end")
        self.txt_dashboard.insert("1.0", txt)

    def plot_production_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showwarning("Matplotlib no disponible", "Instala matplotlib para ver gráficas (pip install matplotlib).")
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT fecha FROM produccion ORDER BY fecha")
        rows = c.fetchall()
        conn.close()
        if not rows:
            messagebox.showinfo("Gráfica", "No hay datos de producción para graficar.")
            return
        # contar por fecha (día)
        counts = {}
        for r in rows:
            day = r[0].split(" ")[0]
            counts[day] = counts.get(day, 0) + 1
        xs = sorted(counts.keys())
        ys = [counts[x] for x in xs]
        plt.figure(figsize=(8,4))
        plt.plot(xs, ys)
        plt.title("Producción por día")
        plt.xlabel("Fecha")
        plt.ylabel("Unidades / registros")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_inventory_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showwarning("Matplotlib no disponible", "Instala matplotlib para ver gráficas (pip install matplotlib).")
            return
        rows = fetch_materials()
        if not rows:
            messagebox.showinfo("Gráfica", "No hay inventario para graficar.")
            return
        names = [r[0] for r in rows]
        qtys = [r[1] for r in rows]
        plt.figure(figsize=(8,4))
        plt.bar(names, qtys)
        plt.title("Inventario actual")
        plt.xlabel("Material")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        plt.show()

    def quick_summary(self):
        # muestra inventario, órdenes top 5 recientes, alertas
        mats = fetch_materials()
        orders = fetch_orders()
        low = []
        for nombre, cantidad, umbral in mats:
            if cantidad <= umbral:
                low.append(f"{nombre} ({cantidad})")
        summary = "Quick summary\n\nInventario:\n" + "\n".join([f"- {m[0]}: {m[1]} (umbral {m[2]})" for m in mats])
        summary += "\n\nÓrdenes recientes:\n" + "\n".join([f"- #{o[0]} {o[1]} ({o[2]}) - {o[3]} - {o[4]}" for o in orders[:5]])
        summary += "\n\nAlertas críticas:\n" + (", ".join(low) if low else "Ninguna")
        self.txt_dashboard.delete("1.0", "end")
        self.txt_dashboard.insert("1.0", summary)

    # ---------------- Refrescar global ----------------
    def refresh_all(self):
        self.refresh_orders()
        self.refresh_materials()
        self.refresh_dashboard()

# ---------------------------------------------------------------------
# Lanzar ventana
# ---------------------------------------------------------------------
if __name__ == "__main__":
    ventana = App()
    ventana.mainloop()
