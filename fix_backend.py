import re

# Update main.py
with open('backend/main.py', 'r', encoding='utf-8') as f:
    main_text = f.read()

main_replace = '''@app.post("/api/chat")
def chat_with_ai(query: schemas.ChatQuery, request: Request, db: Session = Depends(database.get_db)):
    gemini_key = request.headers.get("x-gemini-key")
    if not gemini_key:
        raise HTTPException(status_code=401, detail="Missing Gemini API Key")
    # For now, hardcode user_id=1 as we are in single-user mode
    try:
        response_text = ai_engine.generate_chat_response(db, 1, query.message, gemini_key)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''

main_text = re.sub(r'@app\.post\("/api/chat"\).*?raise HTTPException\(status_code=500, detail=str\(e\)\)', main_replace, main_text, flags=re.DOTALL)
with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(main_text)

# Update ai_engine.py
with open('backend/ai_engine.py', 'r', encoding='utf-8') as f:
    ai_text = f.read()

ai_text = ai_text.replace('def generate_chat_response(db: Session, user_id: int, message: str) -> str:', 'def generate_chat_response(db: Session, user_id: int, message: str, api_key: str) -> str:')
ai_text = ai_text.replace('genai.configure(api_key=os.getenv("GEMINI_API_KEY"))', 'genai.configure(api_key=api_key)')

with open('backend/ai_engine.py', 'w', encoding='utf-8') as f:
    f.write(ai_text)
