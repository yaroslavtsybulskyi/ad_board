**Welcome to the most epic Django project ever!** 🎉

🚀 What does it do?

It does something awesome (or will, once I figure it out). Right now, it’s a solid foundation for a Django app with dynamic pages, proper routing, and some event wizardry.

How to run it?
Option 1: Local setup (for adventurers)
```
git clone https://github.com/yaroslavtsybulskyi/ad_board.git
cd ad_board
```
Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate 
```
On Windows use 
```
venv\Scripts\activate
```
Install dependencies:
```
pip install -r requirements.txt
```
Run the magic:
```
python manage.py runserver
```
Open your browser and enjoy at:
```
http://127.0.0.1:8000/
```

Option 2: (for true heroes)
1.	Clone the project:
```
git clone https://github.com/yaroslavtsybulskyi/ad_board.git
cd ad_board
```
2. Create a .env file with your PostgreSQL credentials:
```
SECRET_KEY=your_secret_key
POSTGRES_DB=ad_board
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3.Build and run the project using Docker Compose:
```
docker compose up --build
```

4. Go to: http://localhost:8000


Known Issues
	•	Bender sometimes steals packages.
	•	Time paradoxes when delivering to the past.
	•	May attract bounty hunters if you ship contraband.
