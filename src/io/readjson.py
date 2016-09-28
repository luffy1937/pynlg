#coding=UTF-8
import json
f='load.json'
fr=open(f,'r').read()
newdict=json.loads(fr)
seq=[]
for term in newdict:
	for t in term:
		seq.append((t,int(term[t]['post_num']),int(term[t]['member_num'])))
newseq=sorted(seq,key=lambda seq:seq[2],reverse=True)


	

		
