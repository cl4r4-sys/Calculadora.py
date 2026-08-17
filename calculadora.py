import tkinter as tk
import ctypes
import re
import math

"""
===================
Funções do Programa
===================
"""

#Efeito visual quando uma tecla é pressionada
def pressionar_visual(tecla):
    if tecla in botoes_tk:
        botao = botoes_tk[tecla]
        bg_original = botao.cget("bg")
        fg_original = botao.cget("fg")
        botao.config(bg="#222222", fg="#A5E7E0")
        janela.after(100, lambda: botao.config(bg=bg_original, fg=fg_original))

#Função de Entrada
def clicar(valor):
    entrada.insert(tk.END, valor)

#Função para calcular porcetagem
def calcular_porcetagem(expressao):
    padrao = r'(\d+(?:\.\d+)?)\s*([+-])\s*(\d+(?:\.\d+)?)%'

    def substituir_soma_subtracao(match):
        valor1 = match.group(1)
        operador = match.group(2)
        valor2 = match.group(3)
        return f'({valor1}{operador}({valor1}*{valor2}/100))'

    while re.search(padrao, expressao):
        expressao = re.sub(padrao, substituir_soma_subtracao, expressao, count=1)

    expressao = re.sub(r'(\d+(?:\.\d+)?)%(?=\d+(?:\.\d+)?)', r'(\1/100)*', expressao)
    expressao = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expressao)

    return expressao

#Função de calculo
def calcular(event=None):
    try:
        expressao = entrada.get()

        #Troca símbolos da calculadora por operadores do python
        expressao = expressao.replace("÷", "/")
        expressao = expressao.replace("x", "*")
        expressao = expressao.replace("Rad", "math.radians")
        expressao = expressao.replace("√", "math.sqrt")
        expressao = expressao.replace("log", "math.log10")
        expressao = expressao.replace("ln", "math.log")
        expressao = expressao.replace("sin", "math.sin")
        expressao = expressao.replace("cos", "math.cos")
        expressao = expressao.replace("tan", "math.tan")

        #Converte as porcentegens
        expressao = calcular_porcetagem(expressao)

        resultado = eval(expressao, {"__builtins__": None}, {"math": math})

        entrada.delete(0, tk.END)
        entrada.insert(tk.END, str(resultado))

    except Exception:
        entrada.delete(0, tk.END)
        entrada.insert(tk.END, "*ERRO* ")

#Função de Limpeza
def limpar(event=None):
    entrada.delete(0, tk.END)

#Abre e fecha parenteses
def parenteses():
    expressao = entrada.get()
    abertos = expressao.count("(")
    fechados = expressao.count(")")

    if abertos > fechados:
        clicar(")")
    else:
        clicar("(")

#Função para teclado
def keypress(event):
    tecla = event.char

    if tecla in "0123456789%+-x().":
        clicar(tecla)
        pressionar_visual(tecla)
    elif tecla.lower() == "c":
        limpar()
        pressionar_visual("C")

"""
==================
Janela do Programa
==================
"""
janela = tk.Tk()
janela.title("")
janela.geometry("300x450")
janela.resizable(False,False)

#Só pra tirar a cor da janela
janela.update()
try:
    hwnd = ctypes.windll.user32.GetParent(janela.winfo_id())
    DWMWA_CAPTION_COLOR = 35
    DWMWA_TEXT_COLOR = 36
    cor_barra = 0x00222222
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(cor_barra)), ctypes.sizeof(ctypes.c_int))
    cor_texto = 0x00FFFFFF
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_TEXT_COLOR, ctypes.byref(ctypes.c_int(cor_texto)), ctypes.sizeof(ctypes.c_int))
except Exception:
    pass

#display
janela.configure(bg="#222222")

entrada = tk.Entry(janela, font=("Arial", 20), bd=10, relief=tk.RIDGE, justify="right", bg="#222222", fg="#A5E7E0", insertbackground="#A5E7E0")
entrada.pack(fill="both", padx=15, ipadx=8, ipady=20)

