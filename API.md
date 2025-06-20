# API Documentation: GenAI Agent System

## Overview

This document provides comprehensive API documentation for the GenAI Agent system, including class interfaces, method signatures, and usage examples.

## Core Classes

### GenAIAgent

Main orchestrator class for the complete workflow.

#### Constructor

```python
GenAIAgent()
```

Creates a new GenAI agent instance with initialized components.

#### Methods

##### `process_job_description(job_text: str) -> Dict[str, Any]`

Processes a job description and returns structured analysis.

**Parameters:**
- `job_text` (str): Raw job description text

**Returns:**
- Dict containing:
  - `original_text`: Original input text
  - `summary`: Generated summary in Markdown format
  - `extracted_info`: Structured data extraction results
  - `processed_at`: ISO timestamp of processing

**Example:**
```python
agent = GenAIAgent()
result = agent.process_job_description(job_text)
print(result['summary'])
```

##### `generate_vp_intro_email(job_context: Optional[str] = None) -> str`

Generates VP introduction email based on job context.

**Parameters:**
- `job_context` (str, optional): Context for email generation. Uses session data if not provided.

**Returns:**
- Complete email text with subject, body, and signature

**Example:**
```python
agent = GenAIAgent()
email = agent.generate_vp_intro_email("AI automation initiative")
print(email)
```

##### `run_complete_workflow(job_text: str) -> Dict[str, Any]`

Executes the complete analysis and email generation workflow.

**Parameters:**
- `job_text` (str): Raw job description text

**Returns:**
- Dict containing:
  - `job_summary`: Generated summary
  - `intro_email`: Generated email
  - `extracted_data`: Structured extraction results
  - `workflow_completed_at`: ISO timestamp

**Example:**
```python
agent = GenAIAgent()
results = agent.run_complete_workflow(job_text)
```

### JobDescriptionSummarizer

Handles job description analysis and summarization.

#### Constructor

```python
JobDescriptionSummarizer()
```

#### Methods

##### `extract_key_information(job_text: str) -> Dict[str, Any]`

Extracts structured information from job description.

**Parameters:**
- `job_text` (str): Raw job description text

**Returns:**
- Dict containing:
  - `timeline`: List of timeline milestones
  - `metrics`: List of success metrics
  - `must_haves`: List of required qualifications
  - `nice_to_haves`: List of preferred qualifications
  - `extracted_at`: ISO timestamp

##### `generate_summary(job_text: str) -> str`

Generates comprehensive summary in Markdown format.

**Parameters:**
- `job_text` (str): Raw job description text

**Returns:**
- Markdown-formatted summary string

### EmailGenerator

Handles email generation with voice profiles.

#### Constructor

```python
EmailGenerator()
```

#### Methods

##### `generate_intro_email(context: str, voice_profile: Optional[VoiceProfile] = None) -> str`

Generates introduction email in specified voice.

**Parameters:**
- `context` (str): Context for email content
- `voice_profile` (VoiceProfile, optional): Voice profile to use. Defaults to VP profile.

**Returns:**
- Complete email text

### VoiceProfile

Defines communication style and characteristics.

#### Constructor

```python
VoiceProfile(
    name: str,
    role: str,
    communication_style: Dict[str, Any],
    key_phrases: List[str],
    priorities: List[str],
    tone_descriptors: List[str]
)
```

**Parameters:**
- `name`: Profile identifier
- `role`: Professional role/title
- `communication_style`: Style characteristics dict
- `key_phrases`: Typical phrases and vocabulary
- `priorities`: Key focus areas
- `tone_descriptors`: Tone characteristics

#### Methods

##### `to_prompt_context() -> str`

Converts voice profile to prompt context for LLM integration.

**Returns:**
- Formatted string suitable for prompt engineering

## CLI Interface

### Command Line Usage

```bash
python cli.py [OPTIONS]
```

#### Options

- `--input, -i`: Path to job description text file
- `--output-dir, -o`: Output directory for results (default: ./results)
- `--demo`: Run demo with sample job description

#### Examples

```bash
# Analyze specific job description
python cli.py --input job.txt --output-dir ./analysis_results

# Run demonstration
python cli.py --demo

# Use default output directory
python cli.py --input job.txt
```

### Output Files

The CLI generates the following output files:

