import random
from fractions import gcd
import math

fp = open("input2","r+")
fp_out=open("output",'w')

i=0

ph=[]
p=[]
e=[]
D=[]

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcmm(*args):
    """Return lcm of args."""   
    return reduce(lcm, args)

for line in fp:
	input_list= line[1:len(line)-2].split(',')
	ph.append(float(input_list[0]))
	p.append(int(input_list[1]))
	e.append(float(input_list[2]))
	D.append(float(input_list[3]))
HYPER= lcmm(*p)

print "------------------------- "
print "HYPER PERIOD IS %d"%(HYPER)
print "------------------------- "

count=0
cnt=0
final_f=[]
for x in range(1,HYPER):
	if (HYPER%x)==0:
		for l in p:
			if (2*x-gcd(l,x))<=(D[count]):
				cnt+=1
			count+=1
		if(cnt==len(p)):
			final_f.append(x)		
		count=0
		cnt=0

if final_f[0]==1:
	final_f.pop(0)

print "\n \n------------------------- "
print "FINAL LIST OF POSSIBLE VALUES OF F IS "
print final_f
print "------------------------- "


''' ******************************** FORD FULKERSON START *********************** '''


def BFS(C, F, source, sink):
    queue = [source]         # the BFS queue                 
    paths = {source: []}     # 1 path ending in the key
    while queue:

        u = queue.pop(0)     # next node to explore (expand) 
        for v in range(len(C)):   # for each possible next node
 
            # path from u to v?     and   not yet at v?
            if C[u][v] - F[u][v] > 0 and v not in paths:
                 paths[v] = paths[u] + [(u,v)]
                 if v == sink:
                      return paths[v]  # path ends in the key!

                 queue.append(v)   # go from v in the future 
    return None

def max_flow(C, source, sink, fSize,Job,frame_counter):
    size=fSize
    n = len(C) # C is the capacity matrix
    F = [[0] * n for i in range(n)] # F is the flow matrix
    # residual capacity from u to v is C[u][v] - F[u][v]
    while True:
        path = BFS(C, F, source, sink)
        if not path: break   # no path - we're done!

        edge_flows = [C[u][v]-F[u][v] for u,v in path]
        path_flow = min( edge_flows )
       
        #print "Augmenting by", path_flow
        for u,v in path: # traverse path to update flow
            F[u][v] += path_flow     # forward edge up 
            F[v][u] -= path_flow     # backward edge down 
	
	    
    for l in range(1,Job+1):
	if(fSize==40):
		for i in range((len(C)-frame_counter-1),len(C)-1):
			fp_out.write(str(F[l][i])+" ") 
		fp_out.write("\n")
    return sum([F[source][i] for i in range(n)])

if __name__ == "__main__":

    # make a capacity graph
    # node   A   B   C   D   E   F
    C = [ [ 00, 16, 13, 00, 00, 00 ],  # A
          [ 00, 00, 10, 12, 00, 00 ],  # B
          [ 00, 04, 00, 00, 14, 00 ],  # C
          [ 00, 00,  9, 00, 00, 20 ],  # D
          [ 00, 00, 00,  7, 00,  4 ],  # E
          [ 00, 00, 00, 00, 00, 00 ] ] # F

    #print "C is", C
    source = 0  # A
    sink = 5    # F

    #max_flow_value = max_flow( C, source, sink )
    #print "max_flow_value is", max_flow_value



''' ******************************** FORD FULKERSON END *********************** '''

JobNode=[]
Tot_Exec=0

for x in range(0,len(p)):
	print "------------------"
	print " JOB %d DETAILS: "%(x+1)
	print " HYPER PERIOD IS: %d"%(HYPER)
	print " PERIOD: %d "%(p[x])
	print " CYCLIC EXECUTIVES: %d "%(HYPER/p[x])
	print " RELATIVE DEADLINE: %d"%(D[x])
	for z in range(0,HYPER/p[x]):
		Tot_Exec+=(float(e[x]))
