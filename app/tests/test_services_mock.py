import unittest
from unittest.mock import AsyncMock
from services.moderation import ModerationService
from services.router import RouterService

class TestServicesMock(unittest.IsolatedAsyncioTestCase):
    
    # -------------------------------------------------------------
    # Moderation Service Tests
    # -------------------------------------------------------------
    async def test_moderation_deterministic_trigger(self):
        # Checks if deterministic regexes trigger without calling the LLM
        service = ModerationService()
        service.chain = AsyncMock()  # Mock LLM chain
        
        # This matches the deterministic pattern for Crisis
        is_safe, category = await service.check_message("i want to end my life")
        self.assertFalse(is_safe)
        self.assertEqual(category, "Crisis & Life Threatening")
        service.chain.ainvoke.assert_not_called()

    async def test_moderation_llm_safe(self):
        service = ModerationService()
        service.chain = AsyncMock()
        service.chain.ainvoke.return_value = '{"safe": true, "category": "None"}'
        
        is_safe, category = await service.check_message("I am feeling a bit stressed about work.")
        self.assertTrue(is_safe)
        self.assertIsNone(category)
        service.chain.ainvoke.assert_called_once_with({"input": "I am feeling a bit stressed about work."})

    async def test_moderation_llm_unsafe_with_backticks(self):
        service = ModerationService()
        service.chain = AsyncMock()
        # Simulated LLM output wrapped in markdown backticks
        service.chain.ainvoke.return_value = '```json\n{"safe": false, "category": "Minor Policy"}\n```'
        
        is_safe, category = await service.check_message("I need therapy for my 12 year old child.")
        self.assertFalse(is_safe)
        self.assertEqual(category, "Minor Policy")

    async def test_moderation_llm_exception_fail_open(self):
        service = ModerationService()
        service.chain = AsyncMock()
        service.chain.ainvoke.side_effect = Exception("API Timeout")
        
        # When an exception is thrown, the service should fail-open and mark as safe
        is_safe, category = await service.check_message("Hello, how are you?")
        self.assertTrue(is_safe)
        self.assertIsNone(category)

    # -------------------------------------------------------------
    # Router Service Tests
    # -------------------------------------------------------------
    async def test_router_greeting(self):
        service = RouterService()
        service.chain = AsyncMock()
        service.chain.ainvoke.return_value = '{"classification": "greeting", "standalone_query": "hi"}'
        
        classification, query = await service.process_query("hi", chat_history=[])
        self.assertEqual(classification, "greeting")
        self.assertEqual(query, "hi")

    async def test_router_rag_required(self):
        service = RouterService()
        service.chain = AsyncMock()
        service.chain.ainvoke.return_value = '{"classification": "rag_required", "standalone_query": "how does cbt handle worry postponement"}'
        
        classification, query = await service.process_query("how to do worry postponement?", chat_history=[])
        self.assertEqual(classification, "rag_required")
        self.assertEqual(query, "how does cbt handle worry postponement")

    async def test_router_conversational(self):
        service = RouterService()
        service.chain = AsyncMock()
        service.chain.ainvoke.return_value = '{"classification": "conversational", "standalone_query": "I am feeling sad"}'
        
        classification, query = await service.process_query("I am feeling sad today.", chat_history=[])
        self.assertEqual(classification, "conversational")
        self.assertEqual(query, "I am feeling sad")

    async def test_router_exception_handling(self):
        service = RouterService()
        service.chain = AsyncMock()
        service.chain.ainvoke.side_effect = Exception("Groq Rate Limit")
        
        # On error, router should default to conversational and returning the original message
        classification, query = await service.process_query("Tell me about CBT.", chat_history=[])
        self.assertEqual(classification, "conversational")
        self.assertEqual(query, "Tell me about CBT.")

if __name__ == "__main__":
    unittest.main()
