#!/usr/bin/env python3
"""
Basic tests for GenAI Agent system
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from genai_agent import GenAIAgent, JobDescriptionSummarizer, EmailGenerator, VoiceProfile


class TestGenAIAgent(unittest.TestCase):
    """Test cases for GenAI Agent system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = GenAIAgent()
        self.sample_job = """
        Vibe Coder-in-Residence (GenAI Tech EA)
        
        Mission: Shadow our VP of Edge AI, capture every friction point in real time.
        
        What You'll Do (First 6 Months)
        * Day 1-30 — Observe → Automate: Ship micro-agents
        * Day 31-60 — Scale → Compose: Chain agents together
        
        Must-Haves
        * Track record of shipping GenAI products in < 2 weeks cycles
        * Mastery of GenAI and agent frameworks
        
        Success Metrics
        * ≥ 5 production agents live by day 30
        * ≥ 30% reduction in VP calendar load by day 90
        """
    
    def test_job_description_processing(self):
        """Test job description analysis."""
        result = self.agent.process_job_description(self.sample_job)
        
        # Check result structure
        self.assertIn('original_text', result)
        self.assertIn('summary', result)
        self.assertIn('extracted_info', result)
        self.assertIn('processed_at', result)
        
        # Check summary is generated
        self.assertIsInstance(result['summary'], str)
        self.assertGreater(len(result['summary']), 0)
    
    def test_email_generation(self):
        """Test email generation."""
        email = self.agent.generate_vp_intro_email("Test context")
        
        # Check email structure
        self.assertIn('Subject:', email)
        self.assertIn('Dear Team,', email)
        self.assertIn('Best regards,', email)
        self.assertIn('VP of Edge AI', email)
    
    def test_complete_workflow(self):
        """Test complete workflow."""
        results = self.agent.run_complete_workflow(self.sample_job)
        
        # Check all expected outputs
        self.assertIn('job_summary', results)
        self.assertIn('intro_email', results)
        self.assertIn('extracted_data', results)
        self.assertIn('workflow_completed_at', results)
        
        # Verify content quality
        self.assertGreater(len(results['job_summary']), 100)
        self.assertGreater(len(results['intro_email']), 500)


class TestJobDescriptionSummarizer(unittest.TestCase):
    """Test cases for job description summarizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.summarizer = JobDescriptionSummarizer()
        self.sample_job = """
        Day 1-30 — Observe: Ship micro-agents
        ≥ 5 production agents live by day 30
        Must-Haves
        * Track record of shipping GenAI products
        * Mastery of GenAI frameworks
        """
    
    def test_timeline_extraction(self):
        """Test timeline milestone extraction."""
        info = self.summarizer.extract_key_information(self.sample_job)
        
        self.assertIn('timeline', info)
        self.assertIsInstance(info['timeline'], list)
        
        # Should find the Day 1-30 milestone
        timeline_found = any('Day 1-30' in item for item in info['timeline'])
        self.assertTrue(timeline_found)
    
    def test_metrics_extraction(self):
        """Test metrics extraction."""
        info = self.summarizer.extract_key_information(self.sample_job)
        
        self.assertIn('metrics', info)
        self.assertIsInstance(info['metrics'], list)
        
        # Should find the ≥ 5 metric
        metrics_found = any('5' in item for item in info['metrics'])
        self.assertTrue(metrics_found)


class TestEmailGenerator(unittest.TestCase):
    """Test cases for email generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = EmailGenerator()
    
    def test_vp_email_generation(self):
        """Test VP email generation."""
        email = self.generator.generate_intro_email("Test initiative")
        
        # Check email structure
        self.assertIn('Subject:', email)
        self.assertIn('Dear Team,', email)
        self.assertIn('VP of Edge AI', email)
        
        # Check VP-specific content
        self.assertIn('ship', email.lower())
        self.assertIn('metrics', email.lower())
    
    def test_custom_voice_profile(self):
        """Test custom voice profile."""
        custom_profile = VoiceProfile(
            name="Test Executive",
            role="Test Role",
            communication_style={"directness": "high"},
            key_phrases=["test phrase"],
            priorities=["test priority"],
            tone_descriptors=["test tone"]
        )
        
        # Should not raise exception
        email = self.generator.generate_intro_email("Test", custom_profile)
        self.assertIsInstance(email, str)
        self.assertGreater(len(email), 100)


class TestVoiceProfile(unittest.TestCase):
    """Test cases for voice profile."""
    
    def test_voice_profile_creation(self):
        """Test voice profile creation."""
        profile = VoiceProfile(
            name="Test",
            role="Test Role",
            communication_style={},
            key_phrases=[],
            priorities=[],
            tone_descriptors=[]
        )
        
        self.assertEqual(profile.name, "Test")
        self.assertEqual(profile.role, "Test Role")
    
    def test_prompt_context_generation(self):
        """Test prompt context generation."""
        profile = VoiceProfile(
            name="Test",
            role="Test Role",
            communication_style={"test": "value"},
            key_phrases=["phrase1"],
            priorities=["priority1"],
            tone_descriptors=["tone1"]
        )
        
        context = profile.to_prompt_context()
        self.assertIn("Test", context)
        self.assertIn("Test Role", context)
        self.assertIn("phrase1", context)


if __name__ == '__main__':
    unittest.main()

