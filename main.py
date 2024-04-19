import logging
import sys
import traceback

from kivy.utils import platform

# if platform != 'android':
#     import os
#     from kivy.config import Config
#     Config.set('graphics', 'resizable', '0')
#     os.environ["KIVY_METRICS_FONTSCALE"] = "1.0"
#
#     # Fairphone 4 5G
#     os.environ["KIVY_METRICS_DENSITY"] = "2.5"  # Adjust this value according to your needs
#     Config.set('graphics', 'width', '1080')
#     Config.set('graphics', 'height', '2139')
#
#     # Honor 90 Lite
#     os.environ["KIVY_METRICS_DENSITY"] = "2.0"  # Adjust this value according to your needs
#     Config.set('graphics', 'width', '1080')
#     Config.set('graphics', 'height', '1920')


from kivy.properties import StringProperty, ColorProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from kivymd.app import MDApp

from screen_intro import ScreenIntro


class ColorCard(BoxLayout):
    text = StringProperty()
    bg_color = ColorProperty()


class KivyMDColors(MDApp):
    def build(self):
        # Setup logging
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

        logging.info("Application started")

        try:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Antiquewhite"
            self.theme_cls.dynamic_scheme_name = "TONAL_SPOT"
            self.theme_cls.dynamic_color = False

            Builder.load_file('resources/kv_files/KivyMDColors.kv')

            sm = ScreenManager(transition=SlideTransition(direction="left"))
            sm.add_widget(ScreenIntro(name='screen_intro'))

            return sm
        except Exception:
            traceback.print_exc()
            logging.exception("Exception occured in build method")


if __name__ == '__main__':
    KivyMDColors().run()
