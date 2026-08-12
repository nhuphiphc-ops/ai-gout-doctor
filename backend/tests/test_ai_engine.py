import sys
import os
# Add parent directory to path so tests can find backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import ai_engine
import database

# Use in-memory SQLite for testing database operations
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def test_gout_risk_scoring():
    # Setup test log with no risk factors
    log = models.HealthLog(
        morning_completed=True,
        afternoon_completed=True,
        water_intake=2.5,
        steps=8000,
        joint_pain=False
    )
    
    # 1. Base check - should be safe
    res = ai_engine.calculate_scores(log)
    assert res["gout_status"] == "Safe"
    assert res["gout_score"] < 30.0

    # 2. Add beer - risk score should rise
    log.had_beer = True
    res = api_calc = ai_engine.calculate_scores(log)
    assert res["gout_score"] >= 30.0
    
    # 3. Add dehydration - should become Danger or high warning
    log.water_intake = 1.0
    res = ai_engine.calculate_scores(log)
    assert res["gout_score"] > 50.0

    # 4. Joint pain triggers absolute danger zone
    log.joint_pain = True
    log.pain_big_toe = True
    res = ai_engine.calculate_scores(log)
    assert res["gout_status"] == "Danger"
    assert "ngón chân cái" in res["recommendations"]["danger_alert"]["message"]

def test_cardio_and_bmi_scoring():
    # Setup normal log
    log = models.HealthLog(
        weight=62.5,  # BMI 21.6 for 1.70m
        bp_systolic=115,
        bp_diastolic=75,
        heart_rate=72
    )
    
    res = ai_engine.calculate_scores(log, user_age=47, user_height=1.70)
    assert res["cardio_status"] == "Safe"

    # Set severe blood pressure
    log.bp_systolic = 165
    log.bp_diastolic = 105
    res = ai_engine.calculate_scores(log, user_age=47, user_height=1.70)
    assert res["cardio_status"] == "Danger"
    assert any("Cao độ 2" in w for w in res["recommendations"]["warnings"])

def test_food_pain_correlation(db_session):
    # Create test user
    user = models.User(email="test@user.com", name="Test User", height=1.70, target_weight=62.5)
    db_session.add(user)
    db_session.commit()
    
    # Generate 5 days of history logs
    # Day 1: Eat Seafood, no pain
    log1 = models.HealthLog(user_id=user.id, log_date=date.today() - timedelta(days=4), joint_pain=False, had_seafood=True)
    db_session.add(log1)
    
    # Day 2: Eat Seafood + Beer, no pain
    log2 = models.HealthLog(user_id=user.id, log_date=date.today() - timedelta(days=3), joint_pain=False, had_seafood=True, had_beer=True)
    db_session.add(log2)
    
    # Day 3: Joint pain reported! (Day T)
    log3 = models.HealthLog(user_id=user.id, log_date=date.today() - timedelta(days=2), joint_pain=True)
    db_session.add(log3)
    
    # Day 4: Eat beef, no pain
    log4 = models.HealthLog(user_id=user.id, log_date=date.today() - timedelta(days=1), joint_pain=False, had_red_meat=True)
    db_session.add(log4)
    
    # Day 5: Joint pain reported!
    log5 = models.HealthLog(user_id=user.id, log_date=date.today(), joint_pain=True)
    db_session.add(log5)
    
    # Add food names to logs
    db_session.commit()
    db_session.add(models.LogFood(log_id=log1.id, food_name="Tôm hùm"))
    db_session.add(models.LogFood(log_id=log2.id, food_name="Tôm hùm"))
    db_session.add(models.LogFood(log_id=log4.id, food_name="Thịt bò xào"))
    db_session.commit()

    # Run correlation calculation
    corr_res = ai_engine.calculate_food_correlation(db_session, user.id, days_limit=10)
    
    assert corr_res["days_analyzed"] == 5
    assert corr_res["pain_days_count"] == 2
    
    correlations = corr_res["correlations"]
    # Check if "Tôm hùm" or "Hải sản" has high correlation
    tom_hum_corr = next((item for item in correlations if item["food_name"] == "Tôm hùm"), None)
    assert tom_hum_corr is not None
    # "Tôm hùm" was eaten on Day 1 (before pain Day 3 - lag 2 days) and Day 2 (before pain Day 3 - lag 1 day).
    # Since Day 3 is a pain day, both consumption events fall within the 2-day trigger window.
    # Total consumption = 2, pain incidents with food = 1 (Day 3 pain is triggered by food eaten on Day 1/2).
    # Wait, in the algorithm, for each pain date, we check if the food was eaten on P, P-1, or P-2.
    # Day 3 pain day: food was eaten on Day 1 (P-2) and Day 2 (P-1). Yes, so pain_incidents_with_food = 1.
    # Day 5 pain day: did we eat "Tôm hùm" on Day 3, 4, 5? No, Day 4 we ate "Thịt bò xào", Day 3/5 no.
    # So pain_incidents_with_food = 1. Total consumption = 2. Correlation = 50.0%.
    assert tom_hum_corr["correlation_percentage"] == 50.0
