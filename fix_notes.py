import re
with open('frontend/src/components/MedicalRecordsView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''              </div>
              {record.notes && (
                <div className="mt-4 pt-3 border-t border-gray-100">
                  <span className="text-gray-500 block text-xs font-semibold mb-1">KẾT LUẬN / GHI CHÚ CHUYÊN KHOA:</span>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">{record.notes}</p>
                </div>
              )}
            </div>
          ))'''

text = text.replace('              </div>\n            </div>\n          ))', replacement)

with open('frontend/src/components/MedicalRecordsView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
