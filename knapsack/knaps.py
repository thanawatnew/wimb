#import knapsack

f=open('result.txt','r')
items=f.readlines()
f.close()
items=[i.strip().split() for i in items]
items=[(int(i[0]),int(i[1])) for i in items]

execfile('knapsack.py')

exampleItems=[[i[0],1,i[1]] for i in items]
exampleSizeLimit=10000

#execfile('knapsack.py')
#knapsack(items,10000)

#size = [21, 11, 15, 9, 34, 25, 41, 52]
#weight = [22, 12, 16, 10, 35, 26, 42, 53]
"""
size=[i[0] for i in items]
weight=[i[1] for i in items]
capacity = 10000
knapsack.knapsack(size, weight).solve(capacity)
"""

pictures=dict([i[::-1] for i in items])

outputs=[]
while len(exampleItems)>0:
	output=pack5(exampleItems,exampleSizeLimit)
	print output
	print sum([pictures[o] for o in output])
	if len(output)<=0: 
		while len(exampleItems)>0:
			outputs.append([exampleItems.pop()[-1]])
		break
	outputs.append(output)
	for o in output: exampleItems.remove([pictures[o],1,o])

f=open('result_2.txt','w')
for i in outputs:
 #f.write('( ')
 f.write(str(i[0]))
 for j in i[1:]: f.write(' '+str(j))
 #f.write(" )")
 f.write("\n")
f.close()
