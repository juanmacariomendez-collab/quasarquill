from datetime import datetime, timedelta, UTC
import random, time, subprocess
from auto_updater.notify import notify

def run():
    notify(f"[{datetime.now(UTC).isoformat()}] Запускаю updater.py")
    subprocess.run(["python3","auto_updater/updater.py"])

def main():
    delay = random.randint(0, 120*60)
    notify(f"Scheduler стартовал, задержка {delay//60} мин")
    time.sleep(delay)
    runs = random.choices([0,1,2], weights=[1,3,2])[0]
    notify(f"Сегодня планируется {runs} запуск(ов)")
    if runs == 0: return
    start, end = 9*3600, 22*3600
    slots = sorted(random.sample(range(start, end), runs))
    notify("Сегодня коммиты будут в: " + ", ".join((datetime.min + timedelta(seconds=s)).strftime("%H:%M") for s in slots))
    for s in slots:
        now = datetime.now(UTC).astimezone()
        target = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=s)
        wait = (target - now).total_seconds()
        if wait > 0: time.sleep(int(wait))
        run()
    notify(f"Scheduler завершил работу, сегодня выполнено {runs} запуск(ов)")

if __name__ == "__main__": main()
