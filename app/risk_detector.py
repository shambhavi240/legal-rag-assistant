def build_risk_prompt(context):

    prompt = f"""
    You are a legal contract risk analysis AI.

    Analyze the contract clauses below.

    Identify:
    - risky clauses
    - unfair terms
    - hidden penalties
    - automatic renewals
    - liability concerns
    - ambiguous wording

    Explain risks clearly.

    Contract Clauses:
    {context}

    Risk Analysis:
    """

    return prompt

def build_risky_clauses_prompt(context):

    prompt = f"""
    Extract ONLY the exact risky legal clauses
    from this document.

    Return short exact clauses only.

    Document:
    {context}
    """

    return prompt