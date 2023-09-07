import getComponents
import compress
import declaredObjects as objs
import convert
import write
import os


cacheFilePath = 'test.py'
workFilePath = 'test.algo'
os.system("cls")
res = getComponents.get(workFilePath)
algo = res.algo  
tdo  = res.tdo
tdnt = res.tdnt
#compress.run(algo)

TDNT = objs.formatTDNT(tdnt)
TDO = objs.formatTDO(tdo,tdnt)
translated = convert.translateLines(algo)
indented = write.indent(translated)
write.commit(TDO,TDNT,indented,cacheFilePath)
write.run(cacheFilePath)
