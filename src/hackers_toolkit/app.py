"""
A set of tools for developers and hackers.
"""
from typing import Optional

import toga
from toga.sources.tree_source import Node
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .tools import ALL_TOOLS
from .tools.utils import BaseTool, DummyTool

class HackersToolkit(toga.App):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tool_box: Box
        self.dummy_tool: DummyTool

    def on_tree_select(self, widget: toga.Widget, node: Optional[Node]):
        if not hasattr(self, "dummy_tool"):
            return # Startup function not yet run.

        for child in self.tool_box.children:
            self.tool_box.remove(child)

        found_tool = self.dummy_tool

        if node is None:
            pass
        else:
            for tool in ALL_TOOLS:
                if node.tools == tool.name:
                    found_tool = tool(self.main_window)
                    break

        self.tool_box.add(found_tool.build_ui())

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        tool_tree = toga.Tree(["Tools"], on_select = self.on_tree_select)
        tool_list = list(ALL_TOOLS)

        categories = set()
        for tool in tool_list:
            categories |= tool.categories
        category_list = list(categories)
        category_list.sort()

        category_nodes = {}
        for category in category_list:
            category_nodes[category] = tool_tree.data.append(None, category.title())

        tool_list.sort(key=lambda tool: tool.name)
        for tool in tool_list:
            for category in tool.categories:
                tool_tree.data.append(category_nodes[category], tool.name)

        self.tool_box = toga.Box()
        main_box = toga.Box(children=[tool_tree, self.tool_box])

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        self.dummy_tool = DummyTool(self.main_window)


def main():
    return HackersToolkit()
