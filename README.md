# 🧠 HireReady: AI-Powered Resume Optimizer

**HireReady** is an AI-driven tool that analyzes your resume and job descriptions to enhance alignment, optimize phrasing, and boost interview chances.  
It uses **Gemini AI** for contextual resume enhancement, skill matching, and professional formatting suggestions.

---

## 🚀 Features

- 📄 Resume Parsing & Analysis  
- 🤖 AI-Powered Resume Optimization (Gemini API)  
- 🎯 Job Description Matching  
- 🧩 Section-wise Enhancement Suggestions  
- 📊 Match Score Calculation  
- 💬 Smart Resume Summary Generation  
- 💾 Export Updated Resume  

---

## 🛠️ Tech Stack

- **Python 3.10+**  
- **Google Gemini API (`google-generativeai`)**  
- **Streamlit / Tkinter (optional UI)**  
- **NLTK / spaCy for text preprocessing**  
- **OpenAI-style Prompt Engineering**

---

## 📂 Project Structure

```bash
AI_HireReady/
│
├── HireReady.py                 # Main application
├── requirements.txt             # Dependencies
├── README.md                    # Project documentation
├── /data                        # Sample resumes & job descriptions
├── /output                      # Updated resumes or match reports
```

---

## ⚙️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/AI_HireReady.git
   cd AI_HireReady
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Gemini API**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the root folder and add:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

---

## ▶️ Usage

Run the app:
```bash
python HireReady.py
```

Provide your:
- Resume text
- Job description

The app will:
- Analyze job-resume match
- Suggest improvements
- Generate an updated version

---


## 🧩 Example Output
1. Adding Job Description and your Resume
<img width="2560" height="1455" alt="{ED00E6FB-3347-482E-80B9-7C1E45A8BFE5}" src="https://github.com/user-attachments/assets/b0e98bfa-936f-46fa-bcd9-5ce405bbba3c" />
2. Matching and Not Matching Skills
<img width="2560" height="1440" alt="{3CD9ADE4-0A2B-408E-8F9E-07A85E1DAC45}" src="https://github.com/user-attachments/assets/3b1fefb6-1d9e-4408-a34e-598491da6ace" />
3. Experience and Education Review
<img width="2550" height="1208" alt="{30F90A34-954B-4382-ACB7-EB1E0450BC54}" src="https://github.com/user-attachments/assets/377db980-d164-48de-bd76-62f47c54921b" />
4. Recommendations
<img width="2560" height="1450" alt="{70057BB4-5D86-4232-9B85-6C741B9C9323}" src="https://github.com/user-attachments/assets/5cf9cc51-5d7a-47ea-9de1-9b53b458076f" />
5. Generate cover letter
<img width="2560" height="1367" alt="{BF6B4C7D-33CF-4257-862D-F10CAC31FC2E}" src="https://github.com/user-attachments/assets/7082be09-9ab7-4610-90a5-658b70c11e74" />
6. Updated resume
<img width="2560" height="720" alt="{E68A7DAB-1DE5-4EFF-A381-A00DA0D003CF}" src="https://github.com/user-attachments/assets/94d175f4-f304-4b26-b07e-53c095a613db" />



---

## 📜 License

This project is licensed under the **MIT License** — feel free to use and modify with attribution.  
See the [LICENSE](LICENSE) file for more details.

---


