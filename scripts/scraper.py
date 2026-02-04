import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
from database import upload_to_gcs
from utils import clean_text

async def scrape_linkedin_jobs():
    async with async_playwright() as p:
        # 1. Jalankan Browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 2. Buka URL Pencarian (Contoh: Data Engineer di Indonesia)
        url = "https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=Indonesia"
        print(f"Membuka halaman: {url}")
        await page.goto(url, wait_until="networkidle")

        # 3. Ambil data (Selektor ini khusus untuk halaman publik LinkedIn)
        jobs = []
        job_cards = await page.locator(".base-search-card__info").all()
        
        for card in job_cards[:10]: # Ambil 10 teratas dulu buat tes
            title = await card.locator(".base-search-card__title").inner_text()
            company = await card.locator(".base-search-card__subtitle").inner_text()
            
            jobs.append({
                "job_title": clean_text(title),
                "company": clean_text(company),
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        # 4. Simpan ke CSV Lokal
        df = pd.DataFrame(jobs)
        filename = f"loker_de_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        local_path = f"data/{filename}"
        df.to_csv(local_path, index=False)
        print(f"Data tersimpan di {local_path}")

        # 5. Upload ke GCS
        upload_to_gcs(local_path, f"raw_jobs/{filename}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_linkedin_jobs())
