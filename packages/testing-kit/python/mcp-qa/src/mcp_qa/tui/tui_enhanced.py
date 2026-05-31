"""
Enhanced TUI for TDD Testing with Session-Scoped OAuth

This integrates the existing TUI with the new TDD session OAuth system:
- Shows OAuth status from session broker
- Real-time test execution with session credentials
- Individual tool testing interface
- Same rich UX as before, but with faster auth
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Optional

try:
    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from .auth_session import AuthCredentials, AuthSessionBroker
from .oauth_progress import OAuthProgressFlow


class TDDTestDashboard:
    """Enhanced test dashboard with session OAuth integration."""

    def __init__(self, auth_broker: AuthSessionBroker):
        self.auth_broker = auth_broker
        self.console = Console() if HAS_RICH else None
        self.credentials: Optional[AuthCredentials] = None
        self.test_results = []
        self.running_tests = False

    async def setup_and_run(self):
        """Setup OAuth and run the dashboard."""
        if not self.console:
            print("Rich not available - falling back to basic mode")
            return

        # Setup OAuth session
        await self.setup_oauth_session()

        # Run dashboard
        await self.run_dashboard()

    async def setup_oauth_session(self):
        """Setup session OAuth with rich progress display."""
        # Create OAuth status panel
        oauth_panel = Panel(
            "[bold blue]🔐 Setting up Session-Scoped OAuth...[/bold blue]",
            title="Authentication",
            border_style="blue"
        )

        with Live(oauth_panel, console=self.console, refresh_per_second=4) as live:
            try:
                with OAuthProgressFlow() as progress:
                    progress.step("Checking cached credentials...")
                    live.update(Panel(
                        "[yellow]⏳ Checking cached credentials...[/yellow]",
                        title="Authentication",
                        border_style="yellow"
                    ))

                    self.credentials = await self.auth_broker.get_authenticated_credentials(
                        provider="authkit",
                        force_refresh=False
                    )

                    if self.credentials.is_valid():
                        progress.complete("OAuth session ready - using cached credentials")
                        live.update(Panel(
                            f"[green]✅ OAuth credentials cached until {self.credentials.expires_at}[/green]",
                            title="Authentication",
                            border_style="green"
                        ))
                    else:
                        progress.step("Performing fresh OAuth authentication...")
                        live.update(Panel(
                            "[yellow]🔑 Performing fresh OAuth authentication...[/yellow]",
                            title="Authentication",
                            border_style="yellow"
                        ))

                        self.credentials = await self.auth_broker.get_authenticated_credentials(
                            provider="authkit",
                            force_refresh=True
                        )

                        progress.complete("OAuth authentication complete")
                        live.update(Panel(
                            "[green]✅ Fresh OAuth credentials acquired[/green]",
                            title="Authentication",
                            border_style="green"
                        ))

                # Brief pause to show success
                await asyncio.sleep(1)

            except Exception as e:
                live.update(Panel(
                    f"[red]❌ OAuth setup failed: {e}[/red]",
                    title="Authentication Error",
                    border_style="red"
                ))
                await asyncio.sleep(2)
                raise

    async def run_dashboard(self):
        """Run the main test dashboard."""
        if not self.credentials:
            self.console.print("[red]❌ No OAuth credentials available[/red]")
            return

        while True:
            # Clear screen and show dashboard
            self.console.clear()

            # Create dashboard layout
            dashboard = self.create_dashboard_layout()
            self.console.print(dashboard)

            # Show menu options
            self.console.print("\n[bold cyan]Test Options:[/bold cyan]")
            self.console.print("[1] Run all tests")
            self.console.print("[2] Run unit tests only")
            self.console.print("[3] Run integration tests only")
            self.console.print("[4] Test specific tool")
            self.console.print("[5] Run custom filter")
            self.console.print("[6] Show OAuth status")
            self.console.print("[q] Quit")

            # Get user choice
            choice = input("\n👉 Choose option: ").strip().lower()

            if choice == 'q':
                break
            elif choice == '1':
                await self.run_all_tests()
            elif choice == '2':
                await self.run_unit_tests()
            elif choice == '3':
                await self.run_integration_tests()
            elif choice == '4':
                await self.test_specific_tool()
            elif choice == '5':
                await self.run_custom_filter()
            elif choice == '6':
                await self.show_oauth_status()
            else:
                self.console.print("[red]Invalid option. Press Enter to continue.[/red]")
                input()
    
    def create_dashboard_layout(self) -> Panel:
        """Create the main dashboard layout."""
        # OAuth Status Section
        oauth_status = self.get_oauth_status_display()
        
        # Test Results Section
        test_results = self.get_test_results_display()
        
        # Combine sections
        content = f"""{oauth_status}

{test_results}"""
        
        return Panel(
            content,
            title="[bold green]🧪 TDD Test Dashboard with Session OAuth[/bold green]",
            border_style="green"
        )
    
    def get_oauth_status_display(self) -> str:
        """Get OAuth status display string."""
        if not self.credentials:
            return "[red]❌ No OAuth credentials[/red]"
        
        status_color = "green" if self.credentials.is_valid() else "red"
        status_icon = "✅" if self.credentials.is_valid() else "❌"
        
        return f"""[bold]{status_icon} OAuth Status[/bold]
