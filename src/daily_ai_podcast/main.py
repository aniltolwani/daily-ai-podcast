from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List
from dotenv import load_dotenv
import uvicorn

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
    # Basic payload validation
    if 'body_plain' not in data:
        raise HTTPException(status_code=400, detail="Missing email body")
    
    # Extract paper links
    paper_links = extract_paper_links(data['body_plain'])
    if not paper_links:
        return {"status": "success", "message": "No paper links found"}

    # Log paper links for debugging
    print(f"Extracted paper links: {paper_links}")

    # Return paper links for testing
    return {"status": "success", "paper_links": paper_links}

    # Commented out the rest of the code for now
    # # Generate summaries
    # audio_files = generate_audio_summaries(paper_links)
    # if not audio_files:
    #     return {"status": "success", "message": "No audio files generated"}

    # # Merge audio files
    # final_podcast = merge_audio_files(audio_files)

    # # Initialize publisher
    # publisher = PodcastPublisher(
    #     github_repo=os.getenv("GITHUB_REPO"),
    #     github_token=os.getenv("GITHUB_TOKEN")
    # )

    # # Generate title and description
    # title = f"AI Papers Summary - {datetime.now().strftime('%B %d, %Y')}"
    # description = f"Summary of {len(paper_links)} AI research papers from arXiv"

    # # Publish podcast
    # success = publisher.publish_podcast(final_podcast, title, description)
    
    # return {
    #     "status": "success" if success else "error",
    #     "message": "Podcast published" if success else "Failed to publish podcast",
    #     "paper_count": len(paper_links),
    #     "audio_files": len(audio_files)
    # }

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
