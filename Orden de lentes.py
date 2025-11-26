import tkinter as tk
from tkinter import ttk, messagebox

# ===============================
# ARREGLO DE ÓRDENES
# ===============================
ordenes = []
contador_orden = 1


# ===============================
# VALIDACIÓN DE NÚMEROS
# ===============================
def es_numero(valor):
    try:
        float(valor)
        return True
    except:
        return False


# ===============================
# REGISTRAR ORDEN
# ===============================
def registrar_orden():
    global contador_orden

    nombre = entry_nombre.get().strip()
    telefono = entry_telefono.get().strip()
    tipo_lentes = combo_lentes.get()
    tipo_mica = combo_mica.get()
    material = combo_material.get()
    armazon = entry_armazon.get().strip()
    pago = combo_pago.get()
    precio = entry_precio.get().strip()

    od_esf = entry_od_esf.get()
    od_cil = entry_od_cil.get()
    od_eje = entry_od_eje.get()

    oi_esf = entry_oi_esf.get()
    oi_cil = entry_oi_cil.get()
    oi_eje = entry_oi_eje.get()

    if nombre == "" or telefono == "" or precio == "":
        messagebox.showwarning("Error", "Nombre, Teléfono y Precio son obligatorios.")
        return

    if not es_numero(precio):
        messagebox.showerror("Error", "El precio debe ser numérico.")
        return

    tratamientos = []
    if var_antireflejo.get(): tratamientos.append("Antirreflejante")
    if var_fotocromatico.get(): tratamientos.append("Fotocromático")
    if var_blue.get(): tratamientos.append("Filtro Azul")
    if var_anti_rayas.get(): tratamientos.append("Antirrayas")

    orden = {
        "id": contador_orden,
        "nombre": nombre,
        "telefono": telefono,
        "tipo_lentes": tipo_lentes,
        "tipo_mica": tipo_mica,
        "material": material,
        "armazon": armazon,
        "graduacion": {
            "OD": {"esf": od_esf, "cil": od_cil, "eje": od_eje},
            "OI": {"esf": oi_esf, "cil": oi_cil, "eje": oi_eje}
        },
        "tratamientos": tratamientos,
        "forma_pago": pago,
        "precio": precio
    }

    ordenes.append(orden)
    contador_orden += 1
    actualizar_lista()
    limpiar_campos()

    messagebox.showinfo("Éxito", "Orden registrada correctamente ✅")


# ===============================
# ACTUALIZAR TABLA
# ===============================
def actualizar_lista():
    lista.delete(*lista.get_children())

    for orden in ordenes:
        lista.insert("", tk.END, values=(
            orden["id"],
            orden["nombre"],
            orden["telefono"],
            orden["tipo_lentes"],
            orden["material"],
            "$" + orden["precio"]
        ))


# ===============================
# ELIMINAR ORDEN
# ===============================
def eliminar_orden():
    seleccion = lista.selection()

    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona una orden primero.")
        return

    item = lista.item(seleccion)
    id_orden = item["values"][0]

    for orden in ordenes:
        if orden["id"] == id_orden:
            ordenes.remove(orden)
            break

    actualizar_lista()
    messagebox.showinfo("Listo", "Orden eliminada correctamente.")


# ===============================
# LIMPIAR CAMPOS
# ===============================
def limpiar_campos():
    campos = [
        entry_nombre, entry_telefono, entry_armazon,
        entry_precio, entry_od_esf, entry_od_cil, entry_od_eje,
        entry_oi_esf, entry_oi_cil, entry_oi_eje
    ]

    for campo in campos:
        campo.delete(0, tk.END)

    var_antireflejo.set(False)
    var_fotocromatico.set(False)
    var_blue.set(False)
    var_anti_rayas.set(False)


# ===============================
# VENTANA PRINCIPAL
# ===============================
ventana = tk.Tk()
ventana.title("Sistema de Registro de Órdenes - Óptica")
ventana.geometry("1100x750")

# ===============================
# CLIENTE
# ===============================
frame_cliente = tk.LabelFrame(ventana, text="Datos del Cliente")
frame_cliente.place(x=20, y=10, width=400, height=130)

tk.Label(frame_cliente, text="Nombre:").place(x=10, y=10)
entry_nombre = tk.Entry(frame_cliente, width=30)
entry_nombre.place(x=90, y=10)

tk.Label(frame_cliente, text="Teléfono:").place(x=10, y=45)
entry_telefono = tk.Entry(frame_cliente, width=30)
entry_telefono.place(x=90, y=45)

tk.Label(frame_cliente, text="Tipo de lentes:").place(x=10, y=80)
combo_lentes = ttk.Combobox(frame_cliente, values=[
    "Monofocal", "Bifocal", "Progresivo", "Ocupacional", "Descanso"
], width=27, state="readonly")
combo_lentes.place(x=90, y=80)
combo_lentes.current(0)

