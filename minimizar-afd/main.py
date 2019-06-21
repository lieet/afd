from AFD import *
from graphviz import Digraph
import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.config import Config

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '665')

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Ler arquivo", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            lista = []

            for line in stream:
                lista.append(line.split())

        try:
            del self._afd
        except AttributeError:
            pass

        self._afd = AFD(lista[0], lista[1][0], lista[2]) #cria o AFD

        for i in lista[4]:
            self._afd.addEF(i)

        for i in range(0, len(lista[3]), 3):
            self._afd.addTransicao(lista[3][i], lista[3][i+1], lista[3][i+2])

        self.dismiss_popup()

    def imagemOriginal(self):
        f = Digraph("AFD", filename="afd-original.gv")
        f.format = "png"

        for i in self._afd.estadosFinais: #A partir dos estados finais do afd cria os circulos duplos
            f.node(i, shape='doublecircle')

        f.node(self._afd.estadoInicial, color='blue') #Colora o estado inicial de azul

        dic = self._afd.transicoes

        for p, q in dic:
            f.edge(p, dic[(p, q)], label=q) #Cria uma ligacao de p ate dic[(p, q)]. Ex: f.edge("q0", "q2", label="1")

        f.render("afd-original") #Cria o afd-original.png na mesma pasta deste arquivo

        content = Image(source="afd-original.png")
        content.reload()
        popup = Popup(title="AFD Original", content=content) #Cria o popup
        popup.open()

    def imagemMinimizada(self):
        lista = self._afd.minimizar()
        f = Digraph("AFD", filename="afd-minimizado.gv")
        f.format = "png"

        for i in self._afd.getEFMin(lista): #A partir dos estados finais do afd cria os circulos duplos
            f.node(i, shape='doublecircle')

        f.node(self._afd.getEIMin(lista), color='blue') #Colora o estado inicial de azul

        dic = self._afd.getTransicoesMin(lista)

        for p, q in dic:
            f.edge(p, dic[(p, q)], label=q) #Cria uma ligacao de p ate dic[(p, q)]. Ex: f.edge("q0", "q2", label="1")

        f.render("afd-minimizado") #Cria o afd-minimizado.png na mesma pasta deste arquivo

        content = Image(source="afd-minimizado.png")
        content.reload()
        popup = Popup(title="AFD Minimizado", content=content) #Cria o popup
        popup.open()


class Editor(App):
    title = "Minimizacao de AFD"

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Editor().run()
