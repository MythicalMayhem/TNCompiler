import decompose
import globalObjects
import newTypes
import convert
import write

import os 



def createCache(filepath,cacheFilePath=str(os.getcwd())+'/src/cache.py'):
    if os.path.isfile(cacheFilePath)==False:
        print(f"file does not exist\n default cache path {str(os.getcwd())+'/src/cache.py'}")
        cacheFilePath=str(os.getcwd())+'/src/cache.py'
     
    f = open(filepath,'r')
    lines = f.readlines()

    indTDNT,indTDO,indALGO = decompose.get(lines) 
    vars,tdnt = newTypes.get(lines,1,indTDNT)

    tdnttxt = newTypes.format(vars,tdnt)
    tdotxt  = globalObjects.format(lines,indTDNT+1,indTDO,tdnttxt)
    algotxt = convert.read(lines,indTDO+1,indALGO)

    final   = write.indent(algotxt)
    write.commit(tdotxt,final)

    f.close()
    return cacheFilePath

def execute(workFilePath,cacheFilePath=str(os.getcwd())+'/src/cache.py'):
    if os.path.isfile(cacheFilePath)==False:
        print(f"file does not exist\n default cache path {str(os.getcwd())+'/src/cache.py'}") 
        cacheFilePath=str(os.getcwd())+'/src/cache.py'
    createCache(workFilePath,cacheFilePath)
    os.system(f'python {cacheFilePath}')
     
def execCache(cacheFilePath=str(os.getcwd())+'/src/cache.py'):
    if os.path.isfile(cacheFilePath)==False:
        print(f"file does not exist\n default cache path {str(os.getcwd())+'/src/cache.py'}") 
        cacheFilePath=str(os.getcwd())+'/src/cache.py'
    os.system(f'python {cacheFilePath}')

execute(r'C:\Users\ameur\Desktop\tncRewrite\test.algo')

