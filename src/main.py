import decompose
import globalObjects
import newTypes

filepath =  r"C:\Users\ameur\Desktop\tncRewrite\ALCompiler\test.algo"
f = open(filepath,'r')
lines = f.readlines()

indTDNT,indTDO,indALGO = decompose.get(lines)

vars,tdnt = newTypes.get(lines,1,indTDNT)

tdnttxt = newTypes.format(vars,tdnt)
tdotxt = globalObjects.format(lines,indTDNT+1,indTDO+1,tdnttxt)

print(tdnttxt,tdotxt)
f.close()