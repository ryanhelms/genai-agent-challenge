"""
GenAI Agent for Job Description Analysis and Email Generation

This module provides a comprehensive agent system for:
1. Analyzing and summarizing job descriptions
2. Generating intro emails in a specific voice/style
3. Demonstrating modular GenAI architecture patterns

Architecture:
- Agent: Main orchestrator class
- Summarizer: Handles job description analysis and summarization
- EmailGenerator: Handles email composition in specific voices
- VoiceProfile: Defines communication style and characteristics
"""

import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VoiceProfile:
    """Defines the communication style and characteristics for email generation."""
    
    name: str
    role: str
    communication_style: Dict[str, Any]
    key_phrases: List[str]
    priorities: List[str]
    tone_descriptors: List[str]
    
    def to_prompt_context(self) -> str:
        """Convert voice profile to prompt context for LLM."""
        return f"""
Voice Profile: {self.name} ({self.role})

Communication Style:
- Tone: {', '.join(self.tone_descriptors)}
- Key Priorities: {', '.join(self.priorities)}
- Typical Phrases: {', '.join(self.key_phrases)}

Style Characteristics:
{json.dumps(self.communication_style, indent=2)}
"""


class JobDescriptionSummarizer:
    """Handles analysis and summarization of job descriptions."""
    
    def __init__(self):
        self.analysis_framework = {
            "core_mission": "What is the primary purpose and mission?",
            "key_responsibilities": "What are the main tasks and duties?",
            "timeline_milestones": "What are the key deadlines and milestones?",
            "required_skills": "What technical and soft skills are required?",
            "success_metrics": "How is success measured?",
            "cultural_fit": "What type of person/culture is this role suited for?"
        }
    
    def extract_key_information(self, job_text: str) -> Dict[str, Any]:
        """Extract structured information from job description text."""
        
        # Parse timeline information
        timeline_pattern = r"(Day|Month|Week)\s+(\d+(?:-\d+)?)[:\s—-]+([^•\n]+)"
        timeline_matches = re.findall(timeline_pattern, job_text, re.IGNORECASE)
        
        # Parse metrics
        metrics_pattern = r"≥\s*(\d+)\s*%?\s*([^.\n]+)"
        metrics_matches = re.findall(metrics_pattern, job_text)
        
        # Extract requirements sections
        must_haves = self._extract_section(job_text, "Must-Haves", "Nice-to-Haves")
        nice_to_haves = self._extract_section(job_text, "Nice-to-Haves", "Success Metrics")
        
        return {
            "timeline": [f"{period} {duration}: {task.strip()}" 
                        for period, duration, task in timeline_matches],
            "metrics": [f"{value}% {description.strip()}" 
                       for value, description in metrics_matches],
            "must_haves": must_haves,
            "nice_to_haves": nice_to_haves,
            "extracted_at": datetime.now().isoformat()
        }
    
    def _extract_section(self, text: str, start_marker: str, end_marker: str) -> List[str]:
        """Extract bullet points from a specific section."""
        start_idx = text.find(start_marker)
        if start_idx == -1:
            return []
        
        end_idx = text.find(end_marker, start_idx)
        if end_idx == -1:
            section_text = text[start_idx:]
        else:
            section_text = text[start_idx:end_idx]
        
        # Extract bullet points
        bullets = re.findall(r'[•*\-]\s*([^•*\-\n]+)', section_text)
        return [bullet.strip() for bullet in bullets if bullet.strip()]
    
    def generate_summary(self, job_text: str) -> str:
        """Generate a comprehensive summary of the job description."""
        
        extracted_info = self.extract_key_information(job_text)
        
        # Create structured summary
        summary_sections = []
        
        # Overview section
        if "Vibe Coder-in-Residence" in job_text:
            summary_sections.append(
                "## Position Overview\n"
                "**Role**: Vibe Coder-in-Residence (GenAI Tech EA)\n"
                "**Focus**: Shadow VP of Edge AI to build automated GenAI workflows and digital twin\n"
                "**Duration**: 6-month program with aggressive milestones\n"
            )
        
        # Timeline section
        if extracted_info["timeline"]:
            summary_sections.append("## Key Timeline Milestones")
            for milestone in extracted_info["timeline"][:6]:  # Top 6 milestones
                summary_sections.append(f"- {milestone}")
            summary_sections.append("")
        
        # Requirements section
        if extracted_info["must_haves"]:
            summary_sections.append("## Critical Requirements")
            for req in extracted_info["must_haves"][:5]:  # Top 5 requirements
                summary_sections.append(f"- {req}")
            summary_sections.append("")
        
        # Success metrics section
        if extracted_info["metrics"]:
            summary_sections.append("## Success Metrics")
            for metric in extracted_info["metrics"]:
                summary_sections.append(f"- {metric}")
            summary_sections.append("")
        
        return "\n".join(summary_sections)


