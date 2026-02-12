---

title: First Agent Template
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 6.5.1
app_file: app.py
pinned: false
tags:
  - smolagents
  - agent
  - smolagent
  - tool
  - agent-course

---

# First Agent (smolagents)

A modular educational AI agent built with **smolagents** and **Gradio**, following the Hugging Face Agents Course.

The agent can:

* Generate images
* Perform web search
* Visit web pages
* Get current time by timezone
* Check disk usage

Runs locally and on **Hugging Face Spaces**.

---

## Project Structure

```
.
├── app.py
├── prompts.yaml
├── src/first_agent/
│   ├── ui.py
│   ├── agent_factory.py
│   └── settings.py
├── tools/
│   ├── final_answer.py
│   ├── web_search.py
│   ├── visit_webpage.py
│   └── disk_free.py
```

* `app.py` – entry point
* `agent_factory.py` – builds model + agent + tools
* `ui.py` – Gradio interface
* `tools/` – custom tools
* `prompts.yaml` – agent prompt templates

---

## Model

```
Qwen/Qwen2.5-Coder-32B-Instruct
```

Accessed via Hugging Face serverless inference (`HfApiModel`).

---

## Local Setup

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set HF token

Create `.env`:

```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxx
```

Get token from:
https://huggingface.co/settings/tokens
Scope: **Read**

### 4. Run

```bash
python app.py
```

---

## Hugging Face Spaces

Add your token in:

**Settings → Secrets → HF_TOKEN**

No need for `share=True` on Spaces.

---

## Runtime Behavior

* `outputs/` directory is created at startup
* Old files are cleaned
* Directory is ignored via `.gitignore`
* Works both locally and inside HF container

---

## Status

Educational project with modular architecture and clean separation of:

* UI
* Agent
* Tools
* Configuration

---

## License

MIT (or specify if different).
