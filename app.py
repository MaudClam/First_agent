from __future__ import annotations

import os
import shutil
from pathlib import Path

import gradio as gr
import yaml
from smolagents import CodeAgent, HfApiModel, load_tool

from tools.final_answer import FinalAnswerTool
from tools.web_search import DuckDuckGoSearchTool
from tools.visit_webpage import VisitWebpageTool
from tools.disk_free import disk_free
from tools.timezone_time import get_current_time_in_timezone
from src.first_agent.ui import GradioUI


print("Gradio version:", gr.__version__)

# --- Load .env locally (HF Spaces will use Settings → Secrets instead) ---
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

# --- Required env ---
if not os.getenv("HF_TOKEN"):
    raise RuntimeError(
        "HF_TOKEN is not set. "
        "Create a .env file locally or configure it in Hugging Face Spaces → Settings → Secrets."
    )

# --- Runtime output directory setup ---
BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "outputs" / "final_answers"
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Make FinalAnswerTool write into the same folder
os.environ["FINAL_ANSWER_DIR"] = str(OUTPUT_DIR)

# --- Tools ---
final_answer = FinalAnswerTool()
web_search = DuckDuckGoSearchTool(max_results=10)
visit_webpage = VisitWebpageTool()

# --- Model ---
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",  # may be overloaded sometimes
    custom_role_conversions=None,
)

# Tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# Prompts
with open("prompts.yaml", "r", encoding="utf-8") as stream:
    prompt_templates = yaml.safe_load(stream)

# --- Agent ---
agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        get_current_time_in_timezone,
        web_search,
        visit_webpage,
        image_generation_tool,
        disk_free,
    ],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates,
)

# On HF Spaces, share=True is not supported; force share=False
GradioUI(agent).launch()
