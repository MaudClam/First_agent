from __future__ import annotations

from typing import Any
import os
import uuid

from smolagents.tools import Tool
from smolagents.agent_types import AgentImage, AgentText, AgentAudio


class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides a final answer to the given problem."
    inputs = {"answer": {"type": "any", "description": "The final answer to the problem"}}
    output_type = "any"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # ВАЖНО
        from pathlib import Path
        self.output_dir = Path.cwd() / "outputs" / "final_answers"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def forward(self, answer: Any) -> Any:
        if isinstance(answer, (AgentImage, AgentText, AgentAudio)):
            return answer

        try:
            from PIL import Image  # pillow обычно уже есть из-за text-to-image
            if isinstance(answer, Image.Image):
                filename = f"{uuid.uuid4().hex}.png"
                path = os.path.join(self.output_dir, filename)
                answer.save(path, format="PNG")
                return AgentImage(path)
        except Exception:
            pass

        return answer
