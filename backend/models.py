from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    age = Column(Integer, default=47)
    height = Column(Float, default=1.70)  # in meters
    target_weight = Column(Float, default=62.5)  # in kg
    google_fit_refresh_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship("HealthLog", back_populates="user", cascade="all, delete-orphan")

class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    log_date = Column(Date, nullable=False)
    
    morning_completed = Column(Boolean, default=False)
    afternoon_completed = Column(Boolean, default=False)

    # Morning log data
    weight = Column(Float, nullable=True)
    bp_systolic = Column(Integer, nullable=True)
    bp_diastolic = Column(Integer, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    sleep_quality = Column(Integer, nullable=True)  # 1-10
    sleep_duration = Column(Float, nullable=True)  # hours
    
    # Joint Pain flags
    joint_pain = Column(Boolean, default=False)
    pain_big_toe = Column(Boolean, default=False)
    pain_ankle = Column(Boolean, default=False)
    pain_knee = Column(Boolean, default=False)
    pain_foot = Column(Boolean, default=False)  # we will use custom name mapping if needed, or simple column
    pain_severity = Column(Integer, default=0)  # 0-10
    
    fatigue_level = Column(Integer, nullable=True)  # 1-10
    stress_level = Column(Integer, nullable=True)  # 1-10
    mood_level = Column(Integer, nullable=True)  # 1-10

    # Afternoon log data
    steps = Column(Integer, default=0)
    walking_duration = Column(Integer, default=0)  # in minutes
    exercise_duration = Column(Integer, default=0)  # in minutes
    water_intake = Column(Float, default=0.0)  # in liters
    
    # High-purine / health impact flags
    had_alcohol = Column(Boolean, default=False)
    had_beer = Column(Boolean, default=False)
    had_seafood = Column(Boolean, default=False)
    had_organ_meat = Column(Boolean, default=False)
    had_red_meat = Column(Boolean, default=False)
    had_sweets = Column(Boolean, default=False)

    # Calculated AI Scores
    gout_score = Column(Float, default=0.0)
    cardio_score = Column(Float, default=0.0)
    metabolic_score = Column(Float, default=0.0)
    qol_score = Column(Float, default=0.0)
    ai_recommendations = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="logs")
    foods = relationship("LogFood", back_populates="log", cascade="all, delete-orphan")
    medications = relationship("LogMedication", back_populates="log", cascade="all, delete-orphan")

class LogFood(Base):
    __tablename__ = "log_foods"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey("health_logs.id"), nullable=False)
    food_name = Column(String, nullable=False)

    log = relationship("HealthLog", back_populates="foods")

class LogMedication(Base):
    __tablename__ = "log_medications"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey("health_logs.id"), nullable=False)
    med_name = Column(String, nullable=False)

    log = relationship("HealthLog", back_populates="medications")
