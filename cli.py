#!/usr/bin/env python3
"""
Command Line Interface for GenAI Agent Challenge

Usage:
    python cli.py --input job_description.txt --output-dir ./results
    python cli.py --demo  # Run with sample data
"""

import argparse
import json
import os
import sys
from pathlib import Path
from genai_agent import GenAIAgent


def load_job_description(file_path: str) -> str:
    """Load job description from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def save_results(results: dict, output_dir: str):
    """Save agent results to output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save job summary
    summary_path = output_path / "job_summary.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# Job Description Summary\n\n")
        f.write(results['job_summary'])
    
    # Save intro email
    email_path = output_path / "vp_intro_email.md"
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(results['intro_email'])
    
    # Save extracted data as JSON
    data_path = output_path / "extracted_data.json"
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(results['extracted_data'], f, indent=2)
    
    # Save complete results
    complete_path = output_path / "complete_results.json"
    with open(complete_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path.absolute()}")
    print(f"- Job Summary: {summary_path}")
    print(f"- VP Email: {email_path}")
    print(f"- Extracted Data: {data_path}")
    print(f"- Complete Results: {complete_path}")


def run_demo():
    """Run demo with sample job description."""
    sample_job = """
Using GenAI, ship a working agent that summarizes this job description, drafts your intro email in the VP's voice, and posts both to a public GitHub repo. Include a README on architecture choices. Fastest high-quality submission wins the initial selection interview.

Vibe Coder-in-Residence (GenAI Tech EA) 

Mission 
Shadow our VP of Edge AI, capture every friction point in real time, and turn it into an automated GenAI workflow—shipping daily. Act as founding engineer for the VP's digital twin "brain" while evangelizing and broadcasting the journey for maximum "AI halo" impact. 

What You'll Do (First 6 Months) 
* Day 1-30 — Observe → Automate: Pair-shadow meetings, Teams, doc reviews. Ship micro-agents that cut repeat tasks (think: LLM-powered agenda generator, decision-tracker bot). 
* Day 31-60 — Scale → Compose: Chain agents together—calendar optimizer calls the meeting-minute bot which feeds the action-item tracker. Instrument with telemetry; cut human touchpoints by >25 %. Build a microsite "tech radar" that maps VP's Deep Research notes into visible tech-trends radar. Build a "team tracker" agent to generate the weekly status radar for whole of VP's org. 
* Day 61-90 — Externalize → Evangelize: Package best agents as internal templates. Produce a public demo or open-sourced repo; partner with Comms for media drops. 
* Month 4-6 — Digital Twin v1: Fine-tune a personal-style LLM and mult-agent fabric that drafts briefs and strategic emails and technical articles indistinguishable from the VP. Formal Turing evaluation: randomize % past emails into twin vs. VP variants, have peers label author; shoot for ≥ 70 % confusion before iterating toward BLEU 0.75 goal.   

Daily Responsibilities 
* Live-code GenAI agents in Python / TypeScript using LangChain, OpenAI etc. 
* Fine-tune and orchestrate LLMs (OpenAI, Claude, local models). 
* Rapid-fire prompt engineering; optimize systems prompts for set of VP agents. 
* Integrate with enterprise APIs (Teams, Confluence, Office). 
* Maintain a "metrics or it didn't happen" dashboard (latency, adoption, minutes saved). 
* Co-write technical blogs and demo scripts with Comms to amplify the story.   

Must-Haves 
* Track record of shipping GenAI products in < 2 weeks cycles. Provide links or repos. 
* Mastery of GenAI and agent frameworks (Langchain, MCP etc). 
* Rapid full-stack micro-site builder (e.g. Vercel). 
* Comfortable pair-programming or pair-prompting in a fast-moving exec environment; ego-less, outcome-obsessed. 
* Storytelling chops—can turn a changelog into a headline. 
* Time zone: The role is based out of San Jose (CA, USA) or Limerick (Ireland), but the applicant can work remotely and must be willing to work in whichever time zone the VP is in, mostly the CA time zone.   

Nice-to-Haves 
* Experience reverse-engineering personal workflows or building AI copilots. 
* Familiar with range of productivity hacks and how to code them as agents 
* Prior startup founding engineer (doesn't matter if company succeeeded) or hacker-in-residence cred. 
* Familiar with enterprise security & compliance for LLM rollouts.   

Success Metrics 
* ≥ 5 production agents live by day 30. 
* ≥ 30 % reduction in VP calendar load by day 90. 
* ≥ 2 external media features or conference demos by month 6.
"""
    
    print("Running GenAI Agent Demo...")
    print("=" * 50)
    
    agent = GenAIAgent()
    results = agent.run_complete_workflow(sample_job)
    
    print("\n=== JOB SUMMARY ===")
    print(results['job_summary'])
    print("\n=== VP INTRO EMAIL ===")
    print(results['intro_email'])
    
    # Save demo results
    save_results(results, "./demo_results")


def main():
    parser = argparse.ArgumentParser(
        description="GenAI Agent for Job Description Analysis and Email Generation"
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Path to job description text file'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='./results',
        help='Output directory for results (default: ./results)'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demo with sample job description'
    )
    
    args = parser.parse_args()
    
    if args.demo:
        run_demo()
        return
    
    if not args.input:
        print("Error: Please provide --input file or use --demo")
        parser.print_help()
        sys.exit(1)
    
    # Load job description
    job_text = load_job_description(args.input)
    
    # Initialize and run agent
    print("Initializing GenAI Agent...")
    agent = GenAIAgent()
    
    print("Processing job description...")
    results = agent.run_complete_workflow(job_text)
    
    # Save results
    save_results(results, args.output_dir)
    
    print("\nWorkflow completed successfully!")


if __name__ == "__main__":
    main()

