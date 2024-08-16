#WindowEditLib/hyperlink_manager.py

import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import webbrowser

def show_popup_menu(window, add_link_callback):
    """ Muestra un menú contextual en la ventana. """
    def on_popup_menu(event):
        popup_menu = tk.Menu(window, tearoff=0)
        popup_menu.add_command(label="Agregar Hipervínculo", command=add_link_callback)
        popup_menu.post(event.x_root, event.y_root)

    window.bind("<Button-3>", on_popup_menu)

def add_link_to_button(widgets, new_window):
    """ Permite agregar un hipervínculo a un botón en la ventana adicional. """
    if new_window is None:
        messagebox.showwarning("Advertencia", "No hay una ventana adicional abierta.")
        return

    widget_name = simpledialog.askstring("Seleccionar Botón", "Introduce el nombre del botón para agregar un hipervínculo:")
    link = simpledialog.askstring("Agregar Hipervínculo", "Introduce el hipervínculo:")
    if widget_name and link:
        for widget_info in widgets:
            widget = widget_info['widget']
            if widget.cget("text") == widget_name and widget_info['window'] == new_window:
                widget_info['link'] = link  # Almacenar el hipervínculo
                messagebox.showinfo("Info", f"Hipervínculo '{link}' agregado al botón '{widget_name}'.")
                return
        messagebox.showerror("Error", "Botón no encontrado.")

def open_link(event):
    """ Abre el hipervínculo asociado al botón cuando se hace clic en él. """
    widget = event.widget
    link = widget.link if hasattr(widget, 'link') else None
    if link:
        webbrowser.open(link)