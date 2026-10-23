#!/usr/bin/env python3
"""Dependency-free lexical retrieval demo; does not diagnose or call APIs."""
import argparse, collections, json, math, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
STOP=set('a an the and or of to for in on is are with from by as this that'.split())
def tokens(text):
    return [t for t in re.findall(r'[a-z0-9]+',text.lower()) if t not in STOP]
def search(query,top_k=5):
    docs=[json.loads(s) for s in (ROOT/'rag/knowledge_chunks.jsonl').read_text().splitlines() if s.strip()]
    bags=[collections.Counter(tokens(d['text'])) for d in docs]
    df=collections.Counter(t for bag in bags for t in bag)
    lengths=[sum(b.values()) for b in bags];avg=sum(lengths)/len(lengths)
    scored=[]
    for doc,bag,length in zip(docs,bags,lengths):
        score=0.0
        for term in set(tokens(query)):
            tf=bag.get(term,0)
            if tf:
                idf=math.log(1+(len(docs)-df[term]+0.5)/(df[term]+0.5))
                score+=idf*tf*2.2/(tf+1.2*(0.25+0.75*length/avg))
        if score>0:scored.append((score,doc))
    scored.sort(key=lambda x:(-x[0],x[1]['chunk_id']))
    return [{'score':round(score,5),**doc} for score,doc in scored[:top_k]]
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('query');p.add_argument('--top-k',type=int,default=5);p.add_argument('--full',action='store_true');a=p.parse_args()
    if not 1<=a.top_k<=120:p.error('--top-k must be 1..120')
    rows=search(a.query,a.top_k)
    if not a.full:rows=[{k:v for k,v in r.items() if k!='text'} for r in rows]
    print(json.dumps(rows,ensure_ascii=False,indent=2))
