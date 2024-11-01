from typing import List
from playwright.sync_api import sync_playwright
import os
import time

BROWSERBASE_API_KEY = os.environ.get("BROWSERBASE_API_KEY", None)
NOTEBOOKLM_EMAIL = os.environ.get("NOTEBOOKLM_EMAIL")
NOTEBOOKLM_PASSWORD = os.environ.get("NOTEBOOKLM_PASSWORD")

def generate_audio_summaries(paper_links: List[str]) -> List[str]:
    """
    Generate audio summaries for the given paper links using NotebookLM.

    Args:
        paper_links (List[str]): A list of URLs for the papers to summarize.

    Returns:
        List[str]: A list of file paths to the generated audio summaries.
    """
    audio_files: List[str] = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"wss://connect.browserbase.com?apiKey={BROWSERBASE_API_KEY}")
        context = browser.contexts()[0]
        page = context.pages()[0]

        # Login to NotebookLM
        page.goto('https://notebooklm.google.com/')
        page.wait_for_load_state('networkidle')
        page.locator('#identifierId').fill(NOTEBOOKLM_EMAIL)
        page.locator('button:has-text("Next")').first.click()
        page.wait_for_selector('input[type="password"]', timeout=5000)
        page.locator('input[type="password"]').fill(NOTEBOOKLM_PASSWORD)
        page.locator('button:has-text("Next")').first.click()
        page.wait_for_load_state('networkidle')

        for link in paper_links:
            # Create new notebook
            page.wait_for_selector('project-button:has-text("New Notebook")')
            page.locator('project-button:has-text("New Notebook")').first.click()

            # Add website
            page.wait_for_selector('mat-chip:has-text("Website")')
            page.locator('mat-chip:has-text("Website")').first.click()
            page.wait_for_selector('input[formcontrolname="newUrl"]')
            page.locator('input[formcontrolname="newUrl"]').fill(link)
            page.wait_for_selector('button:has-text("Insert")')
            page.locator('button:has-text("Insert")').first.click()

            # Generate summary
            page.wait_for_selector('button:has-text("Generate")')
            page.locator('button:has-text("Generate")').first.click()

            # Wait for generation (5 minutes)
            time.sleep(300)

            # Download audio
            page.wait_for_selector('button mat-icon:has-text("more_vert")')
            page.locator('button mat-icon:has-text("more_vert")').first.click()
            page.locator('a mat-icon:has-text("download")').first.click()

            # TODO: Wait for download to complete and get the file path
            # This part depends on how the browser is configured to save downloads
            # You might need to use page.on('download') event handler to get the download path
            # For now, we'll use a placeholder
            audio_file_path = f"summary_{len(audio_files)}.mp3"
            audio_files.append(audio_file_path)

            page.on('download', lambda download: download.save_as(f"summary_{len(audio_files)}.mp3"))

        browser.close()

    return audio_files
