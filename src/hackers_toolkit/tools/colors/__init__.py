import os
from typing import Dict, Callable
import zlib

from toga import Box, Button, Label, NumberInput, Selection, TextInput, Widget
from toga.style import Pack
from toga.style.pack import COLUMN

from ..utils import BaseTool, register_tool


@register_tool
class ColorPicker(BaseTool):
    name = "Color picker"
    categories = {"colors", "web"}

    def build_ui(self) -> Widget:
        hexadecimal_input = TextInput()

        hexadecimal_short_input = TextInput()

        r_8bit = NumberInput(min_value=0, max_value=255)
        g_8bit = NumberInput(min_value=0, max_value=255)
        b_8bit = NumberInput(min_value=0, max_value=255)
        a_8bit = NumberInput(min_value=0, max_value=255)

        r_float = NumberInput(min_value=0, max_value=1, step=0.001)
        g_float = NumberInput(min_value=0, max_value=1, step=0.001)
        b_float = NumberInput(min_value=0, max_value=1, step=0.001)
        a_float = NumberInput(min_value=0, max_value=1, step=0.001)

        hsv_h = NumberInput(min_value=0, max_value=1, step=0.001)
        hsv_s = NumberInput(min_value=0, max_value=1, step=0.001)
        hsv_v = NumberInput(min_value=0, max_value=1, step=0.001)
        hsv_a = NumberInput(min_value=0, max_value=1, step=0.001)

        hsl_h = NumberInput(min_value=0, max_value=1, step=0.001)
        hsl_s = NumberInput(min_value=0, max_value=1, step=0.001)
        hsl_l = NumberInput(min_value=0, max_value=1, step=0.001)
        hsl_a = NumberInput(min_value=0, max_value=1, step=0.001)

        cmyk_c = NumberInput(min_value=0, max_value=100)
        cmyk_y = NumberInput(min_value=0, max_value=100)
        cmyk_m = NumberInput(min_value=0, max_value=100)
        cmyk_k = NumberInput(min_value=0, max_value=100)
        cmyk_a = NumberInput(min_value=0, max_value=100)

        def update_everything(
            red: float, green: float, blue: float, alpha: float
        ) -> None:
            red_8bit = round(red * 255)
            green_8bit = round(green * 255)
            blue_8bit = round(blue * 255)
            alpha_8bit = round(alpha * 255)

            red_hex = format(red_8bit, "02X")
            green_hex = format(green_8bit, "02X")
            blue_hex = format(blue_8bit, "02X")
            alpha_hex = format(alpha_8bit, "02X")

            hexadecimal_input.value = "#" + red_hex + green_hex + blue_hex + alpha_hex
            hexadecimal_short_input.value = (
                "#" + red_hex[:1] + green_hex[:1] + blue_hex[:1] + alpha_hex[:1]
            )

            r_8bit.value = red_8bit
            g_8bit.value = green_8bit
            b_8bit.value = blue_8bit
            a_8bit.value = alpha_8bit

            r_float.value = red
            g_float.value = green
            b_float.value = blue
            a_float.value = alpha

        def update_from_hexadecimal(textInput: Widget):
            pass

        update_everything(0, 0, 0, 1)

        return Box(
            children=[
                Label("Hexadecimal:"),
                hexadecimal_input,
                Label("Hexadecimal (short):"),
                hexadecimal_short_input,
                Label("RGB (8-bit):"),
                Box(
                    children=[
                        Label("R:"),
                        r_8bit,
                        Label("G:"),
                        g_8bit,
                        Label("B:"),
                        b_8bit,
                        Label("A:"),
                        a_8bit,
                    ]
                ),
                Label("RGB (float):"),
                Box(
                    children=[
                        Label("R:"),
                        r_float,
                        Label("G:"),
                        g_float,
                        Label("B:"),
                        b_float,
                        Label("A:"),
                        a_float,
                    ]
                ),
                Label("HSV:"),
                Box(
                    children=[
                        Label("H:"),
                        hsv_h,
                        Label("S:"),
                        hsv_s,
                        Label("V:"),
                        hsv_v,
                        Label("A:"),
                        hsv_a,
                    ]
                ),
                Label("HSL:"),
                Box(
                    children=[
                        Label("H:"),
                        hsl_h,
                        Label("S:"),
                        hsl_s,
                        Label("L:"),
                        hsl_l,
                        Label("A:"),
                        hsl_a,
                    ]
                ),
                Label("CMYK:"),
                Box(
                    children=[
                        Label("C:"),
                        cmyk_c,
                        Label("M:"),
                        cmyk_m,
                        Label("Y:"),
                        cmyk_y,
                        Label("K:"),
                        cmyk_k,
                        Label("A:"),
                        cmyk_a,
                    ]
                ),
                Label("Picker:"),
                # TODO (canvas ?)
            ],
            style=Pack(direction=COLUMN, flex=1),
        )
