"""Mi Cotizador: convierte pesos a dólares y guarda un historial."""
import sys
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk


def carpeta_base() -> Path:
    """Carpeta del .exe (si está empaquetado) o del script."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


HISTORIAL = carpeta_base() / "historial.txt"


def parsear_numero(texto: str) -> float:
    """Acepta '1.500,50', '1500,50' o '1500.50'."""
    t = texto.strip().replace(" ", "").replace("$", "")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    return float(t)


def convertir(pesos: float, cotizacion: float) -> float:
    if cotizacion <= 0:
        raise ValueError("La cotización debe ser mayor a cero.")
    return pesos / cotizacion


def guardar_historial(pesos: float, cotizacion: float, dolares: float) -> None:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = (f"{fecha} | ARS {pesos:,.2f} | Cotización {cotizacion:,.2f} "
             f"| USD {dolares:,.2f}\n")
    with open(HISTORIAL, "a", encoding="utf-8") as f:
        f.write(linea)


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Mi Cotizador")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=20)
        frame.grid()

        ttk.Label(frame, text="Monto en pesos (ARS):").grid(row=0, column=0, sticky="w")
        self.monto = ttk.Entry(frame, width=22)
        self.monto.grid(row=0, column=1, pady=4, padx=(10, 0))

        ttk.Label(frame, text="Cotización del dólar:").grid(row=1, column=0, sticky="w")
        self.cotiz = ttk.Entry(frame, width=22)
        self.cotiz.grid(row=1, column=1, pady=4, padx=(10, 0))

        ttk.Button(frame, text="Convertir", command=self.on_convertir).grid(
            row=2, column=0, columnspan=2, pady=12)

        self.resultado = ttk.Label(frame, text="Resultado: —", font=("Segoe UI", 12, "bold"))
        self.resultado.grid(row=3, column=0, columnspan=2)

        self.monto.focus()
        self.bind("<Return>", lambda e: self.on_convertir())

    def on_convertir(self) -> None:
        try:
            pesos = parsear_numero(self.monto.get())
            cotizacion = parsear_numero(self.cotiz.get())
            dolares = convertir(pesos, cotizacion)
        except ValueError as e:
            msg = str(e) if "cotización" in str(e) else "Ingresá números válidos en ambos campos."
            messagebox.showerror("Dato inválido", msg)
            return
        self.resultado.config(text=f"Resultado: USD {dolares:,.2f}")
        try:
            guardar_historial(pesos, cotizacion, dolares)
        except OSError as e:
            messagebox.showwarning("Historial", f"No se pudo guardar el historial:\n{e}")


if __name__ == "__main__":
    App().mainloop()
