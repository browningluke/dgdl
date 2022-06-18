import os, json, logging
from app.discordClient import DiscordClient

from app.defaults import MAPPING_PATH, LOGGER_NAME

def setupLogging():
    global logger
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)


def loadToken():
    # Get discord token
    discordToken = os.getenv("DISCORD_TOKEN")
    if discordToken is None:
        raise Exception("Discord token is not provided as an environment variable $DISCORD_TOKEN ")

    return discordToken


def loadMappings():
    MAP_PATH = os.getenv("MAPPING_PATH", MAPPING_PATH)
    
    with open(MAP_PATH, "r") as f:
        return json.load(f)


def main():
    setupLogging()
    
    mappings = loadMappings()
    discordToken = loadToken()

    logger.info("Creating Discord client...")
    DiscordClient(mappings).run(discordToken)


if __name__ == "__main__":
    main()
