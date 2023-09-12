import cloudinary
# from jproperties import Properties
from src.configuration import configs

# configs = Properties()
# with open('src/configuration/config.properties', 'rb') as read_prop:
#   configs.load(read_prop)

cloudinary.config(
  cloud_name = configs.get("CLOUD_NAME").data,
  api_key = configs.get("API_KEY").data,
  api_secret = configs.get("API_SECRET").data
)