import re

DISEASE_PRACTICES = {
    "Anthracnose": [
        "Prune and destroy infected leaves/twigs to reduce inoculum.",
        "Spray copper oxychloride or carbendazim as per local agricultural guidance.",
        "Avoid overhead irrigation late in the day to reduce leaf wetness."
    ],
    "Bacterial Canker": [
        "Remove and burn severely infected branches and sanitize pruning tools.",
        "Apply copper-based bactericide during dry weather as recommended locally.",
        "Maintain balanced nutrition and avoid mechanical injury to stems."
    ],
    "Cutting Weevil": [
        "Collect and destroy damaged plant parts and monitor adult weevils.",
        "Use light traps/pheromone traps where available.",
        "Apply approved insecticides only when infestation crosses threshold."
    ],
    "Die Back": [
        "Prune affected shoots 10-15 cm below visible symptoms.",
        "Apply protective fungicide paste on cut surfaces.",
        "Improve orchard drainage and airflow to reduce stress."
    ],
    "Gall Midge": [
        "Remove and destroy galled tissues and fallen debris.",
        "Encourage field sanitation and synchronized orchard spraying.",
        "Use recommended systemic insecticides based on extension advice."
    ],
    "Healthy": [
        "No major disease signs detected; continue regular monitoring.",
        "Maintain balanced irrigation and nutrition schedule.",
        "Scout weekly for early symptoms to act quickly."
    ],
    "Powdery Mildew": [
        "Improve canopy aeration by pruning dense branches.",
        "Apply wettable sulfur or recommended fungicide at early stages.",
        "Avoid excess nitrogen fertilization that promotes tender growth."
    ],
    "Sooty Mould": [
        "Control sap-sucking insects (aphids/scales/mealybugs) causing honeydew.",
        "Wash leaves with water where feasible to remove superficial mould.",
        "Use integrated pest management and avoid unnecessary sprays."
    ],
    "Uncertain": [
        "Image confidence is low; capture a clearer photo in daylight (single leaf, close-up).",
        "Retake from multiple angles and submit 2-3 samples from affected area.",
        "Consult a local plant pathologist/agri-extension officer before spraying chemicals."
    ]
}

ALIASES = {
    "anthracnose": "Anthracnose",
    "bacterial canker": "Bacterial Canker",
    "cutting weevil": "Cutting Weevil",
    "die back": "Die Back",
    "gall midge": "Gall Midge",
    "healthy": "Healthy",
    "powdery mildew": "Powdery Mildew",
    "sooty mould": "Sooty Mould",
    "sooty mold": "Sooty Mould",
}


def normalize_disease_name(name: str) -> str:
    cleaned = re.sub(r"[_-]+", " ", (name or "")).strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return ALIASES.get(cleaned, name.strip() if name else "Uncertain")


def practices_for(disease_name: str):
    normalized = normalize_disease_name(disease_name)
    return DISEASE_PRACTICES.get(
        normalized,
        ["Consult local agricultural extension officer for field-specific recommendations."]
    )
