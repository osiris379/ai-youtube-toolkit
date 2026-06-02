"""
ai-youtube-toolkit: generate_metadata.py
Auto-generate YouTube titles, descriptions, and tags using OpenAI API.

Usage:
    python generate_metadata.py --topic "How to build an AI chatbot with Python"

Setup:
    1. Copy .env.example to .env
    2. Add your OpenAI API key: OPENAI_API_KEY=sk-...
    3. pip install openai python-dotenv
"""

import argparse
import json
import os
from dotenv import load_dotenv

load_dotenv()


def generate_youtube_metadata(topic: str, style: str = "educational") -> dict:
    """
    Generate YouTube metadata for a given topic.

    Args:
        topic: The video topic or subject matter
        style: Content style - 'educational', 'tutorial', or 'vlog'

    Returns:
        dict with keys: title, description, tags
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""You are an expert YouTube SEO strategist for tech/AI content creators.

Generate optimized YouTube metadata for a video about:
Topic: {topic}
Style: {style}

Return ONLY valid JSON with this exact structure:
{{
    "title": "compelling clickable title under 70 chars",
    "description": "full 3-paragraph SEO description with timestamps and CTA",
    "tags": ["tag1", "tag2", "tag3", "up to 15 relevant tags"]
}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except ImportError:
        print("OpenAI package not installed. Run: pip install openai python-dotenv")
        return demo_metadata(topic)
    except Exception as e:
        print(f"API error: {e}")
        print("Falling back to demo mode...")
        return demo_metadata(topic)


def demo_metadata(topic: str) -> dict:
    """Returns demo metadata when no API key is available."""
    return {
        "title": f"How I Built {topic[:40]} (Step-by-Step)",
        "description": (
            f"In this video I walk you through {topic} from zero to a working project.\n\n"
            "Timestamps:\n"
            "0:00 - Intro\n"
            "1:30 - What We're Building\n"
            "5:00 - Setup\n"
            "12:00 - Core Logic\n"
            "25:00 - Demo\n\n"
            "Subscribe for more AI and automation content!"
        ),
        "tags": [
            topic.lower()[:30], "python", "ai", "automation",
            "tutorial", "openai", "developer tools", "youtube creator"
        ]
    }


def print_metadata(metadata: dict, topic: str):
    """Pretty-print the generated metadata."""
    print("\n" + "=" * 60)
    print("AI YOUTUBE TOOLKIT - Metadata Generator")
    print("=" * 60)
    print(f"\nTopic: {topic}\n")
    print(f"TITLE:\n{metadata['title']}\n")
    print(f"DESCRIPTION:\n{metadata['description']}\n")
    print(f"TAGS ({len(metadata['tags'])}):\n{', '.join(metadata['tags'])}")
    print("\n" + "=" * 60)
    print("Done! Copy the metadata above into YouTube Studio.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate YouTube metadata with AI"
    )
    parser.add_argument("--topic", type=str, required=True, help="The video topic")
    parser.add_argument(
        "--style", type=str, default="educational",
        choices=["educational", "tutorial", "vlog"],
        help="Content style (default: educational)"
    )
    args = parser.parse_args()

    print(f"\nGenerating metadata for: '{args.topic}'...")
    metadata = generate_youtube_metadata(args.topic, args.style)
    print_metadata(metadata, args.topic)


if __name__ == "__main__":
    main()
