d={}
f=open('result_110416.csv','r')
content=f.read()
f.close()
for c in content.split('\n'):
 try: c.split(',')[1]
 except: continue
 if not c.split(',')[0] in d: d[c.split(',')[0]]=[set(c.split(',')[1])]
 else: d[c.split(',')[0]][0].add(c.split(',')[1])
