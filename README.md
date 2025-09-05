# python-tarot-card-fortune-teller

A terminal-based Tarot card fortune teller powered by OpenAI's GPT API. Draws cards, asks focus questions, and provides fun, insightful readings. This project leverages a modular architecture, with distinct components for handling the user interface, tarot deck, and reading history, all configurable via the `config.py` file.

## Features
- **NEW:** Get a "Card of the Day" reading for quick, daily insight.
- Draws 3 random Tarot cards from the 22 Major Arcana for a full reading.
- Offers a dynamic selection of random focus questions or lets you enter your own.
- Uses OpenAI GPT (via API key) to generate concise, supportive Tarot readings.
- Rich, immersive terminal experience with progress messages and styled output.
- Logs all readings to a CSV file for easy access and analysis.
- View your complete reading history with easy-to-navigate pagination.
- Search your reading history by date, a keyword in a question, or by a specific card.
- Display a frequency table of drawn cards with an ASCII bar chart to visualize your most-drawn cards.
- Clear your reading history to start fresh.

## Setup
1. **Clone the repository**
2. **Install dependencies**
	```bash
	pip install -r requirements.txt
	```
3. **Set up your environment variables**
	- Copy `.env.example` to `.env` and add your OpenAI API key:
	  ```env
	  OPENAI_API_KEY=your_openai_api_key_here
	  ```

## Usage
Run the app in your terminal:
```bash
python app.py
```

You will be presented with a main menu to guide you through the available actions:
1.  **Get a Card of the Day:** Draws a single card for daily guidance.
2.  **Get a new tarot reading:** Guides you through selecting a question and receiving a new 3-card reading.
3.  **View your reading history:** Browse your past readings with pagination.
4.  **Search your reading history:** Search for specific readings by date, keywords in a question, or by a card that was drawn.
5.  **Show card frequency table:** See how many times each card has been drawn.
6.  **Clear your reading history:** Permanently delete all your saved readings.
7.  **Exit:** Close the application.


All readings are saved to `tarot_readings_log.csv`.

## Requirements
- Python 3.7+
- openai
- python-dotenv
- rich

## Example Output
```
Welcome to the Terminal Tarot Reading App!

1. Get a Card of the Day
2. Get a new tarot reading
3. View your reading history
4. Search your reading history
5. Show card frequency table
6. Clear your reading history
7. Exit
Please enter your choice: 1

Drawing your card of the day...
- The Empress

Generating your reading...

Your Card of the Day:
Today, The Empress encourages you to connect with your creativity and abundance. Nurture your ideas and relationships, and enjoy the beauty that surrounds you.

Press Enter to return to the main menu...
```

## License
This project is licensed under the MIT License.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that the original copyright notice and this permission notice are included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Copyright (c) 2025 halchemylab
