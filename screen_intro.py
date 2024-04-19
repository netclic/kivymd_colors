from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.utils import hex_colormap
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, \
    MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from materialyoucolor.utils.platform_utils import SCHEMES

from config import version


def rgba_color_to_hex(color):
    return "#{0:02X}{1:02X}{2:02X}".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))


class ScreenIntro(MDScreen):

    menu: MDDropdownMenu = None
    scheme_menu: MDDropdownMenu = None
    palette_menu: MDDropdownMenu = None


    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.color_attributes = [attr_name for attr_name in dir(self.theme_cls) if 'Color' in attr_name]
        self.colors_position = {attr_name: index for index, attr_name in enumerate(self.color_attributes)}
        self.initialized = False

    def on_kv_post(self, base_widget):
        Clock.schedule_once(self.generate_cards)

    def display_about(self):
        dialog = MDDialog(
            MDDialogIcon(
                icon="information-outline",
            ),
            MDDialogHeadlineText(
                text="About ... KivyMD Palette colors",
            ),
            MDDialogSupportingText(
                markup=True,
                text=f"[b]Version : {version}[/b]\n\n"
                     "[color=#ff0000]KivyMD Palette colors[/color] is written using Python3, KivyMD 2.0.1dev. KivyMD is a collection of Material Design compliant widgets for use with Kivy, a framework for cross-platform, touch-enabled graphical applications.\n\n"
                     "It is inspired from KivyMD included samples.\n\n"
                     "It's my first published app for Android.\nSo don't forget to comment in PlayStore.\n\n"
                    "-- netclic -- (Franck)\n"
            ),
            MDDialogContentContainer(
                MDDivider(),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="gmail",
                    ),
                    MDListItemSupportingText(
                        text="franky.koa1000@gmail.com",
                    ),
                ),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="web",
                    ),
                    MDListItemSupportingText(
                        text="https://github.com/kivymd",
                    ),
                ),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="web",
                    ),
                    MDListItemSupportingText(
                        text="https://kivy.org/",
                    ),
                ),
                MDDivider(),
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Ok"),
                    on_release=lambda x: dialog.dismiss(),
                    style="text",
                ),
                spacing="8dp",
            ),
        )

        dialog.open()

    def switch_theme_button(self):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"

    def get_instance_from_menu(self, name_item):
        """
        Parameters:
        - menu: The menu that contains the instance we want to retrieve.
        - name_item: The name of the item we are looking for in the menu.

        Returns:
        - The instance of the item in the menu with the given name_item, if found.

        Explanation:
        This method is used to retrieve an instance from a given menu based on the item's name.
        It takes two parameters, menu and name_item. The method iterates over the data in the menu until
        * it finds an item with the same name_item. Once found, it gets the index and position of the item in the menu.
            It then uses the index, data, and view class to get the corresponding instance
        * from the view_adapter. Finally, it sets the position of the instance and returns it.

        """

        index = 0
        data = None
        position = (0, 0)

        rv = self.menu.ids.md_menu
        opts = rv.layout_manager.view_opts
        datas = rv.data

        for data in datas:
            if data["text"] == name_item:
                index = rv.data.index(data)
                position = [rv.right + rv.width / 2, rv.top - (data['height'] * 0.66 + index * data['height'])]
                break

        instance = rv.view_adapter.get_view(
            index, data, opts[index]["viewclass"]
        )

        instance.pos = position

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
        self.palette_menu = MDDropdownMenu(
            caller=instance_from_menu,
            items=menu_items,
            hor_growth="right",
            ver_growth="down"
        )
        self.palette_menu.open()

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
            hor_growth="right",
            ver_growth="down"
        )
        self.scheme_menu.open()

    def switch_palette(self, selected_palette):
        self.theme_cls.primary_palette = selected_palette
        self.generate_cards()

    def update_scheme(self, scheme_name):
        self.theme_cls.dynamic_scheme_name = scheme_name
        self.generate_cards()

    def theme_switch(self) -> None:
        self.theme_cls.switch_theme()
        self.generate_cards()

    def generate_cards(self, *args):
        self.ids['palette_name'].text = self.theme_cls.primary_palette + ' - ' + self.theme_cls.dynamic_scheme_name
        if not self.initialized:
            self.ids.card_list.data = []

            for color_name in self.color_attributes:
                value = f"{color_name}"
                color = getattr(self.theme_cls, value)
                self.ids.card_list.data.append(
                    {
                        "bg_color": color,
                        "text": value + '\n' + rgba_color_to_hex(color),
                    }
                )
                self.initialized = True
        else:
            for color_name in self.color_attributes:
                value = f"{color_name}"
                color = getattr(self.theme_cls, value)
                self.ids.card_list.data[
                    self.colors_position[color_name]
                ]['bg_color'] = color
                self.ids.card_list.data[
                    self.colors_position[color_name]
                ]['text'] = value + '\n' + rgba_color_to_hex(color)
            self.ids.card_list.refresh_from_data()
