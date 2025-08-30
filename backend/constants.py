from enum import Enum

# Whatsapp max export size currently is 18MB
MAX_UPLOAD_FILE_SIZE = 18874368

# Tags for different routes and paths
class Tags(Enum):
    Status = "Status"
    Analyse = "Analyse"

# List of usable Gemini models
class GeminiModels(Enum):
    G25Pro = "gemini-2.5-pro"
    G25Flash = "gemini-2.5-flash"
    G25FlashLite = "gemini-2.5-flash-lite"
    G20Flash = "gemini-2.0-flash"
    G20FlashLite = "gemini-2.0-flash-lite"

DOMAIN_MAPS = {
    "youtube": ["youtube.com","m.youtube.com","youtu.be"],
    "youtube_music": ["music.youtube.com"],
    "spotify": ["spotify.com","open.spotify.com"],
    "twitter": ["twitter.com", "x.com"],
    "instagram": ["instagram.com", "instagr.am"],
    "facebook": ["facebook.com","fb.com","m.facebook.com"],
    "reddit": ["reddit.com","old.reddit.com"],
    "github": ["github.com"],
    "canva": ["canva.com"],
    "chatgpt": ["chatgpt.com"],
    "discord": ["discord.com","discord.gg"],


}


