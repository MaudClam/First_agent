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
        self.is_initialized = False
        # Папка, где будем сохранять финальные изображения
        self.output_dir = os.environ.get("FINAL_ANSWER_DIR", "/tmp/final_answers")
        os.makedirs(self.output_dir, exist_ok=True)

    def forward(self, answer: Any) -> Any:
        # Если уже нормализовано — не трогаем
        if isinstance(answer, (AgentImage, AgentText, AgentAudio)):
            return answer

        # Если это PIL.Image (или PngImageFile и т.п.) — сохраним и вернем AgentImage(path)
        try:
            from PIL import Image  # pillow обычно уже есть из-за text-to-image
            if isinstance(answer, Image.Image):
                filename = f"{uuid.uuid4().hex}.png"
                path = os.path.join(self.output_dir, filename)
                answer.save(path, format="PNG")
                return AgentImage(path)
        except Exception:
            # Если pillow не установлен или что-то пошло не так — просто вернем как есть
            pass

        return answer
