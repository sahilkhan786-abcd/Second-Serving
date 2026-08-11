# Second Serving — Streamlit App

A working prototype of the app described in the "Proposed Solution" section of the
Second Serving project proposal: connects restaurants/cafeterias with surplus food to
shelters/food banks in real time, with a logistics board and a trust & safety layer.

## Files
- `app.py` — the Streamlit app (all pages/UI)
- `database.py` — SQLite data layer (creates `second_serving.db` automatically)
- `requirements.txt` — Python dependencies

## Run it in VS Code

1. Open this folder in VS Code.
2. Open a terminal (PowerShell) in the folder and create/activate a virtual env (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```
5. It opens automatically at `http://localhost:8501`.

The database file `second_serving.db` is created the first time you run it, and gets
pre-loaded with demo data based on your actual interviews (Bagels & Co, Krishna Bakery,
PIE, Wellbeing Bakery) so the app looks alive immediately.

## Pages
- **Home / Impact** — dashboard with live stats and charts
- **Donor Portal** — register a business, post surplus food in seconds
- **Recipient Portal** — register a shelter/food bank, browse & claim food
- **Logistics Board** — donations needing delivery help, volunteer sign-up
- **Trust & Safety Receipts** — auto-generated donation receipts, donor ratings
- **About the Project** — maps the app back to your proposal + interview findings

## Notes / next steps if you want to extend it
- Swap SQLite for a hosted DB (Postgres/Supabase) if you deploy it live.
- Add real push notifications (e.g. Twilio/SMS or email) when a donation is posted.
- Add geolocation + map view (folium/streamlit-folium) instead of text location.
- Add login/auth per donor & recipient (currently anyone can pick "who they are").
