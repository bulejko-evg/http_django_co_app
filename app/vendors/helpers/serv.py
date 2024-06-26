from typing import Literal
from itertools import batched
from collections import UserString


class ListTransaction:
    """Context manager. Change list only if there are no exceptions"""
    def __init__(self, _list):
        self._list = _list

    def __enter__(self):
        self.work_copy = list(self._list)
        return self.work_copy

    def __exit__(self, _type, value, tb):
        if _type is None:
            self._list[:] = self.work_copy
        return False


type StringModifier = Literal[
    "bolt",
    "italic",
    "underline",
    "strikethrough",
    "reverse",
    "invisible",
]
type ColorName = Literal[
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "gray",
    "bright red",
    "bright green",
    "bright yellow",
    "bright blue",
    "bright magenta",
    "bright cyan",
    "bright white",
]


class ColorString(UserString):
    """
    Set color for string. Set background for string. Modify string. Blinking.
    -------------------------------------------------------------------------
    Parameters:
        string (str): string data
        color (ColorName | tuple[int, int, int] | str | int | None):
            ColorName: literal with values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)
            tuple[int, int, int]: tuple with RGB values
            str: hex color (like #FFFFFF or #FFF)
            int: color code from ANSI (VGA)
                (show codes call class method show_names_and_codes_of_colors)
        bg (ColorName | tuple[int, int, int] | str | int | None):
            ColorName: literal with values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)
            tuple[int, int, int]: tuple with RGB values
            str: hex color (like #FFFFFF or #FFF)
            int: color code from ANSI (VGA)
                (show codes call class method show_names_and_codes_of_colors)
        mod (StringModifier | list[StringModifier] | None):
            literal with values (italic, bold, underline, reverse, invisible, strikethrough)
                italic: str to italic font
                bold: str to bold font
                underline: underline str
                reverse: revese foreground and background colors
                invisible: invisible str
                strikethrough: strikethrough str
        blink (bool): if True str is blinking
    Returns:
        (str): colored, modified string, blinking string
    Methods:
        show_names_and_codes_of_colors (classmethod):
            show colors by names and colors by ANSI codes (VGA)
    """
    _BLACK, _WHITE = 15, 0
    _PREFIX = "\u001b["
    _POSTFIX = "\u001b[0m"
    _COLOR_CODES = (0, 255)
    _BLINK = "\u001b[5m"
    _COLOR_BY_NAME = {
        "black": (0, 0, 0),
        "red": (170, 0, 0),
        "green": (0, 170, 0),
        "yellow": (170, 85, 0),
        "blue": (0, 0, 170),
        "magenta": (170, 0, 170),
        "cyan": (0, 170, 170),
        "white": (170, 170, 170),
        "gray": (85, 85, 85),
        "bright red": (255, 85, 85),
        "bright green": (85, 255, 85),
        "bright yellow": (255, 255, 85),
        "bright blue": (85, 85, 255),
        "bright magenta": (255, 85, 255),
        "bright cyan": (85, 255, 255),
        "bright white": (255, 255, 255),
    }
    _modifiers = {
        "italic": "\u001b[3m",
        "bold":"\u001b[1m",
        "underline": "\u001b[4m",
        "reverse": "\u001b[7m",
        "invisible": "\u001b[8m",
        "strikethrough": "\u001b[9m",
    }

    def __init__(self,
        string: str,
        color: ColorName | tuple[int, int, int] | str | int | None = None,
        bg: ColorName | tuple[int, int, int] | str | int | None = None,
        mod: StringModifier | list[StringModifier] | None = None,
        blink: bool = False,
    ):
        """
        Parameters:
            string (str): string data
            color (ColorName | tuple[int, int, int] | str | int | None):
                ColorName: literal with values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)
                tuple[int, int, int]: tuple with RGB values
                str: hex color
                int: color code from ANSI (VGA)
                    (show codes call class method show_names_and_codes_of_colors)
            bg (ColorName | tuple[int, int, int] | str | int | None):
                ColorName: literal with values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)
                tuple[int, int, int]: tuple with RGB values
                str: hex color (like #FFFFFF or #FFF)
                int: color code from ANSI (VGA)
                    (show codes call class method show_names_and_codes_of_colors)
            mod (StringModifier | list[StringModifier] | None):
                literal with values (italic, bold, underline, reverse, invisible, strikethrough)
                    italic: str to italic font
                    bold: str to bold font
                    underline: underline str
                    reverse: revese foreground and background colors
                    invisible: invisible str
                    strikethrough: strikethrough str
            blink (bool): if True str is blinking
        Returns:
            (str): colored, modified string, blinking string
        """
        super().__init__(string)
        self.blink = self._BLINK if blink else ""
        self.color = color
        self.bg = bg
        self.mod = mod

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, val: tuple[int, int, int] | str | int | None) -> None:
        if val is None:
            self._color = ""
            return
        if isinstance(val, tuple):
            _color = self._get_rgb_str(self._get_rgb_color(val))
        if isinstance(val, str):
            _color = self._get_rgb_str(self._get_rgb_from_str(val))
        if isinstance(val, int):
            _color = self._get_code_str(val)
        self._color = self._PREFIX + _color

    @property
    def bg(self) -> str:
        return self._bg

    @bg.setter
    def bg(self, val: tuple[int, int, int] | str | int | None) -> None:
        if val is None:
            self._bg = ""
            return
        if isinstance(val, tuple):
            _bg = self._get_rgb_str(self._get_rgb_color(val), bg=True)
        if isinstance(val, str):
            _bg = self._get_rgb_str(self._get_rgb_from_str(val), bg=True)
        if isinstance(val, int):
            _bg = self._get_code_str(val, bg=True)
        self._bg = self._PREFIX + _bg

    @property
    def mod(self) -> str:
        return self._mod

    @mod.setter
    def mod(self, val: StringModifier | list[StringModifier] | None) -> None:
        self._mod = self._get_str_mod(val)

    @property
    def blink(self) -> str:
        return self._blink

    @blink.setter
    def blink(self, val: bool) -> None:
        self._blink = "\u001b[5m" if val else ""

    @staticmethod
    def _get_rgb_str(rgb: tuple[int, int, int], bg: bool = False) -> str:
        """Get rgb str"""
        r, g, b = rgb
        color_str = f"48;2;{r};{g};{b}m" if bg else f"38;2;{r};{g};{b}m"
        return ColorString._PREFIX + color_str

    @staticmethod
    def _get_code_str(code: int, bg: bool = False) -> str:
        """Get code str"""
        color_str = f"48;5;{code}m" if bg else f"38;5;{code}m"
        return ColorString._PREFIX + color_str

    def _get_str_mod(self, mod_key: StringModifier | None) -> str:
        """
        Get modifyer for str by key
        from literl(italic, bold, underline, strikethrough, reverse, invisible)
        """
        if mod_key is None: return ""
        try:
            if isinstance(mod_key, str):
                _modifiers = self._modifiers[mod_key]
            if isinstance(mod_key, list):
                _modifiers = "".join([self._modifiers[k] for k in mod_key])
        except KeyError as exc:
            raise ValueError("Incorrect str modifier. Correct (italic, bold, underline, strikethrough, reverse, invisible)") from exc
        else:
            return _modifiers

    def _get_rgb_color(self, color: tuple[int, int, int]) -> tuple[int, int, int]:
        """
        Check r, g, b values for color.
        --------------------------------
        Parameters:
            color (tuple[int, int, int]): r, g, b ocolor
        Returns:
            r, g, b (tuple[int, int, int]): r, g, b of color
        """
        for v in color:
            if not 0 <= v <= 255:
                raise ValueError("Incorrect r, g, b of color (Correct value from 0 to 255)")
        try:
            r, g, b = int(color[0]), int(color[1]), int(color[2])
        except IndexError as exc:
            raise ValueError("Incorrect r, g, b tuple") from exc
        except ValueError as exc:
            raise ValueError("Incorrect r, g, b of color. Not converted to int") from exc
        else:
            return r, g, b

    def _get_rgb_from_str(self, color: str) -> tuple[int, int, int]:
        """
        Get r, g, b color by color str.
        -------------------------------
        Parameters:
            color (str): color as hex or key from ColorName literal
        Returns:
            r, g, b (tuple[int, int, int]): r, g, b of color
        """
        if color.startswith("#"):
            r, g, b = self._get_rgb_from_hex(color)
        else:
            r, g, b = self._get_rgb_from_colors(color)

        return r, g, b

    def _get_rgb_from_hex(self, hex_str: str) -> tuple[int, int, int]:
        """
        Get r, g, b from hex string.
        ----------------------------
        Parameters:
            color (str): color as hex str
        Returns:
            r, g, b (tuple[int, int, int]): r, g, b of color
        """
        hex_str_val = self._check_hex_str(hex_str)
        try:
            r, g, b = tuple(int(hex_str_val[i:i + 2], 16) for i in (1, 3, 5))
        except Exception as exc:
            raise ValueError("Incorrect hex string") from exc
        else:
            return r, g, b

    def _check_hex_str(self, hex_str: str) -> str:
        """Check and chenge hex str"""
        _hex_str = hex_str
        if len(_hex_str) != 4 or len(_hex_str) != 7:
            raise ValueError("Incorrect hex string. (valid value #33FF48 or #ccc)")
        if len(_hex_str) == 4:
            _hex_str = [v+v for v in list(_hex_str)[1:]]
        return _hex_str


    def _get_rgb_from_colors(self, color_name: str) -> tuple[int, int, int]:
        """
        Get g, g, b from dict _COLOR_BY_NAME by key color_name.
        -------------------------------------------------------
        Parameters:
            color (str): color str from ColorName literal
        Returns:
            r, g, b (tuple[int, int, int]): r, g, b of color
        """
        try:
            r, g, b = self._COLOR_BY_NAME[color_name]
        except KeyError as exc:
            raise ValueError("Incorrect color name. Correct values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)") from exc
        else:
            return r, g, b

    def _get_color_str(self):
        return f"{self.color}{self.bg}{self.mod}{self.blink}{self.data}{self._POSTFIX}"

    def __str__(self):
        return self._get_color_str()

    @classmethod
    def show_names_and_codes_of_colors(cls):
        """Show colors by names, and colors codes"""
        _show_mask = {
            "Standard colors": slice(0, 8),
            "High-intensity colors": slice(8, 16),
            "Colors": slice(16, 232),
            "Grayscale colors": slice(232, 256),
        }
        _codes = range(cls._COLOR_CODES[1]+1)
        color_items = {k: _codes[v] for k, v in _show_mask.items()}

        group_key = "By names"
        print(f"\n{' '*20}{group_key.upper()}\n")
        for k, v in cls._COLOR_BY_NAME.items():
            r, g, b = v
            fr_color_code = cls._BLACK
            color_str = f"{cls._get_rgb_str(rgb=(r, g, b))}{k:^16}{cls._POSTFIX}"
            color_str_bg = f"{cls._get_rgb_str(rgb=(r, g, b), bg=True)}{' ':^10}{cls._POSTFIX}"
            print(color_str, color_str_bg)

        print(f"\n{' '*20}{'By codes'.upper()}")
        colors_codes = color_items["Standard colors"]
        group_key = "Standard colors"
        print(f"\n{' '*10}{group_key}")
        color_str_list = []
        for i, code in enumerate(colors_codes):
            fr_color_code = cls._WHITE if i == len(colors_codes)-1 else cls._BLACK
            color_str = f"{cls._get_code_str(code=fr_color_code)}{cls._get_code_str(code=code, bg=True)}{code:^8}{cls._POSTFIX}"
            color_str_list.append(color_str)
        print("".join(color_str_list))

        colors_codes = color_items["High-intensity colors"]
        group_key = "High-intensity colors"
        print(f"\n{' '*10}{group_key}")
        color_str_list = []
        for i, code in enumerate(colors_codes):
            fr_color_code = cls._WHITE if i == len(colors_codes)-1 else cls._BLACK
            color_str = f"{cls._get_code_str(code=fr_color_code)}{cls._get_code_str(code=code, bg=True)}{code:^8}{cls._POSTFIX}"
            color_str_list.append(color_str)
        print("".join(color_str_list))

        colors_list = color_items["Colors"]
        group_key = "Colors"
        print(f"\n{' '*10}{group_key}")
        colors_groups = list(batched(list(batched(colors_list, 6)), 6))
        colors_groups = list(zip(*colors_groups))
        for i, color_group in enumerate(colors_groups):
            for j, color_codes in enumerate(color_group):
                color_str_list = []
                fr_color_code = cls._BLACK if i < 3 else cls._WHITE
                for code in color_codes:
                    color_str = f"{cls._get_code_str(code=fr_color_code)}{cls._get_code_str(code=code, bg=True)}{code:^8}{cls._POSTFIX}"
                    color_str_list.append(color_str)
                print("".join(color_str_list))

        colors_codes = color_items["Grayscale colors"]
        group_key = "Grayscale colors"
        print(f"\n{' '*10}{group_key}")
        color_str_list = []
        first_part, second_part = colors_codes[:12], colors_codes[12:]
        for i, code in enumerate(first_part):
            color_str = f"{cls._get_code_str(code=cls._BLACK)}{cls._get_code_str(code=code, bg=True)}{code:^8}{cls._POSTFIX}"
            color_str_list.append(color_str)
        print("".join(color_str_list))
        color_str_list = []
        for i, code in enumerate(second_part):
            color_str = f"{cls._get_code_str(code=cls._WHITE)}{cls._get_code_str(code=code, bg=True)}{code:^8}{cls._POSTFIX}"
            color_str_list.append(color_str)
        print("".join(color_str_list))