modo_cientifico = False

#Criar Botões
frame_botões = tk.Frame(janela, bg="#222222")
frame_botões.pack(expand=True, fill="both")

#Mapeamento
botoes_tk = {}

def alternar_botoes():
    global modo_cientifico
    modo_cientifico = not modo_cientifico
    criar_botoes()

def criar_botoes():
    global botoes_tk
    for widget in frame_botões.winfo_children():
        widget.destroy()
    
    botoes_tk = {}

    layout_padrao = [
            ('C', '()', '%', '÷'),
            ('7', '8', '9', 'x'),
            ('4', '5', '6', '-'),
            ('1', '2', '3', '+'),
            ('+opt', '0', '.', '=')
        ]

    layout_cientifico = [
            ('-opt', 'Rad', '√'),
            ('sin', 'cos', 'tan'),
            ('ln', 'log', '1/X'),
            ('e^x', 'x²', 'x^y'),
            ('|x|', 'π', 'e')
        ]

    botoes_ativos = layout_cientifico if modo_cientifico else layout_padrao

    for linha in botoes_ativos:
        linha_frame = tk.Frame(frame_botões, bg="#222222")
        linha_frame.pack(expand=True, fill="both", padx=10, pady=5)

        for texto in linha:
            cor_bg = "#333333"
            cor_fg = "#FFFFFF"

            if texto == '=':
                cmd = calcular
                cor_fg = "#A5E7E0"
            elif texto == 'C':
                cmd = limpar
                cor_fg = "#FF6B6B"
            elif texto == '()':
                cmd = parenteses
            elif texto in ('+opt', '-opt'):
                cmd = alternar_botoes
                cor_bg = "#444444"
                cor_fg = "#A5E7E0"
            elif texto == '1/X':
                cmd = lambda: clicar("1/")
            elif texto in ('√', 'log', 'ln', 'sin', 'cos', 'tan', 'Rad'):
                cmd = lambda val=texto: clicar(f"{val}(")
            else:
                cmd = lambda val=texto: clicar(val)

            botao = tk.Button(linha_frame, text=texto, font=("Arial", 18 if len(texto)<=2 else 12, "bold"), command=cmd,
                bg=cor_bg, fg=cor_fg, relief=tk.FLAT, borderwidth=0, cursor="hand2", highlightthickness=0
            )

            botao.bind("<Enter>", lambda e, b=botao: b.config(bg="#444444"))
            botao.bind("<Leave>", lambda e, b=botao, original_bg=cor_bg: b.config(bg=original_bg))

            botoes_tk[texto] = botao
            botao.pack(side="left", expand=True, fill="both", padx=5, pady=2)

criar_botoes()

"""
=========================
Associação com o Teclado
=========================
"""

janela.bind("<Key>", keypress)
janela.bind("<Return>", lambda event:(pressionar_visual("="), calcular()))
janela.bind("<KP_Enter>", calcular)
janela.bind("<BackSpace>", lambda event: entrada.delete(len(entrada.get())-1, tk.END))
janela.bind("<c>", lambda event: (pressionar_visual("C"), limpar()))
janela.bind("<C>", lambda event: (pressionar_visual("C"), limpar()))
janela.bind("<Escape>", lambda event:(pressionar_visual("C"), limpar()))
janela.bind("<Up>", lambda event: (alternar_botoes() if not modo_cientifico else None))
janela.bind("<Down>", lambda event: (alternar_botoes() if modo_cientifico else None))
janela.bind("<Left>", lambda event: (alternar_botoes() if modo_cientifico else None))
janela.bind("<Right>", lambda event: (alternar_botoes() if not modo_cientifico else None))
janela.bind("<less>", lambda event: (alternar_botoes() if not modo_cientifico else None)) 
janela.bind("<greater>", lambda event: (alternar_botoes() if modo_cientifico else None))

#Iniciar programa
janela.mainloop()