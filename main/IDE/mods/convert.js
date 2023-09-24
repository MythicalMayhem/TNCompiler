function isVariable(el) {
    return el.trim().match(/[_a-z][_a-z0-9]*/i)
}
function getParams(el) {
    let eltab = el.split(',').filter((str) => String != '')
    let alls = [], unchanges = [], changes = []
    for (v in eltab) {
        i = eltab[v]
        i = i.replace(/ +/i, ' ')
        if (i == ' ' || i == '') { continue }
        test = i.match(/(?<name>^@?[a-z_]+([a-z0-9_])*)(:[a-z_]+([a-z0-9_])*)?$/i)

        if (test && test.groups.name) {
            if (test.groups.name[0] != '@') {
                unchanges.push(["__OLD" + test.groups.name, test.groups.name])
                alls.push(test.groups.name)
            } else {
                changes.push(test.groups.name.substring(1))
                alls.push(test.groups.name.substring(1))
            }
        } else {
            return [false, false, false]
        }
    }
    return [alls, unchanges, changes]
}
function isBoucleFor(el) {
    el = el.replace(/[ ]+/, ' ')
    el = el.split(" ").slice(1, -1)
    var index, start, pas = 0
    for (let i = 0; i < el.length; i++) {
        if (el[i].trim() == "de") { index = i }
        if (el[i].trim() == "a") { start = i }
        if (el[i].trim() == "pas") { pas = i }
    }
    try {
        let test = el.slice(0, pas).match(/pas[ ]*=(?<amount>[0-9]+)/)
        pas = parseInt(test.groups.amount)
    } catch (error) {

        pas = 1
    }

    return `for (let ${el.slice(0, index)}=${el.slice(index + 1, start).join(" ")};${el.slice(0, index)}<(${el.slice(start + 1, el.length).join(" ")});${el.slice(0, index)}+=${pas}){`
}
function isSi(el) {
    let newel = el.match(/si[ ]+(?<arguments>.+)?[ ]+alors:?/i)
    if (newel) {
        return `if (${newel.groups.arguments}){`
    } else {
        return false
    }
}
function isSinonsi(el) {
    let newel = el.match(/sinonsi[ ]+(?<arguments>.+)?[ ]+alors:?/i)
    if (newel) {
        return `}else if (${newel.groups.arguments}){ `
    } else {
        return false
    }
}
function isSinon(el) {
    var newel = el.match(/sinon[ ]*:?/i)
    if (newel) {
        return `}else{ `
    } else {
        return false
    }
}
function isFonction(el) {
    let newel = el.match(/fonction[ ]+(?<name>[a-z]([a-z0-9_])*)[ ]*\((?<arguments>.*)\)[ ]*:[ ]*(?<returntype>[a-z]+[0-9]*)/i)
    if (newel) {
        let [alls, unchanges, changes] = getParams(newel[3])
        if (alls == []) {
            return [`function ${newel.groups.name} ()/*${newel.groups.returntype}*/{`, [], []]
        }
        if (unchanges || changes) {
            return [`function ${newel.groups.name} (${alls.join(',')}){/*${newel.groups.returntype}*/`, unchanges, changes]
        }
    } else {
        return [false, false, false]
    }
    return [false, false, false]
}
function isProcedure(el) {
    newel = el.match(/procedure[ ]+(?<name>[a-z]([a-z0-9_])*)[ ]*\((?<arguments>.*)\)[ ]*:?/i)
    if (newel) {
        let [alls, unchanges, changes] = getParams(newel[3])
        if (alls == []) {
            return [`function ${newel.groups.name} (){`, [], []]
        }
        if (unchanges || changes) {
            return [`function ${newel.groups.name} (${alls.join(',')}){`, unchanges, changes]
        }
    } else {
        return [false, false, false]
    }
    return [false, false, false]
}
function isTantque(el) {
    newel = el.match(/tantque[ ]+(?<arguments>.*)/i)
    if (newel) {
        return `while (${newel.groups.arguments}){ `
    } else {
        return False
    }
}
function isRepeter(el) { return "while (true) {" }

