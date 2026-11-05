
from youtube_transcript_api import YouTubeTranscriptApi


class TranscriptAgent:

    def __init__(self):
        self.api = YouTubeTranscriptApi()

        self.languages = [
            "en",
            "en-US",
            "en-GB",
            "es",
            "pt",
            "pt-BR"
        ]

    def extract(self, video_id):

        print(f"   🔎 Buscando transcripción: {video_id}")

        transcript = self.api.fetch(
            video_id,
            languages=self.languages
        )

        fragments = transcript.snippets

        text = " ".join(
            fragment.text for fragment in fragments
        )

        return {
            "video_id": video_id,
            "language": transcript.language_code,
            "text": text,
            "fragments": len(fragments),
            "characters": len(text)
        }
