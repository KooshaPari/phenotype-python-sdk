"""Composition root — wires adapters to domain."""

from ..adapters import CliAdapter, FastMcpAdapter
from ..domain.engine import AgentEngine
from ..domain.models import Agent


class App:
    def __init__(self, agent: Agent):
        self.engine = AgentEngine(agent)
        self.server = FastMcpAdapter(agent)
        self.cli = CliAdapter(self.engine)

    def run_server(self) -> None:
        self.server.start()

    def run_cli(self) -> None:
        self.cli.run()