- `job_summary.md`: Markdown-formatted job summary
- `vp_intro_email.md`: Generated introduction email
- `extracted_data.json`: Structured extraction results
- `complete_results.json`: Complete workflow results

## Data Structures

### Job Analysis Result

```python
{
    "original_text": str,
    "summary": str,
    "extracted_info": {
        "timeline": List[str],
        "metrics": List[str],
        "must_haves": List[str],
        "nice_to_haves": List[str],
        "extracted_at": str
    },
    "processed_at": str
}
```

### Complete Workflow Result

```python
{
    "job_summary": str,
    "intro_email": str,
    "extracted_data": Dict[str, Any],
    "workflow_completed_at": str
}
```

### Voice Profile Structure

```python
{
    "name": str,
    "role": str,
    "communication_style": {
        "directness": str,
        "technical_depth": str,
        "urgency": str,
        "vision_focus": str,
        "metrics_driven": bool,
        "evangelism": bool
    },
    "key_phrases": List[str],
    "priorities": List[str],
    "tone_descriptors": List[str]
}
```

## Error Handling

### Exception Types

The system may raise the following exceptions:

- `FileNotFoundError`: When input file cannot be found
- `ValueError`: When input data is invalid or malformed
- `TypeError`: When incorrect parameter types are provided
- `RuntimeError`: When processing fails due to system issues

### Error Response Format

```python
{
    "error": str,
    "error_type": str,
    "timestamp": str,
    "context": Dict[str, Any]
}
```

## Integration Examples

### Basic Integration

```python
from genai_agent import GenAIAgent

# Initialize agent
agent = GenAIAgent()

# Process job description
with open('job_description.txt', 'r') as f:
    job_text = f.read()

results = agent.run_complete_workflow(job_text)

# Access results
summary = results['job_summary']
email = results['intro_email']
data = results['extracted_data']
```

### Custom Voice Profile

```python
from genai_agent import EmailGenerator, VoiceProfile

# Create custom voice profile
custom_profile = VoiceProfile(
    name="CTO",
    role="Chief Technology Officer",
    communication_style={
        "directness": "high",
        "technical_depth": "expert",
        "urgency": "moderate"
    },
    key_phrases=["technical excellence", "innovation", "scalability"],
    priorities=["Technology leadership", "Team development"],
    tone_descriptors=["analytical", "strategic", "collaborative"]
)

# Generate email with custom profile
generator = EmailGenerator()
email = generator.generate_intro_email("New tech initiative", custom_profile)
```

### Batch Processing

```python
import os
from genai_agent import GenAIAgent

agent = GenAIAgent()
results = []

# Process multiple job descriptions
for filename in os.listdir('./job_descriptions/'):
    if filename.endswith('.txt'):
        with open(f'./job_descriptions/{filename}', 'r') as f:
            job_text = f.read()
        
        result = agent.run_complete_workflow(job_text)
        result['source_file'] = filename
        results.append(result)

# Save batch results
import json
with open('batch_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## Performance Considerations

### Processing Time

- Job description analysis: ~50-100ms
- Email generation: ~25-50ms
- Complete workflow: ~100-200ms

### Memory Usage

- Minimal memory footprint (~1-5MB per operation)
- No persistent state beyond session
- Efficient string processing

### Optimization Tips

1. **Batch Processing**: Process multiple jobs in single session
2. **Result Caching**: Cache voice profiles for repeated use
3. **Input Validation**: Validate inputs before processing
4. **Error Handling**: Implement proper error handling for production use

## Future API Enhancements

### Planned REST API

```python
# Future REST endpoints
POST /api/v1/analyze
GET /api/v1/profiles
POST /api/v1/profiles
PUT /api/v1/profiles/{id}
DELETE /api/v1/profiles/{id}
```

### Planned Enhancements

- Asynchronous processing support
- Webhook notifications for completion
- Bulk processing endpoints
- Real-time streaming results
- Integration with external LLM APIs

## Support and Troubleshooting

### Common Issues

1. **File Not Found**: Ensure input file path is correct
2. **Permission Errors**: Check file system permissions
3. **Memory Issues**: Process large files in chunks
4. **Encoding Issues**: Ensure UTF-8 encoding for text files

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export GENAI_DEBUG=1
python cli.py --demo
```

### Contact and Support

For technical support and questions:
- GitHub Issues: [Repository Issues Page]
- Documentation: [Repository Wiki]
- Examples: [Examples Directory]

