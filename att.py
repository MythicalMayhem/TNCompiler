def createClass(enregistrement):
    classlist = []
    classlist.append(f'class {list(enregistrement.keys())[0]}:')
    enrdesc = dict(list(enregistrement.values())[0])
    print(enrdesc)
    for i,v in enumerate(enrdesc):
        classlist.append('\t'+v+':'+enrdesc[v])
    print(classlist)
createClass({'sex':{'ss':'fuck','ff':'fsssck','sdfsdfew':'gggg'}})
