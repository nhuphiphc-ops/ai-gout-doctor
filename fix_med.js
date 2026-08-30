const fs = require("fs");
let text = fs.readFileSync("frontend/src/components/MedicalRecordsView.jsx", "utf8");
text = text.replace(/className=\{\\\r?\n?edical-container \\\\\}/g, "className={`medical-container`}");
text = text.replace(/className=\{\\\r?\n?edical-records-list \\\\\}/g, "className={`medical-records-list`}");
fs.writeFileSync("frontend/src/components/MedicalRecordsView.jsx", text);

