# 🎬 AI YouTube Toolkit

Auto-generate SEO-optimized YouTube titles, descriptions, and tags using the OpenAI API.

Built by [osiris379](https://github.com/osiris379) · Part of the **Building AI Tools** series on [YouTube](https://youtube.com/@osiris379)

---

## ✨ What It Does

Paste in a video topic and get back a ready-to-use:
- ✅ Clickable, SEO-optimized **title** (under 70 chars)
- ✅ Full 3-paragraph **description** with timestamps & CTA
- ✅ Up to 15 relevant **tags**

No more staring at a blank YouTube Studio form.

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/osiris379/ai-youtube-toolkit.git
cd ai-youtube-toolkit
```

### 2. Install dependencies
```bash
pip install openai python-dotenv
```

### 3. Set up your API key
```bash
cp .env.example .env
# Open .env and add your OpenAI key:
# OPENAI_API_KEY=sk-your-key-here
```

### 4. Run it!
```bash
python generate_metadata.py --topic "How to build an AI chatbot with Python"
```

---

## 🎮 Demo Mode (No API Key Needed)

No OpenAI key yet? The script falls back to a smart template demo automatically.

```bash
python generate_metadata.py --topic "My first AI project"
```

---

## ⚙️ Options

| Flag | Description | Default |
|---|---|---|
| --topic | The video topic (required) | - |
| --style | educational, tutorial, or vlog | educational |

---

## 🛠️ Tech Stack

- Python 3.8+
- OpenAI API (gpt-4o-mini)
- python-dotenv

---

## 📁 Project Structure

```
ai-youtube-toolkit/
├── generate_metadata.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📬 Connect

- 🎬 YouTube: [youtube.com/@osiris379](https://youtube.com/@osiris379)
- 💻 GitHub: [github.com/osiris379](https://github.com/osiris379)
- 📧 osiris379ai@gmail.com

---

*Building in public. Learning out loud.* 🚀
