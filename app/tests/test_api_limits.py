import unittest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException
from api.v1.chat import chat_rag_stream
from models.request import ChatRequest, PlanLevel

class TestApiLimits(unittest.IsolatedAsyncioTestCase):
    
    @patch("api.v1.chat.rag_service.get_streaming_response")
    async def test_free_plan_within_limit(self, mock_stream):
        mock_stream.return_value = AsyncMock()
        # 80 words (Exactly the limit for Free)
        message = " ".join(["word"] * 80)
        request = ChatRequest(
            message=message,
            plan_level=PlanLevel.FREE,
            remaining_tokens=500
        )
        # Should proceed without raising HTTPException
        response = await chat_rag_stream(request)
        self.assertIsNotNone(response)
        mock_stream.assert_called_once()

    @patch("api.v1.chat.rag_service.get_streaming_response")
    async def test_free_plan_exceeds_limit(self, mock_stream):
        # 81 words (Exceeds Free limit of 80)
        message = " ".join(["word"] * 81)
        request = ChatRequest(
            message=message,
            plan_level=PlanLevel.FREE,
            remaining_tokens=500
        )
        with self.assertRaises(HTTPException) as context:
            await chat_rag_stream(request)
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("exceeds the 80-word limit", context.exception.detail)
        mock_stream.assert_not_called()

    @patch("api.v1.chat.rag_service.get_streaming_response")
    async def test_standard_plan_within_limit(self, mock_stream):
        mock_stream.return_value = AsyncMock()
        # 100 words (Exactly the limit for Standard)
        message = " ".join(["word"] * 100)
        request = ChatRequest(
            message=message,
            plan_level=PlanLevel.STANDARD,
            remaining_tokens=500
        )
        response = await chat_rag_stream(request)
        self.assertIsNotNone(response)
        mock_stream.assert_called_once()

    @patch("api.v1.chat.rag_service.get_streaming_response")
    async def test_standard_plan_exceeds_limit(self, mock_stream):
        # 101 words (Exceeds Standard limit of 100)
        message = " ".join(["word"] * 101)
        request = ChatRequest(
            message=message,
            plan_level=PlanLevel.STANDARD,
            remaining_tokens=500
        )
        with self.assertRaises(HTTPException) as context:
            await chat_rag_stream(request)
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("exceeds the 100-word limit", context.exception.detail)
        mock_stream.assert_not_called()

    @patch("api.v1.chat.rag_service.get_streaming_response")
    async def test_premium_plan_within_limit(self, mock_stream):
        mock_stream.return_value = AsyncMock()
        # 120 words (Exactly the limit for Premium)
        message = " ".join(["word"] * 120)
        request = ChatRequest(
            message=message,
            plan_level=PlanLevel.PREMIUM,
            remaining_tokens=500
        )
        response = await chat_rag_stream(request)
        self.assertIsNotNone(response)
        mock_stream.assert_called_once()

    @patch("api.v1.chat.rag_service.get_streaming_response")
    async def test_premium_plan_exceeds_limit(self, mock_stream):
        # 121 words (Exceeds Premium limit of 120)
        message = " ".join(["word"] * 121)
        request = ChatRequest(
            message=message,
            plan_level=PlanLevel.PREMIUM,
            remaining_tokens=500
        )
        with self.assertRaises(HTTPException) as context:
            await chat_rag_stream(request)
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("exceeds the 120-word limit", context.exception.detail)
        mock_stream.assert_not_called()

if __name__ == "__main__":
    unittest.main()
