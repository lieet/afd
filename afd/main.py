from AFD import *
from graphviz import Digraph
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image

#Ler o arquivo texto
with open("arquivo.txt", "r") as arq:
    lista = []

    for line in arq:
        lista.append(line.split())

afd = AFD(lista[0], lista[1][0], lista[2]) #cria o AFD

for i in lista[4]:
    afd.addEF(i)

for i in range(0, len(lista[3]), 3):
    afd.addTransicao(lista[3][i], lista[3][i+1], lista[3][i+2])

class Page0(GridLayout):
    def __init__(self, **kwargs):
        super(Page0, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Digite a sequencia para teste: "))
        self.entry = TextInput(multiline=False)
        self.entry.bind(on_text_validate=self.testar)
        self.add_widget(self.entry)
        self.b1 = Button(text="Testar")
        self.b1.bind(on_press=self.testar)
        self.add_widget(self.b1)
        self.b2 = Button(text="Gerar imagem")
        self.b2.bind(on_press=self.imagem)
        self.add_widget(self.b2)

    def testar(self, event):
        resultado = afd.teste(self.entry.text)
        if resultado == "":
            popup = Popup(title = "Resultado", content = Label(text="Erro."), size = (300,100), size_hint=(None, None), auto_dismiss=True)
            popup.open()
        else:
            if afd.efinal(resultado):
                popup = Popup(title = "Resultado", content = Label(text="Transicoes acabaram no estado final: " + resultado + "."), size = (300,100), size_hint=(None, None), auto_dismiss=True)
                popup.open()
            else:
                popup = Popup(title = "Resultado", content = Label(text="Transicoes acabaram em: " + resultado + ".\nEsta sequencia nao faz parte do automato definido."), size = (360,100), size_hint=(None, None), auto_dismiss=True)
                popup.open()
        self.entry.text = ""

    def imagem(self, event):
        f = Digraph("AFD", filename="afd.gv")
        f.format = "png"

        for i in afd.estadosFinais: #A partir dos estados finais do afd cria os circulos duplos
            f.node(i, shape='doublecircle')

        f.node(afd.estadoInicial, color='blue') #Colora o estado inicial de azul

        dic = afd.transicoes

        for p, q in dic:
            f.edge(p, dic[(p, q)], label=q) #Cria uma ligacao de p ate dic[(p, q)]. Ex: f.edge("q0", "q2", label="1")

        f.render("afd") #Cria o afd.png na mesma pasta deste arquivo

        popup = Popup(title = "Imagem", content = Image(source="afd.png")) #Cria o popup
        popup.open()

class App(App):
    def build(self):
        self.title = "AFD"
        return Page0()

if __name__ == "__main__":
    App().run()
