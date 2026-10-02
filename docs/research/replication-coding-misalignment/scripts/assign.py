import json,re
FAM={'claude-haiku-4-5-20251001':'Haiku 4.5','claude-sonnet-4-5-20250929':'Sonnet 4.5','claude-sonnet-4-6':'Sonnet 4.6',
     'claude-opus-4-5-20251101':'Opus 4.5','claude-opus-4-6':'Opus 4.6','claude-opus-4-7':'Opus 4.7'}
TIER={'Haiku':0,'Sonnet':1,'Opus':2}
def models(m):
    if m is None: return []
    return m if isinstance(m,list) else [m]
def rule_top(m):
    """drop <synthetic>/unknown; pick highest tier (Opus>Sonnet>Haiku), then latest version"""
    fs=[FAM[x] for x in models(m) if x in FAM]
    if not fs: return None
    return max(fs,key=lambda f:(TIER[f.split()[0]],float(f.split()[1])))
def rule_any(m): return {FAM[x] for x in models(m) if x in FAM}
def rule_last(m):
    ms=[x for x in models(m) if x!='<synthetic>']
    return FAM.get(ms[-1]) if ms else None
def rule_single(m):
    fs={FAM[x] for x in models(m) if x in FAM}; other=[x for x in models(m) if x not in FAM and x!='<synthetic>']
    return next(iter(fs)) if len(fs)==1 and not other else None
def rule_nohaiku_single(m):
    fs={FAM[x] for x in models(m) if x in FAM}
    if len(fs)>1: fs-={'Haiku 4.5'}
    return next(iter(fs)) if len(fs)==1 else None
PUB={'Haiku 4.5':(37,62.2),'Sonnet 4.5':(101,54.5),'Sonnet 4.6':(487,39.6),'Opus 4.5':(166,34.3),'Opus 4.6':(3741,34.5),'Opus 4.7':(46,17.4)}