class EmailGenerator:
    """Handles email generation in specific voices and styles."""
    
    def __init__(self):
        self.vp_voice_profile = VoiceProfile(
            name="VP of Edge AI",
            role="Vice President of Edge AI",
            communication_style={
                "directness": "high",
                "technical_depth": "advanced",
                "urgency": "high",
                "vision_focus": "future-oriented",
                "metrics_driven": True,
                "evangelism": True
            },
            key_phrases=[
                "ship daily",
                "metrics or it didn't happen",
                "the future of work",
                "competitive advantage",
                "unprecedented",
                "non-negotiable",
                "extraordinary"
            ],
            priorities=[
                "Speed and execution",
                "Measurable results",
                "Innovation and disruption",
                "AI evangelism",
                "Operational excellence"
            ],
            tone_descriptors=[
                "confident",
                "visionary",
                "results-oriented",
                "technically sophisticated",
                "urgency-driven"
            ]
        )
    
    def generate_intro_email(self, context: str, voice_profile: Optional[VoiceProfile] = None) -> str:
        """Generate an introduction email in the specified voice."""
        
        if voice_profile is None:
            voice_profile = self.vp_voice_profile
        
        # Email template structure based on VP characteristics
        email_template = {
            "subject": "Welcome to the Future of AI-Powered Executive Operations",
            "opening": self._generate_opening(context, voice_profile),
            "vision": self._generate_vision_section(context, voice_profile),
            "execution": self._generate_execution_section(context, voice_profile),
            "metrics": self._generate_metrics_section(context, voice_profile),
            "closing": self._generate_closing(voice_profile)
        }
        
        return self._assemble_email(email_template)
    
    def _generate_opening(self, context: str, voice_profile: VoiceProfile) -> str:
        """Generate email opening paragraph."""
        return (
            f"I'm excited to introduce an initiative that represents the next evolution "
            f"of how we think about executive productivity and AI integration at our organization. "
            f"As {voice_profile.role}, I've been obsessing over a simple question: What if we could "
            f"eliminate every friction point in executive workflows while simultaneously building "
            f"the most advanced AI-powered digital assistant the industry has ever seen?"
        )
    
    def _generate_vision_section(self, context: str, voice_profile: VoiceProfile) -> str:
        """Generate vision and strategy section."""
        return (
            "This isn't just about automation; it's about creating a living, breathing digital twin "
            "that can think, write, and strategize with the same precision and insight that drives "
            "our most critical decisions. We're not just solving our own problems—we're creating "
            "the playbook that will transform how every executive in every industry operates."
        )
    
    def _generate_execution_section(self, context: str, voice_profile: VoiceProfile) -> str:
        """Generate execution and implementation section."""
        return (
            "Starting immediately, our Coder-in-Residence will shadow every meeting, every document "
            "review, every strategic conversation. They'll identify patterns, capture decision-making "
            "frameworks, and ship micro-agents daily that eliminate repetitive tasks. This is more "
            "than a role—it's a founding engineer position for the future of executive AI."
        )
    
    def _generate_metrics_section(self, context: str, voice_profile: VoiceProfile) -> str:
        """Generate metrics and accountability section."""
        return (
            "The metrics are non-negotiable: ship daily, measure everything, and optimize relentlessly. "
            "We'll track latency, adoption rates, and minutes saved with the same rigor we apply to "
            "our core product metrics. Because if we can't measure it, we can't improve it, and if "
            "we can't improve it, we're not moving fast enough."
        )
    
    def _generate_closing(self, voice_profile: VoiceProfile) -> str:
        """Generate email closing."""
        return (
            "The future of work isn't coming—it's here. And we're going to show everyone exactly "
            "what it looks like. Let's ship something extraordinary."
        )
    
    def _assemble_email(self, template: Dict[str, str]) -> str:
        """Assemble the complete email from template sections."""
        return f"""Subject: {template['subject']}

Dear Team,

{template['opening']}

{template['vision']}

{template['execution']}

{template['metrics']}

{template['closing']}

Best regards,
[VP Name]
VP of Edge AI

P.S. If you're reading this and thinking "this sounds impossible," you're exactly the kind of person we need. The impossible is just another word for "not automated yet."
"""


