from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from BluetoothTest import get_speed, connect_bt

from threading import Thread, Event

class MenuScreen(FloatLayout):
    thread = None
    bt = None
    event = Event()
    connected = False
    Window.size = (562, 1000)
    Window.clearcolor = (77/255, 77/255, 77/255, 1.0)
    window_size = Window.size
    def connect(self):
        if self.connected:
            self.bt.close()
            self.event.set()
            self.thread.join()
            self.speed_label.font_size = 48
            self.speed_label.text = str("Connect BT")
            self.bt = None
            self.thread = None
            self.connected = False
        else:
            if self.bt is None:
                self.bt = connect_bt("COM4")
                self.speed_label.font_size = 100
                self.speed_label.text = str("-")
            if self.thread is None:
                self.thread = Thread(target=self.get_speed)
                self.thread.start()
            self.connected = True

    def get_speed(self):
        while True:
            speed = get_speed(self.bt)
            if speed is not None:
                self.speed_label.text = str(speed)
            if self.event.is_set():
                break


class TRKApp(App):
    def build(self):
        return MenuScreen()

    def get_speed(self, instance):
        self.speed_label.text = str(get_speed(self.bt))


if __name__ == "__main__":
    TRKApp().run()