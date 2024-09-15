from datetime import datetime, timedelta

# 현재 시간 가져오기
current_time = datetime.now()

# 0.5초 추가하기
new_time = current_time + timedelta(seconds=0.5)

# 현재 시간 출력 (년-월-일 시:분:초)
print("현재 시간:", current_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

# 0.5초 추가된 시간 출력
print("0.5초 추가된 시간:", new_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
