resume_schema = {
    "type": "object",
    "properties": {
        "skills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "experience": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "projects": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "education": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "certifications": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "skills",
        "experience",
        "projects",
        "education",
        "certifications"
    ]
}