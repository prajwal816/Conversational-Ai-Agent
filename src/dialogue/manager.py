import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class DialogueManager:
    def __init__(self, config: dict):
        self.max_history = config.get("dialogue", {}).get("max_history_turns", 5)
        self.history: List[Dict[str, str]] = []
        logger.info("Initialized Dialogue Manager")

    def add_user_turn(self, text: str):
        self.history.append({"role": "user", "content": text})
        self._prune_history()

    def add_agent_turn(self, text: str):
        self.history.append({"role": "agent", "content": text})
        self._prune_history()

    def get_context_string(self) -> str:
        turns = []
        for turn in self.history:
            turns.append(f"{turn['role'].capitalize()}: {turn['content']}")
        return "\n".join(turns)

    def _prune_history(self):
        if len(self.history) > self.max_history * 2:
            # keep the latest standard turns
            self.history = self.history[-(self.max_history * 2):]
