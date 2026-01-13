# 🎥 Multi-Agent AI System for Multimedia Content Analysis

## Overview
This project is a multi-agent AI system that automatically analyzes and interprets video and audio content. The system decomposes complex processing tasks into specialized agents responsible for transcription, summarization, explanation of complex concepts, contextual web search, and reflective question generation. By distributing responsibilities across specialized agents, the system improves clarity, accuracy, and user engagement compared to monolithic AI approaches.

---

## Features
- Automatic audio and video transcription
- Content summarization
- Explanation of complex concepts with contextual web search
- Reflective and comprehension-based question generation
- Modular and extensible multi-agent architecture

---

## System Architecture
The system follows a modular multi-agent design coordinated by a central planner agent.

Agents:
- Planner Agent – Orchestrates tasks, downloads media, and performs transcription
- Summarizer Agent – Generates concise summaries of the content
- Explainer Agent – Explains complex concepts and retrieves additional context from the web
- Question Generation Agent – Produces reflective and comprehension-driven questions

Architecture and workflow diagrams:
- Untitled Diagram.drawio.png
- workflow.png

---

## Project Structure
project-root/
│── workflow/
│   ├── downloads/        # Downloaded audio and video files
│   ├── agents/           # Agent implementations
│   └── tools/            # Download, Transcribe, and Search tools
│── src/                  # Core application logic
│── requirements.txt      # Python dependencies
│── main.py               # Application entry point
│── README.md             # Project documentation

---

## Requirements
- Python 3.9 or higher
- Git
- pip (Python package manager)
- Internet connection (required for downloads and web search)

---

## Installation
### Clone the repository:
git clone https://github.com/your-username/multi-agent-multimedia-ai.git
cd multi-agent-multimedia-ai

### Create a virtual environment (recommended):
python -m venv venv

### Activate the virtual environment:
#### Windows:
venv\Scripts\activate

#### macOS / Linux:
source venv/bin/activate

### Install dependencies:
pip install -r requirements.txt

---

## Usage
Run the application:
python main.py

Analyze a video or audio file:
1. Place the media file inside the workflow/downloads/ directory
2. Provide the file path as input when prompted
3. The system will transcribe the content, summarize key ideas, explain complex concepts, and generate reflective questions (optional)

---

## Example Query
What is the video ./workflow/downloads/video.mp4 about?

---

## Example Output
- Transcribed content
- High-level summary
- Explanation of key themes
- Reflective learning questions

---

## Notes
- Supported formats include .mp4, .mp3, and .wav
- Internet access is required for contextual web search
- Each agent can be extended or replaced independently

---

## Future Improvements
- Web-based user interface
- Real-time streaming analysis
- Multilingual transcription support
- Improved agent collaboration and memory

---

## License
MIT License

---

## Author
Elijah Achala  
Aspiring Data Analyst & AI Engineer
