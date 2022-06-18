import os
from app.discordClient import DiscordClient

# Get discord token
discordToken = os.getenv("DISCORD_TOKEN")
if discordToken is None:
    raise Exception("Discord token is not provided as an environment variable $DISCORD_TOKEN ")

# Get listening channels
listeningChannels = os.getenv("LISTENING_CHANNELS")
if listeningChannels is None:
    raise Exception("Listening channels are not provided as an environment variable $LISTENING_CHANNELS")
listeningChannels = listeningChannels.split(",")
listeningChannels = [x for x in map(lambda x: int(x), listeningChannels)]

DiscordClient(listeningChannels).run(discordToken)