from app.agents.reasearch_workflow import run_research_workflow


def answer_question(
    question: str,
    document_id: str | None = None,
) -> dict:
    """
    Run the research workflow for a user's question.
    """

    if not question or len(question.strip()) < 3:
        raise ValueError(
            "Please enter a question containing at least 3 characters."
        )

    return run_research_workflow(
        question=question,
        document_id=document_id,
    )