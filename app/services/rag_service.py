from pathlib import Path
import os

from dotenv import load_dotenv

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(override=True)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE = Path(__file__).resolve().parents[2]

KB = BASE / "data" / "knowledge_base"
VS = BASE / "vectorstore"


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite",
)

GEMINI_EMBEDDING_MODEL = os.getenv(
    "GEMINI_EMBEDDING_MODEL",
    "gemini-embedding-001",
)


# ============================================================
# VECTOR STORE / RAG KNOWLEDGE BASE
# ============================================================

def get_vectorstore():
    """
    Load the local knowledge base, split it into chunks,
    create embeddings, and store/retrieve them using Chroma.
    """

    docs = DirectoryLoader(
        str(KB),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
        },
    ).load()

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    ).split_documents(docs)

    emb = GoogleGenerativeAIEmbeddings(
        model=GEMINI_EMBEDDING_MODEL,
    )

    vectorstore = Chroma(
        collection_name="skill_gap_knowledge",
        embedding_function=emb,
        persist_directory=str(VS),
    )

    # Add documents only when the vector store is empty.
    if not vectorstore.get().get("ids"):
        vectorstore.add_documents(chunks)

    return vectorstore


# ============================================================
# ROADMAP GENERATION
# ============================================================

def generate_roadmap(role, missing, current):
    """
    Generate a personalized learning roadmap using
    Gemini + the local Chroma knowledge base.
    """

    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured."
        )

    # Retrieve relevant knowledge-base documents.
    retriever = get_vectorstore().as_retriever(
        search_kwargs={
            "k": 8,
        }
    )

    docs = retriever.invoke(
        f"""
        Learning roadmap for {role};
        current skills: {', '.join(current)};
        missing skills: {', '.join(missing)}
        """
    )

    context = "\n\n---\n\n".join(
        document.page_content
        for document in docs
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a practical career-learning advisor.

                Use the supplied knowledge-base context for
                skill-specific claims.

                Do not invent technologies.

                Prioritize missing skills.

                Return Markdown with these sections:

                1. Skill Priority
                2. Learning Roadmap
                3. Practical Projects
                4. Expected Outcome
                """,
            ),
            (
                "human",
                """
                Target role: {role}

                Current skills:
                {current}

                Missing skills:
                {missing}

                Knowledge-base context:
                {context}

                Create a personalized learning roadmap.
                """,
            ),
        ]
    )

    # Use the model from .env.
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
    )

    content = (
        prompt | llm
    ).invoke(
        {
            "role": role,
            "current": ", ".join(current),
            "missing": ", ".join(missing),
            "context": context,
        }
    ).content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            block.get("text", "")
            if isinstance(block, dict)
            else str(block)
            for block in content
        ).strip()

    return str(content)


# ============================================================
# SKILL FILE FINDER
# ============================================================

def _skill_path(skill):
    """
    Find a skill's Markdown file in the local knowledge base.
    """

    requested = (
        str(skill)
        .strip()
        .lower()
        .replace(" ", "_")
    )

    path = KB / f"{requested}.md"

    if path.exists():
        return path

    for candidate in KB.glob("*.md"):
        if candidate.stem.lower() == requested:
            return candidate

    return None


# ============================================================
# AI SKILL ANALYSIS
# ============================================================

def analyze_skill_with_gemini(skill, question=None):
    """
    Analyze a specific skill using the local knowledge base
    and Gemini.
    """

    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured."
        )

    path = _skill_path(skill)

    if not path:
        raise ValueError(
            f"Skill '{skill}' was not found in the knowledge base."
        )

    source = path.read_text(
        encoding="utf-8"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a technical instructor.

                Use the supplied knowledge-base material
                as the primary source.

                Clearly distinguish what is directly supported
                by the material from general explanatory context.

                Do not invent APIs, versions, or technologies.

                Give practical examples and learning advice.
                """,
            ),
            (
                "human",
                """
                Skill:
                {skill}

                User question:
                {question}

                Knowledge-base material:
                {source}

                Provide a useful Markdown analysis.

                Cover:

                - Core concepts
                - Practical examples
                - Common mistakes
                - Interview questions
                - Recommended next-learning path
                """,
            ),
        ]
    )

    # Use the model from .env.
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
    )

    content = (
        prompt | llm
    ).invoke(
        {
            "skill": skill,
            "question": question
            or "Give me a complete analysis of this skill.",
            "source": source,
        }
    ).content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            block.get("text", "")
            if isinstance(block, dict)
            else str(block)
            for block in content
        ).strip()

    return str(content)