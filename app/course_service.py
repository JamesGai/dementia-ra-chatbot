from app.firestore_client import init_firestore

def _keywords_to_text(keywords):
    """Convert a keyword list into a comma-separated string."""
    return ", ".join(keywords) if isinstance(keywords, list) else ""

def fetch_all_courses():
    """Fetch all course documents and nested module/section/subsection content."""
    db = init_firestore()
    course_docs = db.collection("course").stream()

    courses = []

    for course_doc in course_docs:
        course_data = course_doc.to_dict() or {}
        modules = []

        module_docs = course_doc.reference.collection("module").stream()
        for module_doc in module_docs:
            module_data = module_doc.to_dict() or {}
            sections = []

            section_docs = module_doc.reference.collection("section").stream()
            for section_doc in section_docs:
                section_data = section_doc.to_dict() or {}
                subsections = []

                subsection_docs = section_doc.reference.collection("subsection").stream()
                for subsection_doc in subsection_docs:
                    subsection_data = subsection_doc.to_dict() or {}
                    subsections.append(
                        {
                            "id": subsection_doc.id,
                            "data": subsection_data,
                        }
                    )

                sections.append(
                    {
                        "id": section_doc.id,
                        "data": section_data,
                        "subsections": subsections,
                    }
                )

            modules.append(
                {
                    "id": module_doc.id,
                    "data": module_data,
                    "sections": sections,
                }
            )

        courses.append(
            {
                "id": course_doc.id,
                "data": course_data,
                "modules": modules,
            }
        )

    return courses

def _transform_intro_module(course_id, course_data, module_id, module_data):
    """Transform module-0 introduction metadata into a knowledge object."""
    course_title = course_data.get("title", "")
    module_title = module_data.get("title", "")
    module_description = module_data.get("description", "")
    module_number = module_data.get("number", "")

    semantic_text = f"""
    Course Title: {course_title}
    Module Title: {module_title}
    Module Number: {module_number}
    Module Description: {module_description}
    """

    return {
        "id": f"course_{course_id}_{module_id}",
        "page": "courses",
        "section": "module_intro",
        "content_type": "resource_metadata",
        "semantic_text": semantic_text.strip(),
        "raw_data": {
            "course_id": course_id,
            "course": course_data,
            "module_id": module_id,
            "module": module_data,
        },
    }

def _transform_subsection(course_id, course_data, module_id, module_data, section_id, section_data, subsection_id, subsection_data):
    """Transform a subsection node into a single embedding-ready knowledge object."""
    course_title = course_data.get("title", "")
    module_title = module_data.get("title", "")
    module_number = module_data.get("number", "")
    section_title = section_data.get("title", "")
    section_number = section_data.get("sectionNumber", section_data.get("number", ""))
    subsection_title = subsection_data.get("title", "")
    subsection_number = subsection_data.get("subsectionNumber", subsection_data.get("number", ""))
    keywords = _keywords_to_text(section_data.get("keywords", []))

    semantic_text = f"""
    Course Title: {course_title}
    Module Title: {module_title}
    Module Number: {module_number}
    Section Title: {section_title}
    Section Number: {section_number}
    Subsection Title: {subsection_title}
    Subsection Number: {subsection_number}
    Keywords: {keywords}
    """

    return {
        "id": f"course_{course_id}_{module_id}_{section_id}_{subsection_id}",
        "page": "courses",
        "section": "course_subsection",
        "content_type": "resource_metadata",
        "semantic_text": semantic_text.strip(),
        "raw_data": {
            "course_id": course_id,
            "course": course_data,
            "module_id": module_id,
            "module": module_data,
            "section_id": section_id,
            "section": section_data,
            "subsection_id": subsection_id,
            "subsection": subsection_data,
        },
    }

def transform_course(course):
    """Transform one raw course tree into a list of knowledge objects."""
    course_id = course["id"]
    course_data = course["data"]
    modules = course["modules"]
    transformed = []

    for module in modules:
        module_id = module["id"]
        module_data = module["data"]
        sections = module["sections"]

        module_number = module_data.get("number")
        is_intro_module = module_id == "module-0" or module_number == 0
        if is_intro_module:
            transformed.append(
                _transform_intro_module(course_id, course_data, module_id, module_data)
            )
            continue

        for section in sections:
            section_id = section["id"]
            section_data = section["data"]
            subsections = section["subsections"]

            for subsection in subsections:
                subsection_id = subsection["id"]
                subsection_data = subsection["data"]
                transformed.append(
                    _transform_subsection(
                        course_id,
                        course_data,
                        module_id,
                        module_data,
                        section_id,
                        section_data,
                        subsection_id,
                        subsection_data,
                    )
                )

    return transformed

def get_course_knowledge_objects():
    """Return all course knowledge as JSON objects ready for embedding."""
    raw_courses = fetch_all_courses()

    structured_courses = []
    for course in raw_courses:
        structured_courses.extend(transform_course(course))

    return structured_courses
