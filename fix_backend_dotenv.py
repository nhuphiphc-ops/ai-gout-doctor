import re
with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add dotenv import at the top
if 'from dotenv import load_dotenv' not in text:
    text = 'import os\nfrom dotenv import load_dotenv\nload_dotenv()\n' + text

# Change chat endpoint
replacement = '''@app.post("/api/chat")
def chat_with_ai(query: schemas.ChatQuery, request: Request, db: Session = Depends(database.get_db)):
    gemini_key = request.headers.get("x-gemini-key") or os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise HTTPException(status_code=401, detail="Missing Gemini API Key")
    # For now, hardcode user_id=1 as we are in single-user mode
    try:
        response_text = ai_engine.generate_chat_response(db, 1, query.message, gemini_key)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''

text = re.sub(r'@app\.post\("/api/chat"\).*?raise HTTPException\(status_code=500, detail=str\(e\)\)', replacement, text, flags=re.DOTALL)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
