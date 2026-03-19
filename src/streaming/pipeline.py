import logging
from typing import AsyncGenerator

from src.asr.transcriber import StreamingASR
from src.dialogue.manager import DialogueManager
from src.llm.generator import LLMGenerator
from src.memory.context import ConversationMemory
from src.rag.retriever import RAGRetriever

logger = logging.getLogger(__name__)

class StreamingPipeline:
    def __init__(self, config: dict):
        self.asr = StreamingASR(config)
        self.dialogue = DialogueManager(config)
        self.llm = LLMGenerator(config)
        self.memory = ConversationMemory()
        self.rag = RAGRetriever(config)
        logger.info("Streaming pipeline orchestrated")

    async def process_audio_chunk(self, audio_chunk: bytes) -> AsyncGenerator[str, None]:
        \"\"\"
        End-to-end processing of a single audio chunk / utterance.
        1. Transcribe
        2. Retrieve RAG
        3. Build Prompt
        4. Generate LLM Stream
        \"\"\"
        # 1. ASR
        text_input = await self.asr.transcribe_chunk(audio_chunk)
        if not text_input.strip() or text_input == "[audio_content]":
            return
            
        logger.info(f"ASR Transcribed: {text_input}")
        
        # 2. Add to dialogue history
        self.dialogue.add_user_turn(text_input)
        
        # 3. Retrieve context
        rag_context = self.rag.retrieve(text_input)
        
        # 4. Build prompt
        prompt = self.llm.build_prompt(
            context_str=self.dialogue.get_context_string(),
            retrieved_context=rag_context,
            current_input=text_input
        )
        
        # 5. Generate Response Stream
        full_response = ""
        async for token in self.llm.generate_stream(prompt):
            full_response += token
            yield token
            
        # 6. Save agent response to dialogue
        self.dialogue.add_agent_turn(full_response.strip())
