import logging
import sys
import traceback

from kivmob import KivMob, TestIds
from kivy.utils import platform

if platform != 'android':
    import os
    from kivy.config import Config
    Config.set('graphics', 'resizable', '0')
    os.environ["KIVY_METRICS_FONTSCALE"] = "1.0"

    # Fairphone 4 5G
    os.environ["KIVY_METRICS_DENSITY"] = "2.5"  # Adjust this value according to your needs
    Config.set('graphics', 'width', '1080')
    Config.set('graphics', 'height', '2139')
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

from config import version
from screen_intro import ScreenIntro

from kivmob_mod import KivMob, TestIds


class ColorCard(BoxLayout):
    text = StringProperty()
    bg_color = ColorProperty()


class KivyMDColors(MDApp):

    ads = None

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

            Builder.load_file('resources/kv_files/screen_intro.kv')

            sm = ScreenManager(transition=SlideTransition(direction="left"))
            sm.add_widget(ScreenIntro(name='screen_intro'))
            sm.current = 'screen_intro'

            return sm

        except Exception:
            traceback.print_exc()
            logging.exception("Exception occured in build method")

    def on_start(self):
        if platform == 'android':
            # Setup ADS using KivMob (banner only)
            self.ads = KivMob(TestIds.APP)
            self.ads.new_banner(TestIds.BANNER, top_pos=False)
            self.ads.request_banner()
            self.ads.show_banner()

    def on_resume(self):
        logging.info("kivmob_test: on_resume()")
        if platform == 'android':
            self.load_ads()

    def load_ads(self):
        if platform == 'android':
            logging.info("kivmob_test: load_ads() fired")
            # banner
            self.ads.request_banner()
            # interstitial
            self.ads.load_interstitial(TestIds.INTERSTITIAL)

    def show_banner(self):
        if platform == 'android':
            logging.info("kivmob_test: show_banner() fired")
            self.ads.show_banner()

    def hide_banner(self):
        if platform == 'android':
            logging.info("kivmob_test: hide_banner() fired")
            self.ads.hide_banner()

    def load_interstitial(self):
        if platform == 'android':
            logging.info("kivmob_test: load_interstitial() fired")
            self.ads.load_interstitial(TestIds.INTERSTITIAL)

    def show_interstitial(self):
        if platform == 'android':
            logging.info("kivmob_test: show_interstitial() fired")
            self.ads.show_interstitial()


if __name__ == '__main__':
    KivyMDColors().run()
