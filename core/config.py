import os

class Config:
    # Example: toggle between demo and production mode
    MODE = os.environ.get("AI_ED_MODE", "demo")
    COUNTRY = os.environ.get("AI_ED_COUNTRY", "universal")
    SUPPORTED_LANGUAGES = ["en", "zh", "fr"]
    DATA_PATH = os.environ.get("AI_ED_DATA_PATH", "data/")
    LOG_LEVEL = os.environ.get("AI_ED_LOG_LEVEL", "INFO")

    # Extend for real DB/API settings as needed

config = Config()