Provider: [{status_color}]{self.credentials.provider}[/{status_color}]
Expires: [{status_color}]{self.credentials.expires_at}[/{status_color}]
User ID: [cyan]{self.credentials.user_id or 'Unknown'}[/cyan]"""
    
    def get_test_results_display(self) -> str:
        """Get test results display string."""
        if not self.test_results:
            return "[dim]No tests run yet[/dim]"
        
        # Show last few test results
        recent_results = self.test_results[-5:]
        result_lines = []
        
        for result in recent_results:
            status_icon = "✅" if result.get("passed", False) else "❌"
            test_name = result.get("name", "Unknown")
            duration = result.get("duration", 0)
            result_lines.append(f"{status_icon} {test_name} ({duration:.2f}s)")
        
        return "\n".join(["[bold]📊 Recent Test Results[/bold]"] + result_lines)
    
    async def run_all_tests(self):
        """Run all tests with progress display."""
        await self.run_pytest_with_progress(["tests/", "-v"], "Running all tests...")
    
    async def run_unit_tests(self):
        """Run unit tests only."""
        await self.run_pytest_with_progress(
            ["tests/unit/", "-m", "unit", "-v"], 
            "Running unit tests..."
        )
    
    async def run_integration_tests(self):
        """Run integration tests only."""
        await self.run_pytest_with_progress(
            ["tests/integration/", "-m", "integration", "-v"],
            "Running integration tests..."
        )
    
    async def test_specific_tool(self):
        """Test a specific tool."""
        tool_name = input("\n🔧 Enter tool name (e.g., workspace, entity): ").strip()
        if not tool_name:
            return
        
        test_paths = [
            f"tests/unit/tools/test_{tool_name}_tool.py",
            f"tests/integration/test_{tool_name}_integration.py"
        ]
        
        existing_paths = [p for p in test_paths if Path(p).exists()]
        
        if not existing_paths:
            self.console.print(f"[red]❌ No tests found for tool: {tool_name}[/red]")
            input("Press Enter to continue...")
            return
        
        await self.run_pytest_with_progress(
            existing_paths + ["-v"],
            f"Testing {tool_name} tool..."
        )
    
    async def run_custom_filter(self):
        """Run tests with custom filter."""
        filter_expr = input("\n🔍 Enter test filter (pytest -k expression): ").strip()
        if not filter_expr:
            return
        
        await self.run_pytest_with_progress(
            ["tests/", "-k", filter_expr, "-v"],
            f"Running tests matching: {filter_expr}"
        )
    
    async def show_oauth_status(self):
        """Show detailed OAuth status."""
        if not self.credentials:
            self.console.print("[red]❌ No OAuth credentials available[/red]")
            return
        
        # Refresh credentials status
        await self.auth_broker._load_cached_credentials()
        
        status_table = Table(title="OAuth Credential Details")
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")
        
        status_table.add_row("Provider", self.credentials.provider)
        status_table.add_row("Token (last 8 chars)", f"...{self.credentials.access_token[-8:]}")
        status_table.add_row("Valid", "✅ Yes" if self.credentials.is_valid() else "❌ No")
        status_table.add_row("Expires At", str(self.credentials.expires_at))
        status_table.add_row("Base URL", self.credentials.base_url)
        status_table.add_row("User ID", self.credentials.user_id or "Unknown")
        
        self.console.print(status_table)
        input("\nPress Enter to continue...")
    
    async def run_pytest_with_progress(self, pytest_args: List[str], description: str):
        """Run pytest with rich progress display."""
        cmd = ["python", "-m", "pytest"] + pytest_args
        
        self.console.print(f"\n[bold green]{description}[/bold green]")
        self.console.print(f"Command: [cyan]{' '.join(cmd)}[/cyan]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task(description, total=None)
            
            # Run pytest
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=Path(__file__).parent.parent.parent
            )
            
            output_lines = []
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                
                line_str = line.decode().strip()
                if line_str:
                    output_lines.append(line_str)
                    # Update progress with current test
                    if "::" in line_str and ("PASSED" in line_str or "FAILED" in line_str):
                        test_name = line_str.split("::")[1].split(" ")[0]
                        progress.update(task, description=f"Running: {test_name}")
            
            await process.wait()
            
            # Show results
            success = process.returncode == 0
            result_color = "green" if success else "red"
            result_icon = "✅" if success else "❌"
            
            progress.update(task, description=f"{result_icon} {'Passed' if success else 'Failed'}")
            
            # Store result
            self.test_results.append({
                "name": description,
                "passed": success,
                "duration": 0,  # Could calculate from timestamps
                "timestamp": datetime.now()
            })
        
        # Show summary
        self.console.print(f"\n[{result_color}]{result_icon} Test run {'completed successfully' if success else 'failed'}[/{result_color}]")
        
        # Show last few lines of output
        if output_lines:
            self.console.print("\n[bold]Last few lines of output:[/bold]")
            for line in output_lines[-10:]:
                self.console.print(f"  {line}")
        
        input("\nPress Enter to continue...")


async def run_tdd_dashboard(auth_broker: AuthSessionBroker):
    """Run the TDD test dashboard."""
    dashboard = TDDTestDashboard(auth_broker)
    await dashboard.setup_and_run()
