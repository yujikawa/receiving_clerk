from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from send_slack import run

# Window size
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '300')

Builder.load_file('template/layout.kv')
# layout
class MyLayout(GridLayout):

    def callback(self):
        print('push button')
        run()

class MyApp(App):
    def build(self):
        self.title = 'receiving clerk'
        self.icon = 'template/yobirin.jpg'

        return MyLayout()

MyApp().run()