import schedule
import time
from datetime import datetime, timedelta
import threading

def setup_reminder(text):
    try:
        # Extract time and message from the command
        command = text.lower().replace("remind me to", "").strip()
        
        # Split command into message and time
        message, time_part = command.rsplit("at", 1)
        message = message.strip()
        time_part = time_part.strip()

        # Convert time into 24-hour format
        alarm_time = datetime.strptime(time_part, "%I:%M %p").time()
        now = datetime.now()

        # Calculate the exact datetime for the reminder
        reminder_time = datetime.combine(now.date(), alarm_time)
        if reminder_time < now:
            reminder_time += timedelta(days=1)  # Set for the next day if time has already passed

        # Calculate delay in seconds
        delay = (reminder_time - now).total_seconds()

        # Schedule the reminder
        threading.Timer(delay, trigger_reminder, args=[message]).start()
        print(f"Reminder set for {reminder_time.strftime('%I:%M %p')}: {message}")

    except ValueError:
        print("Sorry, I couldn't understand the time format. Please use the format: 'remind me to [task] at [time]'.")

def trigger_reminder(message):
    print(f"Reminder: {message}")

# Example usage
setup_reminder("remind me to call at 12:42 AM")

# Keep the script running for reminders to work
while True:
    time.sleep(1)
