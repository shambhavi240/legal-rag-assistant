def classify_clause(text):

    text = text.lower()

    categories = []

    if "confidential" in text:
        categories.append("Confidentiality")

    if "terminate" in text:
        categories.append("Termination")

    if "non-compete" in text:
        categories.append("Non-Compete")

    if "indemn" in text:
        categories.append("Indemnity")

    if "liability" in text:
        categories.append("Liability")

    if "arbitration" in text:
        categories.append("Dispute Resolution")

    return categories