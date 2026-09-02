import json
def process_batch( records ):
    active=[r for r in records if r['active']==True]
    total=0
    for r in active:
        total+=r['score']
    return {'count':len(active),'avg':total/len(active) if active else 0}
