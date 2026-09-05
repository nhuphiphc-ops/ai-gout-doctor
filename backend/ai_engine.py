from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
import models

def calculate_scores(log: models.HealthLog, user_age: int = 47, user_height: float = 1.70) -> Dict[str, Any]:
    """
    Calculates health scores (Gout, Cardio, Metabolic, QoL) and generates recommendations.
    """
    # 1. GOUT RISK SCORE
    gout_score = 0.0
    gout_warnings = []
    
    # High-purine foods & alcohol impact
    if log.had_beer:
        gout_score += 30.0
        gout_warnings.append("Uống bia rượu (đặc biệt là bia) làm tăng mạnh nguy cơ bùng phát gout.")
    elif log.had_alcohol:
        gout_score += 20.0
        gout_warnings.append("Sử dụng đồ uống có cồn cản trở quá trình đào thải acid uric.")
        
    if log.had_organ_meat:
        gout_score += 25.0
        gout_warnings.append("Ăn nội tạng động vật chứa lượng purin cực kỳ lớn.")
    if log.had_seafood:
        gout_score += 15.0
        gout_warnings.append("Hải sản giàu purin có thể kích hoạt cơn gout cấp.")
    if log.had_red_meat:
        gout_score += 15.0
        gout_warnings.append("Thịt đỏ (bò, heo, dê...) làm tăng tích tụ tinh thể urat.")
    if log.had_sweets:
        gout_score += 10.0
        gout_warnings.append("Đồ ngọt chứa đường Fructose thúc đẩy tổng hợp acid uric.")

    # Water intake penalty (dehydration is key gout trigger)
    if log.afternoon_completed:
        if log.water_intake < 1.5:
            gout_score += 25.0
            gout_warnings.append("Thiếu nước nghiêm trọng (< 1.5L). Acid uric dễ bị kết tinh khi cơ thể thiếu nước.")
        elif log.water_intake < 2.0:
            gout_score += 15.0
            gout_warnings.append("Lượng nước uống chưa đạt tiêu chuẩn (< 2.0L). Cần bù nước.")
        elif log.water_intake < 2.5:
            gout_score += 5.0
    else:
        # Default moderate penalty if afternoon is not logged yet
        gout_score += 10.0

    # Activity factor
    if log.afternoon_completed and log.steps < 5000:
        gout_score += 10.0
        gout_warnings.append("Ít vận động trong ngày (< 5000 bước) làm giảm lưu thông máu vùng khớp.")

    # Joint pain is an immediate warning/danger trigger
    if log.joint_pain:
        gout_score += 50.0  # Force to danger zone
        pain_locations = []
        if log.pain_big_toe: pain_locations.append("ngón chân cái")
        if log.pain_ankle: pain_locations.append("mắt cá chân")
        if log.pain_knee: pain_locations.append("đầu gối")
        if log.pain_foot: pain_locations.append("bàn chân")
        
        loc_str = ", ".join(pain_locations) if pain_locations else "khớp chân"
        gout_warnings.append(f"CẢNH BÁO: Phát hiện đau/nhức khớp ở {loc_str}. Nguy cơ bùng phát cơn gout cấp tính!")

    gout_score = min(gout_score, 100.0)

    # Determine status
    if log.joint_pain or gout_score >= 60.0:
        gout_status = "Danger"
    elif gout_score >= 30.0:
        gout_status = "Warning"
    else:
        gout_status = "Safe"


    # 2. CARDIOVASCULAR SCORE (BP, HR, BMI)
    cardio_score = 0.0
    cardio_warnings = []
    
    # Blood Pressure evaluation
    bp_points = 0
    if log.bp_systolic is not None and log.bp_diastolic is not None:
        sys = log.bp_systolic
        dia = log.bp_diastolic
        
        # JNC7 Classification adapted to score
        if sys < 120 and dia < 80:
            bp_points = 0
        elif (120 <= sys < 140) or (80 <= dia < 90):
            bp_points = 30
            cardio_warnings.append(f"Huyết áp ở ngưỡng Tiền cao huyết áp ({sys}/{dia} mmHg).")
        elif (140 <= sys < 160) or (90 <= dia < 100):
            bp_points = 65
            cardio_warnings.append(f"Huyết áp Cao độ 1 ({sys}/{dia} mmHg). Nên kiểm soát muối và nghỉ ngơi.")
        else: # sys >= 160 or dia >= 100
            bp_points = 95
            cardio_warnings.append(f"Huyết áp Cao độ 2 nguy hiểm ({sys}/{dia} mmHg)! Hãy dùng thuốc theo chỉ định hoặc hỏi ý kiến bác sĩ.")
            
    # Heart Rate
    hr_points = 0
    if log.heart_rate is not None:
        hr = log.heart_rate
        if hr < 50 or hr > 100:
            hr_points = 50
            cardio_warnings.append(f"Nhịp tim nghỉ ngơi bất thường ({hr} bpm). Ngưỡng lý tưởng là 60-90 bpm.")
        elif hr < 60 or hr > 90:
            hr_points = 15
            cardio_warnings.append(f"Nhịp tim hơi ngoài ngưỡng tối ưu ({hr} bpm).")

    # BMI
    bmi_points = 0
    bmi_val = 21.6 # default for user
    if log.weight is not None:
        bmi_val = log.weight / (user_height ** 2)
        if bmi_val < 18.5:
            bmi_points = 20
            cardio_warnings.append(f"Chỉ số BMI thấp ({bmi_val:.1f}). Cần đảm bảo dinh dưỡng.")
        elif 25.0 <= bmi_val < 30.0:
            bmi_points = 40
            cardio_warnings.append(f"Thừa cân nhẹ (BMI {bmi_val:.1f}).")
        elif bmi_val >= 30.0:
            bmi_points = 80
            cardio_warnings.append(f"Béo phì (BMI {bmi_val:.1f}). Nguy cơ cao các bệnh tim mạch.")

    cardio_score = (bp_points * 0.5) + (hr_points * 0.25) + (bmi_points * 0.25)
    cardio_score = min(cardio_score, 100.0)
    
    if cardio_score >= 60.0:
        cardio_status = "Danger"
    elif cardio_score >= 25.0:
        cardio_status = "Warning"
    else:
        cardio_status = "Safe"


    # 3. METABOLIC SCORE (Risk of metabolic syndrome/prediabetes)
    metabolic_score = 0.0
    metabolic_warnings = []
    
    # Sweet intake & exercise combined risk
    sweet_points = 35.0 if log.had_sweets else 0.0
    activity_points = 35.0 if (log.afternoon_completed and log.steps < 5000) else 0.0
    bp_risk_points = 30.0 if (log.bp_systolic is not None and log.bp_systolic >= 130) else 0.0
    
    if log.had_sweets:
        metabolic_warnings.append("Sử dụng đồ ngọt/fructose tăng nguy cơ kháng insulin (tiền đái tháo đường).")
    if log.afternoon_completed and log.steps < 5000:
        metabolic_warnings.append("Ít vận động kết hợp đồ ngọt làm tăng nguy cơ mỡ máu và béo bụng.")
    if log.bp_systolic is not None and log.bp_systolic >= 130:
        metabolic_warnings.append("Huyết áp cao là một tiêu chí cấu thành hội chứng chuyển hóa.")
        
    metabolic_score = sweet_points + activity_points + bp_risk_points
    metabolic_score = min(metabolic_score, 100.0)
    
    if metabolic_score >= 60.0:
        metabolic_status = "Danger"
    elif metabolic_score >= 30.0:
        metabolic_status = "Warning"
    else:
        metabolic_status = "Safe"


    # 4. QUALITY OF LIFE (QoL) INDEX
    # Sleep Score (0 - 100)
    sleep_score = 100.0
    if log.sleep_quality is not None:
        # sleep quality factor (60% weight)
        q_factor = log.sleep_quality * 10
        # sleep duration factor (40% weight) - optimal is 7-8 hours
        d_factor = 100.0
        dur = log.sleep_duration or 7.0
        if dur < 6.0:
            d_factor = max(0.0, 100.0 - (6.0 - dur) * 30)
        elif dur > 9.0:
            d_factor = max(0.0, 100.0 - (dur - 9.0) * 20)
        elif 7.0 <= dur <= 8.5:
            d_factor = 100.0
        
        sleep_score = (q_factor * 0.6) + (d_factor * 0.4)
    else:
        sleep_score = 70.0 # Default if sleep is not entered
        
    # Stress / Mood Score (0 - 100)
    stress_mood_score = 100.0
    if log.stress_level is not None and log.mood_level is not None and log.fatigue_level is not None:
        # Higher mood = good, Higher stress/fatigue = bad
        mood_pts = log.mood_level * 10
        stress_pts = (11 - log.stress_level) * 10
        fatigue_pts = (11 - log.fatigue_level) * 10
        stress_mood_score = (mood_pts * 0.4) + (stress_pts * 0.3) + (fatigue_pts * 0.3)
    else:
        stress_mood_score = 70.0

    # Diet Score (0 - 100)
    diet_score = 100.0
    if log.had_beer or log.had_alcohol:
        diet_score -= 20
    if log.had_organ_meat:
        diet_score -= 20
    if log.had_red_meat:
        diet_score -= 10
    if log.had_seafood:
        diet_score -= 10
    if log.had_sweets:
        diet_score -= 15
    if log.afternoon_completed:
        if log.water_intake >= 2.5:
            diet_score += 10 # Hydration reward
        elif log.water_intake < 1.5:
            diet_score -= 15 # Dehydration penalty
    diet_score = max(0.0, min(100.0, diet_score))

    # Activity Score (0 - 100)
    activity_score = 0.0
    if log.afternoon_completed:
        step_pts = min(100.0, (log.steps / 8000.0) * 100.0)
        dur_pts = min(100.0, ((log.walking_duration + log.exercise_duration) / 45.0) * 100.0)
        activity_score = (step_pts * 0.6) + (dur_pts * 0.4)
    else:
        activity_score = 50.0 # moderate default before evening update

    # Compliance Score (0 - 100)
    compliance_score = 0.0
    if log.morning_completed:
        compliance_score += 50.0
    if log.afternoon_completed:
        compliance_score += 50.0

    # Total QoL Score (average weights)
    qol_score = (
        (sleep_score * 0.25) +
        (stress_mood_score * 0.25) +
        (diet_score * 0.20) +
        (activity_score * 0.20) +
        (compliance_score * 0.10)
    )
    qol_score = round(max(0.0, min(100.0, qol_score)), 1)


    # 5. SMART RECOMMENDATIONS GENERATION
    rec_diet_eat = ["Rau xanh phong phú", "Trái cây giàu vitamin C (cam, chanh, kiwi)", "Cá sông/cá thịt trắng nhỏ"]
    rec_diet_limit = []
    
    if gout_status in ["Warning", "Danger"]:
        rec_diet_limit.extend(["Thịt bò, thịt chó, thịt thú rừng", "Hải sản vỏ cứng (tôm, cua, sò)", "Bia rượu, nước ngọt ngọt có ga"])
    else:
        rec_diet_limit.extend(["Hạn chế thịt đỏ khối lượng lớn", "Hạn chế bia rượu nhiều ngày liên tục"])

    # Water recommendation
    water_rec = ""
    if log.afternoon_completed:
        if log.water_intake < 2.5:
            missing = round(2.5 - log.water_intake, 1)
            water_rec = f"Hôm nay anh mới uống {log.water_intake} lít nước. Mục tiêu là 2.5 lít. Anh cần uống thêm khoảng {missing} lít nữa để tối ưu đào thải uric."
        else:
            water_rec = f"Tuyệt vời! Anh đã uống {log.water_intake} lít nước. Duy trì lượng nước này giúp thận lọc bỏ tinh thể acid uric."
    else:
        water_rec = "Mục tiêu uống nước hôm nay là 2.5 lít. Hãy chuẩn bị sẵn bình nước 1L tại bàn làm việc để theo dõi."

    # Activity recommendation
    activity_rec = []
    if log.joint_pain:
        activity_rec.append("Hạn chế đi lại mạnh. Nằm nghỉ ngơi, nâng cao chân bị đau và có thể chườm đá lạnh giảm sưng.")
    else:
        if log.afternoon_completed:
            if log.steps < 5000:
                activity_rec.append(f"Hôm nay anh mới đi {log.steps} bước. Nên đi bộ thêm 3000-4000 bước nhẹ nhàng.")
            else:
                activity_rec.append("Số bước chân đạt mức tốt. Nên thực hiện thêm bài tập kéo giãn khớp cổ chân (Ankle stretch) trong 5 phút.")
        else:
            activity_rec.append("Anh hãy dành 30 phút đi bộ nhẹ hoặc tập squat nhẹ vào buổi chiều nhé.")

    # Medical warning disclaimer for Gout Danger
    danger_alert = None
    if gout_status == "Danger":
        danger_alert = {
            "title": "CẢNH BÁO NGUY CƠ GOUT CẤP",
            "message": "Các khớp của anh đang có dấu hiệu đau hoặc sưng đỏ kết hợp thói quen ăn uống purin. Vui lòng uống nhiều nước ngay, nghỉ ngơi, hạn chế cử động khớp đau. Nếu tình trạng đau nhức dữ dội kéo dài, hãy liên hệ bác sĩ chuyên khoa Cơ Xương Khớp để được kê đơn thuốc giảm đau (Colchicine/NSAID). *Hệ thống AI không thay thế chỉ định y tế.*"
        }

    return {
        "gout_score": gout_score,
        "gout_status": gout_status,
        "cardio_score": cardio_score,
        "cardio_status": cardio_status,
        "metabolic_score": metabolic_score,
        "metabolic_status": metabolic_status,
        "qol_score": qol_score,
        "recommendations": {
            "diet": {
                "eat": rec_diet_eat,
                "limit": rec_diet_limit
            },
            "activity": activity_rec,
            "water": water_rec,
            "warnings": gout_warnings,
            "danger_alert": danger_alert
        }
    }


