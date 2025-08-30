import os
import csv
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markup import escape

class HistoryManager:
    """Manages the reading history stored in a CSV file."""
    def __init__(self, file_path="tarot_readings_log.csv"):
        self.file_path = file_path
        self.console = Console()

    def log_reading(self, question, cards, reading):
        """Logs a single tarot reading to the CSV file."""
        file_exists = os.path.isfile(self.file_path)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.file_path, mode="a", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["datetime", "question", "cards", "reading"])
                writer.writerow([now, question, ", ".join(cards), reading])
        except IOError as e:
            self.console.print(f"[red]Error saving reading: {escape(str(e))}[/red]")

    def view_history(self):
        """Displays the tarot reading history from the log file with pagination."""
        if not os.path.isfile(self.file_path):
            self.console.print("\n[yellow]No reading history found.[/yellow]")
            Prompt.ask("\nPress Enter to return to the main menu...")
            return

        self.console.print(Panel.fit("[bold magenta]--- Your Reading History ---[/bold magenta]", padding=(1, 2)))
        try:
            with open(self.file_path, mode="r", newline='', encoding="utf-8") as f:
                reader = csv.reader(f)
                try:
                    header = next(reader)
                except StopIteration:
                    self.console.print("[yellow]Your history is empty.[/yellow]")
                    Prompt.ask("\nPress Enter to return to the main menu...")
                    return

                readings = list(reader)
                if not readings:
                    self.console.print("[yellow]Your history is empty.[/yellow]")
                    Prompt.ask("\nPress Enter to return to the main menu...")
                    return
                
                page_size = 5
                page_number = 0
                reversed_readings = list(reversed(readings))
                total_pages = (len(reversed_readings) + page_size - 1) // page_size

                while True:
                    self.console.print(f"\n[bold]Page {page_number + 1} of {total_pages}[/bold]")
                    start_index = page_number * page_size
                    end_index = start_index + page_size
                    page_readings = reversed_readings[start_index:end_index]

                    for row in page_readings:
                        self.console.print(f"\n[bold]Date:[/bold] {escape(row[0])}")
                        self.console.print(f"[bold]Question:[/bold] {escape(row[1])}")
                        self.console.print(f"[bold]Cards:[/bold] [yellow]{escape(row[2])}[/yellow]")
                        self.console.print(f"[bold]Reading:[/bold] {escape(row[3])}")
                        self.console.print("-" * 20)

                    if total_pages <= 1:
                        break

                    nav_choices = []
                    prompt_text = "[bold]Enter 'q' to quit history view"
                    if page_number > 0:
                        nav_choices.append("p")
                        prompt_text += ", 'p' for previous"
                    if page_number < total_pages - 1:
                        nav_choices.append("n")
                        prompt_text += ", 'n' for next"
                    nav_choices.append("q")
                    prompt_text += "[/bold]"
                    
                    nav_choice = Prompt.ask(prompt_text, choices=nav_choices)

                    if nav_choice == 'n':
                        page_number += 1
                    elif nav_choice == 'p':
                        page_number -= 1
                    elif nav_choice == 'q':
                        break

        except Exception as e:
            self.console.print(f"[red]Error reading history: {escape(str(e))}[/red]")
        
        Prompt.ask("\nPress Enter to return to the main menu...")

    def clear_history(self):
        """Deletes the tarot reading history log file after confirmation."""
        if not os.path.isfile(self.file_path):
            self.console.print("\n[yellow]No reading history found. Nothing to clear.[/yellow]")
            Prompt.ask("\nPress Enter to return to the main menu...")
            return

        self.console.print("\n[bold red]This will permanently delete your entire reading history.[/bold red]")
        confirm = Prompt.ask("Are you sure you want to continue?", choices=["y", "n"], default="n")

        if confirm == 'y':
            try:
                os.remove(self.file_path)
                self.console.print("\n[green]Reading history has been cleared.[/green]")
            except Exception as e:
                self.console.print(f"\n[red]Error clearing history: {escape(str(e))}[/red]")
        else:
            self.console.print("\nHistory clearing cancelled.")
        
        Prompt.ask("\nPress Enter to return to the main menu...")
