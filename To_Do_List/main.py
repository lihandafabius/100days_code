from To_Do_List import create_app, db
from To_Do_List.models import User, Task
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from To_Do_List.routes import check_due_tasks

app = create_app()
with app.app_context():
    db.create_all()

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_due_tasks, trigger="cron", hour=12)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':

    app.run(debug=True)


