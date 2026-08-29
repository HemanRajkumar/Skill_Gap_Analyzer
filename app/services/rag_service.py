from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
BASE=Path(__file__).resolve().parents[2];KB=BASE/"data/knowledge_base";VS=BASE/"vectorstore"
def get_vectorstore():
    docs=DirectoryLoader(str(KB),glob="**/*.md",loader_cls=TextLoader,loader_kwargs={"encoding":"utf-8"}).load()
    chunks=RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=120).split_documents(docs)
    emb=GoogleGenerativeAIEmbeddings(model=os.getenv("GEMINI_EMBEDDING_MODEL","gemini-embedding-001"))
    v=Chroma(collection_name="skill_gap_knowledge",embedding_function=emb,persist_directory=str(VS))
    if not v.get().get("ids"):v.add_documents(chunks)
    return v
def generate_roadmap(role,missing,current):
    if not os.getenv("GOOGLE_API_KEY"):raise RuntimeError("GOOGLE_API_KEY is not configured.")
    docs=get_vectorstore().as_retriever(search_kwargs={"k":8}).invoke(f"Learning roadmap for {role}; current: {', '.join(current)}; missing: {', '.join(missing)}")
    context="\n\n---\n\n".join(d.page_content for d in docs)
    prompt=ChatPromptTemplate.from_messages([
        ("system","You are a practical career-learning advisor. Use supplied context for skill-specific claims. Do not invent technologies. Prioritize missing skills. Return Markdown with Skill Priority, Learning Roadmap, Practical Projects, and Expected Outcome."),
        ("human","Target role: {role}\nCurrent skills: {current}\nMissing skills: {missing}\nContext:\n{context}\nCreate the personalized roadmap.")
    ])
    llm=ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL","gemini-3.6-flash"))
    content=(prompt|llm).invoke({"role":role,"current":", ".join(current),"missing":", ".join(missing),"context":context}).content
    if isinstance(content,str):return content
    if isinstance(content,list):return "\n".join(b.get("text","") if isinstance(b,dict) else str(b) for b in content).strip()
    return str(content)



def _skill_path(skill):
    requested = str(skill).strip().lower().replace(" ", "_")
    path = KB / f"{requested}.md"
    if path.exists():
        return path
    for candidate in KB.glob("*.md"):
        if candidate.stem.lower() == requested:
            return candidate
    return None


def analyze_skill_with_gemini(skill, question=None):
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is not configured.")
    path = _skill_path(skill)
    if not path:
        raise ValueError(f"Skill '{skill}' was not found in the knowledge base.")
    source = path.read_text(encoding="utf-8")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical instructor. Use the supplied knowledge-base material as the primary source. Clearly distinguish what is directly supported by the material from general explanatory context. Do not invent APIs, versions, or technologies. Give practical examples and learning advice."),
        ("human", "Skill: {skill}\nUser question: {question}\nKnowledge-base material:\n{source}\n\nProvide a useful Markdown analysis. Cover core concepts, practical examples, common mistakes, interview questions, and a recommended next-learning path when appropriate."),
    ])
    llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"))
    content = (prompt | llm).invoke({
        "skill": skill,
        "question": question or "Give me a complete analysis of this skill.",
        "source": source,
    }).content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content).strip()
    return str(content)