class Cstr:
    """
    Get or print color for string. Set background for string. Modify string. Blinking.
    ----------------------------------------------------------------------------------
    """
    def __call__(
        self,
        string: str = "",
        color: ColorName | tuple[int, int, int] | str | int | None = None,
        bg: ColorName | tuple[int, int, int] | str | int | None = None,
        mod: StringModifier | list[StringModifier] | None = None,
        blink: bool = False,
    ) -> str:
        """
        Get string in color with background color, modifier and blinking.
        ------------------------------------------------------------------
        Parameters:
            string (str): string data, opional, default ""
            color (ColorName | tuple[int, int, int] | str | int | None):
                ColorName: literal with values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)
                tuple[int, int, int]: tuple with RGB values
                str: hex color (like #FFFFFF or #FFF)
                int: color code from ANSI (VGA)
                    (show codes call class method show_names_and_codes_of_colors)
                optional, default None
            bg (ColorName | tuple[int, int, int] | str | int | None):
                ColorName: literal with values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)
                tuple[int, int, int]: tuple with RGB values
                str: hex color (like #FFFFFF or #FFF)
                int: color code from ANSI (VGA)
                    (show codes call class method show_names_and_codes_of_colors)
                optional, default None
            mod (StringModifier | list[StringModifier] | None):
                literal with values (italic, bold, underline, reverse, invisible, strikethrough)
                    italic: str to italic font
                    bold: str to bold font
                    underline: underline str
                    reverse: revese foreground and background colors
                    invisible: invisible str
                    strikethrough: strikethrough str
                optional, default None
            blink (bool): if True str is blinking, optional, default False
        Returns:
            (str): colored, modified string, blinking string
        """
        return ColorString(string=string, color=color, bg=bg, mod=mod, blink=blink)
    
    def print(
        self,
        string: str,
        color: ColorName | tuple[int, int, int] | str | int | None = None,
        bg: ColorName | tuple[int, int, int] | str | int | None = None,
        mod: StringModifier | list[StringModifier] | None = None,
        blink: bool = False,
    ) -> str:
        """
        Primt string in color, with background, modifier and blinking.
        -------------------------------------------------------------
        Parameters:
            string (str): string data
            color (ColorName | tuple[int, int, int] | str | int | None):
                ColorName: literal with values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)
                tuple[int, int, int]: tuple with RGB values
                str: hex color (like #FFFFFF or #FFF)
                int: color code from ANSI (VGA)
                    (show codes call class method show_names_and_codes_of_colors)
                optional, default None
            bg (ColorName | tuple[int, int, int] | str | int | None):
                ColorName: literal with values (black, red, green, yellow, blue, magenta, cyan, white, gray, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white)
                tuple[int, int, int]: tuple with RGB values
                str: hex color (like #FFFFFF or #FFF)
                int: color code from ANSI (VGA)
                    (show codes call class method show_names_and_codes_of_colors)
                optional, default None
            mod (StringModifier | list[StringModifier] | None):
                literal with values (italic, bold, underline, reverse, invisible, strikethrough)
                    italic: str to italic font
                    bold: str to bold font
                    underline: underline str
                    reverse: revese foreground and background colors
                    invisible: invisible str
                    strikethrough: strikethrough str
                optional, default None
            blink (bool): if True str is blinking, optional, default False
        Returns:
            (str): colored, modified string, blinking string
        """
        return ColorString(string=string, color=color, bg=bg, mod=mod, blink=blink)
    
    def show_default_colors(self):
        """Show default colors, by namse and codes"""
        ColorString.show_names_and_codes_of_colors()


cstr = Cstr()