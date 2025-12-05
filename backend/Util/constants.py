from cachetools import TTLCache
from backend.Util.enums import SysMsgActions

# Chat data is temp stored in cache and cleared after 10 min
file_cache = TTLCache(maxsize=100, ttl=6000)

# Whatsapp max export size currently is 18MB
MAX_UPLOAD_FILE_SIZE = 18874368

ACTIONS = {
    SysMsgActions.CreateGroup: lambda parts: {
        "author": parts[0].strip(),
        "name":  parts[1].strip()
    },
    SysMsgActions.AddUser: lambda parts: {
        "author": parts[0].strip(),
        "added": parts[1].strip() if len(parts) > 1 else None,
    },
    SysMsgActions.ChangeGrpDesc: lambda parts: {
        "author": parts[0].strip(),
    },
    SysMsgActions.ChangeGrpIcon: lambda parts: {
        "author": parts[0].strip(),
    },
    SysMsgActions.RemoveGrpIcon: lambda parts: {
        "author": parts[0].strip(),
    },
    SysMsgActions.ChangeGrpName: lambda parts: {
        "author": parts[0].strip(),
        "name_change": parts[1].strip() if len(parts) > 1 else None,
    },
    SysMsgActions.PinMsg: lambda parts: {
        "author": parts[0].strip(),
    },
    SysMsgActions.AddAdmin: lambda parts: {
        "author": parts[0].strip(),
    },
    SysMsgActions.RemoveAdmin: lambda parts: {
        "author": parts[0].strip(),
    },
}

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


