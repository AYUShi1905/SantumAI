import unittest
from services.rag_service import RAGService
from models.request import PlanLevel

class TestRAGHeuristics(unittest.TestCase):
    def setUp(self):
        self.rag_service = RAGService()

    def test_pure_greetings(self):
        # List of queries that should be identified as pure greetings
        greetings = [
            "hi",
            "hello",
            "hey",
            "yo",
            "hi there",
            "hello there",
            "good morning",
            "good afternoon",
            "good evening",
            "hi sai",
            "hello santum",
            "hi sai!",
            "hello?",
        ]
        for query in greetings:
            with self.subTest(query=query):
                self.assertTrue(
                    self.rag_service._is_pure_greeting(query),
                    f"Failed to detect pure greeting: '{query}'"
                )

    def test_non_greetings(self):
        # List of queries that have greeting words but contain emotional context or requests
        non_greetings = [
            "hello I am feeling very anxious today",
            "hi my stress level is extremely high",
            "good morning can you help me with a panic attack",
            "hey what is a cbt exercise?",
            "hi what is the suicide prevention hotline",
            "is anyone there to talk about depression",
            "hello how do i delete my account",
        ]
        for query in non_greetings:
            with self.subTest(query=query):
                self.assertFalse(
                    self.rag_service._is_pure_greeting(query),
                    f"Incorrectly flagged non-greeting as greeting: '{query}'"
                )

if __name__ == "__main__":
    unittest.main()
