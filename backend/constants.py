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


