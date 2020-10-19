def print_unicode_codepoint(text: str):
    print(text.encode("raw_unicode_escape"))


emojies = {
    "emoji_up": "⬆",  # same as "\u2b06" aka hex 0x2b06
    "discord_emoji_up": "⬆️",  # same as "\u2b06\ufe0f"
    "some_text": "Some 😀 emojis 😇"
}

if __name__ == "__main__":
    for emoji in emojies.values():
        print_unicode_codepoint(emoji)
