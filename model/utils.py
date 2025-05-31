import re

def escape_markdown_v2(text:str) -> str:
  """
  Escapes special characters for Telegram MarkdownV2 formatting
  """
  # Escape all MarkdownV2 special characters
  return re.sub(r'(!@/$%^&+[_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)

def shorten_address(address: str, chars: int = 4) -> str:
    """Shorten an ethereum address to a specific number of characters"""
    return f"{address[:chars]}...{address[-chars:]}"