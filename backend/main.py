from datetime import date, datetime, timedelta
from typing import Optional, List
import os
import shutil
import cloudinary
import cloudinary.uploader
from fastapi import FastAPI, Depends, HTTPException, status, Query, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
import database
import models
import schemas
import auth
import ai_engine
import export_service

# Initialize DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="AI Personal Health Assistant API",
    description="Backend API for managing gout, cardio, and metabolic health indicators.",
    version="1.0.0"
)

# Cloudinary config - dung bien moi truong tren Railway
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", ""),
    api_key=os.getenv("CLOUDINARY_API_KEY", ""),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", ""),
    secure=True
)

# Mount static files (fallback cho local dev)
os.makedirs("static/avatars", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS setup - chap nhan ca Vercel va LAN
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://*.vercel.app",
    os.getenv("FRONTEND_URL", ""),
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open to all - supports Vercel, LAN, Cloudflare Tunnel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Health Assistant API is running"}

# --- AUTHENTICATION ---

@app.post("/api/auth/google")
async def google_login(payload: dict, db: Session = Depends(database.get_db)):
    id_token = payload.get("id_token")
    if not id_token:
        raise HTTPException(status_code=400, detail="Missing ID Token")
        
    google_user = await auth.verify_google_token(id_token)
    if not google_user:
        raise HTTPException(status_code=401, detail="Invalid Google Token")
        
    email = google_user["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            email=email,
            name=google_user["name"],
            avatar_url=google_user["picture"],
            age=47,
            height=1.70,
            target_weight=62.5
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
    access_token = auth.create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "name": user.name,
            "avatar_url": user.avatar_url,
            "age": user.age,
            "height": user.height,
            "target_weight": user.target_weight
        }
    }

@app.post("/api/auth/mock")
def mock_login(db: Session = Depends(database.get_db)):
    """
    Mock login bypass for easy local deployment and testing.
    """
    default_email = "mrphi@health.local"
    user = db.query(models.User).filter(models.User.email == default_email).first()
    if not user:
        user = models.User(
            email=default_email,
            name="Mr. Phi",
            avatar_url="",
            age=47,
            height=1.70,
            target_weight=62.5
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
    access_token = auth.create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "name": user.name,
            "avatar_url": user.avatar_url,
            "age": user.age,
            "height": user.height,
            "target_weight": user.target_weight
        }
    }

# --- USER PROFILE ---

@app.get("/api/user/profile", response_model=schemas.UserResponse)
def get_profile(current_user: models.User = Depends(auth.get_current_user)):
    current_user.google_fit_connected = current_user.google_fit_refresh_token is not None
    return current_user

