from abc import ABC, abstractmethod
from typing import Set, Type

from toga import Box, Label, MainWindow, Widget
from toga.style import Pack
from toga.style.pack import COLUMN

ALL_TOOLS: Set[Type["BaseTool"]] = set()

def register_tool(tool_class: Type["BaseTool"]) -> Type["BaseTool"]:
    assert hasattr(tool_class, "name"), f"Tool class {tool_class.__name__} has no 'name' attribute."
    assert hasattr(tool_class, "categories"), f"Tool class {tool_class.__name__} has not 'categories' attribute."
    ALL_TOOLS.add(tool_class)
    print("Registered tool:", tool_class.__name__)
    return tool_class

class BaseTool(ABC):
    """The base class for all tools."""
    name: str
    categories: Set[str]

    def __init__(self, main_window: MainWindow) -> None:
        self.main_window = main_window

    @abstractmethod
    def build_ui(self) -> Widget:
        """Return a Toga widget that will be displayed when using the tool."""

class DummyTool(BaseTool):
    """A dummy tool displayed when no real tool is selected."""
    name = "DUMMY"
    categories = set()

    def build_ui(self) -> Widget:
        return Box(children=[Label("No tool selected."), Label("Please select a tool on the left panel.")], style=Pack(direction=COLUMN))
