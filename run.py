import os

from crontab import CronTab

from app import create_app

cron = CronTab(user=True)

job = cron.new(
    command='export PYTHONPATH={0} && cd $PYTHONPATH && $PYTHONPATH/venv/bin/python $PYTHONPATH/common/AQICalculator.py'.format(
        os.getcwd())
)
job.minute.every(int(os.environ.get('DB_UPDATE_PERIOD_MINUTES')))
cron.write()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080)
