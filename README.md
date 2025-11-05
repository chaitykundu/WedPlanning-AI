# WedPlanning-AI

# WedFlow AI — Smart Wedding Planner Assistant

###  AI-Powered Wedding Planning Made Simple

**WedFlow AI** is an intelligent chatbot and planning assistant designed to automate wedding day scheduling.  
It allows planners to upload consultation files or meeting recordings, then automatically extracts key details and generates optimized, dynamic **Day-of Timelines** — just like a professional wedding coordinator.

---

##  Key Features

###  Secure Planner Login
Planners log in using verified credentials to securely manage projects and client data.

### Smart Intake via Consultation Upload
Upload **meeting recordings**, **intake questionnaires**, or **planning documents** — the AI automatically extracts:
- Wedding date  
- Venue and rental hours  
- Vendors and service durations  
- Client preferences and special notes  

### AI-Generated Timeline
Using extracted data and reference templates, WedFlow creates a **chronological, optimized wedding day schedule** that adapts dynamically to:
- Venue rules and policies  
- Sunset time and lighting conditions  
- Vendor contracts  
- Client preferences  

### Ceremony & Reception Suggestions
The system intelligently recommends ideal **ceremony and reception start times**, ensuring seamless transitions that align with venue and vendor constraints.

### Coverage Gap Alerts
WedFlow automatically identifies when vendor coverage (e.g., photography or catering hours) doesn’t fully match the event duration — then suggests:
- Extending service hours  
- Adjusting event timing  
- Restructuring timeline flow  

### Export Options
Planners can download or share the final schedule in multiple formats:
- **PDF** — ready for clients  
- **CSV** — easy editing  
- **ICS** — import into calendar apps  
- **Web link** — shareable live version  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend (Chat UI)** | Streamlit |
| **Backend API** | FastAPI |
| **AI Model** | Gemini / Open Source Whisper + LLM |
| **Text Extraction** | PyMuPDF, python-docx, pandas |
| **Authentication** | JWT-based secure login (planned) |
| **Export** | reportlab / pandas / calendar libraries |
| **Language** | Python 3.10+ |
---

## 🚀 Getting Started

###  Clone the repository
```bash
git clone https://github.com/yourusername/wedflow-ai.git
cd wedflow-ai

###  Clone the repository
python -m venv myenv
myenv\Scripts\activate       # On Windows
# or
source myenv/bin/activate    # On macOS/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

5️⃣  Run FastAPI backend
python -m uvicorn main:app --reload




