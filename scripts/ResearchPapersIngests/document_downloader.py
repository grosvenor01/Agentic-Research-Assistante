import ssl
import aiohttp
import asyncio
from pathlib import Path
import json

async def download_pdf(url: str, save_dir: str = "docs") -> str:
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    filename = url.split("/")[-1]
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    file_path = Path(save_dir) / filename

    # Ignore SSL certificates errors
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.get(url) as response:
            content = await response.read()

    file_path.write_bytes(content)
    return str(file_path)

async def download_pdfs(urls: list[str]) -> list[str]:
    return await asyncio.gather(
        *(download_pdf(url) for url in urls)
    )

def extract_ids(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            print(f"Processing line {line_number}")
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if "id" in obj:
                    yield obj["id"]
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON on line {line_number}: {line[:50]}...")

if __name__ == "__main__":

    urls = []
    for id in extract_ids("sources/arxiv-metadata-oai-snapshot.json"):
        urls.append(f"https://arxiv.org/pdf/{id}.pdf")
    print(len(urls))
    asyncio.run(download_pdfs(urls[:10])) # just  took the first 10 for testing