# A stopwatch to chime off at various times during a workout

# Timer
import time
import winsound

def timer(minutes):
    start_time = time.time()
    for i in range(minutes):
        elapsed_time = time.time() - start_time
        remaining_time = (minutes - i) * 60 - elapsed_time
        minutes_remaining, seconds_remaining = divmod(int(remaining_time), 60)
        print(f"Time remaining: {minutes_remaining:02d}:{seconds_remaining:02d}", end="\r")
        while remaining_time > 0:
            time.sleep(1)
            elapsed_time = time.time() - start_time
            remaining_time = (minutes - i) * 60 - elapsed_time
            minutes_remaining, seconds_remaining = divmod(int(remaining_time), 60)
            print(f"Time remaining: {minutes_remaining:02d}:{seconds_remaining:02d}", end="\r")
        winsound.Beep(2500, 500)
    print("\nTime's up!")
    winsound.Beep(2500, 500)

minutes = int(input("Enter the number of minutes for the timer: "))
timer(minutes)



