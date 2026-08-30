import re

with open('backend/models.py', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''    creatinine = Column(Float, nullable=True) # umol/L
    egfr = Column(Float, nullable=True) # mL/min/1.73m2
    kidney_cyst_size = Column(String, nullable=True) # e.g. "11.7x10 mm"
    
    tsh = Column(Float, nullable=True) # mIU/L
    ft3 = Column(Float, nullable=True) # pmol/L
    ft4 = Column(Float, nullable=True) # pmol/L'''

text = text.replace('    creatinine = Column(Float, nullable=True) # umol/L', replacement)

with open('backend/models.py', 'w', encoding='utf-8') as f:
    f.write(text)
