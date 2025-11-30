import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, Image, ImageOps
import time

# ===========================
# CONSTANTES DE LOGIN
# ===========================
USUARIO_FABRICANTE = "fabricante"
CONTRASENA_FABRICANTE = "lentes123"

# ===========================
# ARREGLOS EN MEMORIA
# ===========================
usuarios_registrados = [{"usuario": USUARIO_FABRICANTE, "password": CONTRASENA_FABRICANTE}]
ordenes = []
materiales = []
proveedores = []
inventario = []
contador_orden = 1

# ===========================
# UTILIDADES GLOBALES
# ===========================
menu_abierto = False

def desbloquear_menu():
    btn_reg_material.config(state="normal")
    btn_reg_orden.config(state="normal")
    btn_proveedores.config(state="normal")
    btn_inventario.config(state="normal")
    btn_reportes.config(state="normal")
    btn_gestion_usuario.config(state="normal")  # habilita gestión de usuario sólo después del login
    # opcional: abrir automáticamente la sección de órdenes
    mostrar_seccion("ordenes")

# ===========================
# VENTANA PRINCIPAL (ROOT)
# ===========================
root = tk.Tk()
root.title("Three Ways Optics - Inicio")
root.geometry("900x750")
root.configure(bg="#F7F9FC")

# --------------------------
# Cargar logo (si existe)
# --------------------------
try:
    logo_img = Image.open("wa.jpg")
    logo_img = logo_img.resize((150, 100), Image.Resampling.LANCZOS)
    logo_render = ImageTk.PhotoImage(logo_img)
except Exception:
    logo_render = None

if logo_render:
    tk.Label(root, image=logo_render, bg="#F7F9FC").place(x=10, y=10)
    root.logo = logo_render

# --------------------------
# Encabezado (tal como pediste)
# --------------------------
header_frame = tk.Frame(root, bg="#F7F9FC")
header_frame.pack(pady=25)

tk.Label(
    header_frame,
    text="Three Ways Optics",
    font=("Georgia", 38, "bold"),
    fg="#0A62B3",
    bg="#F7F9FC"
).pack()

tk.Label(
    header_frame,
    text="Una mejor visión, un mejor futuro: Donde la claridad es poder",
    font=("Georgia", 16, "italic"),
    fg="#3A3A3A",
    bg="#F7F9FC"
).pack(pady=5)

# --------------------------
# Contenedor principal para secciones (home, ordenes, etc.)
# --------------------------
secciones_container = tk.Frame(root, bg="#F7F9FC")
secciones_container.pack(fill="both", expand=True, padx=40, pady=(0,20))

# ===========================
# SECCION: INICIO (home_frame)
# ===========================
home_frame = tk.Frame(secciones_container, bg="#F7F9FC")
home_frame.place(relwidth=1, relheight=1)

info_frame = tk.Frame(home_frame, bg="white", bd=2, relief="solid")
info_frame.pack(pady=10, ipadx=20, ipady=20, fill="both", expand=False)

info_text = """
Misión:
"Proporcionar lentes de alta calidad y diseños innovadores,
combinando tecnología avanzada con un servicio excepcional."

Visión:
"Ser el referente en innovación y calidad en el mercado de lentes,
ofreciendo soluciones ópticas personalizadas y accesibles."

-------------------------------------------------------------

Contacto:
Número Telefónico: +52 55 1234 5678
Correo: threewaysoptics@gmail.com
Ubicación: CDMX, CP 06000

Sucursal Puebla:
Dirección: Avenida Presidente Masaryk, 456
"""
tk.Label(info_frame, text=info_text, font=("Arial", 12),
         justify="left", bg="white").pack()

# ===========================
# SECCION: REGISTRO DE ÓRDENES (orders_frame)
# ===========================
orders_frame = tk.Frame(secciones_container, bg="#F7F9FC")

# We'll create the widgets and functions needed for the orders frame.
# Using globals for widgets so functions can access them easily.

# CLIENTE
frame_cliente = tk.LabelFrame(orders_frame, text="Datos del Cliente")
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

