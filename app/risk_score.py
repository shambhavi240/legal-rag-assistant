def build_risk_score_prompt(context):

    prompt = f"""
    Analyze the legal document risks.

    Explain:
    - financial risks
    - legal risks
    - compliance risks
    - liability concerns

    DO NOT calculate any risk score.

    ONLY explain the risks clearly.

    Document:
    {context}
    """

    return prompt