"""Composition root — wires adapters to domain."""

from ..domain.models import Agent
from ..domain.engine import AgentEngine
from ..adapters import FastMcpAdapter, CliAdapter


class App:
    def __init__(self, agent: Agent):
        self.engine = AgentEngine(agent)
        self.server = FastMcpAdapter(agent)
        self.cli = CliAdapter(self.engine)

    def run_server(self) -> None:
        self.server.start()

    def run_cli(self) -> None:
        self.cli.run()
