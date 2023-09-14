
class TDNTtamplates {
    tables = {}
    Matrices = {}
    classes = []
    classNames = []
}


//TODO : ADD CASCADING CHECK FOR NEW TYPES (TDNT) before executing


function createVar(type, templates) {
    if (type == "entier") { return "0" }
    else if (type in ["chaine", "caractere"]) { return '""' }
    else if (type == "reel") { return "0.0" }
    else if (type == "booleen") { return "False" }
    else if (type in templates.classNames) { return `new ${type} + "()"` }
    else if (type in Object.keys(templates.tables)) { return createTable(type, templates.tables[type][0], templates.tables[type][1], templates) }
    else if (type in Object.keys(templates.Matrices)) { return createMatrix(type, templates.tables[type][0], templates.tables[type][1], templates) }
    return type
}

function createClass(enregistrement, template) {
    let classlist = []
    classlist.push(`class ${Object.keys(enregistrement)[0]} {`)
    let enrdesc = Object(Object.values(enregistrement)[0])
    for (const [i, v] of enrdesc.entries()) { classlist.push(`${v} = ${createVar(enrdesc[v], template)} ;`) }
    classlist.push("}")
    return classlist
}

function createArray(item, length) { let tea = []; for (let i = 0; i < length + 1; i++) { tea.push(item) } return tea }

function createTable(length, type, templates) {
    if (type == "entier") { return `${String(createArray(0, length))}` }
    else if (type == "reel") { return `${String(createArray(0.0, length))}` }
    else if (type == "booleen") { return `${String(createArray(false, length))}` }
    else if (type in templates.classNames) { return `${String(createArray('new ' + type + '()', length))}` }
    else if (type in Object.keys(templates.Matrices)) { return `${String(createMatrix(templates.Matrices[key][0], templates.Matrices[key][1], templates.Matrices[key][2], templates))}` }
    else if (type in Object.keys(templates.tables)) { return `${String(createArray(createTable(templates.tables[key][0], templates.tables[key][1], templates), length))}` }
    else { return `${String(createArray([""], length))}` }

}
function createMatrix(row, col, type, templates) {
    if (type == "entier") { return String((createArray(createArray(0, col), row))) }
    else if (type == "reel") { return String((createArray(createArray(0.0, col), row))) }
    else if (type == "booleen") { return String((createArray(createArray(false, col), row))) }
    else if (type in templates.classNames) { return String((createArray(createArray(`new ${templates.classNames[type]}()`, col), row))) }
    else if (type in Object.keys(templates.tables)) { return String((createArray(createArray(String(createTable(templates.tables[type][0], templates.tables[type][1], templates)), col), row))) }
    else if (type in Object.keys(templates.Matrices)) { return String((createArray(createArray(String(createMatrix(templates.Matrices[type][0], templates.Matrices[type][1], templates.Matrices[type][2], templates)), col), row))) }
    return createArray(createArray('', col), row)
}


