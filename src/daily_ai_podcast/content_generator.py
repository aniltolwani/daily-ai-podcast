from typing import List
from playwright.async_api import async_playwright
import os
import asyncio

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
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"wss://connect.browserbase.com?apiKey={BROWSERBASE_API_KEY}")
        context = (await browser.contexts())[0]
        page = (await context.pages())[0]

        # Login to NotebookLM
        await page.goto('https://notebooklm.google.com/')
        await page.wait_for_load_state('networkidle')
        await page.locator('#identifierId').fill(NOTEBOOKLM_EMAIL)
        await page.locator('button:has-text("Next")').first.click()
        await page.wait_for_selector('input[type="password"]', timeout=5000)
        await page.locator('input[type="password"]').fill(NOTEBOOKLM_PASSWORD)
        
        # Add website
        await page.wait_for_selector('mat-chip:has-text("Website")')
        await page.locator('mat-chip:has-text("Website")').first.click()
        await page.wait_for_selector('input[formcontrolname="newUrl"]')
        await page.locator('input[formcontrolname="newUrl"]').fill(paper_link)
        await page.wait_for_selector('button:has-text("Insert")')
        await page.locator('button:has-text("Insert")').first.click()

        # Generate summary
        await page.wait_for_selector('button:has-text("Generate")')
        await page.locator('button:has-text("Generate")').first.click()

        # Wait for generation (5 minutes)
        await asyncio.sleep(300)

        # Download audio
        await page.wait_for_selector('button mat-icon:has-text("more_vert")')
        await page.locator('button mat-icon:has-text("more_vert")').first.click()
        await page.locator('a mat-icon:has-text("download")').first.click()

        output_path = f"summary_{index}.mp3"
        
        # Handle download
        async def handle_download(download):
            await download.save_as(output_path)

        page.on('download', handle_download)
        await browser.close()
        
        return output_path

async def generate_audio_summaries(paper_links: List[str]) -> List[str]:
    """
    Generate audio summaries for the given paper links using NotebookLM in parallel.

    Args:
        paper_links (List[str]): A list of URLs for the papers to summarize.

    Returns:
        List[str]: A list of file paths to the generated audio summaries.
    """
    tasks = [
        generate_single_summary(link, idx) 
        for idx, link in enumerate(paper_links)
    ]
    return await asyncio.gather(*tasks)