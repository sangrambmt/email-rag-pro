from fastapi import FastAPI, HTTPException
from app.schemas import AskRequest, AskResponse
from app.retrieve import retrieve
from app.prompt import build_prompt
from app.llm import generate_answer

app = FastAPI(title="Email RAG Pro")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        chunks = retrieve(req.question, req.top_k, req.file_filter)
        
        if not chunks:
            return AskResponse(
                answer="I couldn't find any relevant information in the emails.",
                sources=[]
            )
        
        prompt = build_prompt(req.question, chunks)
        answer = generate_answer(prompt)
        sources = list({c["meta"]["file"] for c in chunks})
        
        return AskResponse(answer=answer, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))