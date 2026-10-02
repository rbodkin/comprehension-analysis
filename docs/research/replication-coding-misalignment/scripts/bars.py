from PIL import Image
import sys
C=(154,161,172)
def bars(fn):
    im=Image.open(fn).convert('RGB'); px=im.load(); W,H=im.size
    ys=[y for y in range(H) if px[150,y]==(232,234,237)]
    groups=[]
    for y in ys:
        if groups and y-groups[-1][-1]<=1: groups[-1].append(y)
        else: groups.append([y])
    g=[sum(a)/len(a) for a in groups]; y100,y0=g[0],g[-1]; scale=(y0-y100)/100
    xs=[x for x in range(200,W) if sum(px[x,y]==C for y in range(int(y100),int(y0)))>=6]
    cents=[];cur=[]
    for x in xs:
        if cur and x-cur[-1]>1: cents.append(cur);cur=[]
        cur.append(x)
    if cur: cents.append(cur)
    out=[]
    for c in cents:
        xc=sum(c)/len(c); xo=int(round(xc))+6  # sample cap away from stem
        # weight = whiteness deficit relative to white, only near-grey pixels
        def w(y):
            p=px[xo,y]; 
            return max(0,(255-p[0]))/ (255-154) if abs(p[2]-p[0])<25 else 0
        rows=[(y,w(y)) for y in range(int(y100)-10,int(y0)+5) if w(y)>0.05]
        # cluster rows
        cl=[];cu=[]
        for y,ww in rows:
            if cu and y-cu[-1][0]>1: cl.append(cu);cu=[]
            cu.append((y,ww))
        if cu: cl.append(cu)
        caps=[sum(y*ww for y,ww in k)/sum(ww for _,ww in k) for k in cl if len(k)<=4]
        out.append((round(xc,1),[round((y0-y)/scale,2) for y in caps]))
    return out,(y0,y100)
if __name__=='__main__':
    for f in sys.argv[1:]: print(f,bars(f))
