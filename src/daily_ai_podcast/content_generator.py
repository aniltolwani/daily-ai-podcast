from typing import List
from playwright.async_api import async_playwright
import os
import asyncio
import browserbase
from browserbase import Browserbase
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BROWSERBASE_API_KEY = os.environ.get("BROWSERBASE_API_KEY", None)
NOTEBOOKLM_EMAIL = os.environ.get("NOTEBOOKLM_EMAIL")
NOTEBOOKLM_PASSWORD = os.environ.get("NOTEBOOKLM_PASSWORD")

async def generate_single_summary(paper_link: str, index: int) -> str:
    """
    Generate audio summary for a single paper link using NotebookLM.

    Args:
        paper_link (str): URL of the paper to summarize
        index (int): Index for naming the output file

    Returns:
        str: File path to the generated audio summary
    """
    # Initialize BrowserBase client
    bb = Browserbase(api_key=BROWSERBASE_API_KEY)
    
    # Create a new session using BrowserBase
    session = bb.sessions.create(project_id="f525ba7a-7f52-478a-81d7-6e198ebea369")

    async with async_playwright() as playwright:
        # Connect to the remote session using the connect URL
        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp('wss://connect.browserbase.com?apiKey='+ BROWSERBASE_API_KEY)
        logger.info(
        "Connected to Browserbase.",
            f"{browser.browser_type.name} version {browser.version}",
        )
        
        async with browser.contexts[0] as context:
            async with context.pages[0] as browser_page:
                # Login to NotebookLM
                logger.info("Logging in to NotebookLM...")
                await browser_page.goto('https://notebooklm.google.com/')
                await browser_page.wait_for_load_state('networkidle')
                await browser_page.locator('#identifierId').fill(NOTEBOOKLM_EMAIL)
                await browser_page.locator('button:has-text("Next")').click()
                await browser_page.wait_for_selector('input[type="password"]', timeout=5000)
                await browser_page.locator('input[type="password"]').fill(NOTEBOOKLM_PASSWORD)

                # Add website
                logger.info("Adding website to NotebookLM...")
                await browser_page.wait_for_selector('mat-chip:has-text("Website")')
                await browser_page.locator('mat-chip:has-text("Website")').click()
                await browser_page.wait_for_selector('input[formcontrolname="newUrl"]')
                await browser_page.locator('input[formcontrolname="newUrl"]').fill(paper_link)
                await browser_page.wait_for_selector('button:has-text("Insert")')
                await browser_page.locator('button:has-text("Insert")').click()

                # Generate summary
                logger.info("Generating summary...")
                await browser_page.wait_for_selector('button:has-text("Generate")')
                await browser_page.locator('button:has-text("Generate")').click()

                # Wait for generation (5 minutes)
                logger.info("Waiting for generation...")
                await asyncio.sleep(300)

                # Download audio
                logger.info("Downloading audio...")
                await browser_page.wait_for_selector('button mat-icon:has-text("more_vert")')
                await browser_page.locator('button mat-icon:has-text("more_vert")').click()
                await browser_page.locator('a mat-icon:has-text("download")').click()

                output_path = f"summary_{index}.mp3"
    
                # Handle download
        # async def handle_download(download):
        #     await download.save_as(output_path)

        # page.on('download', handle_download)
                return output_path
async def generate_audio_summaries(paper_links: List[str]) -> List[str]:
    """
    Generate audio summary for the first paper link using NotebookLM.

    Args:
        paper_links (List[str]): A list of URLs for the papers to summarize.
                                Only the first paper will be processed.

    Returns:
        List[str]: A list containing a single file path to the generated audio summary.
    """
    if not paper_links:
        return []
    
    result = await generate_single_summary(paper_links[0], 0)
    return [result]