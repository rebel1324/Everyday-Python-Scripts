# When I start coding or doing something, I usually forget to rest.
# I just want to continue working on my stuffs.

import os
import time
import datetime
from win10toast import ToastNotifier

if __name__ == "__main__":
    try:
        while True:
            toaster = ToastNotifier()
            toaster.show_toast("일 시작!", "일을 시작할 시간이 되었습니다.", duration=10)
            time.sleep(60*90) # 1.5 hours
            toaster = ToastNotifier()
            toaster.show_toast("휴식 시간", "휴식을 취할 시간이 되었습니다.", duration=10)
            time.sleep(60*30) # 0.5 hours
    except KeyboardInterrupt:
        print("일을 완전히 끝냅니다.")
