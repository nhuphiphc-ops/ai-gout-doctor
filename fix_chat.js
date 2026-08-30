const fs = require("fs");
let text = fs.readFileSync("frontend/src/components/ChatView.jsx", "utf8");
text = text.replace(/content: Chào anh , tôi là Trợ lý AI Gout Doctor. Hôm nay sức khỏe của anh thế nào\? Anh có cần tôi phân tích chỉ số xét nghiệm hay tư vấn thực đơn không\? /g, "content: `Chào anh, tôi là Trợ lý AI Gout Doctor. Hôm nay sức khỏe của anh thế nào? Anh có cần tôi phân tích chỉ số xét nghiệm hay tư vấn thực đơn không?`");
text = text.replace(/className=\{\\\r?\n?lex \\\\\}/g, "className={`flex`}");
fs.writeFileSync("frontend/src/components/ChatView.jsx", text);

