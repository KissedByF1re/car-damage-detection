def has_damage(text: str) -> bool:
    keywords = ["сервис", "service", "город", "city"]
    return any(word in text.lower() for word in keywords)