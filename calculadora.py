import tkinter as tk

"""
===================
Funções do Programa
===================
"""
#Função de Entrada
def clicar(valor):
    entrada.insert(tk.END, valor)

#Função de calculo
def calcular():
    try:
        resultado = eval(entrada.get())
        entrada.delete(0, tk.END)
        entrada.insert(tk.END, str(resultado))
    except:
        entrada.delete(0, tk.END)
        entrada.insert(tk.END, "ERRO")

#Função de Limpeza
def limpar():
    entrada.delete(0, tk.END)

"""
==================
Janela do Programa
==================
"""
janela = tk.Tk()
janela.title("Projeto Cálculadora")
janela.geometry("300x400")
janela.resizable(False,False)

#display

entrada = tk.Entry(
    janela, 
    font=("Arial", 20),
    bd=10,
    relief=tk.RIDGE,
    justify="right"
)
entrada.pack(fill="both", ipadx=8, ipady=15)

#Criar Botões
frame_botões = tk.Frame(janela)
frame_botões.pack(expand=True, fill="both")

#Mapeamento
botoes = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', 'C', '=', '+')
]

for linha in botoes:
    linha_frame = tk.Frame(frame_botões)
    linha_frame.pack(expand=True, fill="both")
    for texto in linha:
        if texto == '=':
            botao = tk.Button(linha_frame, text=texto, font=("Arial", 18), command=calcular)
        elif texto == 'C':
            botao = tk.Button(linha_frame, text=texto, font=("Arial", 18), command=limpar)
        else:
            botao = tk.Button(linha_frame, text=texto, font=("Arial", 18), command=lambda val=texto: clicar(val))

            botao.pack(side="left", expand=True, fill="both")

janela.mainloop()