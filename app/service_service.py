from app.firestore_client import init_firestore

def fetch_all_services():
    """Fetch all raw service documents from Firestore."""
    db = init_firestore()
    docs = db.collection("services").stream()

    services = []

    for doc in docs:
        data = doc.to_dict()
        services.append({
            "id": doc.id,
            "data": data
        })

    return services

def transform_service(doc_id, data):
    """Convert a raw service record into a knowledge JSON object for embeddings."""
    name = data.get("name", "")
    description = data.get("description", "")
    address = data.get("address", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    link = data.get("link", "")
    keywords = data.get("keywords", [])

    keyword_text = ", ".join(keywords) if isinstance(keywords, list) else ""

    semantic_text = f"""
    Service Name: {name}
    Description: {description}
    Address: {address}
    Email: {email}
    Phone: {phone}
    Website: {link}
    Keywords: {keyword_text}
    """

    return {
        "id": f"service_{doc_id}",
        "page": "services",
        "section": "service_metadata",
        "content_type": "resource_metadata",
        "semantic_text": semantic_text.strip(),
        "raw_data": data
    }

def get_service_knowledge_objects():
    """Return all service knowledge as JSON objects ready for embedding."""
    raw_services = fetch_all_services()

    structured_services = []

    for service in raw_services:
        transformed = transform_service(service["id"], service["data"])
        structured_services.append(transformed)

    return structured_services
