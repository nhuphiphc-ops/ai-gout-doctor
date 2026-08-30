const fs = require("fs");
let text = fs.readFileSync("frontend/src/App.jsx", "utf8");
text = text.replace(/className=\{\\\r?\n?av-btn \\\\\}/g, "className={`nav-btn ${currentView === \"foo\" ? \"active\" : \"\"}`}");
text = text.replace(/className=\{\\\r?\n?mobile-nav-btn \\\\\}/g, "className={`mobile-nav-btn ${currentView === \"foo\" ? \"active\" : \"\"}`}");
text = text.replace(/className=\{\\\r?\n?main-content \\\\\}/g, "className={`main-content ${currentView === \"chat\" ? \"\" : \"container\"}`}");
text = text.replace(/className=\{\\\r?\n?mobile-bottom-nav-btn \\\\\}/g, "className={`mobile-bottom-nav-btn ${currentView === \"foo\" ? \"active\" : \"\"}`}");
fs.writeFileSync("frontend/src/App.jsx", text);

