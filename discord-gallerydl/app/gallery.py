import os, asyncio
from gallery_dl import config, job

DEFAULT_PATH = "/gallery-dl/"
CONFIG_PATH = os.getenv("DL_CONFIG_PATH", "/config.json")

class GalleryDownloader:

    def __init__(self, loop=None):
        self._setup()
        self._loop = asyncio.get_event_loop() if loop is None else loop

    def _setup(self):
        config.load([CONFIG_PATH])

    async def download(self, url, path=DEFAULT_PATH):
        config.set(("extractor",), "base-directory", path)
        
        downloadJob = job.DownloadJob(url)
        return await self._loop.run_in_executor(None, downloadJob.run)
