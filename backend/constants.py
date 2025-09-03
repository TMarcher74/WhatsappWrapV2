from enum import Enum

# Whatsapp max export size currently is 18MB
MAX_UPLOAD_FILE_SIZE = 18874368

# Tags for different routes and paths
class Tags(Enum):
    Status = "Status"
    Analyse = "Analyse"

# List of usable Gemini models
class GeminiModels(str, Enum):
    G25Pro = "gemini-2.5-pro"
    G25Flash = "gemini-2.5-flash"
    G25FlashLite = "gemini-2.5-flash-lite"
    G20Flash = "gemini-2.0-flash"
    G20FlashLite = "gemini-2.0-flash-lite"

class SysMsgActions(str, Enum):
    CreateGroup = "created group"
    AddUser = "added"
    ChangeGrpDesc = "changed the group description"
    ChangeGrpIcon = "changed this group's icon"
    RemoveGrpIcon = "deleted this group's icon"
    ChangeGrpName = "changed the group name from"
    PinMsg = "pinned a message"
    AddAdmin = "now an admin"
    RemoveAdmin = "no longer an admin"

ACTIONS = {
    SysMsgActions.CreateGroup: lambda parts: {
        "author": parts[0].strip(),
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


