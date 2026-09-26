"""FINNIE package — AI Finance Assistant capstone (Interview Kickstart).

FINNIE routes every user query through a LangGraph router into one of six
specialist agents, all behind a single chat interface:

    finance_qa        General finance questions (RAG-grounded)
    portfolio         Portfolio analysis & holdings math
    market            Live market quotes & analysis
    goals             Goal-based financial planning
    news              News synthesis on markets/companies
    tax_education     Tax EDUCATION only — never tax advice
"""
from finnie.config import settings

__all__ = ["settings"]
__version__ = "1.0.0"
