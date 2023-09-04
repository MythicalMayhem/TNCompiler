import re
def getSpanTable(start,ende):
    begin = int(ord(start))
    ender = int(ord(ende))
    count = int(begin)
    tab = []
    print(count,ender)
    for i in range(begin,ender+1):
        tab.append(chr(i))
    return tab

x = 'as:dff:ii::'
x = re.sub("([^:]*)(:+)$",r"\1", x)

print(x)