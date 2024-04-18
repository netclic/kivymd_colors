from kivy.clock import Clock
from kivy.utils import hex_colormap

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from materialyoucolor.utils.platform_utils import SCHEMES


def rgba_color_to_hex(color):
    return "#{0:02X}{1:02X}{2:02X}".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))


class ScreenIntro(MDScreen):

    menu: MDDropdownMenu = None

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def on_kv_post(self, base_widget):
        Clock.schedule_once(self.generate_cards)

    def switch_theme_button(self):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"

    def get_instance_from_menu(self, name_item):
        index = 0
        rv = self.menu.ids.md_menu
        opts = rv.layout_manager.view_opts
        datas = rv.data[0]

        for data in rv.data:
            if data["text"] == name_item:
                index = rv.data.index(data)
                break

        instance = rv.view_adapter.get_view(
            index, datas, opts[index]["viewclass"]
        )

        return instance

    def open_menu(self, menu_button):
        menu_items = []
        for item, method in {
            "Set palette": lambda: self.set_palette(),
            "Set scheme type": lambda: self.set_scheme_type(),
            "Switch theme style": lambda: self.theme_switch(),
        }.items():
            menu_items.append({"text": item, "on_release": method})
        self.menu = MDDropdownMenu(
            caller=menu_button,
            items=menu_items,
        )
        self.menu.open()

    def set_palette(self):
        instance_from_menu = self.get_instance_from_menu("Set palette")
        available_palettes = [
            name_color.capitalize() for name_color in hex_colormap.keys()
        ]

        menu_items = []
        for name_palette in available_palettes:
            menu_items.append(
                {
                    "text": name_palette,
                    "on_release": lambda x=name_palette: self.switch_palette(x),
                }
            )
        MDDropdownMenu(
            caller=instance_from_menu,
            items=menu_items,
        ).open()

    def set_scheme_type(self):
        instance_from_menu = self.get_instance_from_menu("Set scheme type")

        menu_items = []
        for scheme_name in SCHEMES.keys():
            menu_items.append(
                {
                    "text": scheme_name,
                    "on_release": lambda x=scheme_name: self.update_scheme(x),
                }
            )

        self.scheme_menu = MDDropdownMenu(
            caller=instance_from_menu,
            items=menu_items,
            width=400,
            max_height=590,
            hor_growth="left",
            ver_growth="down"
        )
        self.scheme_menu.open()

    def switch_palette(self, selected_palette):
        self.theme_cls.primary_palette = selected_palette
        Clock.schedule_once(self.generate_cards, 0.5)

    def update_scheme(self, scheme_name):
        self.theme_cls.dynamic_scheme_name = scheme_name
        Clock.schedule_once(self.generate_cards, 0.5)
        # self.scheme_menu.dismiss()

    def theme_switch(self) -> None:
        self.theme_cls.switch_theme()
        Clock.schedule_once(self.generate_cards, 0.5)

    def generate_cards(self, *args):
        self.ids['palette_name'].text = self.theme_cls.primary_palette + ' - ' + self.theme_cls.dynamic_scheme_name
        self.ids.card_list.data = []

        color_attributes = [attr_name for attr_name in dir(self.theme_cls) if 'Color' in attr_name]

        for color_name in color_attributes:
            value = f"{color_name}"
            color = getattr(self.theme_cls, value)
            self.ids.card_list.data.append(
                {
                    "bg_color": color,
                    "text": value + '\n' + rgba_color_to_hex(color),
                }
            )
