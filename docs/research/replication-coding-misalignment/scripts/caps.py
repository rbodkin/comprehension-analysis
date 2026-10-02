from PIL import Image
C=(154,161,172)
def caps(fn,stem_x,top_pct,dx=6):
    im=Image.open(fn).convert('RGB'); px=im.load(); W,H=im.size
    ys=[y for y in range(H) if px[150,y]==(232,234,237)]
    groups=[]
    for y in ys:
        if groups and y-groups[-1][-1]<=1: groups[-1].append(y)
        else: groups.append([y])
    g=[sum(a)/len(a) for a in groups]; y100,y0=g[0],g[-1]; scale=(y0-y100)/top_pct
    out={}
    for x in stem_x:
        res=[]
        for side in (-dx,dx):
            xx=x+side; bgx=x+side*3
            cov=[]
            for y in range(int(y100)-5,int(y0)+4):
                p=px[xx,y]; b=px[bgx,y]
                if b[0]==C[0]: continue
                c=(b[0]-p[0])/(b[0]-C[0]) if b[0]!=C[0] else 0
                # require bluish-grey hue consistent with stem
                if c>0.05: cov.append((y,min(c,1.0)))
            cl=[];cu=[]
            for y,c in cov:
                if cu and y-cu[-1][0]>1: cl.append(cu);cu=[]
                cu.append((y,c))
            if cu: cl.append(cu)
            res.append([ (round(sum(y*c for y,c in k)/sum(c for _,c in k),2), round(sum(c for _,c in k),2)) for k in cl])
        out[x]=res
    return out,(y0,y100,scale)
