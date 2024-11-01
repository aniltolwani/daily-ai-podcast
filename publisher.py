import requests
from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET
from datetime import datetime
import os
from pathlib import Path
import base64
from io import BytesIO

class PodcastPublisher:
    def __init__(self, github_repo: str, github_token: str):
        """
        Initialize the podcast publisher using GitHub Pages.

        Args:
            github_repo (str): Repository name in format 'username/repo'
            github_token (str): GitHub personal access token
        """
        self.github_repo = github_repo
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.api_base = 'https://api.github.com'
        
    def _upload_audio_file(self, audio_file: str) -> Optional[str]:
        """Upload audio file to GitHub repository."""
        try:
            # Read file content
            with open(audio_file, 'rb') as f:
                content = f.read()
            
            # Create file in 'audio' directory
            filename = Path(audio_file).name
            path = f'audio/{filename}'
            
            # GitHub API requires base64 encoded content
            import base64
            encoded = base64.b64encode(content).decode()
            
            # Create or update file through GitHub API
            response = requests.put(
                f'{self.api_base}/repos/{self.github_repo}/contents/{path}',
                headers=self.headers,
                json={
                    'message': f'Add podcast episode: {filename}',
                    'content': encoded
                }
            )
            
            if response.status_code in (201, 200):
                return f'https://raw.githubusercontent.com/{self.github_repo}/main/{path}'
                
        except Exception as e:
            print(f"Error uploading audio file: {e}")
        return None

    def _update_rss_feed(self, audio_url: str, title: str, description: str) -> bool:
        """Update RSS feed in GitHub repository."""
        try:
            # First, get the current feed content if it exists
            response = requests.get(
                f'{self.api_base}/repos/{self.github_repo}/contents/feed.xml',
                headers=self.headers
            )
            
            if response.status_code == 200:
                # Update existing feed
                current_file = response.json()
                current_content = base64.b64decode(current_file['content']).decode()
                tree = ET.ElementTree(ET.fromstring(current_content))
            else:
                # Create new feed
                tree = self._create_new_feed()
            
            # Add new item
            channel = tree.getroot().find('channel')
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'description').text = description
            ET.SubElement(item, 'enclosure', {
                'url': audio_url,
                'type': 'audio/mpeg',
                'length': '0'  # GitHub doesn't provide direct file size
            })
            ET.SubElement(item, 'pubDate').text = datetime.utcnow().strftime(
                '%a, %d %b %Y %H:%M:%S GMT'
            )
            ET.SubElement(item, 'guid').text = audio_url
            
            # Convert to string
            from io import BytesIO
            feed_content = BytesIO()
            tree.write(feed_content, encoding='UTF-8', xml_declaration=True)
            encoded_content = base64.b64encode(feed_content.getvalue()).decode()
            
            # Update feed.xml in repository
            update_response = requests.put(
                f'{self.api_base}/repos/{self.github_repo}/contents/feed.xml',
                headers=self.headers,
                json={
                    'message': f'Update RSS feed with new episode: {title}',
                    'content': encoded_content,
                    'sha': response.json()['sha'] if response.status_code == 200 else None
                }
            )
            
            return update_response.status_code in (201, 200)
                
        except Exception as e:
            print(f"Error updating RSS feed: {e}")
            return False

    def _create_new_feed(self) -> ET.ElementTree:
        """Create a new RSS feed structure."""
        rss = ET.Element('rss', {'version': '2.0'})
        channel = ET.SubElement(rss, 'channel')
        
        ET.SubElement(channel, 'title').text = 'Daily AI Papers Podcast'
        ET.SubElement(channel, 'description').text = 'Daily summaries of interesting AI research papers'
        ET.SubElement(channel, 'link').text = f'https://{self.github_repo.split("/")[0]}.github.io/{self.github_repo.split("/")[1]}'
        
        return ET.ElementTree(rss)

    def publish_podcast(self, podcast_file: str, title: str, description: str) -> bool:
        """
        Publish a podcast episode by uploading the audio and updating the RSS feed.

        Args:
            podcast_file (str): Path to the podcast audio file
            title (str): Episode title
            description (str): Episode description

        Returns:
            bool: True if podcast was successfully published
        """
        # Upload audio file
        audio_url = self._upload_audio_file(podcast_file)
        if not audio_url:
            return False
            
        # Update RSS feed
        return self._update_rss_feed(audio_url, title, description)

