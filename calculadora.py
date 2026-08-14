import tkinter as tk
import ctypes

"""
===================
Funções do Programa
===================
"""
#Função de Entrada
def clicar(valor):
    entrada.insert(tk.END, valor)

#Função de calculo
def calcular(event=None):
    try:
        expressao = entrada.get()
        expressao = expressao.replace("÷", "/")
        expressao = expressao.replace("x", "*")
        resultado = eval(expressao)
        entrada.delete(0, tk.END)
        entrada.insert(tk.END, str(resultado))
    except:
        entrada.delete(0, tk.END)
        entrada.insert(tk.END, "*ERRO* ")

#Função de Limpeza
def limpar(event=None):
    entrada.delete(0, tk.END)

def keypress(event):
    tecla = event.char

    if tecla in "0123456789+-x().":
        clicar(tecla)
        pressionar_visual(tecla)

"""
==================
Janela do Programa
==================
"""
janela = tk.Tk()
janela.title("")
janela.geometry("300x400")
janela.resizable(False,False)

#Só pra tirar a cor da janela
janela.update()

hwnd = ctypes.windll.user32.GetParent(janela.winfo_id())

DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36

cor_barra = 0x00222222

ctypes.windll.dwmapi.DwmSetWindowAttribute(
    hwnd,
    DWMWA_CAPTION_COLOR,
    ctypes.byref(ctypes.c_int(cor_barra)),
    ctypes.sizeof(ctypes.c_int)
)

# Texto da barra em branco
cor_texto = 0x00FFFFFF

ctypes.windll.dwmapi.DwmSetWindowAttribute(
    hwnd,
    DWMWA_TEXT_COLOR,
    ctypes.byref(ctypes.c_int(cor_texto)),
    ctypes.sizeof(ctypes.c_int)
)

janela.configure(bg="#222222")

#display
janela.configure(bg="#222222")

entrada = tk.Entry(
    janela, 
    font=("Arial", 20),
    bd=10,
    relief=tk.RIDGE,
    justify="right",
    bg="#222222",
    fg="#10E1CC",
    insertbackground="#10E1CC"
)
entrada.pack(fill="both", ipadx=8, ipady=15)

#Criar Botões
frame_botões = tk.Frame(janela, bg="#222222")
frame_botões.pack(expand=True, fill="both")

#Mapeamento
botoes = [
    ('7', '8', '9', '÷'),
    ('4', '5', '6', 'x'),
    ('1', '2', '3', '-'),
    ('0', 'C', '=', '+')
]


botoes_tk = {}
for linha in botoes:
    linha_frame = tk.Frame(frame_botões, bg="#222222")
    linha_frame.pack(expand=True, fill="both")

    for texto in linha:
        if texto == '=':
            botao = tk.Button(linha_frame, text=texto, font=("Arial", 18), command=calcular,
                bg="#333333", fg="#10E1CC", activebackground="#444444", activeforeground="#10E1CC", relief=tk.FLAT
            )
        elif texto == 'C':
            botao = tk.Button(linha_frame, text=texto, font=("Arial", 18), command=limpar,
                bg="#333333", fg="#FF6B6B", activebackground="#444444", activeforeground="#FF6B6B", relief=tk.FLAT
            )
        else:
            botao = tk.Button(linha_frame, text=texto, font=("Arial", 18), command=lambda val=texto: clicar(val),
                bg="#333333", fg="#FFFFFF", activebackground="#444444", activeforeground="#FFFFFF", relief=tk.FLAT
            )

        botoes_tk[texto] = botao
        botao.pack(side="left", expand=True, fill="both")

def pressionar_visual(tecla):
    if tecla in botoes_tk:
        botao = botoes_tk[tecla]

        bg_original = botao.cget("bg")
        fg_original = botao.cget("fg")

        botao.config(
            bg="#222222",
            fg="#10E1CC"
        )

        janela.after(
            100,
            lambda: botao.config(
                bg=bg_original,
                fg=fg_original
            )
        )

"""
=========================
Associação com o Teclado
=========================
"""

janela.bind("<Key>", keypress)

janela.bind("<Return>", lambda event:(pressionar_visual("="), calcular()))
janela.bind("<KP_Enter>", calcular)

janela.bind("<BackSpace>", lambda event: entrada.delete(len(entrada.get())-1, tk.END))
janela.bind("<Escape>", lambda event:(pressionar_visual("C"), limpar()))

janela.mainloop()