function isJusqua(el) {
    newel = el.match(/Jusqu'?a[ ]+(?<arguments>.+)/i)
    if (newel) {
        return `if (${newel.groups.arguments}){ `
    } else { return False }
}
function isLire(el, key) {
    lire = el.match(/^(lire)\((?<stuff>.+)\)/i)
    if (lire && lire[2]) {
        inptstr = [
            `if ((typeof ${lire[2]}) === 'boolean') {`,
            `${lire[2]} = Boolean(input('${lire[2]}'))`,
            `}else if ( typeof ${lire[2]} === 'number' && !Number.isNaN(${lire[2]}) && !Number.isInteger(${lire[2]}) ){`,
            `${lire[2]}= parseFloat(input('${lire[2]}'))`,
            `}else if (typeof ${lire[2]} === 'number' && !Number.isNaN(${lire[2]}) && Number.isInteger(${lire[2]})){`,
            `${lire[2]}= parseInt(input('${lire[2]}'))`,
            `}else{`,
            `${lire[2]}= input('${lire[2]}')`,
            `}`,
        ]
        return inptstr
    } else {
        return False
    }
}
function getSpanTable(start, enD) {
    let begin = Number(start.charCodeAt(0))
    let ender = Number(enD.charCodeAt(0))
    let tab = []
    for (let i = begin; i < ender + 1; i++) {
        tab.push(String.fromCharCode(i))
    }
    return tab
}
// function replaceDoubleComparison(stringer) {
//     let re1 = /(?<before>\w+){1}[ ]*((?<equal12>=)?(?<compare1>[\>\<]{1})(?<equal11>=)?)(?<inside>.*)((?<equal22>=)?(?<compare2>[\>\<])(?<equal21>=)?)[ ]*(?<after>\w+)/
//     let item = stringer.match(re1)  
//     console.log(item)
//     if (!item) { return stringer } 
//     let before = item.groups.before
//     let inside = item.groups.inside
//     let after = item.groups.after
//     let compare1 = item.groups.compare1
//     let compare2 = item.groups.compare2
//     let equal1 = item.groups.equal11 || item.groups.equal12 || ''
//     let equal2 = item.groups.equal21 || item.groups.equal22 || ''
//     let result = '( ' + '( ' + before + compare1 + equal1 + inside + ' ) ' + '&&' + ' ( ' + inside + compare2 + equal2 + after + ' )' + ' )'
//     console.log(stringer.replace(re1,result) )
//     return stringer.replace()
// }
//replaceDoubleComparison('5=<=x=<=10')
function replacement(el) {
    return L = el.replace(/\[A\.\.Z\]/g, `${getSpanTable('A', 'Z')}`)
        .replaceAll(/\[a\.\.z\]/g, `${getSpanTable('a', 'z')}`)
        .replaceAll(/\[0\.\.9\]/g, `${getSpanTable('0', '9')}`)
        .replaceAll(/[^a-z0-9_]non[^a-z0-9_]/ig, " ! ")
        .replaceAll(/[^a-z0-9_]et[^a-z0-9_]/gi, " && ")
        .replaceAll(/[^a-z0-9_]ou[^a-z0-9_]/gi, " || ")
        .replaceAll(/[^a-z0-9_]dans[^a-z0-9_]/gi, " in ")
        .replaceAll(/ +/g, " ")
        .replaceAll(/=/g, "==")
        .replaceAll(/(>==)|(==>)/g, ">=")
        .replaceAll(/(<==)|(==<)/g, "<=")
        .replaceAll(/ div /gi, " // ")
        .replaceAll(/ mod /ig, " % ")
        .replaceAll(/\^/g, " ** ")
        .replaceAll(/<--/g, '=').trim()

}

function replaceInString(el) {
    let opened = null
    let start = 0
    let end = el.length
    let quoted = []
    let legit = []
    let full = ''
    for (let i = 0; i < el.length; i++) {
        const item = el[i].trim();
        let before; if (i > 0) { before = i - 1 }
        if ((item == '"' || item == "'") && el[before] != '\\') {
            if (opened == null) {
                opened = i, end = i - 1
                full += replacement(el.substring(start, end + 1))
            } else if (el[opened] == item) {
                quoted.push([opened, i])
                legit.push([start, end])
                full += el.substring(opened, i + 1)
                start = i + 1, end = el.length - 1, opened = null
            }
        }
    }
    full += replacement(el.substring(start, end + 1))
    if (opened != null) { console.error('unformatted String ') }
    return full
}

function translateLines(r) {
    let res = [...r]
    let newres = []
    for (const [i, v] of Object.entries(res)) {
        if (res[i] == undefined) {
            console.error(`line ${i} malformed`)
            continue
        }
        let key = Object.keys(res[i])[0]
        res[i][key] = replaceInString(res[i][key])
            .replace(/([^:]*)(:+)$/, /$1/).replace(/([^;]*)(;+)$/, /$1/).replace(/^(selon) (.+)/, /switch $2{/)
        let starter = res[i][key].split(' ')[0].toLowerCase().trim() + ' '
        if (starter.match(/^(pour)[ ]+/i)) {
            let test = isBoucleFor(res[i][key])
            if (test) {
                newres.push(test )
            } else {
                console.error("pour invalide")
            }
        } else if (starter.match(/^(si)[ ]+/i)) {
            let test = isSi(res[i][key])
            if (test) {
                newres.push(test )
            } else {
                console.error("si invalide ")
            }
        } else if (starter.match(/^(sinonsi)[ ]/i)) {
            let test = isSinonsi(res[i][key])
            if (test) {
                newres.push(test )
            } else {
                console.error("sinonsi invalide ")
            }
        } else if (starter.match(/^(sinon)[ ]*:?/i)) {
            let test = isSinon(res[i][key])
            if (test) {

                newres.push(test )
            } else {
                console.error("sinon invalide ")
            }
        } else if (res[i][key].match(/^((cas[ ])+(?<start>.+)):?(?<other>)?/i)) {
            let temp = res[i][key].match(/^((cas[ ])+(?<start>.+)+):?(?<other>)?/i)
            if (temp && temp.groups.start) {
                newres.push("case" + temp.groups.start + ":" )
            }
            if (temp.groups.other) {
                newres.push(temp.groups.other )
            }
        } else if (starter.match(/^tant[ ]?que/i)) {
            let test = isTantque(res[i][key])
            if (test) {
                newres.push(test )
            }
            else {
                console.error("tantque invalide ")
            }
        }
        else if (starter.match(/^jusqu'?(a|à)/i)) {
            let test = isJusqua(res[i][key])
            if (test) {
                newres.push(test )
                newres.push("break" )
                newres.push("}" )
                newres.push("finsi" )
            }
            else {
                console.error(" Jusqu'a invalide ")
            }
        } else if (starter.match(/^R(e|é)p(e|é)ter[ ]*/i)) {
            let test = isRepeter(res[i][key])
            if (test) {
                newres.push(test )
            } else {
                console.error("repeter invalide ")
            }
        } else if (starter.match(/^(fonction)[ ]+/i)) {
            let [a, b, c] = isFonction(res[i][key])
            if (a) {
                newres.push(a )
                newres.push(b)
                newres.push(c)
                for (l in b) {
                    newres.push(b[l][0] + " = " + b[l][1] )
                }
            }

            else {
                console.error("fonction invalide ")
            }
        } else if (starter.match(/^(procedure)[ ]+/i)) {
            let [a, b, c] = isProcedure(res[i][key])
            console.log(newres)
            if (a) {
                newres.push(a )
                newres.push(b)
                newres.push(c)
                for (l in b) {
                    newres.push(b[l][0] + " = " + b[l][1] )
                }
            } else {
                console.error("procedure invalide ")
            }
        } else if (starter.match(/^retourner[ ]+/i)) {
            let test = res[i][key].match(/^retourner[ ]+(?<stuff>(.*))/i)
            if (test) {
                newres.push(`return ${test[1]}` )
            } else {
                newres.push("return ")
            }
        } else if (starter.match(/^lire\(.+\)/i)) {
            let test = isLire(res[i][key], String(key))
            if (test) {
                newres.push(test.join('') )
            } else {
                console.error("lire invalide ")
            }
        }
        else {
            newres.push(res[i][key] )
        }
    }

    let wres = []
    for (let i = 0; i < newres.length; i++) {
        if (Array.isArray(newres[i])) {
            continue
        }
        if (newres[i].split(" ")[0] in ["return", "fin"]) {
            for (let k = i; i < -1; i--) {

                if (Array.isArray(newres[k])) { continue }
                if (newres[k].split(" ")[0].trim() == 'function') {
                    botargs = newres[k + 2]
                    for (l of botargs) { wres.push(l[1] + " = " + l[0]) }
                    botargs2 = newres[k + 3]
                    for (l of botargs2) {
                        //wres.push('globals()[str("{l}")]=' + l) 
                    }
                    break
                }
            }
        }
        if (!Array.isArray(newres[i])) { wres.push(newres[i]) }
    }

    return wres
}