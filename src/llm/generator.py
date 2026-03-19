import asyncio
import logging
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

class LLMGenerator:
    def __init__(self, config: dict):
        self.model_id = config.get("llm", {}).get("model_id", "distilgpt2")
        self.stream_tokens = config.get("llm", {}).get("stream_tokens", True)
        self.ttft_ms = config.get("llm", {}).get("simulated_ttft_ms", 80)
        self.inter_token_ms = config.get("llm", {}).get("simulated_inter_token_ms", 5)
        logger.info(f"Initialized LLM Generator with simulated model {self.model_id}")

    def build_prompt(self, context_str: str, retrieved_context: list[str], current_input: str) -> str:
        prompt = f"Background Info:\n"
        for doc in retrieved_context:
            prompt += f"- {doc}\n"
        prompt += f"\nConversation History:\n{context_str}\n\nUser: {current_input}\nAgent:"
        return prompt

    async def generate_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        \"\"\"
        Simulates an LLM streaming response generation.
        In production, this would use a HuggingFace TextIteratorStreamer or vLLM server.
        \"\"\"
        logger.debug(f"LLM Generating stream for prompt length: {len(prompt)}")
        
        # Simulate Time-To-First-Token (TTFT)
        await asyncio.sleep(self.ttft_ms / 1000.0)
        
        # Dummy response logic
        if "latency" in prompt.lower() or "fast" in prompt.lower():
            response = "I can respond in under 100 milliseconds because of my optimized streaming architecture. "
        elif "hello" in prompt.lower():
            response = "Hello! How can I assist you today? "
        else:
            response = "That is an interesting point. Let me help you with that. "
            
        # Stream out words (simulating token streaming)
        words = response.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(self.inter_token_ms / 1000.0)
