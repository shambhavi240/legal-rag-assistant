def build_chat_prompt(context, query):

    prompt = f"""
    You are an expert legal AI assistant.

    Use ONLY the provided context to answer.

    Give clear, professional,
    human-readable legal explanations.

    Do NOT copy raw clauses directly unless necessary.

    Summarize the meaning of the clauses clearly.

    If the answer is not present,
    say:
    "Answer not found in document."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    return prompt


def build_summary_prompt(context):

    prompt = f"""
    You are a legal document summarization AI.

    Summarize the legal document using ONLY the provided context.

    Include:
    - Agreement type
    - Parties involved
    - Key obligations
    - Important dates and deadlines
    - Payment or compensation terms
    - Important clauses
    - Termination conditions
    - Risks and liabilities

    Keep the summary concise, professional, and factual.

    Do NOT invent information.

    Document:
    {context}

    Summary:
    """

    return prompt


def build_risk_prompt(context):

    prompt = f"""
    You are a legal risk analysis AI.

    Analyze the document and identify:

    - Legal risks
    - Financial risks
    - Compliance concerns
    - Liability concerns

    Explain each risk clearly.

    Do NOT assign numerical risk scores.

    Use ONLY the provided context.

    Document:
    {context}

    Risk Analysis:
    """

    return prompt


def build_clause_prompt(context):

    prompt = f"""
    You are a legal clause extraction AI.

    Extract and explain important clauses.

    Include:
    - Termination clauses
    - Confidentiality clauses
    - Payment clauses
    - Liability clauses
    - Non-compete clauses
    - Non-solicitation clauses

    Use ONLY the provided context.

    Document:
    {context}

    Extracted Clauses:
    """

    return prompt


def build_comparison_prompt(contract1, contract2):

    prompt = f"""
    You are a legal contract comparison AI.

    Compare the two contracts.

    Highlight differences in:

    - Parties involved
    - Obligations
    - Payment terms
    - Deadlines
    - Termination clauses
    - Risks and liabilities

    Contract 1:
    {contract1}

    Contract 2:
    {contract2}

    Comparison:
    """

    return prompt
