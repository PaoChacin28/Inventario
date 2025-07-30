# movement_management.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db_connection import conectar_db # Importamos la función de conexión
import mysql.connector
from tkinter import ttk

def registrar_movimiento(id_usuario):
    win = ttk.Toplevel()
    win.title("Registrar Movimiento")
    win.geometry("400x300")
    # No usamos transient con ventana_login directamente aquí, sino que la abrimos desde main.py

    ttk.Label(win, text="ID Producto").pack(pady=5)
    e_id = ttk.Entry(win)
    e_id.pack()

    ttk.Label(win, text="Tipo (Entrada/Salida)").pack(pady=5)
    e_tipo = ttk.Entry(win)
    e_tipo.pack()

    ttk.Label(win, text="Cantidad").pack(pady=5)
    e_cant = ttk.Entry(win)
    e_cant.pack()

    def guardar():
        try:
            tipo = e_tipo.get().capitalize()
            cantidad = int(e_cant.get())
            id_prod = int(e_id.get())

            if tipo not in ["Entrada", "Salida"]:
                messagebox.showerror("Error", "Tipo debe ser 'Entrada' o 'Salida'.")
                return

            db = conectar_db()
            if db is None:
                return
            cursor = db.cursor()

            # Verificar si el producto existe y obtener stock actual
            cursor.execute("SELECT id_producto, cantidad FROM producto WHERE id_producto = %s", (id_prod,))
            producto_data = cursor.fetchone()
            if producto_data is None:
                messagebox.showerror("Error", "El ID de Producto no existe.")
                return

            current_stock = producto_data[1]

            if tipo == "Salida" and cantidad > current_stock:
                messagebox.showerror("Error", "Cantidad de salida excede el stock actual.")
                return

            # Registrar el movimiento
            cursor.execute("INSERT INTO movimiento (tipo, cantidad, fecha, id_producto, id_usuario) VALUES (%s, %s, %s, %s, %s)",
                           (tipo, cantidad, datetime.now().date(), id_prod, id_usuario))

            # Actualizar el stock del producto
            signo = 1 if tipo == "Entrada" else -1
            cursor.execute("UPDATE producto SET cantidad = cantidad + %s WHERE id_producto = %s", (signo * cantidad, id_prod))

            db.commit()
            messagebox.showinfo("Éxito", "Movimiento registrado y stock actualizado.")
            win.destroy()

        except ValueError:
            messagebox.showerror("Error de Entrada", "Cantidad o ID de Producto deben ser números válidos.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al guardar el movimiento: {err}")
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()

    ttk.Button(win, text="Guardar Movimiento", command=guardar).pack(pady=10)
    win.mainloop()