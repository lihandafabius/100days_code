from To_Do_List import create_app, db
from To_Do_List.models import User, Task
from To_Do_List.routes import check_due_tasks
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = create_app()

with app.app_context():
    db.create_all()

# --------------------- Scheduler ---------------------
scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: check_due_tasks(app), trigger="cron", hour=12)  # pass app context
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# --------------------- Run Flask ---------------------
if __name__ == "__main__":
    app.run(debug=True)
