import asyncio, discord, validators
from .gallery import GalleryDownloader

class DiscordClient(discord.Client):

    def __init__(self, listeningChannels):
        self._loop = asyncio.get_event_loop()
        super().__init__(loop=self._loop)

        self._galleryDownloader = GalleryDownloader(self._loop)
        self._listeningChannels = listeningChannels
        self._setup()

    def _setup(self):
        self._initCommandsAndEvents()
        pass

    def _initCommandsAndEvents(self):

        @self.event
        async def on_ready():
            print(f"Logged in as {self.user}")

        @self.event
        async def on_message(message):
            if message.channel.id in self._listeningChannels:
                if DiscordClient._ensureValidURL(message.content):
                    print(message.content)

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

                    # Do download
                    try:
                        status = await self._galleryDownloader.download(message.content)
                        if status != 0: raise
                    except Exception:
                        await message.clear_reactions()
                        await message.add_reaction("❌")
                        return

                    await message.clear_reactions()
                    await message.add_reaction("✅")
                    for x in reaction_list:
                        await message.add_reaction(x)
                else:
                    print(f"Ignoring (wrong type): {message.content}")
            else:
                print(f"Ignoring (outside channel): {message.content}")

    @staticmethod
    def _ensureValidURL(string):
        return validators.url(string)

    def run(self, token):
        try:
            self._loop.run_until_complete(self.start(token))
        except KeyboardInterrupt:
            print("Logging out")
            self._loop.run_until_complete(self.close())
            # cancel all tasks lingering
        finally:
            self._loop.close()
