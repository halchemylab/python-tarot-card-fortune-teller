# python-tarot-card-fortune-teller

A terminal-based Tarot card fortune teller powered by OpenAI's GPT API. Draws cards, asks focus questions, and provides fun, insightful readings.

## Features
- Draws 3 random Tarot cards from the 22 Major Arcana
- Offers random focus questions or lets you enter your own
- Uses OpenAI GPT (via API key) to generate concise, supportive Tarot readings
- Rich, immersive terminal experience with progress messages and styled output
- Logs all readings to a CSV file
- View your complete reading history with pagination
- Search your reading history by date, question, or card
- Display a frequency table of drawn cards with an ASCII bar chart
- Clear your reading history

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
1.  **Get a new tarot reading:** Guides you through selecting a question and receiving a new reading.
2.  **View your reading history:** Browse your past readings with pagination.
3.  **Search your reading history:** Search for specific readings by date, keywords in a question, or by a card that was drawn.
4.  **Show card frequency table:** See how many times each card has been drawn.
5.  **Clear your reading history:** Permanently delete all your saved readings.
6.  **Exit:** Close the application.


All readings are saved to `tarot_readings_log.csv`.

## Requirements
- Python 3.7+
- openai
- python-dotenv
- rich

## Example Output
```
Welcome to the Terminal Tarot Reading App!

1. Get a new tarot reading
2. View your reading history
3. Search your reading history
4. Show card frequency table
5. Clear your reading history
6. Exit
Please enter your choice: 1

Please choose one of the following focuses:
1. What's the general energy around me right now?
2. What positive transformation is on its way to me?
3. How can I embrace change in my life?
4. Enter your own question

Enter the number of your choice (1-4): 4
Please type your personalized question: What should I focus on this week?

Drawing 3 cards...
- The Fool
- The Tower
- The Sun

Interpreting the cards...
Consulting the spirits...

Your Tarot Reading:
You are entering a period of transformation. The Fool and The Tower suggest a sudden change, but The Sun promises a positive outcome. Embrace new beginnings with optimism.
```

## License
This project is licensed under the MIT License.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that the original copyright notice and this permission notice are included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Copyright (c) 2025 halchemylab
