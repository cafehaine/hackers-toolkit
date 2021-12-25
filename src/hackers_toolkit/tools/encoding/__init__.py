import base64
import hashlib
import os
from typing import Dict, Callable
import zlib

from toga import Box, Button, Label, MultilineTextInput, Selection, TextInput, Widget
from toga.style import Pack
from toga.style.pack import COLUMN

from ..utils import BaseTool, register_tool

ENCODERS: Dict[str, Callable[[bytes], bytes]] = {
    "base64": base64.b64encode,
    "raw": lambda x: x,
    "base64 (urlsafe)": base64.urlsafe_b64encode,
    "base32": base64.b32encode,
    "base16": base64.b16encode,
    "base85": base64.b85encode,
    "ascii85": base64.a85encode,
}

DECODERS: Dict[str, Callable[[bytes], bytes]] = {
    "base64": base64.b64decode,
    "raw": lambda x: x,
    "base64 (urlsafe)": base64.urlsafe_b64decode,
    "base32": base64.b32decode,
    "base16": base64.b16decode,
    "base85": base64.b85decode,
    "ascii85": base64.a85decode,
}


@register_tool
class TranscodeText(BaseTool):
    name = "Transcode text"
    categories = {"encoding", "text"}

    def build_ui(self) -> Widget:
        decoder_selection = Selection(items=list(DECODERS))
        encoder_selection = Selection(items=list(ENCODERS))
        input_field = MultilineTextInput()
        output_field = MultilineTextInput(readonly=True)

        def transcode(_button: Widget):
            decoder = DECODERS[decoder_selection.value]
            encoder = ENCODERS[encoder_selection.value]
            raw_data = decoder(input_field.value.encode())
            encoded = encoder(raw_data).decode()
            output_field.value = encoded

        return Box(
            children=[
                Label("Input base:"),
                decoder_selection,
                Label("Input:"),
                input_field,
                Button("Transcode", on_press=transcode),
                Label("Output base:"),
                encoder_selection,
                Label("Output:"),
                output_field,
            ],
            style=Pack(direction=COLUMN, flex=1),
        )
