import json,math,random,collections
from assign import rule_top
z=1.959963984540054
def wilson(k,n):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h
def wald(k,n):
    p=k/n; h=z*math.sqrt(p*(1-p)/n); return max(0,p-h),min(1,p+h)
def agresti(k,n):
    nn=n+z*z; p=(k+z*z/2)/nn; h=z*math.sqrt(p*(1-p)/nn); return max(0,p-h),p+h
def jeffreys(k,n):
    return betainv(0.025,k+.5,n-k+.5) if k>0 else 0.0, betainv(0.975,k+.5,n-k+.5) if k<n else 1.0
def betacf(a,b,x):
    MAXIT=300;EPS=3e-14;FPMIN=1e-300
    qab=a+b;qap=a+1;qam=a-1;c=1;d=1-qab*x/qap
    d=1/(d if abs(d)>FPMIN else FPMIN);h=d
    for m in range(1,MAXIT+1):
        m2=2*m;aa=m*(b-m)*x/((qam+m2)*(a+m2))
        d=1+aa*d;d=FPMIN if abs(d)<FPMIN else d;c=1+aa/c;c=FPMIN if abs(c)<FPMIN else c;d=1/d;h*=d*c
        aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2))
        d=1+aa*d;d=FPMIN if abs(d)<FPMIN else d;c=1+aa/c;c=FPMIN if abs(c)<FPMIN else c;d=1/d;de=d*c;h*=de
        if abs(de-1)<EPS:break
    return h
def betai(a,b,x):
    if x<=0:return 0.
    if x>=1:return 1.
    bt=math.exp(math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)+a*math.log(x)+b*math.log(1-x))
    return bt*betacf(a,b,x)/a if x<(a+1)/(a+b+2) else 1-bt*betacf(b,a,1-x)/b
def betainv(q,a,b):
    lo,hi=0.,1.
    for _ in range(200):
        m=(lo+hi)/2
        if betai(a,b,m)<q: lo=m
        else: hi=m
    return (lo+hi)/2
def cp(k,n):
    return (betainv(0.025,k,n-k+1) if k>0 else 0.0, betainv(0.975,k+1,n-k) if k<n else 1.0)
def boot_cluster(items,B=4000,seed=0):
    # items: list of (cluster, y)
    rnd=random.Random(seed); cl=collections.defaultdict(list)
    for c,y in items: cl[c].append(y)
    keys=list(cl); sums=[(sum(cl[k]),len(cl[k])) for k in keys]; m=len(keys); est=[]
    for _ in range(B):
        s=n=0
        for _ in range(m):
            a,b=sums[rnd.randrange(m)]; s+=a;n+=b
        est.append(s/n)
    est.sort(); return est[int(.025*B)],est[int(.975*B)-1]
def boot_iid(items,B=4000,seed=0):
    return boot_cluster([(i,y) for i,(c,y) in enumerate(items)],B,seed)
