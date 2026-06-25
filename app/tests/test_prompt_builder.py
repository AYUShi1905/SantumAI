import unittest
from services.prompt_builder import SystemPromptBuilder
from models.request import PlanLevel

class TestSystemPromptBuilder(unittest.TestCase):
    def test_mood_tone_happy(self):
        # Happy mood (happiness >= 8)
        builder = SystemPromptBuilder(happiness=8.5, stress=3.0, energy=5.0)
        prompt = builder.build(has_context=False)
        self.assertIn("The user is in a positive mood; be upbeat and celebratory", prompt)

    def test_mood_tone_sad(self):
        # Low mood (happiness <= 3)
        builder = SystemPromptBuilder(happiness=2.0, stress=3.0, energy=5.0)
        prompt = builder.build(has_context=False)
        self.assertIn("The user is feeling low; prioritize deep empathy and validation", prompt)

    def test_mood_tone_stressed(self):
        # Stressed mood (stress >= 8)
        builder = SystemPromptBuilder(happiness=5.0, stress=9.0, energy=5.0)
        prompt = builder.build(has_context=False)
        self.assertIn("The user is stressed; be soothing and exceptionally calm", prompt)

    def test_plan_free(self):
        # Free plan (k limit instruction and active listening)
        builder = SystemPromptBuilder(plan_level=PlanLevel.FREE)
        prompt = builder.build(has_context=False)
        self.assertIn("Focus on active listening and emotional validation", prompt)
        self.assertIn("Your response MUST be under 80 words", prompt)

    def test_plan_standard(self):
        # Standard plan
        builder = SystemPromptBuilder(plan_level=PlanLevel.STANDARD)
        prompt = builder.build(has_context=False)
        self.assertIn("Focus on high-quality emotional validation and structured inquiry", prompt)
        self.assertIn("Your response MUST be under 100 words", prompt)

    def test_plan_premium(self):
        # Premium plan
        builder = SystemPromptBuilder(plan_level=PlanLevel.PREMIUM)
        prompt = builder.build(has_context=False)
        self.assertIn("Incorporate CBT techniques when relevant to the context", prompt)
        self.assertIn("Your response MUST be under 120 words", prompt)

    def test_follow_up_disallowed(self):
        # Disable follow-up questions
        builder = SystemPromptBuilder()
        prompt = builder.build(has_context=False, follow_up_allowed=False)
        self.assertIn("Do NOT ask any follow-up questions or end your response with a question", prompt)

    def test_follow_up_allowed(self):
        # Enable follow-up questions
        builder = SystemPromptBuilder()
        prompt = builder.build(has_context=False, follow_up_allowed=True)
        self.assertIn("DYNAMIC FOLLOW-UPS:", prompt)
        self.assertNotIn("Do NOT ask any follow-up questions or end your response with a question", prompt)

if __name__ == "__main__":
    unittest.main()
