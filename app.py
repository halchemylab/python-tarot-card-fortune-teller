import random
import os
import openai
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markup import escape

# Import new classes and config
from config import questions, ORIGINAL_PROGRESS_PAIRS
from deck import TarotDeck
from history import HistoryManager

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class App:
    """The main application class for the Tarot Reading App."""
    def __init__(self):
        self.console = Console()
        self.deck = TarotDeck()
        self.history_manager = HistoryManager()
        self.progress_pairs = ORIGINAL_PROGRESS_PAIRS.copy()

    def _get_progress_pair(self):
        """Return a random progress pair and reset the list when all have been used."""
        if not self.progress_pairs:
            self.progress_pairs = ORIGINAL_PROGRESS_PAIRS.copy()
        pair = random.choice(self.progress_pairs)
        self.progress_pairs.remove(pair)
        return pair

    def _get_reading(self, question, cards):
        """Generate a tarot reading using the OpenAI API."""
        prompt = (
            f"I have drawn the following tarot cards: {', '.join(cards)}. "
            f"The focus question is: '{question}'. "
            "Please provide a fun, insightful, and easy-to-understand tarot reading that interprets these cards."
        )
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a tarot card reader that provides supportive, concise, and easy-to-understand readings. Focus specifically on answering the user's question using the symbolism of the drawn cards. Provide interpretations that are both meaningful and practical. In 3 sentences or less."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating reading: {e}"

    def _perform_new_reading(self):
        """Guides the user through getting a new tarot reading."""
        sample_questions = random.sample(questions, 3)
        self.console.print("\n[bold]Please choose one of the following focuses:[/bold]")
        for idx, q in enumerate(sample_questions, start=1):
            self.console.print(f"[cyan]{idx}[/cyan]. {escape(q)}")
        self.console.print("[cyan]4[/cyan]. Enter your own question")
        
        user_choice = Prompt.ask("Enter the number of your choice", choices=["1", "2", "3", "4"], default="1")
        
        if user_choice in ["1", "2", "3"]:
            selected_question = sample_questions[int(user_choice)-1]
        elif user_choice == "4":
            selected_question = Prompt.ask("[bold]Please type your personalized question[/bold]").strip()
            # Add validation for the custom question
            if not selected_question or len(selected_question) < 10 or len(selected_question.split()) < 2:
                self.console.print("[red]Your question seems too short or may not be a valid question. Please provide a more detailed question.[/red]")
                Prompt.ask("\nPress Enter to return to the main menu...")
                return

        drawn_cards = self.deck.draw_cards(3)
        self.console.print("\n[bold yellow]Drawing 3 cards...[/bold yellow]")
        with self.console.status("[italic green]Drawing cards...[/italic green]"):
            for card in drawn_cards:
                self.console.print(f"- [bold]{escape(card)}[/bold]")
                time.sleep(1)

        time.sleep(2)

        interpret_msg, consult_msg = self._get_progress_pair()
        with self.console.status(f"[italic green]{escape(interpret_msg)}[/italic green]"):
            time.sleep(2)
        with self.console.status(f"[italic green]{escape(consult_msg)}[/italic green]"):
            time.sleep(2)

        with self.console.status("[bold green]Generating your reading...[/bold green]"):
            reading = self._get_reading(selected_question, drawn_cards)
        
        self.console.print(Panel(escape(reading), title="[bold blue]Your Tarot Reading[/bold blue]", border_style="blue", padding=(1, 1)))

        self.history_manager.log_reading(selected_question, drawn_cards, reading)
        Prompt.ask("\nPress Enter to return to the main menu...")

    def run(self):
        """The main loop of the application."""
        while True:
            self.console.print(Panel.fit(
                "[bold magenta]Welcome to the Terminal Tarot Reading App![/bold magenta]",
                padding=(1, 2)
            ))
            self.console.print("1. Get a new tarot reading")
            self.console.print("2. View your reading history")
            self.console.print("3. Search your reading history")
            self.console.print("4. Show card frequency table")
            self.console.print("5. Clear your reading history")
            self.console.print("6. Exit")
            choice = Prompt.ask("Please enter your choice", choices=["1", "2", "3", "4", "5", "6"], default="1")

            if choice == '1':
                self._perform_new_reading()
            elif choice == '2':
                self.history_manager.view_history()
            elif choice == '3':
                self.history_manager.search_history()
            elif choice == '4':
                self.history_manager.show_card_frequency()
            elif choice == '5':
                self.history_manager.clear_history()
            elif choice == '6':
                self.console.print("[bold magenta]Thank you for using the Terminal Tarot Reading App.[/bold magenta]")
                break

if __name__ == "__main__":
    app = App()
    app.run()
