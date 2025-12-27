import json


def load_schemes(file_path="schemes.json"):
    """
    Load scheme data from JSON file
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_scheme_eligibility(user, scheme):
    """
    Check if a user is eligible for a single scheme.
    Returns (True/False, reasons)
    """
    reasons = []
    eligibility = scheme.get("eligibility", {})

    # Age check
    if "min_age" in eligibility:
        if user["age"] >= eligibility["min_age"]:
            reasons.append("Age criteria satisfied")
        else:
            return False, ["Age criteria not satisfied"]

    # Income check
    if "max_income" in eligibility:
        if user["income"] <= eligibility["max_income"]:
            reasons.append("Income criteria satisfied")
        else:
            return False, ["Income exceeds allowed limit"]

    # Category check
    if "categories" in eligibility:
        if user["category"] in eligibility["categories"]:
            reasons.append("Category criteria satisfied")
        else:
            return False, ["Category not eligible"]

    # Occupation check
    if "occupation" in eligibility:
        if user["occupation"].lower() == eligibility["occupation"].lower():
            reasons.append("Occupation criteria satisfied")
        else:
            return False, ["Occupation not eligible"]

    return True, reasons


def find_eligible_schemes(user):
    """
    Find all schemes a user is eligible for
    """
    schemes = load_schemes()
    eligible_schemes = []

    for scheme in schemes:
        is_eligible, reasons = check_scheme_eligibility(user, scheme)
        if is_eligible:
            eligible_schemes.append({
                "scheme_id": scheme["id"],
                "scheme_name": scheme["name"],
                "benefits": scheme["benefits"],
                "reasons": reasons,
                "documents": scheme["documents"]
            })

    return eligible_schemes


# Temporary test (will be removed later)
if __name__ == "__main__":
    test_user = {
        "age": 62,
        "income": 150000,
        "category": "OBC",
        "occupation": "farmer"
    }

    results = find_eligible_schemes(test_user)

    print("Eligible Schemes:")
    for scheme in results:
        print(f"- {scheme['scheme_name']}")
        for reason in scheme["reasons"]:
            print(f"  • {reason}")
