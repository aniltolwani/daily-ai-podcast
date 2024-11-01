from typing import List, Dict, Any
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook/email")
async def process_email_webhook(request: Request) -> Dict[str, Any]:
    """
    Process incoming email data from Zapier webhook.
    
    Args:
        request (Request): FastAPI request object containing email data
        
    Returns:
        Dict[str, Any]: Response with extracted paper links and status
    """
    email_data = await request.json()
    
    # Extract email body from Zapier's payload
    email_body: str = email_data.get('body_plain', '')
    
    # Extract paper links
    paper_links: List[str] = extract_paper_links(email_body)
    
    return {
        "status": "success",
        "paper_links": paper_links
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
    
    # Pattern for matching arxiv links
    arxiv_pattern = r'https?://arxiv\.org/(?:abs|pdf)/\d+\.\d+(?:v\d+)?'
    
    # Find all matches
    links = re.findall(arxiv_pattern, email_body)
    
    return links
