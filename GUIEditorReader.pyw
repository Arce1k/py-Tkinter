import tkinter as tk
import json
import webbrowser

# Leer parámetros desde el archivo JSON con codificación UTF-8
with open('Parameters/buttons.json', 'r', encoding='utf-8') as file:
    params = json.load(file)

# Extraer parámetros de la ventana
window_params = params.get('window', {})
window_title = window_params.get('window_title', 'Ventana')
window_width = window_params.get('window_width', 300)
window_height = window_params.get('window_height', 300)
window_x = window_params.get('window_x', 100)
window_y = window_params.get('window_y', 100)

# Crear la ventana principal
root = tk.Tk()
root.title(window_title)
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Crear un diccionario para almacenar los enlaces de los botones
button_links = {}


# Función para manejar el clic en los botones y abrir el hipervínculo
def open_link(event):
    widget = event.widget
    link = button_links.get(widget)
    if link:
        webbrowser.open(link)


# Extraer y crear los botones
buttons_params = params.get('buttons', [])
for button in buttons_params:
    if button.get('type') == 'Button':
        text = button.get('text', 'Botón')
        x = button.get('x', 0)
        y = button.get('y', 0)
        link = button.get('link', None)
        color = button.get('color', 'SystemButtonFace')  # Usa un color predeterminado si no se especifica

        btn = tk.Button(root, text=text, bg=color)  # Establece el color de fondo del botón
        btn.place(x=x, y=y)

        if link:
            button_links[btn] = link  # Almacena el enlace en el diccionario
            btn.bind("<Button-1>", open_link)  # Asocia el clic izquierdo del ratón a la apertura del enlace

# Ejecutar el bucle principal de la aplicación
root.mainloop()
