const fs = require("fs");
let text = fs.readFileSync("frontend/src/components/ChatView.jsx", "utf8");
text = text.replace(/className=\{\\\r?\n?lex \\\\\}/g, "className={`flex`}");
text = text.replace(/className=\{\\?r?\\n?.*flex.*\\?\\}/g, "className={`flex`}"); // Try broader
fs.writeFileSync("frontend/src/components/ChatView.jsx", text);

