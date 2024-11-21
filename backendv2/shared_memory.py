# 공유 메모리 모듈
#notifications = []  # SSE를 위한 전역 알림 큐

# shared_memory.py
from collections import deque

# 전역적으로 사용할 알림 큐
notifications = deque(maxlen=100)  # 큐 크기 제한

