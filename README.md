# 🛠️ Back-End Server for AI Financial Report Generator

This is the back-end server for the AI Financial Report Generator. It is built with Python (FastAPI) and uses various external APIs and a SQLite database.

---

## 🚀 Getting Started

Follow the steps below to set up and run the back-end server on your local machine.

### ✅ Prerequisites

- [Python 3.8+](https://www.python.org/downloads/) installed on your machine
- `virtualenv` installed (`pip install virtualenv`)
- Internet connection to install dependencies
- API key for Gemini (see `.env` section below)

---

## 🔧 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/siddheshk599/ai-fin-report-generator-backend
   cd ai-fin-report-generator-backend
   ```

2. **Create a Virtual Environment**

   ```bash
   virtualenv env
   ```

3. **Activate the Virtual Environment**

   - On macOS/Linux:

     ```bash
     source env/bin/activate
     ```

   - On Windows:

     ```bash
     env\Scripts\activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` File**

   In the root of the project directory, create a `.env` file with the following content:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=sqlite:///your_database_file.db
   ```

   - `GEMINI_API_KEY`: Get your API key from [Google AI Studio](https://aistudio.google.com).
   - `DATABASE_URL`: SQLite connection string. Example: `sqlite:///data.db`

---

## 🏃‍♂️ Running the Server

Once everything is set up:

```bash
python main.py
```
