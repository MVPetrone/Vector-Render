lis = []
count = 0
ans = False

def mbs(c):
    global count, ans
    e = c ** 2 + 0.25
    if c >= 2:
        return False
    if count < 100:
        if e in lis:
            return "True"
        else:
            print(e)
            lis.append(e)
            count += 1
            mbs(e)
    else:
        return "False"

print(mbs(0))
