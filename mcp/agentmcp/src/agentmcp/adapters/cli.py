"""CLI adapter — interactive shell for AgentMCP."""

import sys
from ..domain.engine import AgentEngine


class CliAdapter:
    def __init__(self, engine: AgentEngine):
        self.engine = engine

    def run(self) -> None:
        print(f"AgentMCP shell: {self.engine.agent.name}")
        print("Commands: tools, add <tool>, quit")
        while True:
            try:
                line = input("> ").strip()
            except EOFError:
                break
            if line == "quit":
                break
            if line == "tools":
                for t in self.engine.list_tools():
                    print(f"  - {t}")
            elif line.startswith("add "):
                name = line[4:]
                self.engine.add_tool(...)
                print(f"Added {name}")
            else:
                print("Unknown command")
