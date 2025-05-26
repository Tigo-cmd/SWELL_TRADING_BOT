import re

def escape_markdown_v2(text:str) -> str:
  """
  Escapes special characters for Telegram MarkdownV2 formatting
  """
  # Escape all MarkdownV2 special characters
  return re.sub(r'(!@/$%^&+[_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)