function formatTDNT(tdnt) {
    newObjects = new TDNTtamplates()
    for (const [i, V] of Object.entries(tdnt)) {
        let k = Object.keys(V)[0].trim()
        let v = Object.values(V)[0].trim()
        if (v in ["fin", "debut", "", "__SKIP__"]) { continue }
        if ((v.find(":") == -1) && (v.substring(0, 8) != "tableau ")) {
            let estr = `declaration d'objet invalide dans TDNT ligne ${i} :${v}`
            throw Exception(estr)
        }
        let key = v.trim().split(":")[0].trim()
        let Ivalue = v.trim().split(":")[1].trim()
        let s1 = Ivalue.trim().match(/^tableau[ ]+de[ ]+(?<long>[0-9]+)+[ ]+(?<type>[0-9a-z]+)$/i)
        let s2 = Ivalue.trim().match(/^(tableau|matrice)[ ]+de[ ]+(((?<rows1>[0-9]+)[ ]+lignes \* (?<cols1>[0-9]+)[ ]+colon?nes)|((?<cols2>[0-9]+)[ ]+colon?nes) \* (?<rows2>[0-9]+)[ ]+lignes)[ ]*(?<type>[a-z][0-9a-z]*)$/i)
        if (Ivalue.trim() == "enregistrement") {
            for (let j = i; j < tdnt.length; j++) {
                if (Object.values(tdnt[j])[0].trim() == "fin") {
                    let details = tdnt.slice(i, j + 1).slice(2, -1)
                    for (let exp = i; exp < j + 1; j++) { tdnt[exp] = { k: "__SKIP__" } }
                    let detailsdict = {}
                    for (H of details) {
                        if (H in ["fin", "debut", ""]) { continue }
                        detailsdict[Object.values(H)[0].split(":")[0]] = Object.values(H)[0].split(":")[1]
                    }
                    newObjects.classes.push(createClass({ key: detailsdict }, newObjects)) // * classes should be for templates createClass should be called in TDO
                    newObjects.classNames.push(key.trim())
                    break
                }
            }
        } else if (s1 && s1.groups["long"] && s1.groups["type"]) {
            newObjects.tables[key] = [Number(s1.groups["long"]), s1.groups["type"]]
        } else if (s2.groups["rows1"] && s2.groups["cols1"] && s2.groups["type"]) {
            newObjects.Matrices[key] = [Number(s2.groups["rows1"]), Number(s2.groups["cols1"]), s2.groups["type"],]
        } else if (s2.groups["rows2"] && s2.groups["cols2"] && s2.groups["type"]) {
            newObjects.Matrices[key] = [Number(s2.groups["rows1"]), Number(s2.groups["cols1"]), s2.groups["type"],]
        }
    }
    return newObjects
}
function formatTDO(tdo, tdnt) {
    let template = formatTDNT(tdnt)
    let tdoDict = {}
    for (const [i, v] of Object.entries(tdo)) {
        let v = Object.values(v)[0].trim()
        if (v == "") { continue }
        let keys = v.split(":")[0].trim()
        let val = v.split(":")[1].trim()
        for (let j of keys.split(",")) { tdoDict[j] = val }
    }
    let tdoResult = []
    for (const i of tdoDict) {
        let s1 = tdoDict[i].trim().match(/^tableau[ ]+de[ ]+(?<long>[0-9]+)+[ ]+(?<type>[0-9a-z]+)$/i)
        let s2 = tdoDict[i].trim().match(/^(tableau|matrice)[ ]+de[ ]+(((?<rows1>[0-9]+)[ ]+lignes \* (?<cols1>[0-9]+)[ ]+colon?nes)|((?<cols2>[0-9]+)[ ]+colon?nes) \* (?<rows2>[0-9]+)[ ]+lignes)[ ]*(?<type>[a-z][0-9a-z]*)$/i)
        if (tdoDict[i] in list(template.tables.keys())) {
            tdoResult.push(`${i} = ` + createTable(Number(template.tables[tdoDict[i]][0]), template.tables[tdoDict[i]][1], template))
        } else if (tdoDict[i] in list(template.Matrices.keys())) {
            tdoResult.push(`${i} = ` + createMatrix(Number(template.Matrices[tdoDict[i]][0]), Number(template.Matrices[tdoDict[i]][1]), template.Matrices[tdoDict[i]][2], template))
        } else if (s1 && s1.groups["long"] && s1.groups["type"]) {
            tdoResult.push(`${i} = ` + createTable(Number(s1.groups["long"]), s1.groups["type"]))
        } else if (s2.groups["rows1"] && s2.groups["cols1"] && s2.groups["type"]) {
            tdoResult.push(`${i} = ` + createMatrix(Number(s2.groups["rows1"]), Number(s2.groups["cols1"]), s2.groups["type"], template))
        } else if (s2.groups["rows2"] && s2.groups["cols2"] && s2.groups["type"]) {
            tdoResult.push(`${i} = ` + createMatrix(Number(s2.groups["rows2"]), Number(s2.groups["cols2"]), s2.groups["type"], template))
        } else {
            if (createVar(tdoDict[i].trim(), template)) { tdoResult.push(`${i.trim()} = ` + createVar(tdoDict[i].trim(), template) + "\n") }
            else { tdoResult.push(i + `= ${tdoDict[i]}\n`) }
        }
    }
    return tdoResult
}