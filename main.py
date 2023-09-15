import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color, Line
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)  # White background color

class PaintWindow(Widget):
    def on_touch_down(self, touch):
        # Randomize colors for drawing
        colorR = random.random()
        colorG = random.random()
        colorB = random.random()

        with self.canvas:
            Color(rgb=(colorR, colorG, colorB))
            # Draw a circle for the paintbrush
            d = 5
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=2)

    def on_touch_move(self, touch):
        # Continue drawing when moving
        touch.ud['line'].points += [touch.x, touch.y]

class PaintApp(App):
    def build(self):
        self.painter = PaintWindow()
        self.root = self.create_ui()
        return self.root

    def create_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        clear_button = Button(text='Clear', size_hint=(None, 1))
        clear_button.bind(on_release=self.clear_canvas)
        save_button = Button(text='Save', size_hint=(None, 1))
        save_button.bind(on_release=self.save_canvas)
        load_button = Button(text='Load', size_hint=(None, 1))
        load_button.bind(on_release=self.load_canvas)

        top_bar.add_widget(clear_button)
        top_bar.add_widget(save_button)
        top_bar.add_widget(load_button)

        layout.add_widget(top_bar)
        layout.add_widget(self.painter)

        return layout

    def clear_canvas(self, instance):
        # Clear the canvas by removing all instructions
        self.painter.canvas.clear()

    def save_canvas(self, instance):
        # Create a popup for saving the canvas
        popup_layout = BoxLayout(orientation='vertical')
        filename_input = TextInput(hint_text='Enter filename', multiline=False, size_hint=(1, None), height=30)
        save_button = Button(text='Save', size_hint=(1, None), height=50)

        popup_layout.add_widget(filename_input)
        popup_layout.add_widget(save_button)

        popup_content = GridLayout(cols=1)
        popup_content.add_widget(popup_layout)

        popup = Popup(title='Save Canvas', content=popup_content, size_hint=(None, None), size=(300, 150))

        def save_callback(instance):
            filename = filename_input.text + ".png"
            self.painter.export_to_png(filename)
            popup.dismiss()

        save_button.bind(on_release=save_callback)
        popup.open()

    def load_canvas(self, instance):
        # Create a popup for loading a canvas
        popup_layout = BoxLayout(orientation='vertical')
        file_chooser = FileChooserIconView()
        file_chooser.path = "./"
        load_button = Button(text='Load', size_hint=(1, None), height=50)

        popup_layout.add_widget(file_chooser)
        popup_layout.add_widget(load_button)

        popup_content = GridLayout(cols=1)
        popup_content.add_widget(popup_layout)

        popup = Popup(title='Load Canvas', content=popup_content, size_hint=(None, None), size=(400, 400))

        def load_callback(instance):
            filename = file_chooser.selection and file_chooser.selection[0] or ""
            if filename:
                self.painter.canvas.clear()
                self.painter.add_widget(Image(source=filename))
            popup.dismiss()

        load_button.bind(on_release=load_callback)
        popup.open()

if __name__ == '__main__':
    PaintApp().run()