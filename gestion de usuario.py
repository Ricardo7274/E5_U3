import tkinter as tk
from tkinter import messagebox

# ========= ARREGLO PARA GUARDAR EL PERFIL =========
perfil_usuario = []


# ==========================
# GUARDAR PERFIL EN ARREGLO
# ==========================

def guardar_perfil():
    nombre = entry_nombre.get()
    usuario = entry_usuario.get()
    telefono = entry_telefono.get()
    correo = entry_correo.get()

    if nombre == "" or usuario == "":
        messagebox.showerror("Error", "Nombre y usuario son obligatorios")
        return

    # Limpiar arreglo anterior
    perfil_usuario.clear()

    # Guardar en arreglo
    perfil_usuario.append(nombre)
    perfil_usuario.append(usuario)
    perfil_usuario.append(telefono)
    perfil_usuario.append(correo)

    messagebox.showinfo("Guardado", "Perfil guardado en el arreglo correctamente")


# ==========================
# CARGAR PERFIL DESDE ARREGLO
# ==========================

def cargar_perfil():
    if not perfil_usuario:
        messagebox.showwarning("Aviso", "No hay datos en el arreglo")
        return

    entry_nombre.delete(0, tk.END)
    entry_usuario.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_correo.delete(0, tk.END)

    entry_nombre.insert(0, perfil_usuario[0])
    entry_usuario.insert(0, perfil_usuario[1])
    entry_telefono.insert(0, perfil_usuario[2])
    entry_correo.insert(0, perfil_usuario[3])

    messagebox.showinfo("Perfil", "Perfil cargado desde el arreglo")


# ==========================
# VENTANA PRINCIPAL
# ==========================

ventana = tk.Tk()
ventana.title("Gestión de Perfil - Óptica")
ventana.geometry("700x500")
ventana.config(bg="#F9F9F9")


# ==========================
# TÍTULO
# ==========================

titulo = tk.Label(
    ventana,
    text="👤 Gestión de Perfil de Usuario",
    font=("Arial", 14, "bold"),
    bg="#F9F9F9"
)
titulo.pack(pady=10)


# ==========================
# CAMPOS DE PERFIL
# ==========================

tk.Label(ventana, text="Nombre completo:", bg="#F9F9F9").pack(anchor="w", padx=20)
entry_nombre = tk.Entry(ventana, width=35)
entry_nombre.pack(pady=5)

tk.Label(ventana, text="Usuario:", bg="#F9F9F9").pack(anchor="w", padx=20)
entry_usuario = tk.Entry(ventana, width=35)
entry_usuario.pack(pady=5)

tk.Label(ventana, text="Teléfono:", bg="#F9F9F9").pack(anchor="w", padx=20)
entry_telefono = tk.Entry(ventana, width=35)
entry_telefono.pack(pady=5)

tk.Label(ventana, text="Correo electrónico:", bg="#F9F9F9").pack(anchor="w", padx=20)
entry_correo = tk.Entry(ventana, width=35)
entry_correo.pack(pady=5)


# ==========================
# BOTONES
# ==========================

frame_botones = tk.Frame(ventana, bg="#F9F9F9")
frame_botones.pack(pady=20)

btn_guardar = tk.Button(
    frame_botones,
    text="Guardar Perfil",
    bg="#28A745",
    fg="white",
    width=15,
    command=guardar_perfil
)
btn_guardar.grid(row=0, column=0, padx=10)

btn_cargar = tk.Button(
    frame_botones,
    text="Cargar Perfil",
    bg="#007BFF",
    fg="white",
    width=15,
    command=cargar_perfil
)
btn_cargar.grid(row=0, column=1, padx=10)

ventana.mainloop()
