count = 0
for i in range (1,26):
    print('<tr height="40px" style="border:3px white solid">')
    for j in range(1,26):
        count += 1 
        print('<td height="40px" width="40px" style="border:3px white solid">'+str(count)+'</td>')
    print('</tr>')