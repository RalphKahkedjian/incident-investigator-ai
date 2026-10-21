from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from rich.table import Table
from rich.text import Text
from rich.markup import escape

from agent import agent

console = Console()

def display_report(report):
    console.print()

    console.print(
        Panel(
            "[bold green]Investigation Completed[/bold green]",
            title="INCIDENT INVESTIGATOR AI",
            border_style="green"
        )
    )

    console.print(
        Panel(
            Text(report.problem),
            title="[bold cyan]Problem[/bold cyan]",
            border_style="cyan"
        )
    )

    console.print(
        Panel(
            Text(report.root_cause),
            title="[bold red]Root Cause[/bold red]",
            border_style="red"
        )
    )

    details = Table(title="Investigation Details", show_header=False)
    details.add_column("Field", style="bold cyan")
    details.add_column("Value")

    confidence_color = {
        "low": "red",
        "medium": "yellow",
        "high": "green"
    }.get(report.confidence, "white")

    details.add_row(
        "Confidence",
        f"[{confidence_color}]{escape(report.confidence.upper())}[/{confidence_color}]"
    )

    details.add_row(
        "Suspected Commit",
        escape(report.suspected_commit or "Not identified")
    )

    details.add_row(
        "Affected Files",
        Text("\n".join(report.affected_files))
    )

    console.print(details)

    evidence_text = Text()

    for index, item in enumerate(report.evidence, start=1):
        evidence_text.append(f"{index}. {item}\n\n")

    console.print(
        Panel(
            evidence_text,
            title="[bold yellow]Evidence[/bold yellow]",
            border_style="yellow"
        )
    )

    # Suggested fix
    console.print(
        Panel(
            Text(report.suggested_fix),
            title="[bold green]Suggested Fix[/bold green]",
            border_style="green"
        )
    )


def main():
    console.print(
        Panel(
            "[bold cyan]INCIDENT INVESTIGATOR AI[/bold cyan]",
            subtitle="AI-Powered Root Cause Analysis",
            border_style="cyan"
        )
    )

    user_query = Prompt.ask(
        "[bold green]What would you like to investigate?[/bold green]"
    )

    with console.status(
        "[bold cyan]Gemini is investigating...[/bold cyan]",
        spinner="dots"
    ):

            
        messages = [
            {"role": "user", "content": user_query}
        ]

        report = None

        console.print("\n[bold cyan]Investigation started...[/bold cyan]\n")

        try:
            for event in agent.stream(
                {"messages": messages},
                stream_mode=["updates", "values"]
            ):
                mode, data = event

                if mode == "updates":
                    for node_name, update in data.items():
                        if not isinstance(update, dict):
                            continue

                        for message in update.get("messages", []):
                            if getattr(message, "tool_calls", None):
                                for call in message.tool_calls:
                                    console.print(
                                        f"[cyan]→ Tool requested:[/cyan] {call['name']}"
                                    )

                            if message.type == "tool":
                                console.print(
                                    f"[green]✓ Tool finished:[/green] {message.name}"
                                )

                elif mode == "values":
                    report = data.get("structured_response") or report

            if report is not None:
                display_report(report)
            else:
                console.print("[red]No structured report was returned.[/red]")

        except Exception as error:
            console.print(
                f"\n[bold red]Investigation failed:[/bold red] {error}"
            )
            return



if __name__ == "__main__":
    main()