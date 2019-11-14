def print_unicode_codepoint(text: str, *, hex_value: bool = False):
    print(text.encode("raw_unicode_escape"))
    if hex_value and len(text) == 1:
        print("Hex:", hex(ord(text)))


emoji_up = "⬆"  # same as "\u2b06"
discord_emoji_up = "⬆️"  # same as "\u2b06\ufe0f"
some_text = "Some 😀 emojis 😇"

print_unicode_codepoint(emoji_up)
print_unicode_codepoint(discord_emoji_up)
print_unicode_codepoint(some_text)
