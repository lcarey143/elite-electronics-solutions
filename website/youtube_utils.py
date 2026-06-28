import re

YOUTUBE_ID_PATTERN = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})"
)


def extract_youtube_id(url: str) -> str:
    if not url:
        return ""
    match = YOUTUBE_ID_PATTERN.search(url)
    return match.group(1) if match else ""


def youtube_embed_url(url: str, *, autoplay: bool = False) -> str:
    video_id = extract_youtube_id(url)
    if not video_id:
        return ""
    params = "rel=0&modestbranding=1&playsinline=1"
    if autoplay:
        params += "&autoplay=1&mute=1"
    return f"https://www.youtube.com/embed/{video_id}?{params}"