# PRODUCTO
frame_producto = tk.LabelFrame(orders_frame, text="Datos del Producto")
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

# GRADUACIÓN
frame_graduacion = tk.LabelFrame(orders_frame, text="Graduación")
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

# TRATAMIENTOS
frame_trat = tk.LabelFrame(orders_frame, text="Tratamientos")
frame_trat.place(x=450, y=200, width=600, height=100)

var_antireflejo = tk.BooleanVar()
var_fotocromatico = tk.BooleanVar()
var_blue = tk.BooleanVar()
var_anti_rayas = tk.BooleanVar()

tk.Checkbutton(frame_trat, text="Antirreflejante", variable=var_antireflejo).place(x=10, y=10)
tk.Checkbutton(frame_trat, text="Fotocromático", variable=var_fotocromatico).place(x=200, y=10)
tk.Checkbutton(frame_trat, text="Filtro Azul", variable=var_blue).place(x=400, y=10)
tk.Checkbutton(frame_trat, text="Antirrayas", variable=var_anti_rayas).place(x=10, y=40)

# FUNCIONES DE LA SECCIÓN DE ÓRDENES
def es_numero(valor):
    try:
        float(valor)
        return True
    except:
        return False

def registrar_orden():
    global contador_orden
    nombre = entry_nombre.get().strip()
    telefono = entry_telefono.get().strip()
    tipo_lentes_v = combo_lentes.get()
    tipo_mica_v = combo_mica.get()
    material_v = combo_material.get()
    armazon_v = entry_armazon.get().strip()
    pago_v = combo_pago.get()
    precio_v = entry_precio.get().strip()

    od_esf_v = entry_od_esf.get()
    od_cil_v = entry_od_cil.get()
    od_eje_v = entry_od_eje.get()

    oi_esf_v = entry_oi_esf.get()
    oi_cil_v = entry_oi_cil.get()
    oi_eje_v = entry_oi_eje.get()

    if nombre == "" or telefono == "" or precio_v == "":
        messagebox.showwarning("Error", "Nombre, Teléfono y Precio son obligatorios.")
        return

    if not es_numero(precio_v):
        messagebox.showerror("Error", "El precio debe ser numérico.")
        return

    tratamientos_list = []
    if var_antireflejo.get(): tratamientos_list.append("Antirreflejante")
    if var_fotocromatico.get(): tratamientos_list.append("Fotocromático")
    if var_blue.get(): tratamientos_list.append("Filtro Azul")
    if var_anti_rayas.get(): tratamientos_list.append("Antirrayas")

    orden = {
        "id": contador_orden,
        "nombre": nombre,
        "telefono": telefono,
        "tipo_lentes": tipo_lentes_v,
        "tipo_mica": tipo_mica_v,
        "material": material_v,
        "armazon": armazon_v,
        "graduacion": {
            "OD": {"esf": od_esf_v, "cil": od_cil_v, "eje": od_eje_v},
            "OI": {"esf": oi_esf_v, "cil": oi_cil_v, "eje": oi_eje_v}
        },
        "tratamientos": tratamientos_list,
        "forma_pago": pago_v,
        "precio": precio_v
    }

    ordenes.append(orden)
    contador_orden += 1
    actualizar_lista_ordenes()
    limpiar_campos_orden()
    messagebox.showinfo("Éxito", "Orden registrada correctamente ✅")

def actualizar_lista_ordenes():
    tree_orders.delete(*tree_orders.get_children())
    for o in ordenes:
        tree_orders.insert("", tk.END, values=(o["id"], o["nombre"], o["telefono"], o["tipo_lentes"], o["material"], "$" + o["precio"]))

def eliminar_orden():
    sel = tree_orders.selection()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona una orden primero.")
        return
    item = tree_orders.item(sel)
    id_orden = item["values"][0]
    for o in ordenes:
        if o["id"] == id_orden:
            ordenes.remove(o)
            break
    actualizar_lista_ordenes()
    messagebox.showinfo("Listo", "Orden eliminada correctamente.")

