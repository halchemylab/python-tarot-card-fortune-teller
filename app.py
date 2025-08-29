import random
import os
import openai
import time
import csv
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markup import escape

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key here or ensure it's set as the environment variable "OPENAI_API_KEY"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Rich Console
console = Console()

# List of tarot cards (using the 22 major arcana for simplicity)
tarot_cards = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
]

# List of 10 potential focus questions
questions = [
    "What's the general energy around me right now?",
    "What's a good area for personal growth?",
    "What positive transformation is on its way to me?",
    "How can I embrace change in my life?",
    "What should I focus on to improve my relationships?",
    "What guidance do the cards have for my career?",
    "How can I better connect with my intuition?",
    "What steps can I take for personal healing?",
    "What is something exciting coming my way?",
    "How can I best prepare for the future?"
]

# List of 10 progress-message pairs (interpreting, consulting)
ORIGINAL_PROGRESS_PAIRS = [
    ("Interpreting the cards...", "Consulting the spirits..."),
    ("Decoding the cosmic signals...", "Channeling ancient wisdom..."),
    ("Reading the energies...", "Aligning with the universe..."),
    ("Analyzing the symbols...", "Awakening hidden insights..."),
    ("Unraveling the mysteries...", "Summoning ethereal guidance..."),
    ("Connecting the dots...", "Listening to the cosmic hum..."),
    ("Exploring card meanings...", "Drawing on universal energy..."),
    ("Unlocking the secrets...", "Manifesting clarity..."),
    ("Sifting through symbolism...", "Hearing whispers from beyond..."),
    ("Distilling cosmic clues...", "Embracing celestial messages...")
]
# Create a mutable copy that we will draw from
progress_pairs = ORIGINAL_PROGRESS_PAIRS.copy()

def get_progress_pair():
    """Return a random progress pair and remove it from the global list.
        Reset the list when all pairs have been used."""
    global progress_pairs
    if not progress_pairs:
        progress_pairs = ORIGINAL_PROGRESS_PAIRS.copy()
    pair = random.choice(progress_pairs)
    progress_pairs.remove(pair)
    return pair

def get_reading(question, cards):
    """
    Call the OpenAI API to generate a tarot reading based on the selected question and drawn cards.
    """
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
        reading = response.choices[0].message.content.strip()
    except Exception as e:
        reading = f"Error generating reading: {e}"
    return reading

def view_history():
    """Displays the tarot reading history from the log file."""
    csv_file = "tarot_readings_log.csv"
    if not os.path.isfile(csv_file):
        console.print("\n[yellow]No reading history found.[/yellow]")
        Prompt.ask("\nPress Enter to return to the main menu...")
        return

    console.print(Panel.fit("[bold magenta]--- Your Reading History ---[/bold magenta]", padding=(1, 2)))
    try:
        with open(csv_file, mode="r", newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)  # Check for header
            except StopIteration:
                console.print("[yellow]Your history is empty.[/yellow]")
                Prompt.ask("\nPress Enter to return to the main menu...")
                return

            readings = list(reader)
            if not readings:
                console.print("[yellow]Your history is empty.[/yellow]")
                Prompt.ask("\nPress Enter to return to the main menu...")
                return
            
            # Display readings in reverse chronological order
            for row in reversed(readings):
                console.print(f"\n[bold]Date:[/bold] {escape(row[0])}")
                console.print(f"[bold]Question:[/bold] {escape(row[1])}")
                console.print(f"[bold]Cards:[/bold] [yellow]{escape(row[2])}[/yellow]")
                console.print(f"[bold]Reading:[/bold] {escape(row[3])}")
                console.print("-" * 20)

    except Exception as e:
        console.print(f"[red]Error reading history: {escape(str(e))}[/red]")
    
    Prompt.ask("\nPress Enter to return to the main menu...")

def main():
    while True:
        console.print(Panel.fit(
            "[bold magenta]Welcome to the Terminal Tarot Reading App![/bold magenta]",
            padding=(1, 2)
        ))
        console.print("1. Get a new tarot reading")
        console.print("2. View your reading history")
        console.print("3. Exit")
        choice = Prompt.ask("Please enter your choice", choices=["1", "2", "3"], default="1")

        if choice == '1':
            # Randomly select 3 questions from the list of 10
            sample_questions = random.sample(questions, 3)
            console.print("\n[bold]Please choose one of the following focuses:[/bold]")
            for idx, q in enumerate(sample_questions, start=1):
                console.print(f"[cyan]{idx}[/cyan]. {escape(q)}")
            console.print("[cyan]4[/cyan]. Enter your own question")
            
            user_choice = Prompt.ask("Enter the number of your choice", choices=["1", "2", "3", "4"], default="1")
            
            if user_choice in ["1", "2", "3"]:
                selected_question = sample_questions[int(user_choice)-1]
            elif user_choice == "4":
                selected_question = Prompt.ask("[bold]Please type your personalized question[/bold]").strip()
                if not selected_question:
                    console.print("[red]You must enter a question. Returning to main menu.[/red]")
                    continue
            
            # Draw 3 random tarot cards with pauses between each card
            drawn_cards = random.sample(tarot_cards, 3)
            console.print("\n[bold yellow]Drawing 3 cards...[/bold yellow]")
            with console.status("[italic green]Drawing cards...[/italic green]"):
                for card in drawn_cards:
                    console.print(f"- [bold]{escape(card)}[/bold]")
                    time.sleep(1)

            time.sleep(2)

            # Pick a progress pair randomly
            interpret_msg, consult_msg = get_progress_pair()
            with console.status(f"[italic green]{escape(interpret_msg)}[/italic green]"):
                time.sleep(2)
            with console.status(f"[italic green]{escape(consult_msg)}[/italic green]"):
                time.sleep(2)

            # Get the tarot reading from OpenAI
            with console.status("[bold green]Generating your reading...[/bold green]"):
                reading = get_reading(selected_question, drawn_cards)
            
            console.print(Panel(escape(reading), title="[bold blue]Your Tarot Reading[/bold blue]", border_style="blue", padding=(1, 1)))

            # Save the result to a CSV file
            csv_file = "tarot_readings_log.csv"
            file_exists = os.path.isfile(csv_file)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(csv_file, mode="a", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["datetime", "question", "cards", "reading"])
                writer.writerow([
                    now,
                    selected_question,
                    ", ".join(drawn_cards),
                    reading
                ])
            Prompt.ask("\nPress Enter to return to the main menu...")

        elif choice == '2':
            view_history()
        
        elif choice == '3':
            console.print("[bold magenta]Thank you for using the Terminal Tarot Reading App.[/bold magenta]")
            break

if __name__ == "__main__":
    main()