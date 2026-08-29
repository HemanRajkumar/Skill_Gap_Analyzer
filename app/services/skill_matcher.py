from pathlib import Path
import re,pandas as pd
DATA_PATH=Path(__file__).resolve().parents[2]/"data/roles/role_skills.csv"
ALIASES={"sklearn":"scikit-learn","scikit learn":"scikit-learn","postgres":"postgresql","postgre sql":"postgresql","ml ops":"mlops","rest api":"rest apis","rest":"rest apis","llm":"llms","vector db":"vector databases"}
def normalize_skill(s):
    v=re.sub(r"\s+"," ",s.strip().lower());return ALIASES.get(v,v)
def load_roles():return pd.read_csv(DATA_PATH)
def available_roles():return sorted(load_roles()["role"].drop_duplicates().tolist())
def analyze_role(role,user_skills):
    df=load_roles();rdf=df[df.role.str.casefold()==role.casefold()].copy()
    if rdf.empty:raise ValueError(f"Unknown role: {role}")
    user={normalize_skill(s) for s in user_skills};rdf["n"]=rdf.skill.map(normalize_skill)
    matched=rdf[rdf.n.isin(user)];missing=rdf[~rdf.n.isin(user)];w={"High":3,"Medium":2,"Low":1}
    total=sum(w.get(x,1) for x in rdf.importance);earned=sum(w.get(x,1) for x in matched.importance)
    missing=missing.sort_values("importance",key=lambda s:s.map({"High":0,"Medium":1,"Low":2}))
    return {"role":role,"match_percentage":round(earned/total*100,1) if total else 0.0,"matched_skills":matched.skill.tolist(),"skill_gaps":[{"skill":r.skill,"category":r.category,"importance":r.importance,"reason":f"{r.importance} priority skill for {role}."} for _,r in missing.iterrows()]}
