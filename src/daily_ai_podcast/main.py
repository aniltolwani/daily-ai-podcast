from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List
from dotenv import load_dotenv
import uvicorn
from daily_ai_podcast.content_generator import generate_audio_summaries

import logging
import asyncio

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "healthy"}

@app.post("/webhook/email")
async def process_email_webhook(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process incoming email data from Zapier webhook.
    
    Args:
        data (Dict[str, Any]): The webhook payload containing email data
        
    Returns:
        Dict[str, Any]: Response with processing status
    """
    logger.info(f"Received webhook data: {data}")
    
    # Basic payload validation
    if 'body_plain' not in data:
        logger.error("Missing email body in webhook data")
        raise HTTPException(status_code=400, detail="Missing email body")
    
    # Extract paper links
    paper_links = extract_paper_links(data['body_plain'])
    if not paper_links:
        logger.info("No paper links found in email body")
        return {"status": "success", "message": "No paper links found"}

    # Log extracted links
    logger.info(f"Found {len(paper_links)} paper links: {paper_links}")

    try:
        # Generate summaries
        logger.info("Starting audio summary generation...")
        audio_files = await generate_audio_summaries(paper_links)
        logger.info(f"Successfully generated {len(audio_files)} audio summaries: {audio_files}")

        return {
            "status": "success", 
            "paper_links": paper_links, 
            "audio_files": audio_files,
            "message": f"Generated {len(audio_files)} audio summaries"
        }
        
    except Exception as e:
        logger.error(f"Error generating audio summaries: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate audio summaries: {str(e)}"
        )

def extract_paper_links(email_body: str) -> List[str]:
    """
    Extract paper links from email body text.
    
    Args:
        email_body (str): Plain text email content
        
    Returns:
        List[str]: List of extracted arxiv URLs
    """
    import re
    arxiv_pattern = r'https?://arxiv\.org/(?:abs|pdf)/\d+\.\d+(?:v\d+)?'
    return list(set(re.findall(arxiv_pattern, email_body)))

def main():
    uvicorn.run(app, host="0.0.0.0", port=80)

if __name__ == "__main__":
    main()