# ===============================
# PRODUCTO
# ===============================
frame_producto = tk.LabelFrame(ventana, text="Datos del Producto")
frame_producto.place(x=20, y=150, width=400, height=180)

tk.Label(frame_producto, text="Tipo de mica:").place(x=10, y=10)
combo_mica = ttk.Combobox(frame_producto,
                           values=["Clara", "Fotocromática", "Polarizada", "Solar"],
                           width=25, state="readonly")
combo_mica.place(x=100, y=10)
combo_mica.current(0)

tk.Label(frame_producto, text="Material:").place(x=10, y=45)
combo_material = ttk.Combobox(frame_producto,
                               values=["CR-39", "Policarbonato", "Hi-Index 1.67", "Hi-Index 1.74"],
                               width=25, state="readonly")
combo_material.place(x=100, y=45)
combo_material.current(0)

tk.Label(frame_producto, text="Armazón:").place(x=10, y=80)
entry_armazon = tk.Entry(frame_producto, width=27)
entry_armazon.place(x=100, y=80)

tk.Label(frame_producto, text="Forma de pago:").place(x=10, y=115)
combo_pago = ttk.Combobox(frame_producto,
                           values=["Efectivo", "Tarjeta", "Transferencia"],
                           width=25, state="readonly")
combo_pago.place(x=100, y=115)
combo_pago.current(0)

tk.Label(frame_producto, text="Precio: $").place(x=10, y=150)
entry_precio = tk.Entry(frame_producto, width=15)
entry_precio.place(x=80, y=150)

# ===============================
# GRADUACIÓN
# ===============================
frame_graduacion = tk.LabelFrame(ventana, text="Graduación")
frame_graduacion.place(x=450, y=10, width=600, height=180)

tk.Label(frame_graduacion, text="").grid(row=0, column=0)
tk.Label(frame_graduacion, text="ESF").grid(row=0, column=1)
tk.Label(frame_graduacion, text="CIL").grid(row=0, column=2)
tk.Label(frame_graduacion, text="EJE").grid(row=0, column=3)

tk.Label(frame_graduacion, text="OD").grid(row=1, column=0)
entry_od_esf = tk.Entry(frame_graduacion, width=10)
entry_od_esf.grid(row=1, column=1)
entry_od_cil = tk.Entry(frame_graduacion, width=10)
entry_od_cil.grid(row=1, column=2)
entry_od_eje = tk.Entry(frame_graduacion, width=10)
entry_od_eje.grid(row=1, column=3)

tk.Label(frame_graduacion, text="OI").grid(row=2, column=0)
entry_oi_esf = tk.Entry(frame_graduacion, width=10)
entry_oi_esf.grid(row=2, column=1)
entry_oi_cil = tk.Entry(frame_graduacion, width=10)
entry_oi_cil.grid(row=2, column=2)
entry_oi_eje = tk.Entry(frame_graduacion, width=10)
entry_oi_eje.grid(row=2, column=3)

# ===============================
# TRATAMIENTOS
# ===============================
frame_trat = tk.LabelFrame(ventana, text="Tratamientos")
frame_trat.place(x=450, y=200, width=600, height=100)

var_antireflejo = tk.BooleanVar()
var_fotocromatico = tk.BooleanVar()
var_blue = tk.BooleanVar()
var_anti_rayas = tk.BooleanVar()

tk.Checkbutton(frame_trat, text="Antirreflejante", variable=var_antireflejo).place(x=10, y=10)
tk.Checkbutton(frame_trat, text="Fotocromático", variable=var_fotocromatico).place(x=200, y=10)
tk.Checkbutton(frame_trat, text="Filtro Azul", variable=var_blue).place(x=400, y=10)
tk.Checkbutton(frame_trat, text="Antirrayas", variable=var_anti_rayas).place(x=10, y=40)

# ===============================
# BOTONES
# ===============================
btn_registrar = tk.Button(ventana, text="Registrar Orden",
                          bg="#2ecc71", fg="white",
                          font=("Arial", 12, "bold"),
                          width=20,
                          command=registrar_orden)
btn_registrar.place(x=150, y=350)

btn_eliminar = tk.Button(ventana, text="Eliminar Orden",
                         bg="#e74c3c", fg="white",
                         font=("Arial", 11, "bold"),
                         width=18,
                         command=eliminar_orden)
btn_eliminar.place(x=450, y=350)

# ===============================
# TABLA DE ÓRDENES
# ===============================
frame_lista = tk.LabelFrame(ventana, text="Órdenes Registradas")
frame_lista.place(x=20, y=420, width=1030, height=250)

tabla = ("ID", "Cliente", "Teléfono", "Tipo", "Material", "Precio")
lista = ttk.Treeview(frame_lista, columns=tabla, show="headings")

for col in tabla:
    lista.heading(col, text=col)
    lista.column(col, width=160)

lista.pack(fill="both", expand=True)

ventana.mainloop()