def calculate_food_correlation(db: Session, user_id: int, days_limit: int = 30) -> Dict[str, Any]:
    """
    Calculates the statistical correlation between foods eaten in the prior 1-2 days
    and the onset of joint pain flare-ups.
    """
    start_date = date.today() - timedelta(days=days_limit)
    
    # Query all logs of the user in the time frame
    logs = db.query(models.HealthLog).filter(
        models.HealthLog.user_id == user_id,
        models.HealthLog.log_date >= start_date
    ).order_by(models.HealthLog.log_date.asc()).all()
    
    if not logs:
        return {"correlations": [], "days_analyzed": 0, "pain_days_count": 0}
        
    # Build maps
    pain_dates = set()
    log_map = {} # date -> log
    food_dates = {} # food_name -> set of dates it was eaten
    
    for l in logs:
        log_map[l.log_date] = l
        if l.joint_pain:
            pain_dates.add(l.log_date)
            
        # Get foods for this log
        foods = [f.food_name.lower().strip() for f in l.foods]
        # Include high-purine flags as pseudo foods for broader analysis
        if l.had_beer: foods.append("bia")
        if l.had_alcohol and not l.had_beer: foods.append("rượu/cồn")
        if l.had_seafood: foods.append("hải sản")
        if l.had_organ_meat: foods.append("nội tạng động vật")
        if l.had_red_meat: foods.append("thịt đỏ (bò/heo)")
        if l.had_sweets: foods.append("đồ ngọt/nước ngọt")
        
        for food in set(foods):
            if food not in food_dates:
                food_dates[food] = set()
            food_dates[food].add(l.log_date)
            
    correlation_list = []
    
    # Analyze each food
    for food, dates_eaten in food_dates.items():
        total_consumption = len(dates_eaten)
        pain_incidents_with_food = 0
        
        # Check if eating this food on day T led to pain on T, T+1, or T+2
        # Which is equivalent to: for a pain day P, was the food eaten on P, P-1, or P-2?
        for pain_date in pain_dates:
            p_minus_1 = pain_date - timedelta(days=1)
            p_minus_2 = pain_date - timedelta(days=2)
            
            if (pain_date in dates_eaten) or (p_minus_1 in dates_eaten) or (p_minus_2 in dates_eaten):
                pain_incidents_with_food += 1
                
        # Correlation rate = (Incidents where food was consumed prior to pain) / (Total consumption days)
        # Note: If no pain days exist, rate is 0.
        correlation_percentage = 0.0
        if total_consumption > 0:
            correlation_percentage = round((pain_incidents_with_food / total_consumption) * 100.0, 1)
            
        correlation_list.append({
            "food_name": food.capitalize(),
            "pain_incidents_with_food": pain_incidents_with_food,
            "total_consumption": total_consumption,
            "correlation_percentage": correlation_percentage
        })
        
    # Sort: highest percentage first, then by total consumption
    correlation_list.sort(key=lambda x: (-x["correlation_percentage"], -x["total_consumption"]))
    
    # Cap to top 20
    top_20 = correlation_list[:20]
    
    return {
        "correlations": top_20,
        "days_analyzed": len(logs),
        "pain_days_count": len(pain_dates)
    }

