import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import json
from services.rag_service import RAGService
from models.request import PlanLevel
from langchain_core.documents import Document

class TestRAGTierRestrictions(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # We patch the services initialized in RAGService constructor
        self.patch_moderation = patch("services.rag_service.ModerationService")
        self.patch_router = patch("services.rag_service.RouterService")
        self.patch_vector_db = patch("services.rag_service.VectorDBService")
        self.patch_llm = patch("services.rag_service.LLMProviderService")

        self.mock_mod_class = self.patch_moderation.start()
        self.mock_router_class = self.patch_router.start()
        self.mock_vector_db_class = self.patch_vector_db.start()
        self.mock_llm_class = self.patch_llm.start()

        # Instantiate mocks
        self.mock_mod = self.mock_mod_class.return_value
        self.mock_router = self.mock_router_class.return_value
        self.mock_vector_db = self.mock_vector_db_class.return_value
        self.mock_llm = self.mock_llm_class.return_value

        # Setup standard mock behaviors
        self.mock_mod.check_message = AsyncMock(return_value=(True, None))
        self.mock_router.process_query = AsyncMock(return_value=("rag_required", "query", "none"))

        self.mock_vectorstore = MagicMock()
        self.mock_retriever = MagicMock()
        self.mock_vector_db.get_vectorstore.return_value = self.mock_vectorstore
        self.mock_vectorstore.as_retriever.return_value = self.mock_retriever

        # Instantiate RAGService
        self.rag_service = RAGService()

        # Mock prompt template __or__ and RunnableSequence pipeline to avoid LangChain internals
        self.mock_prompt = MagicMock()
        self.rag_service._get_prompts = MagicMock(return_value=self.mock_prompt)

        self.mock_chain = MagicMock()
        self.mock_prompt.__or__.return_value = self.mock_chain
        self.mock_chain.with_config.return_value = self.mock_chain

        # Mock LLM stream response on the chain
        mock_chunk = MagicMock()
        mock_chunk.content = "Response content"
        # We mock usage_metadata as a dict with integer values so it serializes to JSON cleanly
        mock_chunk.usage_metadata = {"output_tokens": 5}
        
        async def mock_astream(*args, **kwargs):
            yield mock_chunk
        self.mock_chain.astream = mock_astream

    def tearDown(self):
        self.patch_moderation.stop()
        self.patch_router.stop()
        self.patch_vector_db.stop()
        self.patch_llm.stop()

    async def test_free_tier_restricted_chunk(self):
        # Setup retriever to return a restricted document
        mock_doc = Document(
            page_content="This is restricted content.", 
            metadata={"id": "restricted_chunk_001", "is_restricted": True}
        )
        self.mock_retriever.ainvoke = AsyncMock(return_value=[mock_doc])

        # Consume the async generator
        chunks = []
        async for chunk in self.rag_service.get_streaming_response("query", chat_history=[], plan_level=PlanLevel.FREE, remaining_tokens=1000):
            chunks.append(chunk)

        # Free tier user gets blocked and presented with upgrade prompt
        self.assertIn("To access interactive exercises, worksheets, and specialized CBT tools, please upgrade to our Standard or Premium plan.", chunks[0])
        # Last chunk is the metadata JSON
        meta = json.loads(chunks[-1].strip())
        self.assertEqual(meta["mode"], "tier_restriction_refusal")
        self.assertEqual(meta["plan"], PlanLevel.FREE)

    async def test_free_tier_unrestricted_chunk(self):
        # Setup retriever to return an unrestricted document
        mock_doc = Document(
            page_content="This is unrestricted content.", 
            metadata={"id": "unrestricted_chunk_001", "is_restricted": False}
        )
        self.mock_retriever.ainvoke = AsyncMock(return_value=[mock_doc])

        chunks = []
        async for chunk in self.rag_service.get_streaming_response("query", chat_history=[], plan_level=PlanLevel.FREE, remaining_tokens=1000):
            chunks.append(chunk)

        # Standard RAG behavior goes through, doesn't get blocked
        self.assertIn("Response content", chunks[0])
        meta = json.loads(chunks[-1].strip())
        self.assertEqual(meta["mode"], "rag_complex")
        self.assertEqual(meta["plan"], PlanLevel.FREE)

    async def test_paid_tier_restricted_chunk_allowed(self):
        # Setup retriever to return a restricted document
        mock_doc = Document(
            page_content="This is restricted content.", 
            metadata={"id": "restricted_chunk_001", "is_restricted": True}
        )
        self.mock_retriever.ainvoke = AsyncMock(return_value=[mock_doc])

        # Standard plan is not blocked by restricted chunks
        chunks = []
        async for chunk in self.rag_service.get_streaming_response("query", chat_history=[], plan_level=PlanLevel.STANDARD, remaining_tokens=1000):
            chunks.append(chunk)

        self.assertIn("Response content", chunks[0])
        meta = json.loads(chunks[-1].strip())
        self.assertEqual(meta["mode"], "rag_complex")
        self.assertEqual(meta["plan"], PlanLevel.STANDARD)

    async def test_domain_based_retrieval_filtering(self):
        # Setup router mock to return a specific domain
        self.mock_router.process_query = AsyncMock(return_value=("rag_required", "how to stop a panic attack", "cbt_panic"))
        
        mock_doc = Document(
            page_content="CBT panic control techniques.", 
            metadata={"id": "panic_chunk_001", "domain": "cbt_panic"}
        )
        self.mock_retriever.ainvoke = AsyncMock(return_value=[mock_doc])

        chunks = []
        async for chunk in self.rag_service.get_streaming_response("how to stop a panic attack", chat_history=[], plan_level=PlanLevel.STANDARD, remaining_tokens=1000):
            chunks.append(chunk)

        # Verify that as_retriever was called with the cbt_panic domain filter in search_kwargs
        self.mock_vectorstore.as_retriever.assert_called()
        call_kwargs = self.mock_vectorstore.as_retriever.call_args[1]
        search_kwargs = call_kwargs.get("search_kwargs", {})
        
        self.assertEqual(search_kwargs.get("k"), 2) # Standard plan gets k=2
        self.assertIn("filter", search_kwargs)
        
        # Verify Qdrant filter structure
        qdrant_filter = search_kwargs["filter"]
        self.assertEqual(len(qdrant_filter.must), 1)
        field_condition = qdrant_filter.must[0]
        self.assertEqual(field_condition.key, "metadata.domain")
        self.assertEqual(field_condition.match.value, "cbt_panic")

if __name__ == "__main__":
    unittest.main()
