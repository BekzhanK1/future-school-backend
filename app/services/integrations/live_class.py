import os


class LiveClassService:
    def __init__(self):
        self.provider = os.getenv("LIVE_CLASS_API_PROVIDER", "stub")

    async def create_meeting(self, topic: str) -> str:
        # TODO: integrate with real provider (Zoom/Meet)
        return f"https://live.example.com/meet/{topic.replace(' ', '-')}-stub"


live_class_service = LiveClassService()



