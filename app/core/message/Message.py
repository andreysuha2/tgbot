class Message:
    def __init__(self, source: str, source_id: str, message_id: str, text: str) -> None:
        self.source = source
        self.source_id = source_id
        self.message_id = message_id
        self.text = text

    def __repr__(self) -> str:
        return f"""
            source: {self.source}
            source_id: {self.source_id}
            message_id: {self.message_id}
            text: {self.text}
        """

    def __eq__(self, other: object) -> bool:
        return self.source == other.source and self.source_id == other.source_id and self.message_id == other.message_id