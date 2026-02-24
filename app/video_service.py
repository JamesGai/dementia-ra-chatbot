from app.firestore_client import init_firestore


def fetch_all_videos():
    db = init_firestore()
    docs = db.collection("videos").stream()

    videos = []

    for doc in docs:
        data = doc.to_dict()
        videos.append({
            "id": doc.id,
            "data": data
        })

    return videos


def transform_video(doc_id, data):
    title = data.get("title", "")
    description = data.get("description", "")
    keywords = data.get("keywords", [])
    module = data.get("module", "")
    duration = data.get("durationText", "")

    keyword_text = ", ".join(keywords) if isinstance(keywords, list) else ""

    semantic_text = f"""
    Video Title: {title}
    Description: {description}
    Keywords: {keyword_text}
    Module: {module}
    Duration: {duration}
    """

    return {
        "id": f"video_{doc_id}",
        "page": "videos",
        "section": "video_metadata",
        "content_type": "resource_metadata",
        "semantic_text": semantic_text.strip(),
        "raw_data": data
    }


def get_video_knowledge_objects():
    raw_videos = fetch_all_videos()

    structured_videos = []

    for video in raw_videos:
        transformed = transform_video(video["id"], video["data"])
        structured_videos.append(transformed)

    return structured_videos