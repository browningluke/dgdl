import asyncio, discord, validators, logging
from .gallery import GalleryDownloader

from .defaults import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class DiscordClient(discord.Client):

    def __init__(self, mappings):
        self._loop = asyncio.get_event_loop()
        super().__init__(loop=self._loop)

        self._galleryDownloader = GalleryDownloader(self._loop)
        self._mappings = mappings
        self._listeningChannels = list(mappings.keys())

        logging.info(f"Monitoring channels: {self._listeningChannels}")

        self._setup()

    def _setup(self):
        @self.event
        async def on_ready():
            logger.info(f"Logged in as {self.user}")

        @self.event
        async def on_message(message):
            if str(message.channel.id) in self._listeningChannels:
                if DiscordClient._ensureValidURL(message.content):
                    logger.info(f"({message.channel.id}) Caught URL: {message.content}")

                    await message.add_reaction("📥")
                    await message.add_reaction("↔️")
                    await message.add_reaction("↕️")

                    reaction, user = await self.wait_for('reaction_add',
                        check=lambda reaction, user: 
                            user == message.author and str(reaction.emoji) == "📥",
                        timeout=(60 * 60 * 2))

                    # Clear reactions
                    reaction_list = []
                    for x in message.reactions:
                        if x.count > 1 and str(x.emoji) != "📥":
                            reaction_list.append(x)

                    await message.clear_reactions()
                    await message.add_reaction("🔄")

                    path = self._mappings[str(message.channel.id)]
                    logger.info(f"Mapping to path: {path}")

                    # Do download
                    try:
                        status = await self._galleryDownloader.download(message.content, path=path)
                        if status != 0: raise
                    except Exception as e:
                        await message.clear_reactions()
                        await message.add_reaction("❌")
                        logger.error(e, exc_info=1)
                        return

                    await message.clear_reactions()
                    await message.add_reaction("✅")
                    for x in reaction_list:
                        await message.add_reaction(x)
                else:
                    logger.info(f"Ignoring (wrong type): {message.content}")
            else:
                logger.info(f"Ignoring (outside channel): {message.content}")

    @staticmethod
    def _ensureValidURL(string):
        return validators.url(string)

    def run(self, token):
        try:
            self._loop.run_until_complete(self.start(token))
        except KeyboardInterrupt:
            logger.info("Logging out")
            self._loop.run_until_complete(self.close())
            # cancel all tasks lingering
        finally:
            self._loop.close()
