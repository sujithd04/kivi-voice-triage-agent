# Kivi Voice Feedback Triage Agent 🎙️

An agentic workflow built for the Sarvam Campus Connect Hackathon. Users speak app feedback in Hindi or Hinglish, and the agent turns it into clean, deduplicated bug tickets and confirms back by voice.

## Features
* Transcribes Hindi/Hinglish voice notes with Sarvam Saaras.
* Extracts a structured ticket (title, category, severity, summary) using Sarvam-105B.
* Detects duplicate reports and merges them into one ticket with a report count.
* Writes a prioritised backlog to `tickets.md` and replies by voice with Bulbul.

## Pipeline
Audio → Saaras (transcribe) → Sarvam-105B (extract JSON) → Sarvam-105B (dedupe) → tickets.md + Bulbul voice reply

## Setup Steps
1. Clone this repository: `git clone <your-repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a file named `.env` containing `SARVAM_API_KEY=your_key_here` (never commit it).
4. Run the application: `python agent.py`

## Notes
* Sample audio files `feedback_1.wav` to `feedback_4.wav` are included. Files 1 and 2 are intentional duplicates, so 4 recordings produce 3 tickets.
* If the API key is missing or out of quota, the agent runs in an offline demo mode with simulated responses.