class GenAIAgent:
    """Main agent orchestrator for job analysis and email generation."""
    
    def __init__(self):
        self.summarizer = JobDescriptionSummarizer()
        self.email_generator = EmailGenerator()
        self.session_data = {}
    
    def process_job_description(self, job_text: str) -> Dict[str, Any]:
        """Process a job description and return analysis results."""
        
        # Generate summary
        summary = self.summarizer.generate_summary(job_text)
        
        # Extract structured information
        extracted_info = self.summarizer.extract_key_information(job_text)
        
        # Store in session for email generation
        self.session_data['job_analysis'] = {
            'original_text': job_text,
            'summary': summary,
            'extracted_info': extracted_info,
            'processed_at': datetime.now().isoformat()
        }
        
        return self.session_data['job_analysis']
    
    def generate_vp_intro_email(self, job_context: Optional[str] = None) -> str:
        """Generate VP introduction email based on job context."""
        
        if job_context is None and 'job_analysis' in self.session_data:
            job_context = self.session_data['job_analysis']['summary']
        elif job_context is None:
            job_context = "GenAI and automation initiative"
        
        return self.email_generator.generate_intro_email(job_context)
    
    def run_complete_workflow(self, job_text: str) -> Dict[str, Any]:
        """Run the complete workflow: analyze job + generate email."""
        
        # Process job description
        job_analysis = self.process_job_description(job_text)
        
        # Generate intro email
        intro_email = self.generate_vp_intro_email()
        
        return {
            'job_summary': job_analysis['summary'],
            'intro_email': intro_email,
            'extracted_data': job_analysis['extracted_info'],
            'workflow_completed_at': datetime.now().isoformat()
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize agent
    agent = GenAIAgent()
    
    # Sample job description for testing
    sample_job = """
    Vibe Coder-in-Residence (GenAI Tech EA) 

    Mission 
    Shadow our VP of Edge AI, capture every friction point in real time, and turn it into an automated GenAI workflow—shipping daily.
    
    What You'll Do (First 6 Months) 
    * Day 1-30 — Observe → Automate: Ship micro-agents that cut repeat tasks
    * Day 31-60 — Scale → Compose: Chain agents together, cut human touchpoints by >25%
    * Day 61-90 — Externalize → Evangelize: Package best agents as internal templates
    * Month 4-6 — Digital Twin v1: Fine-tune a personal-style LLM, shoot for ≥ 70% confusion
    
    Must-Haves 
    * Track record of shipping GenAI products in < 2 weeks cycles
    * Mastery of GenAI and agent frameworks (Langchain, MCP etc)
    * Rapid full-stack micro-site builder
    
    Success Metrics 
    * ≥ 5 production agents live by day 30
    * ≥ 30% reduction in VP calendar load by day 90
    * ≥ 2 external media features by month 6
    """
    
    # Run workflow
    results = agent.run_complete_workflow(sample_job)
    
    print("=== JOB SUMMARY ===")
    print(results['job_summary'])
    print("\n=== INTRO EMAIL ===")
    print(results['intro_email'])

