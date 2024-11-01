import requests
from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET
from datetime import datetime
import os
from pathlib import Path

class PodcastPublisher:
    def __init__(self, rss_path: str, audio_host_url: str, feed_host_url: str):
        """
        Initialize the podcast publisher.

        Args:
            rss_path (str): Local path to RSS feed XML file
            audio_host_url (str): Base URL where audio files will be hosted
            feed_host_url (str): Base URL where the RSS feed will be hosted
        """
        self.rss_path = rss_path
        self.audio_host_url = audio_host_url.rstrip('/')
        self.feed_host_url = feed_host_url.rstrip('/')
        
    def _upload_audio_file(self, audio_file: str) -> Optional[str]:
        """
        Upload the audio file to hosting service.

        Args:
            audio_file (str): Path to audio file

        Returns:
            Optional[str]: URL of uploaded file or None if upload failed
        """
        try:
            with open(audio_file, 'rb') as f:
                response = requests.post(
                    f"{self.audio_host_url}/upload",
                    files={'file': f},
                    headers={'Authorization': f"Bearer {os.getenv('AUDIO_HOST_TOKEN')}"}
                )
                if response.status_code == 200:
                    return f"{self.audio_host_url}/{response.json()['file_path']}"
        except Exception as e:
            print(f"Error uploading audio file: {e}")
        return None

    def _update_rss_feed(self, audio_url: str, title: str, description: str) -> bool:
        """
        Update the RSS feed with new episode.

        Args:
            audio_url (str): URL of the hosted audio file
            title (str): Episode title
            description (str): Episode description

        Returns:
            bool: True if RSS feed was updated successfully
        """
        try:
            tree = ET.parse(self.rss_path)
            channel = tree.getroot().find('channel')
            
            # Create new item element
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'description').text = description
            ET.SubElement(item, 'enclosure', {
                'url': audio_url,
                'type': 'audio/mpeg',
                'length': str(Path(audio_url).stat().st_size)
            })
            ET.SubElement(item, 'pubDate').text = datetime.utcnow().strftime(
                '%a, %d %b %Y %H:%M:%S GMT'
            )
            ET.SubElement(item, 'guid').text = audio_url
            
            # Save updated RSS feed
            tree.write(self.rss_path, encoding='UTF-8', xml_declaration=True)
            
            # Upload RSS feed to hosting
            with open(self.rss_path, 'rb') as f:
                response = requests.put(
                    f"{self.feed_host_url}/feed.xml",
                    data=f,
                    headers={'Authorization': f"Bearer {os.getenv('FEED_HOST_TOKEN')}"}
                )
                return response.status_code == 200
                
        except Exception as e:
            print(f"Error updating RSS feed: {e}")
            return False

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
