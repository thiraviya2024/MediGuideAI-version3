# utils/report_classifier.py

import re
from typing import Dict, Tuple, List

def detect_report_type(text: str) -> Tuple[str, float, List[str]]:
    """
    Detects the type of medical report with confidence score.
    Returns: (report_type, confidence, matched_keywords)
    """
    
    text_lower = text.lower()
    text_sample = text_lower[:4000]  # Use first 4000 chars for efficiency
    
    # Define report type patterns
    report_patterns = {
        "Blood Test Report": [
            "hemoglobin", "hb", "rbc", "wbc", "platelet", "glucose", "cholesterol",
            "triglycerides", "ldl", "hdl", "sgpt", "creatinine", "blood test", "lab report"
        ],
        "Prescription": [
            "rx", "tablet", "capsule", "bd", "tds", "od", "sos", "prescription",
            "dr\.", "doctor", "sig:", "take", "tab\."
        ],
        "Laboratory Report": [
            "laboratory", "pathology", "biochemistry", "hematology", "microbiology",
            "reference range", "test name", "result"
        ],
        "X-Ray Report": [
            "x-ray", "xray", "radiograph", "chest pa", "ap view", "impression:",
            "radiologist"
        ],
        "MRI Report": [
            "mri", "magnetic resonance", "t1", "t2", "flair", "contrast",
            "axial", "sagittal", "coronal"
        ],
        "CT Scan Report": [
            "ct scan", "computed tomography", "contrast enhanced", "axial section",
            "hrct"
        ],
        "ECG Report": [
            "ecg", "electrocardiogram", "heart rate", "sinus rhythm", "st elevation",
            "pr interval", "qrs"
        ],
        "Discharge Summary": [
            "discharge summary", "admitted on", "discharged on", "hospital course",
            "final diagnosis", "follow up advice"
        ],
        "Medical Certificate": [
            "medical certificate", "fitness certificate", "medically fit",
            "rest for", "from date", "to date"
        ]
    }
    
    best_type = "Unknown Medical Document"
    best_score = 0.0
    best_keywords = []
    
    for report_type, keywords in report_patterns.items():
        matched = [kw for kw in keywords if kw in text_sample]
        score = len(matched) / len(keywords) if keywords else 0
        
        if score > best_score:
            best_score = score
            best_type = report_type
            best_keywords = matched[:8]  # Top 8 keywords
    
    # Boost confidence for very strong matches
    if best_score > 0.6:
        confidence = min(98, int(best_score * 100) + 15)
    elif best_score > 0.4:
        confidence = int(best_score * 100) + 10
    else:
        confidence = int(best_score * 100)
    
    return best_type, confidence, best_keywords


def get_report_type_display(report_type: str) -> str:
    """Returns nice display name with emoji"""
    emojis = {
        "Blood Test Report": "🩸",
        "Prescription": "💊",
        "Laboratory Report": "🔬",
        "X-Ray Report": "📸",
        "MRI Report": "🧠",
        "CT Scan Report": "🩻",
        "ECG Report": "❤️",
        "Discharge Summary": "🏥",
        "Medical Certificate": "📜",
        "Unknown Medical Document": "📄"
    }
    return f"{emojis.get(report_type, '📄')} {report_type}"
