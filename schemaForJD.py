jd_schema = {
    "type": "object",
    "properties": {
        "role": {
            "type": "string"
        },
        "requiredSkills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "preferredSkills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "requiredExperience": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "responsibilities": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "qualifications": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "role",
        "requiredSkills",
        "preferredSkills",
        "requiredExperience",
        "responsibilities",
        "qualifications"
    ]
}