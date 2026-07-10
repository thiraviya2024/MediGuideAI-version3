def is_medical_document(text):
    """
    Check whether the uploaded PDF is a medical document.
    Returns:
        True, matched_keywords
        False, matched_keywords
    """

    medical_keywords = [
        "patient",
        "doctor",
        "hospital",
        "diagnosis",
        "prescription",
        "medicine",
        "tablet",
        "capsule",
        "blood",
        "laboratory",
        "lab",
        "test",
        "scan",
        "x-ray",
        "mri",
        "ct",
        "ecg",
        "hemoglobin",
        "glucose",
        "bp",
        "pulse",
        "discharge",
        "medical",
        "clinic",
        "treatment",
        "report"
    ]

    text = text.lower()

    matched = []

    for word in medical_keywords:
        if word in text:
            matched.append(word)

    return len(matched) >= 3, matched