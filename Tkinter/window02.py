import tkinter as tk

def calcular_imc():
    altura = float(entry_altura.get())
    peso = float(entry_peso.get())
    imc = peso / (altura * altura)
    label_resultado.config(text=f"Seu IMC é: {imc:.2f}")
    entry_altura.delete(0, tk.END)
    entry_peso.delete(0, tk.END)

window = tk.Tk()
window.title("Calculador de IMC")
window.geometry("300x200")

#.pack(pady=5) O método .pack() (assim como .grid() e .place()) arruma o widget na janela, mas ele retorna None (nada). 

label_altura = tk.Label(window, text="Altura")#.pack(pady=5)
label_altura.pack(pady=5)

entry_altura = tk.Entry(window)#.pack(pady=5)
entry_altura.pack(pady=5)

label_peso = tk.Label(window, text="Peso")#.pack(pady=5)
label_peso.pack(pady=5)

entry_peso = tk.Entry(window)#.pack(pady=5)
entry_peso.pack(pady=5)

botao_resultado = tk.Button(window, text="Resultado", command=calcular_imc)#.pack(pady=5)
botao_resultado.pack(pady=5)

label_resultado = tk.Label(window, text="")#.pack(pady=5)
label_resultado.pack(pady=5)

window.mainloop()