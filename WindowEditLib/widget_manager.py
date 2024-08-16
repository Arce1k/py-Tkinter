import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import json
import os
from .draggable_widget import DraggableWidget
from .hyperlink_manager import open_link

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Botones + Window")
        self.root.geometry("240x600")

        # Inicialización de atributos
        self.widgets = []
        self.button_count = 1
        self.new_window = None
        self.next_x = 10
        self.next_y = 50

        # Crear y colocar botones en la ventana principal
        self.create_main_buttons()

    def create_main_buttons(self):
        self.add_button = tk.Button(self.root, text="Añadir Botón", command=self.add_widget)
        self.add_button.pack(pady=10)

        self.save_positions_button = tk.Button(self.root, text="Guardar Posiciones", command=self.save_positions)
        self.save_positions_button.pack(pady=10)

        self.edit_button = tk.Button(self.root, text="Editar Nombre de Botón", command=self.edit_widget_name)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Eliminar Botón", command=self.delete_widget)
        self.delete_button.pack(pady=10)

        self.change_color_button = tk.Button(self.root, text="Cambiar Color de Botón", command=self.change_button_color)
        self.change_color_button.pack(pady=10)

        self.add_link_button = tk.Button(self.root, text="Añadir Hipervínculo", command=self.add_link_to_widget)
        self.add_link_button.pack(pady=10)

        self.open_new_window_button = tk.Button(self.root, text="Abrir Nueva Ventana", command=self.open_new_window)
        self.open_new_window_button.pack(pady=10)

    def add_widget(self):
        if self.new_window is None:
            messagebox.showwarning("Advertencia", "No hay una ventana adicional abierta.")
            return

        button_name = f"Botón {self.button_count}"
        button = tk.Button(self.new_window, text=button_name)
        button.place(x=self.next_x, y=self.next_y)
        button.link = None
        button.color = None  # Inicializar el color del botón
        self.widgets.append({'widget': button, 'window': self.new_window, 'link': None, 'color': None})
        DraggableWidget(button)

        # Eliminar la vinculación del menú contextual
        # button.bind("<Button-3>", self.show_button_popup_menu)

        self.button_count += 1
        self.next_x += 100
        if self.next_x > self.new_window.winfo_width() - 100:
            self.next_x = 10
            self.next_y += 50

    def save_positions(self):
        if not self.widgets and self.new_window is None:
            messagebox.showinfo("Info", "No hay datos para guardar.")
            return

        window_info = {}
        if self.new_window is not None:
            window_info = {
                "window": {
                    "window_title": self.new_window.title(),
                    "window_width": self.new_window.winfo_width(),
                    "window_height": self.new_window.winfo_height(),
                    "window_x": self.new_window.winfo_x(),
                    "window_y": self.new_window.winfo_y()
                }
            }

        buttons_info = []
        for widget_info in self.widgets:
            widget = widget_info['widget']
            button_data = {
                "type": widget.winfo_class(),
                "text": widget.cget("text"),
                "x": widget.winfo_x(),
                "y": widget.winfo_y(),
                "link": widget_info['link'],
                "color": widget_info['color']  # Añadir el color
            }
            buttons_info.append(button_data)

        final_data = window_info
        if window_info:
            final_data["buttons"] = buttons_info

        directory = "Parameters"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, "buttons.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(final_data, file, indent=4, ensure_ascii=False)

        messagebox.showinfo("Posiciones", f"Datos guardados en {file_path}.")

    def edit_widget_name(self):
        widget_text = simpledialog.askstring("Editar Nombre", "Introduce el nuevo nombre del botón:")
        if widget_text:
            if self.widgets:
                selected_button = simpledialog.askstring("Seleccionar Botón", "Introduce el número del botón a editar (1, 2, 3, ...):")
                try:
                    index = int(selected_button) - 1
                    if 0 <= index < len(self.widgets):
                        self.widgets[index]['widget'].config(text=widget_text)
                    else:
                        messagebox.showerror("Error", "Número de botón no válido.")
                except ValueError:
                    messagebox.showerror("Error", "Entrada no válida.")
            else:
                messagebox.showinfo("Info", "No hay botones para editar.")

    def delete_widget(self):
        if self.new_window is None:
            messagebox.showwarning("Advertencia", "No hay una ventana adicional abierta.")
            return

        widget_name = simpledialog.askstring("Eliminar Botón", "Introduce el nombre exacto del botón a eliminar:")
        if widget_name:
            for widget_info in self.widgets:
                widget = widget_info['widget']
                if widget.cget("text") == widget_name and widget_info['window'] == self.new_window:
                    widget.destroy()
                    self.widgets.remove(widget_info)
                    messagebox.showinfo("Info", f"Botón '{widget_name}' eliminado.")
                    return
            messagebox.showerror("Error", "Botón no encontrado.")

    def change_button_color(self):
        """ Permite cambiar el color de un botón existente. """
        color = simpledialog.askstring("Cambiar Color", "Introduce el color para el botón (por ejemplo, 'red', 'blue'):")
        if color:
            widget_name = simpledialog.askstring("Seleccionar Botón", "Introduce el nombre del botón a cambiar de color:")
            if widget_name:
                for widget_info in self.widgets:
                    widget = widget_info['widget']
                    if widget.cget("text") == widget_name and widget_info['window'] == self.new_window:
                        widget.config(bg=color)  # Cambiar el color del botón
                        widget_info['color'] = color  # Guardar el color
                        messagebox.showinfo("Info", f"Color '{color}' cambiado para el botón '{widget_name}'.")
                        return
                messagebox.showerror("Error", "Botón no encontrado.")

    def add_link_to_widget(self):
        """ Permite añadir un hipervínculo a un botón existente. """
        widget_name = simpledialog.askstring("Seleccionar Botón", "Introduce el nombre del botón al que añadir hipervínculo:")
        if widget_name:
            link = simpledialog.askstring("Añadir Hipervínculo", "Introduce la URL del hipervínculo:")
            if link:
                for widget_info in self.widgets:
                    widget = widget_info['widget']
                    if widget.cget("text") == widget_name and widget_info['window'] == self.new_window:
                        widget_info['link'] = link
                        widget.config(command=lambda url=link: open_link(url))  # Configura el comando del botón
                        messagebox.showinfo("Info", f"Hipervínculo '{link}' añadido al botón '{widget_name}'.")
                        return
                messagebox.showerror("Error", "Botón no encontrado.")

    def open_new_window(self):
        if self.new_window is not None:
            messagebox.showwarning("Advertencia", "Ya hay una ventana adicional abierta.")
            return

        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Nueva Ventana")
        self.new_window.geometry("300x300")
        self.new_window.resizable(True, True)
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_new_window_close)

        for widget_info in self.widgets:
            if widget_info['window'] == self.new_window:
                widget = widget_info['widget']
                if widget_info['link']:
                    widget.config(command=lambda url=widget_info['link']: open_link(url))
                # Eliminar la vinculación de clic izquierdo
                # widget.bind("<Button-1>", open_link)

    def on_new_window_close(self):
        self.new_window.destroy()
        self.new_window = None
