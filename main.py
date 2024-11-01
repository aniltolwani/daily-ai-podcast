from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List
import os
from content_generator import generate_audio_summaries
from audio_processor import merge_audio_files
from publisher import publish_podcast

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
    # Basic payload validation
    if 'body_plain' not in data:
        raise HTTPException(status_code=400, detail="Missing email body")
    
    # Extract paper links
    paper_links = extract_paper_links(data['body_plain'])
    if not paper_links:
        return {"status": "success", "message": "No paper links found"}

    # Generate summaries
    audio_files = generate_audio_summaries(paper_links)
    if not audio_files:
        return {"status": "success", "message": "No audio files generated"}

    # Merge audio files
    final_podcast = merge_audio_files(audio_files)

    # Publish podcast
    success = publish_podcast(final_podcast)
    
    return {
        "status": "success" if success else "error",
        "message": "Podcast published" if success else "Failed to publish podcast",
        "paper_count": len(paper_links),
        "audio_files": len(audio_files)
    }

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
