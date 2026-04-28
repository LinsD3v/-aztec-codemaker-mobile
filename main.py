import treepoem
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window

from PIL import Image as PILImage
from kivy.graphics.texture import Texture
import io


class AztecApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Input numérico
        self.input = TextInput(
            hint_text="Digite um número (ex: 42)",
            multiline=False,
            font_size=32,
            size_hint=(1, 0.2)
        )

        # Botão gerar
        self.button = Button(
            text="Gerar Aztec",
            font_size=28,
            size_hint=(1, 0.2)
        )
        self.button.bind(on_press=self.generate_code)

        # Imagem do código
        self.image = Image(size_hint=(1, 0.6))

        self.layout.add_widget(self.input)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.image)

        return self.layout

    def generate_code(self, instance):
        value = self.input.text.strip()

        if not value:
            return

        # Gera Aztec
        img = treepoem.generate_barcode(
            barcode_type='azteccode',
            data=value
        )
        
        # Converte para Buffer
        buffer = io.BytesIO()
        img.convert('RGBA').save(buffer, format='PNG')
        buffer.seek(0)
        
        pil_image = PILImage.open(buffer)
        
        data = pil_image.tobytes()
        texture = Texture.create(size=pil_image.size)
        texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        
        self.image.texture = texture


if __name__ == "__main__":
    Window.size = (400, 700)  # útil pra testar no PC
    AztecApp().run()