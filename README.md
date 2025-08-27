# python-tarot-card-fortune-teller

A terminal-based Tarot card fortune teller powered by OpenAI's GPT API. Draws cards, asks focus questions, and provides fun, insightful readings.

## Features
- Draws 3 random Tarot cards from the 22 Major Arcana
- Offers 3 random focus questions per reading
- Uses OpenAI GPT (via API key) to generate concise, supportive Tarot readings
- Progress messages for immersive experience
- Logs all readings to a CSV file with timestamp

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

Follow the prompts to select a focus question and receive your Tarot reading. All readings are saved to `tarot_readings_log.csv`.

## Requirements
- Python 3.7+
- openai
- python-dotenv

## Example Output
```
Welcome to the Terminal Tarot Reading App!

Please choose one of the following focuses:
1. What's the general energy around me right now?
2. What positive transformation is on its way to me?
3. How can I embrace change in my life?

Enter the number of your choice (1-3): 2

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
MIT