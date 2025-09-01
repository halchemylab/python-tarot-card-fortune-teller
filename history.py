import os
import csv
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markup import escape

class HistoryManager:
    def show_card_frequency(self):
        """Displays a table and ASCII bar chart of tarot card draw frequencies."""
        if not os.path.isfile(self.file_path):
            self.console.print("\n[yellow]No reading history found.[/yellow]")
            Prompt.ask("\nPress Enter to return to the main menu...")
            return

        from collections import Counter

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

                all_cards = []
                for row in readings:
                    cards = [c.strip() for c in row[2].split(",") if c.strip()]
                    all_cards.extend(cards)
                if not all_cards:
                    self.console.print("[yellow]No cards found in history.[/yellow]")
                    Prompt.ask("\nPress Enter to return to the main menu...")
                    return

                freq = Counter(all_cards)
                sorted_cards = freq.most_common()
                max_card_len = max(len(card) for card, _ in sorted_cards)
                max_count = max(count for _, count in sorted_cards)
                bar_width = 30

                self.console.print(Panel.fit("[bold magenta]--- Card Frequency Table ---[/bold magenta]", padding=(1, 2)))
                self.console.print(f"{'Card'.ljust(max_card_len)} | Count | Bar")
                self.console.print("-" * (max_card_len + 18))
                for card, count in sorted_cards:
                    bar = '#' * int((count / max_count) * bar_width)
                    self.console.print(f"{card.ljust(max_card_len)} | {str(count).rjust(5)} | {bar}")
        except Exception as e:
            self.console.print(f"[red]Error displaying card frequency: {escape(str(e))}[/red]")
        Prompt.ask("\nPress Enter to return to the main menu...")
    def search_history(self):
        """Allows the user to search/filter tarot reading history by date, question, or card."""
        if not os.path.isfile(self.file_path):
            self.console.print("\n[yellow]No reading history found.[/yellow]")
            Prompt.ask("\nPress Enter to return to the main menu...")
            return

        self.console.print(Panel.fit("[bold magenta]--- Search Your Reading History ---[/bold magenta]", padding=(1, 2)))
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

                # Prompt for filter type
                filter_type = Prompt.ask(
                    "How would you like to search?",
                    choices=["date", "question", "card", "all", "cancel"],
                    default="date"
                )
                if filter_type == "cancel":
                    return

                filtered = readings
                if filter_type == "date":
                    date_str = Prompt.ask("Enter date (YYYY-MM-DD) or part of date (e.g. 2025-08)").strip()
                    filtered = [r for r in readings if date_str in r[0]]
                elif filter_type == "question":
                    q_str = Prompt.ask("Enter keyword or phrase from your question").strip().lower()
                    filtered = [r for r in readings if q_str in r[1].lower()]
                elif filter_type == "card":
                    card_str = Prompt.ask("Enter card name or part of card name").strip().lower()
                    filtered = [r for r in readings if card_str in r[2].lower()]
                elif filter_type == "all":
                    # Show all readings
                    pass

                if not filtered:
                    self.console.print("[yellow]No readings found for your search.[/yellow]")
                else:
                    self.console.print(f"[green]Found {len(filtered)} matching readings:[/green]")
                    for row in filtered:
                        self.console.print(f"\n[bold]Date:[/bold] {escape(row[0])}")
                        self.console.print(f"[bold]Question:[/bold] {escape(row[1])}")
                        self.console.print(f"[bold]Cards:[/bold] [yellow]{escape(row[2])}[/yellow]")
                        self.console.print(f"[bold]Reading:[/bold] {escape(row[3])}")
                        self.console.print("-" * 20)
        except Exception as e:
            self.console.print(f"[red]Error searching history: {escape(str(e))}[/red]")
        Prompt.ask("\nPress Enter to return to the main menu...")
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
