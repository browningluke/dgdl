import os, asyncio, logging
from gallery_dl import config, job

from .defaults import GDL_DOWNLOAD_PATH, GDL_CONFIG_PATH, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

DOWNLOAD_PATH = os.getenv("GDL_DOWNLOAD_PATH", GDL_DOWNLOAD_PATH)
CONFIG_PATH = os.getenv("GDL_CONFIG_PATH", GDL_CONFIG_PATH)


class GalleryDownloader:

    def __init__(self, loop=None):
        self._setup()
        self._loop = asyncio.get_event_loop() if loop is None else loop

    def _setup(self):
        config.load([CONFIG_PATH])

    async def download(self, url, path=GDL_DOWNLOAD_PATH):
        config.set(("extractor",), "base-directory", path)

        logging.info(f"Attempting download to path: {path}")

        downloadJob = job.DownloadJob(url)
        return await self._loop.run_in_executor(None, downloadJob.run)
