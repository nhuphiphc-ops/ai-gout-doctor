from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime

# User schemas
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    age: int = 47
    height: float = 1.70
    target_weight: float = 62.5

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    google_fit_connected: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

# Log nested items
class FoodItem(BaseModel):
    food_name: str
    class Config:
        from_attributes = True

class MedicationItem(BaseModel):
    med_name: str
    class Config:
        from_attributes = True

# Check-in input schemas
class MorningLogInput(BaseModel):
    weight: float = Field(..., description="Cân nặng hiện tại (kg)")
    bp_systolic: int = Field(..., description="Huyết áp tâm thu (mmHg)")
    bp_diastolic: int = Field(..., description="Huyết áp tâm trương (mmHg)")
    heart_rate: int = Field(..., description="Nhịp tim (bpm)")
    sleep_quality: int = Field(..., ge=1, le=10, description="Chất lượng giấc ngủ từ 1 đến 10")
    sleep_duration: float = Field(..., description="Thời gian ngủ (giờ)")
    
    joint_pain: bool = Field(False, description="Có bị đau khớp không")
    pain_big_toe: bool = Field(False, description="Đau ngón chân cái")
    pain_ankle: bool = Field(False, description="Đau mắt cá chân")
    pain_knee: bool = Field(False, description="Đau đầu gối")
    pain_foot: bool = Field(False, description="Đau bàn chân")
    pain_severity: int = Field(0, ge=0, le=10, description="Mức độ đau từ 0 đến 10")
    
    fatigue_level: int = Field(..., ge=1, le=10, description="Mức độ mệt mỏi từ 1 đến 10")
    stress_level: int = Field(..., ge=1, le=10, description="Mức độ stress từ 1 đến 10")
    mood_level: int = Field(..., ge=1, le=10, description="Tâm trạng từ 1 đến 10")

class AfternoonLogInput(BaseModel):
    steps: int = Field(..., description="Số bước chân trong ngày")
    walking_duration: int = Field(..., description="Thời gian đi bộ (phút)")
    exercise_duration: int = Field(..., description="Thời gian tập luyện khác (phút)")
    water_intake: float = Field(..., description="Lượng nước uống (lít)")
    
    foods_consumed: List[str] = Field(default=[], description="Danh sách các món ăn đã dùng")
    had_alcohol: bool = Field(False, description="Có sử dụng chất cồn nói chung")
    had_beer: bool = Field(False, description="Có uống bia")
    had_seafood: bool = Field(False, description="Có ăn hải sản")
    had_organ_meat: bool = Field(False, description="Có ăn nội tạng động vật")
    had_red_meat: bool = Field(False, description="Có ăn thịt đỏ (bò, heo, dê...)")
    had_sweets: bool = Field(False, description="Có ăn đồ ngọt/nước ngọt")
    
    medications: List[str] = Field(default=[], description="Danh sách thuốc sử dụng hôm nay")

# Output schema for health logs
class HealthLogResponse(BaseModel):
    id: int
    user_id: int
    log_date: date
    morning_completed: bool
    afternoon_completed: bool
    
    weight: Optional[float] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    sleep_quality: Optional[int] = None
    sleep_duration: Optional[float] = None
    
    joint_pain: bool
    pain_big_toe: bool
    pain_ankle: bool
    pain_knee: bool
    pain_foot: bool
    pain_severity: int
    
    fatigue_level: Optional[int] = None
    stress_level: Optional[int] = None
    mood_level: Optional[int] = None
    
    steps: int
    walking_duration: int
    exercise_duration: int
    water_intake: float
    
    had_alcohol: bool
    had_beer: bool
    had_seafood: bool
    had_organ_meat: bool
    had_red_meat: bool
    had_sweets: bool
    
    foods: List[FoodItem] = []
    medications: List[MedicationItem] = []
    
    gout_score: float
    cardio_score: float
    metabolic_score: float
    qol_score: float
    ai_recommendations: Optional[Dict[str, Any]] = None
    
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Dashboard schemas
class ScoreTrend(BaseModel):
    date: str
    gout_score: float
    cardio_score: float
    metabolic_score: float
    qol_score: float
    weight: Optional[float] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    steps: int
    water_intake: float

class DashboardResponse(BaseModel):
    today_log: Optional[HealthLogResponse] = None
    trends: List[ScoreTrend]

# Food Correlation schema
class CorrelationItem(BaseModel):
    food_name: str
    pain_incidents_with_food: int
    total_consumption: int
    correlation_percentage: float  # Percentage of times food was eaten before pain

class CorrelationResponse(BaseModel):
    correlations: List[CorrelationItem]
    days_analyzed: int
    pain_days_count: int
