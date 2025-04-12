import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

lembretes = []

def lembrete(medicacao):
    
    aviso = tk.Tk()
    aviso.title("Hora do Remédio!")
    aviso.geometry("300x150")
    aviso.resizable(False, False)

    aviso.update_idletasks()
    largura = aviso.winfo_width()
    altura = aviso.winfo_height()
    x = (aviso.winfo_screenwidth() // 2) - (largura // 2)
    y = (aviso.winfo_screenheight() // 2) - (altura // 2)
    aviso.geometry(f"{largura}x{altura}+{x}+{y}")

    msg = tk.Label(aviso, text=f"É hora de tomar:\n{medicacao}", font=("Helvetica", 14), pady=20)
    msg.pack()

    btn_ok = tk.Button(aviso, text="OK", command=aviso.destroy)
    btn_ok.pack(pady=10)

    aviso.attributes("-topmost", True)
    aviso.mainloop()

def agendar_lembrete():

    try:
        hora = int(entrada_hora.get())
        minuto = int(entrada_minuto.get())
        medicacao = entrada_medicacao.get()

        if not medicacao:
            messagebox.showerror("Erro", "Por favor, insira o nome da medicação.")
            return

        agora = datetime.now()
        horario_lembrete = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)

        if horario_lembrete < agora:
            horario_lembrete += timedelta(days=1)

        tempo_segundos = int((horario_lembrete - agora).total_seconds())
        root.after(tempo_segundos * 1000, lembrete, medicacao)

# Guardar lembrete na lista:

        lembretes.append((f"{hora:02d}:{minuto:02d}", medicacao))
        atualizar_lista_lembretes()

        entrada_hora.delete(0, tk.END)
        entrada_minuto.delete(0, tk.END)
        entrada_medicacao.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um horário válido.")

def atualizar_lista_lembretes():
    for widget in lista_frame.winfo_children():
        widget.destroy()

    for i, (horario, medicamento) in enumerate(lembretes):
        frame = tk.Frame(lista_frame)
        frame.pack(fill="x", pady=2)

# Exibe o lembrete e o botão de exclusão:

        lembrete_label = tk.Label(frame, text=f"{horario} - {medicamento}", width=40, anchor="w")
        lembrete_label.pack(side="left", padx=10)

        botao_excluir = tk.Button(frame, text="Excluir", command=lambda idx=i: excluir_lembrete(idx))
        botao_excluir.pack(side="right", padx=10)

def excluir_lembrete(index):

    del lembretes[index]
    atualizar_lista_lembretes()

# Interface:

root = tk.Tk()
root.title("LEMBRETE DE MEDICAÇÃO")

tk.Label(root, text="Hora:").grid(row=0, column=0)
entrada_hora = tk.Entry(root, width=5)
entrada_hora.grid(row=0, column=1)

tk.Label(root, text="Minuto:").grid(row=1, column=0)
entrada_minuto = tk.Entry(root, width=5)
entrada_minuto.grid(row=1, column=1)

tk.Label(root, text="Medicação:").grid(row=2, column=0)
entrada_medicacao = tk.Entry(root)
entrada_medicacao.grid(row=2, column=1)

botao_agendar = tk.Button(root, text="Agendar lembrete", command=agendar_lembrete)
botao_agendar.grid(row=3, column=0, columnspan=2, pady=5)

tk.Label(root, text="Lembretes agendados:").grid(row=4, column=0, columnspan=2)
lista_frame = tk.Frame(root)
lista_frame.grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()