# WindowEditLib/draggable_widget.py
import tkinter as tk

class DraggableWidget:
    def __init__(self, widget):
        self.widget = widget
        self.widget.bind("<Button-1>", self.on_start)  # Usar el botón izquierdo
        self.widget.bind("<B1-Motion>", self.on_drag)  # Usar el botón izquierdo
        self.start_x = 0
        self.start_y = 0

    def on_start(self, event):
        # Guardar las coordenadas iniciales del ratón
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        # Calcular la nueva posición y mover el widget
        x = self.widget.winfo_x() + event.x - self.start_x
        y = self.widget.winfo_y() + event.y - self.start_y
        self.widget.place(x=x, y=y)
