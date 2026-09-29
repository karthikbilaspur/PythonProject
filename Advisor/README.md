# Random Advisor App - Wisdom on Demand

Modern Tkinter GUI that fetches random life advice from AdviceSlip API with history, export & copy features.

📁 Folder Name for GitHub
Random_Advisor_App

Your repo already has Advisor folder - this is the upgraded GUI version. Use Random_Advisor_App or Advisor_GUI_Upgraded.

🚀 Features (Upgraded)
Original Upgraded Version
2 same buttons (Get Advice + Refresh did same thing)Single smart fetch + Copy button
History only 10 items, lost on close 50 items, saved to advice_history.json
No error handling for timeout Timeout, offline fallback, retry logic
Basic tk look Modern card UI with ttk, Segoe UI, colors
No export Export to JSON / TXT
No timestamp Each advice saved with date/time
No copy feature One-click copy to clipboard
Footer only text Live status bar + last updated time
📂 File Structure
Random_Advisor_App/
├── advisor_app.py        # Main upgraded app
├── advice_history.json   # Auto-created
├── requirements.txt
└── README.md
🛠️ Installation
bash
pip install requests
Run:

bash
python advisor_app.py
💻 Screenshot Flow
App opens with a wisdom card: "Don't eat non-snow-coloured snow."
Click ✨ Get New Advice for new advice
📋 Copy copies current advice
📜 History opens scrollable history window
💾 Export History saves all 50 advices
🧠 Code Improvements
root.minsize() for responsive layout
requests with Cache-Control: no-cache to avoid duplicate advice (AdviceSlip caches)
Path for safe file handling
Duplicate advice check
JSON persistence
Separate advice and date tags in history window
Disabled button while fetching to prevent spam
📝 Requirements
requests
Tkinter comes built-in with Python.

🌟 Push to Your Repo
bash
git clonehttps://github.com/karthikbilaspur/PythonProject.git

Put this folder inside

cd PythonProject
git add Random_Advisor_App/
git commit -m "Add Random Advisor App - Upgraded GUI with history & export"
git push origin main
🔮 Future Ideas
Add categories (life, work, love)
Add text-to-speech for advice
System tray widget
👤 Author
karthikbilaspur - PythonProject Series