def limpiar_campos_orden():
    campos = [
        entry_nombre, entry_telefono, entry_armazon,
        entry_precio, entry_od_esf, entry_od_cil, entry_od_eje,
        entry_oi_esf, entry_oi_cil, entry_oi_eje
    ]
    for c in campos:
        try:
            c.delete(0, tk.END)
        except:
            pass
    var_antireflejo.set(False)
    var_fotocromatico.set(False)
    var_blue.set(False)
    var_anti_rayas.set(False)

# BOTONES de la sección órdenes
btn_registrar_orden = tk.Button(orders_frame, text="Registrar Orden", bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), width=20, command=registrar_orden)
btn_registrar_orden.place(x=150, y=350)

btn_eliminar_orden = tk.Button(orders_frame, text="Eliminar Orden", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), width=18, command=eliminar_orden)
btn_eliminar_orden.place(x=450, y=350)

# TABLA DE ÓRDENES (Treeview)
frame_lista = tk.LabelFrame(orders_frame, text="Órdenes Registradas")
frame_lista.place(x=20, y=420, width=1030, height=250)

cols = ("ID", "Cliente", "Teléfono", "Tipo", "Material", "Precio")
tree_orders = ttk.Treeview(frame_lista, columns=cols, show="headings")
for col in cols:
    tree_orders.heading(col, text=col)
    tree_orders.column(col, width=160)
tree_orders.pack(fill="both", expand=True)

# ===========================
# SECCIÓN: OTROS (placeholders)
# ===========================
# Puedes expandir estos frames para registrar materiales/proveedores/inventario.
materials_frame = tk.Frame(secciones_container, bg="#F7F9FC")
providers_frame = tk.Frame(secciones_container, bg="#F7F9FC")
inventory_frame = tk.Frame(secciones_container, bg="#F7F9FC")
reports_frame = tk.Frame(secciones_container, bg="#F7F9FC")

# Rellenar mínimamente para evitar errores visuales
tk.Label(materials_frame, text="Registro de Materiales (vacío por ahora)", bg="#F7F9FC").pack(pady=50)
tk.Label(providers_frame, text="Proveedores (vacío por ahora)", bg="#F7F9FC").pack(pady=50)
tk.Label(inventory_frame, text="Inventario (vacío por ahora)", bg="#F7F9FC").pack(pady=50)
tk.Label(reports_frame, text="Reportes (vacío por ahora)", bg="#F7F9FC").pack(pady=50)

# ===========================
# FUNCION PARA MOSTRAR SECCIÓN
# ===========================
secciones = {
    "home": home_frame,
    "ordenes": orders_frame,
    "materiales": materials_frame,
    "proveedores": providers_frame,
    "inventario": inventory_frame,
    "reportes": reports_frame
}

def ocultar_todas_secciones():
    for f in secciones.values():
        f.place_forget()

def mostrar_seccion(nombre):
    ocultar_todas_secciones()
    frame = secciones.get(nombre, home_frame)
    frame.place(relwidth=1, relheight=1)

# mostrar home al inicio
mostrar_seccion("home")

# ===========================
# PIE DE PÁGINA
# ===========================
separator = tk.Frame(root, bg="#C4C4C4", height=1)
separator.pack(fill="x", pady=(10, 0))

footer_bg = tk.Frame(root, bg="#F7F9FC", height=70)
footer_bg.pack(side="bottom", fill="x", pady=(0, 10))

tk.Label(
    footer_bg,
    text="Todos los derechos reservados por: K.A.R.S",
    font=("Arial", 11),
    fg="#1F1F1F",
    bg="#F7F9FC"
).pack()

tk.Label(
    footer_bg,
    text="Diseño elegante y minimalista",
    font=("Arial", 9, "italic"),
    fg="#5A5A5A",
    bg="#F7F9FC"
).pack()

# ===========================
# MENÚ HAMBURGUESA DESLIZANTE (parte superior derecha)
# ===========================
menu_frame = tk.Frame(root, width=200, height=750, bg="#E9F1FA")
menu_frame.place(x=900, y=0)  # off-screen initially

