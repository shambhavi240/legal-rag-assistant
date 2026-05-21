def build_summary_prompt(context):

    prompt = f"""
    You are a legal document summarization AI.

    Summarize the legal document clearly.

    Include:
    - agreement type
    - key obligations
    - deadlines
    - payment terms
    - important clauses
    - risks

    Keep summary concise and professional.

    Document:
    {context}

    Summary:
    """

    return prompt