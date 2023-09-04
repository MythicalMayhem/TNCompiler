typer = None
def stringcheck(el):
    kids = el.split('"')
    for i in range(0,len(kids),2):
        print(i,kids[i])
stringcheck('ecrire("jai une pomme ") et je suis un bien "sex" uhhh "nikmke" ')