@app.put("/api/user/profile", response_model=schemas.UserResponse)
def update_profile(profile_data: schemas.UserBase, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    current_user.name = profile_data.name
    current_user.age = profile_data.age
    current_user.height = profile_data.height
    current_user.target_weight = profile_data.target_weight
    
    db.commit()
    db.refresh(current_user)
    current_user.google_fit_connected = current_user.google_fit_refresh_token is not None
    return current_user

@app.post("/api/user/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    file_ext = os.path.splitext(file.filename)[1]
    if file_ext.lower() not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file ảnh định dạng JPG, JPEG, PNG, WEBP, GIF.")
    
    # Dung Cloudinary neu da cau hinh, fallback ve local neu chua
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    if cloud_name:
        # Upload len Cloudinary cloud
        try:
            file_bytes = await file.read()
            upload_result = cloudinary.uploader.upload(
                file_bytes,
                public_id=f"health_app/avatars/user_{current_user.id}",
                overwrite=True,
                resource_type="image",
                transformation=[{"width": 400, "height": 400, "crop": "fill", "gravity": "face"}]
            )
            avatar_url = upload_result["secure_url"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi upload ảnh lên Cloudinary: {str(e)}")
    else:
        # Fallback: luu file local (cho dev)
        os.makedirs("static/avatars", exist_ok=True)
        filename = f"avatar_{current_user.id}{file_ext.lower()}"
        filepath = os.path.join("static", "avatars", filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        avatar_url = f"/static/avatars/{filename}"
        
    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    
    return {"avatar_url": avatar_url}

# --- GOOGLE FIT ENDPOINTS ---

@app.get("/api/auth/google-fit/url")
def get_google_fit_url(current_user: models.User = Depends(auth.get_current_user)):
    url = auth.get_google_fit_auth_url(current_user.email)
    return {"url": url}

@app.get("/api/auth/google-fit/callback")
async def google_fit_callback(request: Request, code: str, state: str, db: Session = Depends(database.get_db)):
    # Exchange code for tokens
    tokens = await auth.exchange_google_fit_code(code)
    if not tokens:
        raise HTTPException(status_code=400, detail="Failed to exchange authorization code for tokens")
        
    refresh_token = tokens.get("refresh_token")
    
    # Save refresh token to user (state parameter is the user's email)
    user = db.query(models.User).filter(models.User.email == state).first()
    if user and refresh_token:
        user.google_fit_refresh_token = refresh_token
        db.commit()
        
    # Redirect back to the frontend.
    # Determine domain dynamically from headers to support Cloudflare Tunnel perfectly!
    host = request.headers.get("host", "localhost:3000")
    proto = request.headers.get("x-forwarded-proto", "http")
    
    if "localhost:8000" in host:
        redirect_url = "http://localhost:5173/?google_fit=success"
    else:
        redirect_url = f"{proto}://{host}/?google_fit=success"
        
    return RedirectResponse(url=redirect_url)

@app.post("/api/user/sync-steps", response_model=schemas.HealthLogResponse)
async def sync_google_fit_steps(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.google_fit_refresh_token:
        raise HTTPException(status_code=400, detail="Tài khoản chưa được kết nối với Google Fit.")
        
    access_token = await auth.get_google_fit_access_token(current_user.google_fit_refresh_token)
    if not access_token:
        raise HTTPException(status_code=401, detail="Không thể làm mới mã truy cập Google Fit.")
        
    steps = await auth.fetch_google_fit_steps(access_token)
    
    today = date.today()
    log = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id,
        models.HealthLog.log_date == today
    ).first()
    
    if not log:
        log = models.HealthLog(
            user_id=current_user.id,
            log_date=today
        )
        db.add(log)
        
    log.steps = steps
    # Calculate appropriate walking duration if not set
    if log.walking_duration == 0:
        log.walking_duration = max(5, int(steps / 120))
        
    # Recalculate AI scores since steps changed
    analysis = ai_engine.calculate_scores(log, current_user.age, current_user.height)
    log.gout_score = analysis["gout_score"]
    log.cardio_score = analysis["cardio_score"]
    log.metabolic_score = analysis["metabolic_score"]
    log.qol_score = analysis["qol_score"]
    log.ai_recommendations = analysis["recommendations"]
    
    db.commit()
    db.refresh(log)
    return log

# --- HEALTH LOGS ---

@app.get("/api/logs/today", response_model=Optional[schemas.HealthLogResponse])
def get_today_log(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    today = date.today()
    log = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id,
        models.HealthLog.log_date == today
    ).first()
    return log

@app.post("/api/logs/morning", response_model=schemas.HealthLogResponse)
def create_morning_log(
    log_input: schemas.MorningLogInput, 
    current_user: models.User = Depends(auth.get_current_user), 
    db: Session = Depends(database.get_db)
):
    today = date.today()
    log = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id,
        models.HealthLog.log_date == today
    ).first()

    if not log:
        log = models.HealthLog(
            user_id=current_user.id,
            log_date=today
        )
        db.add(log)

    # Update morning fields
    log.morning_completed = True
    log.weight = log_input.weight
    log.bp_systolic = log_input.bp_systolic
    log.bp_diastolic = log_input.bp_diastolic
    log.heart_rate = log_input.heart_rate
    log.sleep_quality = log_input.sleep_quality
    log.sleep_duration = log_input.sleep_duration
    
    log.joint_pain = log_input.joint_pain
    log.pain_big_toe = log_input.pain_big_toe
    log.pain_ankle = log_input.pain_ankle
    log.pain_knee = log_input.pain_knee
    log.pain_foot = log_input.pain_foot
    log.pain_severity = log_input.pain_severity
    
    log.fatigue_level = log_input.fatigue_level
    log.stress_level = log_input.stress_level
    log.mood_level = log_input.mood_level

    # Run AI calculations
    analysis = ai_engine.calculate_scores(log, current_user.age, current_user.height)
    log.gout_score = analysis["gout_score"]
    log.cardio_score = analysis["cardio_score"]
    log.metabolic_score = analysis["metabolic_score"]
    log.qol_score = analysis["qol_score"]
    log.ai_recommendations = analysis["recommendations"]

    db.commit()
    db.refresh(log)
    return log

@app.post("/api/logs/afternoon", response_model=schemas.HealthLogResponse)
def create_afternoon_log(
    log_input: schemas.AfternoonLogInput,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    today = date.today()
    log = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id,
        models.HealthLog.log_date == today
    ).first()

    if not log:
        # If morning log wasn't filled, create new log
        log = models.HealthLog(
            user_id=current_user.id,
            log_date=today
        )
        db.add(log)

    log.afternoon_completed = True
    log.steps = log_input.steps
    log.walking_duration = log_input.walking_duration
    log.exercise_duration = log_input.exercise_duration
    log.water_intake = log_input.water_intake
    
    log.had_alcohol = log_input.had_alcohol
    log.had_beer = log_input.had_beer
    log.had_seafood = log_input.had_seafood
    log.had_organ_meat = log_input.had_organ_meat
    log.had_red_meat = log_input.had_red_meat
    log.had_sweets = log_input.had_sweets

    # Handle foods list (clear and recreate)
    db.query(models.LogFood).filter(models.LogFood.log_id == log.id).delete()
    for food_name in log_input.foods_consumed:
        if food_name.strip():
            db.add(models.LogFood(log_id=log.id, food_name=food_name.strip()))

    # Handle medications list (clear and recreate)
    db.query(models.LogMedication).filter(models.LogMedication.log_id == log.id).delete()
    for med_name in log_input.medications:
        if med_name.strip():
            db.add(models.LogMedication(log_id=log.id, med_name=med_name.strip()))

    # Commit nested tables first so they are available for recalculating
    db.commit()
    db.refresh(log)

    # Recalculate AI scores (since food, alcohol, water, steps might have changed)
    analysis = ai_engine.calculate_scores(log, current_user.age, current_user.height)
    log.gout_score = analysis["gout_score"]
    log.cardio_score = analysis["cardio_score"]
    log.metabolic_score = analysis["metabolic_score"]
    log.qol_score = analysis["qol_score"]
    log.ai_recommendations = analysis["recommendations"]

    db.commit()
    db.refresh(log)
    return log

@app.get("/api/logs/history", response_model=List[schemas.HealthLogResponse])
def get_logs_history(
    limit: int = 100,
    offset: int = 0,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    logs = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id
    ).order_by(models.HealthLog.log_date.desc()).offset(offset).limit(limit).all()
    return logs

# --- ANALYTICS & DASHBOARD ---

@app.get("/api/analytics/correlation", response_model=schemas.CorrelationResponse)
def get_food_correlations(
    days: int = 30,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    analysis = ai_engine.calculate_food_correlation(db, current_user.id, days_limit=days)
    return analysis

@app.get("/api/analytics/dashboard", response_model=schemas.DashboardResponse)
def get_dashboard_data(
    view: str = Query("week", description="View type: day (7 logs), week, month, year"),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    today = date.today()
    today_log = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id,
        models.HealthLog.log_date == today
    ).first()

    trends = []
    
    if view == "day":
        # Last 7 individual days
        start_date = today - timedelta(days=7)
        logs = db.query(models.HealthLog).filter(
            models.HealthLog.user_id == current_user.id,
            models.HealthLog.log_date >= start_date
        ).order_by(models.HealthLog.log_date.asc()).all()
        
        for l in logs:
            trends.append(schemas.ScoreTrend(
                date=l.log_date.strftime("%d/%m"),
                gout_score=l.gout_score,
                cardio_score=l.cardio_score,
                metabolic_score=l.metabolic_score,
                qol_score=l.qol_score,
                weight=l.weight,
                bp_systolic=l.bp_systolic,
                bp_diastolic=l.bp_diastolic,
                steps=l.steps,
                water_intake=l.water_intake
            ))
            
    elif view == "week":
        # Group by week (last 12 weeks)
        start_date = today - timedelta(weeks=12)
        logs = db.query(models.HealthLog).filter(
            models.HealthLog.user_id == current_user.id,
            models.HealthLog.log_date >= start_date
        ).order_by(models.HealthLog.log_date.asc()).all()
        
        # Group in python by week number
        weekly_groups = {}
        for l in logs:
            # Get start date of the week (Monday)
            monday = l.log_date - timedelta(days=l.log_date.weekday())
            week_key = monday.strftime("%d/%m")
            if week_key not in weekly_groups:
                weekly_groups[week_key] = []
            weekly_groups[week_key].append(l)
            
        for week_str, w_logs in weekly_groups.items():
            valid_weights = [l.weight for l in w_logs if l.weight]
            valid_systolics = [l.bp_systolic for l in w_logs if l.bp_systolic]
            valid_diastolics = [l.bp_diastolic for l in w_logs if l.bp_diastolic]
            
            trends.append(schemas.ScoreTrend(
                date=f"T. {week_str}",
                gout_score=sum(l.gout_score for l in w_logs) / len(w_logs),
                cardio_score=sum(l.cardio_score for l in w_logs) / len(w_logs),
                metabolic_score=sum(l.metabolic_score for l in w_logs) / len(w_logs),
                qol_score=sum(l.qol_score for l in w_logs) / len(w_logs),
                weight=sum(valid_weights) / len(valid_weights) if valid_weights else None,
                bp_systolic=int(sum(valid_systolics) / len(valid_systolics)) if valid_systolics else None,
                bp_diastolic=int(sum(valid_diastolics) / len(valid_diastolics)) if valid_diastolics else None,
                steps=int(sum(l.steps for l in w_logs) / len(w_logs)),
                water_intake=sum(l.water_intake for l in w_logs) / len(w_logs)
            ))
            
    elif view == "month":
        # Group by month (last 12 months)
        start_date = today - timedelta(days=365)
        logs = db.query(models.HealthLog).filter(
            models.HealthLog.user_id == current_user.id,
            models.HealthLog.log_date >= start_date
        ).order_by(models.HealthLog.log_date.asc()).all()
        
        monthly_groups = {}
        for l in logs:
            month_key = l.log_date.strftime("%m/%Y")
            if month_key not in monthly_groups:
                monthly_groups[month_key] = []
            monthly_groups[month_key].append(l)
            
        for month_str, m_logs in monthly_groups.items():
            valid_weights = [l.weight for l in m_logs if l.weight]
            valid_systolics = [l.bp_systolic for l in m_logs if l.bp_systolic]
            valid_diastolics = [l.bp_diastolic for l in m_logs if l.bp_diastolic]
            
            trends.append(schemas.ScoreTrend(
                date=f"Thg {month_str.split('/')[0]}",
                gout_score=sum(l.gout_score for l in m_logs) / len(m_logs),
                cardio_score=sum(l.cardio_score for l in m_logs) / len(m_logs),
                metabolic_score=sum(l.metabolic_score for l in m_logs) / len(m_logs),
                qol_score=sum(l.qol_score for l in m_logs) / len(m_logs),
                weight=sum(valid_weights) / len(valid_weights) if valid_weights else None,
                bp_systolic=int(sum(valid_systolics) / len(valid_systolics)) if valid_systolics else None,
                bp_diastolic=int(sum(valid_diastolics) / len(valid_diastolics)) if valid_diastolics else None,
                steps=int(sum(l.steps for l in m_logs) / len(m_logs)),
                water_intake=sum(l.water_intake for l in m_logs) / len(m_logs)
            ))
            
    elif view == "year":
        # Group by year
        logs = db.query(models.HealthLog).filter(
            models.HealthLog.user_id == current_user.id
        ).order_by(models.HealthLog.log_date.asc()).all()
        
        yearly_groups = {}
        for l in logs:
            year_key = l.log_date.strftime("%Y")
            if year_key not in yearly_groups:
                yearly_groups[year_key] = []
            yearly_groups[year_key].append(l)
            
        for year_str, y_logs in yearly_groups.items():
            valid_weights = [l.weight for l in y_logs if l.weight]
            valid_systolics = [l.bp_systolic for l in y_logs if l.bp_systolic]
            valid_diastolics = [l.bp_diastolic for l in y_logs if l.bp_diastolic]
            
            trends.append(schemas.ScoreTrend(
                date=year_str,
                gout_score=sum(l.gout_score for l in y_logs) / len(y_logs),
                cardio_score=sum(l.cardio_score for l in y_logs) / len(y_logs),
                metabolic_score=sum(l.metabolic_score for l in y_logs) / len(y_logs),
                qol_score=sum(l.qol_score for l in y_logs) / len(y_logs),
                weight=sum(valid_weights) / len(valid_weights) if valid_weights else None,
                bp_systolic=int(sum(valid_systolics) / len(valid_systolics)) if valid_systolics else None,
                bp_diastolic=int(sum(valid_diastolics) / len(valid_diastolics)) if valid_diastolics else None,
                steps=int(sum(l.steps for l in y_logs) / len(y_logs)),
                water_intake=sum(l.water_intake for l in y_logs) / len(y_logs)
            ))
            
    return schemas.DashboardResponse(
        today_log=today_log,
        trends=trends
    )

# --- REPORT EXPORTS ---

@app.get("/api/export/excel")
def get_excel_report(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    logs = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id
    ).order_by(desc(models.HealthLog.log_date)).all()
    
    file_buffer = export_service.export_to_excel(logs)
    
    headers = {
        'Content-Disposition': f'attachment; filename="health_report_{date.today().isoformat()}.xlsx"'
    }
    return StreamingResponse(
        file_buffer,
        headers=headers,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.get("/api/export/word")
def get_word_report(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    logs = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id
    ).order_by(desc(models.HealthLog.log_date)).all()
    
    corr_data = ai_engine.calculate_food_correlation(db, current_user.id, days_limit=30)
    
    file_buffer = export_service.export_to_docx(logs, current_user, corr_data.get("correlations", []))
    
    headers = {
        'Content-Disposition': f'attachment; filename="health_report_{date.today().isoformat()}.docx"'
    }
    return StreamingResponse(
        file_buffer,
        headers=headers,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@app.get("/api/export/pdf")
def get_pdf_report(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    logs = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == current_user.id
    ).order_by(desc(models.HealthLog.log_date)).all()
    
    corr_data = ai_engine.calculate_food_correlation(db, current_user.id, days_limit=30)
    
    file_buffer = export_service.export_to_pdf(logs, current_user, corr_data.get("correlations", []))
    
    headers = {
        'Content-Disposition': f'attachment; filename="health_report_{date.today().isoformat()}.pdf"'
    }
    return StreamingResponse(
        file_buffer,
        headers=headers,
        media_type='application/pdf'
    )

# --- DOCUMENT AGGREGATOR & OCR ROUTES ---
try:
    from document_aggregator import DocumentAggregator
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from document_aggregator import DocumentAggregator

@app.post("/api/documents/analyze")
async def analyze_uploaded_document(file: UploadFile = File(...)):
    """Phân tích, OCR và bóc tách thực thể từ tài liệu tải lên."""
    import tempfile
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        agg = DocumentAggregator(project_name="Du An Suc Khoe Mr Phi", verbose=False)
        result = agg.read_file(tmp_path)
        summary = agg.get_project_summary()
        return {
            "success": True,
            "filename": file.filename,
            "file_type": result.get("type"),
            "text_pages": len(result.get("text", [])),
            "tables_found": len(result.get("tables", [])),
            "insights": agg.key_insights,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích tài liệu: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
