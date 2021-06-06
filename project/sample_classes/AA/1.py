import sys

m_len = 0
for line in sys.stdin:
    line.rstrip('\n')
    data = [int(k) for k in line.split('; ')]
    if m_len <= len(list(filter(lambda x: len(str(x)) == 2, data))):
        answer = list(filter(lambda x: len(str(x)) == 2, data))
        m_len = len(list(filter(lambda x: len(str(x)) == 2, data)))
print(*answer)