tk.Label(menu_frame, text="MENÚ", bg="#E9F1FA", font=("Georgia", 20, "bold")).pack(pady=20)

# LOGIN (abre Toplevel)
def abrir_login():
    # crea Toplevel para login (no duplicar root)
    login_win = tk.Toplevel(root)
    login_win.title("Login Fabricante - Óptica")
    login_win.geometry("380x320")
    login_win.configure(bg="white")
    login_win.transient(root)  # vincula con root

    tk.Label(login_win, text="Acceso para Fabricante", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

    tk.Label(login_win, text="Usuario:", bg="white", font=("Arial", 12)).pack()
    entry_usr = tk.Entry(login_win, width=30)
    entry_usr.pack(pady=5)

    tk.Label(login_win, text="Contraseña:", bg="white", font=("Arial", 12)).pack()
    entry_pwd = tk.Entry(login_win, width=30, show="*")
    entry_pwd.pack(pady=5)

    def verificar_login_local():
        usr = entry_usr.get()
        pwd = entry_pwd.get()
        if usr == USUARIO_FABRICANTE and pwd == CONTRASENA_FABRICANTE:
            messagebox.showinfo("Acceso permitido", "Bienvenido fabricante 👓")
            desbloquear_menu()
            login_win.destroy()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")

    tk.Button(login_win, text="Iniciar sesión", font=("Arial", 12), width=15, bg="#3498db", fg="white", command=verificar_login_local).pack(pady=18)

# Formulario de contacto en Toplevel (tal como lo pediste)
def abrir_contacto():
    ventana = tk.Toplevel(root)
    ventana.title("Formulario de Contacto - Three Ways Optics")
    ventana.geometry("700x600")
    ventana.config(bg="#F9F9F9")

    try:
        img_logo = Image.open("log.jpeg")
        img_logo = img_logo.resize((120, 120))
        img_logo_render = ImageTk.PhotoImage(img_logo)
    except:
        img_logo_render = None

    if img_logo_render:
        tk.Label(ventana, image=img_logo_render, bg="#F9F9F9").pack(pady=10)
        ventana.logo = img_logo_render

    tk.Label(ventana, text="📞 Contáctanos - Three Ways Optics",
             font=("Arial", 16, "bold"), bg="#F9F9F9").pack(pady=5)

    tk.Label(ventana, text="Nombre:", bg="#F9F9F9").pack(anchor="w", padx=20)
    entry_nombre_contact = tk.Entry(ventana, width=45)
    entry_nombre_contact.pack()

    tk.Label(ventana, text="Teléfono:", bg="#F9F9F9").pack(anchor="w", padx=20)
    entry_telefono_contact = tk.Entry(ventana, width=45)
    entry_telefono_contact.pack()

    tk.Label(ventana, text="Correo:", bg="#F9F9F9").pack(anchor="w", padx=20)
    entry_correo_contact = tk.Entry(ventana, width=45)
    entry_correo_contact.pack()

    tk.Label(ventana, text="Mensaje:", bg="#F9F9F9").pack(anchor="w", padx=20)
    txt_mensaje_contact = tk.Text(ventana, height=6, width=43)
    txt_mensaje_contact.pack(pady=10)

    def enviar_formulario_local():
        nombre = entry_nombre_contact.get()
        telefono = entry_telefono_contact.get()
        correo = entry_correo_contact.get()
        mensaje = txt_mensaje_contact.get("1.0", tk.END).strip()

        if nombre == "" or telefono == "" or mensaje == "":
            messagebox.showerror("Error", "Por favor llena los campos obligatorios.")
            return

        info = (
            f"📋 NUEVO MENSAJE\n\n"
            f"Nombre: {nombre}\n"
            f"Teléfono: {telefono}\n"
            f"Correo: {correo}\n\n"
            f"Mensaje:\n{mensaje}"
        )

        print(info)
        messagebox.showinfo("Formulario enviado", "Mensaje enviado correctamente.")

        entry_nombre_contact.delete(0, tk.END)
        entry_telefono_contact.delete(0, tk.END)
        entry_correo_contact.delete(0, tk.END)
        txt_mensaje_contact.delete("1.0", tk.END)

    tk.Button(ventana, text="Enviar mensaje", bg="#007BFF", fg="white", command=enviar_formulario_local).pack(pady=20)

# NUEVA FUNCIÓN: GESTIÓN DE USUARIO (Change password + add email)
def abrir_gestion_usuario():
    gestion_win = tk.Toplevel(root)
    gestion_win.title("Gestión de usuario - Fabricante")
    gestion_win.geometry("420x420")
    gestion_win.configure(bg="white")
    gestion_win.transient(root)

    tk.Label(gestion_win, text="Gestión de usuario - Fabricante", font=("Arial", 14, "bold"), bg="white").pack(pady=12)

    # Mostrar usuario actual
    tk.Label(gestion_win, text=f"Usuario: {USUARIO_FABRICANTE}", bg="white", font=("Arial", 11)).pack(pady=(0,8))

    # --- Sección: Añadir/editar correo ---
    correo_frame = tk.LabelFrame(gestion_win, text="Correo electrónico", bg="white")
    correo_frame.pack(padx=12, pady=8, fill="x")

    tk.Label(correo_frame, text="Correo:", bg="white").grid(row=0, column=0, padx=8, pady=8, sticky="w")
    entry_nuevo_correo = tk.Entry(correo_frame, width=35)
    entry_nuevo_correo.grid(row=0, column=1, padx=8, pady=8)

    def guardar_correo():
        nuevo_correo = entry_nuevo_correo.get().strip()
        if nuevo_correo == "":
            messagebox.showwarning("Atención", "Introduce un correo válido.")
            return
        # Buscar al usuario en usuarios_registrados y actualizar/añadir campo 'email'
        updated = False
        for u in usuarios_registrados:
            if u.get("usuario") == USUARIO_FABRICANTE:
                u["email"] = nuevo_correo
                updated = True
                break
        if not updated:
            usuarios_registrados.append({"usuario": USUARIO_FABRICANTE, "password": CONTRASENA_FABRICANTE, "email": nuevo_correo})
        messagebox.showinfo("Listo", "Correo actualizado correctamente ✅")
        entry_nuevo_correo.delete(0, tk.END)

    tk.Button(correo_frame, text="Guardar correo", command=guardar_correo, bg="#2ecc71", fg="white", width=18).grid(row=1, column=0, columnspan=2, pady=(4,10))

    # --- Sección: Cambiar contraseña ---
    pwd_frame = tk.LabelFrame(gestion_win, text="Cambiar contraseña", bg="white")
    pwd_frame.pack(padx=12, pady=8, fill="x")

    tk.Label(pwd_frame, text="Contraseña actual:", bg="white").grid(row=0, column=0, padx=8, pady=6, sticky="w")
    entry_pwd_actual = tk.Entry(pwd_frame, show="*", width=30)
    entry_pwd_actual.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(pwd_frame, text="Nueva contraseña:", bg="white").grid(row=1, column=0, padx=8, pady=6, sticky="w")
    entry_pwd_nueva = tk.Entry(pwd_frame, show="*", width=30)
    entry_pwd_nueva.grid(row=1, column=1, padx=8, pady=6)

    tk.Label(pwd_frame, text="Confirmar nueva:", bg="white").grid(row=2, column=0, padx=8, pady=6, sticky="w")
    entry_pwd_conf = tk.Entry(pwd_frame, show="*", width=30)
    entry_pwd_conf.grid(row=2, column=1, padx=8, pady=6)

    def cambiar_contrasena():
        global CONTRASENA_FABRICANTE
        actual = entry_pwd_actual.get()
        nueva = entry_pwd_nueva.get()
        conf = entry_pwd_conf.get()

        if actual == "" or nueva == "" or conf == "":
            messagebox.showwarning("Atención", "Completa todos los campos de contraseña.")
            return

        # validar contraseña actual
        if actual != CONTRASENA_FABRICANTE:
            messagebox.showerror("Error", "La contraseña actual es incorrecta.")
            return

        if nueva != conf:
            messagebox.showerror("Error", "La nueva contraseña y la confirmación no coinciden.")
            return

        # Actualizar la constante en memoria y el registro del usuario
        CONTRASENA_FABRICANTE = nueva
        for u in usuarios_registrados:
            if u.get("usuario") == USUARIO_FABRICANTE:
                u["password"] = nueva
                break
        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente ✅")

        # limpiar campos
        entry_pwd_actual.delete(0, tk.END)
        entry_pwd_nueva.delete(0, tk.END)
        entry_pwd_conf.delete(0, tk.END)

    tk.Button(pwd_frame, text="Cambiar contraseña", command=cambiar_contrasena, bg="#3498db", fg="white", width=18).grid(row=3, column=0, columnspan=2, pady=(6,12))

    # Mostrar correo actual si existe
    correo_actual = ""
    for u in usuarios_registrados:
        if u.get("usuario") == USUARIO_FABRICANTE and u.get("email"):
            correo_actual = u.get("email")
            break
    if correo_actual:
        tk.Label(gestion_win, text=f"Correo registrado: {correo_actual}", bg="white", font=("Arial", 10)).pack(pady=(6,8))

    tk.Button(gestion_win, text="Cerrar", command=gestion_win.destroy, width=12).pack(pady=10)

# Botones del menú (inicialmente solo Login y Formulario, el resto deshabilitados)
tk.Button(menu_frame, text="Iniciar sesión", width=20, command=abrir_login).pack(pady=5)
tk.Button(menu_frame, text="Formulario de contacto", width=20, command=abrir_contacto).pack(pady=5)

btn_reg_material = tk.Button(menu_frame, text="Registrar material", width=20, state="disabled", command=lambda: mostrar_seccion("materiales"))
btn_reg_material.pack(pady=5)

btn_reg_orden = tk.Button(menu_frame, text="Registrar orden", width=20, state="disabled", command=lambda: mostrar_seccion("ordenes"))
btn_reg_orden.pack(pady=5)

btn_proveedores = tk.Button(menu_frame, text="Proveedores", width=20, state="disabled", command=lambda: mostrar_seccion("proveedores"))
btn_proveedores.pack(pady=5)

btn_inventario = tk.Button(menu_frame, text="Inventario", width=20, state="disabled", command=lambda: mostrar_seccion("inventario"))
btn_inventario.pack(pady=5)

btn_reportes = tk.Button(menu_frame, text="Reportes", width=20, state="disabled", command=lambda: mostrar_seccion("reportes"))
btn_reportes.pack(pady=5)

# NUEVO BOTÓN: GESTIÓN DE USUARIO (inicialmente deshabilitado, se habilita tras login)
btn_gestion_usuario = tk.Button(menu_frame, text="Gestión de usuario", width=20, state="disabled", command=abrir_gestion_usuario)
btn_gestion_usuario.pack(pady=5)

# Botón hamburguesa en esquina superior derecha
def toggle_menu():
    global menu_abierto
    if not menu_abierto:
        abrir_menu_animado()
        menu_abierto = True
    else:
        cerrar_menu_animado()
        menu_abierto = False

btn_menu = tk.Button(root, text="≡", font=("Arial", 22, "bold"), bg="#0A62B3", fg="white", bd=0, command=toggle_menu)
btn_menu.place(x=840, y=20)

# Animación simple: mueve menu_frame desde x=900 (fuera) hasta x=700 (visible)
def abrir_menu_animado():
    current_x = 900
    target_x = 700
    step = 20
    while current_x > target_x:
        current_x -= step
        if current_x < target_x:
            current_x = target_x
        menu_frame.place(x=current_x, y=0)
        root.update()
        time.sleep(0.01)

def cerrar_menu_animado():
    current_x = 700
    target_x = 900
    step = 20
    while current_x < target_x:
        current_x += step
        if current_x > target_x:
            current_x = target_x
        menu_frame.place(x=current_x, y=0)
        root.update()
        time.sleep(0.01)

# ===========================
# Lanzar aplicación
# ===========================
root.mainloop()
