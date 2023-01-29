from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def func(self):
        pass


class TRKApp(App):
    def build(self):
        return MyRoot()


TRKApp().run()
