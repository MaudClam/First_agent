from smolagents import CodeAgent, HfApiModel, load_tool, tool
import datetime
import requests
import pytz
import yaml
import shutil
import gradio as gr
print("Gradio version:", gr.__version__)
from tools.final_answer import FinalAnswerTool
from tools.web_search import DuckDuckGoSearchTool
from tools.visit_webpage import VisitWebpageTool

from Gradio_UI import GradioUI

@tool
def disk_free(path: str = "/") -> str:
    """
    Show total/used/free disk space for a given filesystem path.
    Args:
        path: Filesystem path to inspect (e.g., '/', '/home/user').
    Returns:
        A human-friendly string with total/used/free sizes.
    """
    try:
        usage = shutil.disk_usage(path)  # returns (total, used, free) in bytes
    except Exception as e:
        return f"Error reading disk usage for path='{path}': {e}"

    def fmt_bytes(n: int) -> str:
        # binary units (KiB, MiB, GiB...)
        units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
        x = float(n)
        i = 0
        while x >= 1024.0 and i < len(units) - 1:
            x /= 1024.0
            i += 1
        return f"{x:.2f} {units[i]}"

    total = fmt_bytes(usage.total)
    used = fmt_bytes(usage.used)
    free = fmt_bytes(usage.free)
    return f"Disk usage for '{path}': total={total}, used={used}, free={free}"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()
web_search = DuckDuckGoSearchTool(max_results=10)
visit_webpage = VisitWebpageTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = HfApiModel(
max_tokens=2096,
temperature=0.5,
model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
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
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()