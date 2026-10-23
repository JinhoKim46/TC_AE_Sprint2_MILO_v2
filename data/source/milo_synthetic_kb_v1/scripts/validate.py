#!/usr/bin/env python3
"""Validate corpus invariants and traceability using Python standard library."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def require(ok,message):
    if not ok:raise ValueError(message)
def main():
    cases=[json.loads(p.read_text()) for p in sorted((ROOT/'cases').glob('*.json'))]
    ids={c['case_id'] for c in cases};require(len(ids)==len(cases)==20,'case count/unique IDs')
    for c in cases:
        cid=c['case_id'];require(c['synthetic'] is True and c['evidence_origin']=='synthetic_fixture',cid+' provenance')
        require(len(c['diagnostic_interview'])>=4,cid+' interview')
        evidence={e['id'] for e in c['evidence']};tests={t['id'] for t in c['automation_spec']['acceptance_tests']}
        for d in c['diagnoses']:require(set(d['evidence_refs'])<=evidence,cid+' diagnosis refs')
        for r in c['automation_spec']['requirements']:
            require(set(r['evidence_refs'])<=evidence,cid+' requirement evidence')
            require(set(r['verification_refs'])<=tests,cid+' test refs')
        require(set(c['related_case_ids'])<=ids,cid+' related refs')
        require(all(c['evaluation'][x] is None for x in ['baseline_value','post_value','target']),cid+' invented measured number')
        require(c['implementation']['real_world_outcomes_available'] is False,cid+' outcome flag')
        require((ROOT/'cases'/f'{cid}.md').exists(),cid+' markdown mirror')
        for directory,prefix,key in [('playbooks','P','playbook_id'),('blueprints','B','blueprint_id')]:
            doc=read(f'{directory}/{prefix}{cid[1:]}.json');require(doc['source_case_ids']==[cid] and doc[key]==prefix+cid[1:],cid+' derivative mapping')
    chunks=[json.loads(x) for x in (ROOT/'rag/knowledge_chunks.jsonl').read_text().splitlines()]
    require(len(chunks)==len({x['chunk_id'] for x in chunks})==120,'chunk count/duplicates')
    for x in chunks:
        require(x['split']=='knowledge' and x['synthetic'] is True,'chunk provenance')
        require(x['source_path'].split('/')[0] in {'cases','playbooks','blueprints'},'source allowlist')
        require((ROOT/x['source_path']).is_file(),'missing source')
        require(not x['doc_id'].startswith('DEV'),'evaluation leakage')
    manifest=read('rag/ingestion_manifest.json');require(manifest['allowlist']==['rag/knowledge_chunks.jsonl'],'ingestion allowlist')
    evals=[json.loads(x) for x in (ROOT/'evaluation/dev_scenarios.jsonl').read_text().splitlines()]
    require(len(evals)==len({x['eval_id'] for x in evals})==30,'evaluation IDs')
    for x in evals:require(set(x['relevant_case_ids'])<=ids,'evaluation relevance refs')
    for path,digest in read('manifest.json')['sha256'].items():require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'hash mismatch: '+path)
    # These check behavior of the helper, not MILO diagnostic quality.
    from search import search
    require(search('')==[],'empty query')
    require(search('zzzxxyyqqq')==[],'unmatched query')
    require(any(x['doc_id'] in {'C05','P05','B05'} for x in search('meter readings pooled allowance counter billing',5)),'meter retrieval smoke check')
    print(json.dumps({'status':'PASS','cases':20,'playbooks':20,'blueprints':20,'retrieval_records':120,'development_scenarios':30,'checks':'structure, references, provenance, checksums, basic lexical search','not_tested':'MILO integration, model diagnosis accuracy, real-world effectiveness'},indent=2))
if __name__=='__main__':main()
