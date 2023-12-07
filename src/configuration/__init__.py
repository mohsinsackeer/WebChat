from jproperties import Properties

configs = Properties()
with open('src/configuration/config.properties', 'rb') as read_prop:
  configs.load(read_prop)

__all__ = ["configs"]