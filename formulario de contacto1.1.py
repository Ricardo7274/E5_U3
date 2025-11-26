import tkinter as tk
from tkinter import messagebox

# ==========================
# FUNCIÓN AL ENVIAR FORMULARIO
# ==========================

def enviar_formulario():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    correo = entry_correo.get()
    mensaje = txt_mensaje.get("1.0", tk.END).strip()

    if nombre == "" or telefono == "" or mensaje == "":
        messagebox.showerror("Error", "Por favor llena los campos obligatorios.")
        return

    info = (
        f"📋 NUEVO MENSAJE DE CLIENTE\n\n"
        f"Nombre: {nombre}\n"
        f"Teléfono: {telefono}\n"
        f"Correo: {correo}\n\n"
        f"Mensaje:\n{mensaje}"
    )

    print(info)
    messagebox.showinfo("Formulario enviado", "Mensaje enviado correctamente. Nos contactaremos contigo.")

    # Limpiar campos
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    txt_mensaje.delete("1.0", tk.END)


# ==========================
# VENTANA PRINCIPAL
# ==========================

ventana = tk.Tk()
ventana.title("Formulario de Contacto - Three ways optics")
ventana.geometry("700x550")
ventana.config(bg="#F9F9F9")

# ==========================
# TÍTULO
# ==========================

titulo = tk.Label(
    ventana,
    text="📞 Contáctanos - three ways optic",
    font=("Arial", 14, "bold"),
    bg="#F9F9F9"
)
titulo.pack(pady=10)

# ==========================
# CAMPOS DEL FORMULARIO
# ==========================

tk.Label(ventana, text="Nombre:", bg="#F9F9F9").pack(anchor="w", padx=20)
entry_nombre = tk.Entry(ventana, width=40)
entry_nombre.pack(pady=5)

tk.Label(ventana, text="Teléfono:", bg="#F9F9F9").pack(anchor="w", padx=20)
entry_telefono = tk.Entry(ventana, width=40)
entry_telefono.pack(pady=5)

tk.Label(ventana, text="Correo electrónico:", bg="#F9F9F9").pack(anchor="w", padx=20)
entry_correo = tk.Entry(ventana, width=40)
entry_correo.pack(pady=5)

tk.Label(ventana, text="Mensaje:", bg="#F9F9F9").pack(anchor="w", padx=20)
txt_mensaje = tk.Text(ventana, height=6, width=38)
txt_mensaje.pack(pady=10)

# ==========================
# BOTÓN ENVIAR
# ==========================

btn_enviar = tk.Button(
    ventana,
    text="Enviar mensaje",
    bg="#007BFF",
    fg="white",
    font=("Arial", 11, "bold"),
    command=enviar_formulario,
    width=20
)

btn_enviar.pack(pady=20)

ventana.mainloop()