frame_count=0
Final_frames=[]
Job_Nodes=0
Job_array=[]
element=0
Adj_array=[]
Original_frame_count=0
final_f=[40]
for frame in reversed(final_f):
	frame_count=HYPER/frame
	Original_frame_count=frame_count
	residue=max(ph)
	if(residue>=0):
		extra_frames=int(residue/frame)
		if((residue%frame)==0):
			frame_count=frame_count+extra_frames
		else:
			frame_count=frame_count+extra_frames+1
        Adj_array.append(element)
	for x in range(0,len(p)):
		for z in range(0,HYPER/p[x]):
			Job_Nodes+=1
	Adj_Matrix = [[0 for x in range(0,Original_frame_count+Job_Nodes+2)] for x in range(0,Original_frame_count+Job_Nodes+2)]

	for x in range(0,Original_frame_count+Job_Nodes+2):
		Adj_Matrix[x][x]=0
		
	for x in range(0,len(p)):
		 for z in range(0,HYPER/p[x]):
			e1='J'+str(x+1)+'_'+str(z+1)
			if (frame==40):
				Job_array.append(e1)
			element+=1
			Adj_array.append(e1)
			Adj_Matrix[0][element]=e[x]
	
	print " ======== FRAME SIZE: %d ========"%(frame)
	for x in range(0,frame_count):
		if((x+1)<=Original_frame_count):	
			e2='F'+str(x+1)
			element+=1
			Adj_array.append(element)
			Adj_Matrix[element][Original_frame_count+Job_Nodes+2-1]=frame
		for y in range(0,len(p)):
			for z in range(0,HYPER/p[y]):
				if(not((x*frame)<((z)*p[y])+ph[y])and(not(((z*(p[y])+D[y]+ph[y])<((x+1)*frame))))):
					e1='J'+str(y+1)+'_'+str(z+1)
					if((x+1)<=Original_frame_count):
						e2='F'+str(x+1)
						temp=Adj_array.index(e1)
						Adj_Matrix[temp][element]=frame
					else:
						e2='F'+str((x+1)-Original_frame_count-1)
						temp=Adj_array.index(e1)
						Adj_Matrix[temp][(x+1)-Original_frame_count+Job_Nodes-1]=frame
	element+=1
	Adj_array.append(element)
	print "*************** "
	MAX_FLOW_ADJ=max_flow(Adj_Matrix,0,Original_frame_count+Job_Nodes+2-1,frame,Job_Nodes,Original_frame_count)
	print " MAX FLOW IS %f TOTAL EXEC TIME IS %f FOR FRAME %d"%(MAX_FLOW_ADJ, Tot_Exec, frame)
	if (MAX_FLOW_ADJ==Tot_Exec):
		Final_frames.append(frame)
		print "!!!! MAX FLOW ACHEIVED FOR FRAME SIZE %d !!!!"%(frame)
		#print Job_array
	print "*************** "
	MAX_FLOW=0
	Adj_array=[]
	element=0
	Adj_Matrix = [[0 for x in range(0,Original_frame_count+Job_Nodes+2)] for x in range(0,Original_frame_count+Job_Nodes+2)] 
	Job_Nodes=0
        frame_count=0
print "=================================== "
print " FINAL LIST OF FRAMES THAT PROVIDE MAX FLOW "
for x in Final_frames:
	print x,
print "\n=================================== "

fp_out.close()
array=[]
fp_main_out=open("main_output_2","w+")
fp_out=open("output","r+")
i=0
j=0
z=[]
Y=[]
sliced=0
for line in fp_out:
	z=line.split(" ")
	for x in z:
		if (x!='0' and x!='\n'):
			#print "%s: F%d: TIME:%s  "%(Job_array[j],i+1,x),
			fp_main_out.write(str(Job_array[j])+": F"+str(i+1)+": TIME:"+str(x))
			if sliced>=1:
				fp_main_out.write(" SLICED")
				sliced=0
			sliced+=1
		i+=1
	j+=1
	i=0
	sliced=0
	#print "\n"
	fp_main_out.write("\n")
fp_main_out.close()