import os
import google.generativeai as genai

def generate_chat_response(
    user: models.User, 
    checkups: List[models.MedicalCheckup], 
    recent_logs: List[models.HealthLog],
    query: str, 
    history: List[Dict[str, str]]
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Xin lỗi, hệ thống chưa được cấu hình GEMINI_API_KEY. Vui lòng cập nhật API Key để sử dụng tính năng Tư vấn AI."
        
    genai.configure(api_key=api_key)
    
    # Chuẩn bị Context
    context = f"Thông tin người dùng: {user.name or 'Bệnh nhân'} - {user.age} tuổi - Cân nặng mục tiêu: {user.target_weight}kg.\n"
    
    if checkups:
        latest = checkups[0] # Assume descending order
        context += f"\nChỉ số xét nghiệm gần nhất ({latest.checkup_date}):\n"
        if latest.uric_acid: context += f"- Axit Uric: {latest.uric_acid} mg/dL (nguy cơ gout nếu > 7.0)\n"
        if latest.fasting_glucose: context += f"- Đường huyết đói: {latest.fasting_glucose} mmol/L\n"
        if latest.cholesterol_total: context += f"- Cholesterol tổng: {latest.cholesterol_total} mmol/L\n"
        if latest.ast or latest.alt: context += f"- Men gan AST/ALT: {latest.ast}/{latest.alt} U/L\n"
        if latest.creatinine: context += f"- Creatinine (thận): {latest.creatinine} µmol/L\n"
    else:
        context += "\nChưa có hồ sơ xét nghiệm y tế nào được cung cấp.\n"
        
    if recent_logs:
        context += "\nTóm tắt nhật ký sức khỏe 7 ngày qua:\n"
        pain_days = sum(1 for l in recent_logs if l.joint_pain)
        context += f"- Số ngày bị đau khớp: {pain_days}/{len(recent_logs)}\n"
        # Gather recent foods
        recent_foods = set()
        for log in recent_logs:
            for food in log.foods:
                recent_foods.add(food.food_name)
        if recent_foods:
            context += f"- Thực phẩm mới ăn gần đây: {', '.join(list(recent_foods)[:10])}\n"
            
    system_prompt = f"""
Bạn là AI Gout Doctor - Trợ lý bác sĩ cá nhân chuyên nghiệp, tận tâm và có chuyên môn về bệnh Gout, Tim mạch và Chuyển hóa.
Dưới đây là thông tin y tế của người dùng:
{context}

Nhiệm vụ: Dựa vào câu hỏi của người dùng và các chỉ số sức khỏe trên, hãy đưa ra lời khuyên y tế, phân tích, hoặc giải đáp thắc mắc. 
- Nếu người dùng có Axit Uric cao và đang bị đau khớp, khuyên dùng thuốc theo đơn hoặc đi khám ngay, đồng thời kiêng khem chặt chẽ.
- Cảnh báo rõ ràng rằng bạn là AI và lời khuyên chỉ mang tính tham khảo, không thay thế bác sĩ.
- Trả lời bằng tiếng Việt, thân thiện, rõ ràng, chia đoạn dễ đọc.
"""

    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
    
    # Build chat history for Gemini (role 'user' or 'model')
    formatted_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        formatted_history.append({"role": role, "parts": [msg["content"]]})
        
    try:
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(query)
        return response.text
    except Exception as e:
        return f"Xin lỗi, có lỗi xảy ra khi gọi AI: {str(e)}"


def generate_video_script(topic: str, format: str, tone: str, audience: str, api_key: str = None) -> str:
    import os
    import google.generativeai as genai
    
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        return "Lỗi: Không tìm thấy API Key. Hãy cấu hình API Key trong trang Cài đặt (Nhật ký)."
        
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
Bạn là một chuyên gia sáng tạo nội dung đa nền tảng cho kênh "Sức khỏe Mr. Phi".
Hãy viết một kịch bản video y tế / sức khỏe.
Chủ đề: {topic}
Định dạng: {format}
Tông giọng: {tone}
Đối tượng mục tiêu: {audience}

Yêu cầu xuất đầu ra CHÍNH XÁC theo chuẩn Markdown để dễ đọc:
# Kịch bản Video: [Tên chủ đề]

**Thông tin chung:**
- **Định dạng:** {format}
- **Tông giọng:** {tone}
- **Đối tượng:** {audience}

---

## 1. Mở bài (Hook - 3-5 giây đầu)
[Viết câu giật tít, nêu vấn đề chạm nỗi đau hoặc phản trực giác]

## 2. Thân bài (Nội dung chính)
| Cảnh / Thời gian | Lời thoại (Voice-over / Host) | Hình ảnh mô tả (Visual/B-roll/Text) |
|---|---|---|
| [0:05 - 0:10] | [Lời thoại] | [Mô tả hình ảnh] |
| [0:10 - 0:20] | [Lời thoại] | [Mô tả hình ảnh] |
(Tiếp tục các dòng tùy theo độ dài video)

## 3. Kêu gọi hành động (Call-to-Action)
[Viết lời kêu gọi tương tác, theo dõi kênh Sức khỏe Mr. Phi]

## 4. Miễn trừ trách nhiệm y tế
*Lưu ý: Nội dung video này chỉ mang tính chất tham khảo, không thay thế chẩn đoán và điều trị y khoa. Vui lòng tham khảo ý kiến Bác sĩ trước khi áp dụng.*
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Đã xảy ra lỗi khi tạo kịch bản AI: {str(e)}"
