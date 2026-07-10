import re
from typing import Dict

def extract_health_data(text: str) -> Dict:
    """
    Extracts key health parameters from medical report text using regex + keyword matching.
    Returns structured data for dashboard.
    """
    text_lower = text.lower()
    
    health_data = {
        "Hemoglobin": {"value": "N/A", "unit": "g/dL", "status": "Unknown"},
        "Blood Sugar": {"value": "N/A", "unit": "mg/dL", "status": "Unknown"},
        "HbA1c": {"value": "N/A", "unit": "%", "status": "Unknown"},
        "LDL": {"value": "N/A", "unit": "mg/dL", "status": "Unknown"},
        "Cholesterol": {"value": "N/A", "unit": "mg/dL", "status": "Unknown"},
        "Creatinine": {"value": "N/A", "unit": "mg/dL", "status": "Unknown"},
        "Platelet": {"value": "N/A", "unit": "", "status": "Unknown"},
    }

    # Hemoglobin
    hb_match = re.search(r'hemoglobin[:\s]*(\d+\.?\d*)', text_lower)
    if hb_match:
        hb = float(hb_match.group(1))
        health_data["Hemoglobin"]["value"] = str(hb)
        health_data["Hemoglobin"]["status"] = "Normal" if 12 <= hb <= 17 else "Low" if hb < 12 else "High"

    # HbA1c
    hba1c_match = re.search(r'hba1c[:\s]*(\d+\.?\d*)', text_lower)
    if hba1c_match:
        hba1c = float(hba1c_match.group(1))
        health_data["HbA1c"]["value"] = str(hba1c)
        if hba1c < 5.7:
            health_data["HbA1c"]["status"] = "Normal"
        elif hba1c < 6.5:
            health_data["HbA1c"]["status"] = "Prediabetes"
        else:
            health_data["HbA1c"]["status"] = "High"

    # Blood Sugar / Glucose
    sugar_match = re.search(r'(blood sugar|glucose|fasting)[:\s]*(\d+\.?\d*)', text_lower)
    if sugar_match:
        sugar = float(sugar_match.group(2))
        health_data["Blood Sugar"]["value"] = str(sugar)
        health_data["Blood Sugar"]["status"] = "Normal" if sugar < 140 else "High"

    # LDL Cholesterol
    ldl_match = re.search(r'ldl[:\s]*(\d+\.?\d*)', text_lower)
    if ldl_match:
        ldl = float(ldl_match.group(1))
        health_data["LDL"]["value"] = str(ldl)
        health_data["LDL"]["status"] = "Normal" if ldl < 100 else "Borderline" if ldl < 130 else "High"

    # Total Cholesterol
    chol_match = re.search(r'(total cholesterol|cholesterol)[:\s]*(\d+\.?\d*)', text_lower)
    if chol_match:
        chol = float(chol_match.group(2))
        health_data["Cholesterol"]["value"] = str(chol)

    return health_data


def calculate_health_score(health_data: Dict) -> int:
    """Simple scoring system"""
    score = 100
    
    penalties = {
        "HbA1c": 12 if health_data["HbA1c"]["status"] in ["Prediabetes", "High"] else 0,
        "LDL": 10 if health_data["LDL"]["status"] == "High" else 5 if health_data["LDL"]["status"] == "Borderline" else 0,
        "Blood Sugar": 10 if health_data["Blood Sugar"]["status"] == "High" else 0,
        "Hemoglobin": 15 if health_data["Hemoglobin"]["status"] in ["Low", "High"] else 0,
    }
    
    for penalty in penalties.values():
        score -= penalty
        
    return max(70, score)  # Minimum score 70


def get_status_color(status: str) -> str:
    if status in ["Normal", "Healthy"]:
        return "🟢"
    elif status in ["Prediabetes", "Borderline"]:
        return "🟡"
    else:
        return "🔴"