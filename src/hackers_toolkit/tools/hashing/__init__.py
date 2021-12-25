import hashlib
import os
from typing import Dict, Callable
import zlib

from toga import Box, Button, Label, MultilineTextInput, Selection, TextInput, Widget
from toga.style import Pack
from toga.style.pack import COLUMN

from ..utils import BaseTool, register_tool

HASH_FUNCTIONS: Dict[str, Callable[[bytes], str]] = {
    "md5": lambda x: hashlib.md5(x).hexdigest(),
    "sha1": lambda x: hashlib.sha1(x).hexdigest(),
    "sha256": lambda x: hashlib.sha256(x).hexdigest(),
    "sha512": lambda x: hashlib.sha512(x).hexdigest(),
    "sha224": lambda x: hashlib.sha224(x).hexdigest(),
    "sha384": lambda x: hashlib.sha384(x).hexdigest(),
    "crc32": lambda x: hex(zlib.crc32(x) & 0xFFFFFFFF)[2:],
    "adler32": lambda x: hex(zlib.adler32(x) & 0xFFFFFFFF)[2:],
}


@register_tool
class HashText(BaseTool):
    name = "Hash text"
    categories = {"hashing", "text"}

    def build_ui(self) -> Widget:
        hash_selection = Selection(items=list(HASH_FUNCTIONS))
        text_input = MultilineTextInput()
        output_field = TextInput(readonly=True)

        def compute_hash(_button: Widget):
            hash_result = HASH_FUNCTIONS[hash_selection.value](
                text_input.value.encode()
            )
            output_field.value = hash_result

        return Box(
            children=[
                Label("Hashing algorithm:"),
                hash_selection,
                Label("Input:"),
                text_input,
                Button("Compute hash", on_press=compute_hash),
                Label("Output:"),
                output_field,
            ],
            style=Pack(direction=COLUMN),
        )


@register_tool
class HashFiles(BaseTool):
    name = "Hash files"
    categories = {"hashing", "files"}

    def build_ui(self) -> Widget:
        hash_selection = Selection(items=list(HASH_FUNCTIONS))
        file_input = TextInput(readonly=True)
        output_field = TextInput(readonly=True)

        def select_file(_button: Widget) -> None:
            try:
                path = self.main_window.open_file_dialog("Select a file to hash")
            except ValueError:
                return  # Use cancelled the action
            file_input.value = path

        def compute_hash(_button: Widget) -> None:
            if not os.path.isfile(file_input.value):
                return  # TODO error message
            with open(file_input.value, mode="rb") as input_file:
                hash_result = HASH_FUNCTIONS[hash_selection.value](input_file.read())
            output_field.value = hash_result

        return Box(
            children=[
                Label("Hashing algorithm:"),
                hash_selection,
                Label("Input:"),
                Box(children=[file_input, Button("Select file", on_press=select_file)]),
                Button("Compute hash", on_press=compute_hash),
                Label("Output:"),
                output_field,
            ],
            style=Pack(direction=COLUMN),
        )
