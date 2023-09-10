import os 
import getComponents
import compress as compress
import declaredObjects as objs
import convert
import write  
os.system("cls")

def createCache(workFilePath,cacheFilePath=str(os.getcwd())+'/src/cache.py'):
    if os.path.isfile(cacheFilePath)==False:
        print(f"file does not exist\n default cache path {str(os.getcwd())+'/src/cache.py'}")
        cacheFilePath=str(os.getcwd())+'/src/cache.py'

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

execute(r'C:\Users\ameur\Desktop\AlgorithmicLanguageCompiler\test.algo','sdfgsdfg')