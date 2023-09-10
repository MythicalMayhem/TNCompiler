function isVariable(el) {
    return el.trim().match(/[_a-z][_a-z0-9]*/i)
}
function getParams(el) {
    let eltab = el.split(',').filter((str) => str != '')
    let alls = [], unchanges = [], changes = []
    for (v in eltab) {
        i = eltab[v]
        i = i.replace(/ +/i, ' ')
        if (i == ' ' || i == '') { continue }
        test = i.match(/(?<name>^@?[a-z_]+([a-z0-9_])*)(:[a-z_]+([a-z0-9_])*)?$/i)

        if (test && test[1]) {
            if (test[1][0] != '@') {
                unchanges.push(["__OLD" + test[1], test[1]])
                alls.push(test[1])
            } else {
                changes.push(test[1].substring(1))
                alls.push(test[1].substring(1))
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
    var index, start, end = 0
    for (let i = 0; i < el.length; i++) {
        if (el[i].trim() == "de") { index = i }
        if (el[i].trim() == "a") { start = i }
    }

    return `for (let ${el.slice(0, index)}=${el.slice(index + 1, start).join(" ")};i<${el.slice(start + 1, el.length).join(" ")}),i++){`
}
function isSi(el) {
    let newel = el.match(/si[ ]+(?<arguments>.+)?[ ]+alors:?/i)
    if (newel) {
        return `if (${newel[1]}){`
    } else {
        return false
    }
}
function isSinonsi(el) {
    let newel = el.match(/sinonsi[ ]+(?<arguments>.+)?[ ]+alors:?/i)
    if (newel) {
        return `}else if (${newel[1]}){ `
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
            return [`function ${newel[1]} ()/*${newel[4]}*/{`, [], []]
        }
        if (unchanges || changes) {
            return [`function ${newel[1]} (${alls.join(',')}){/*${newel[4]}*/`, unchanges, changes]
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
        console.log(alls, unchanges, changes)
        if (alls == []) {
            return [`procedure ${newel[1]} (){`, [], []]
        }
        if (unchanges || changes) {
            return [`procedure ${newel[1]} (${alls.join(',')}){`, unchanges, changes]
        }
    } else {
        return [false, false, false]
    }
    return [false, false, false]
}
function isTantque(el) {
    newel = el.match(/tantque[ ]+(?<arguments>.*)/i)
    if (newel) {
        return `while (${newel[1]}){ `
    } else {
        return False
    }
}
function isJusqua(el) {
    newel = el.match(/Jusqu'?a[ ]+(?<arguments>.+)/i)
    if (newel) {
        return `if (${newel[1]}){ `
    } else { return False }
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
function replacement(el) {
    return L = el.replace(/\[A\.\.Z\]/, `${getSpanTable('A', 'Z')}`)
        .replace(/\[a\.\.z\]/, `${getSpanTable('a', 'z')}`)
        .replace(/\[0\.\.9\]/, `${getSpanTable('0', '9')}`)
        .replace(/[^a-z0-9_]non[^a-z0-9_]/i, " ! ")
        .replace(/[^a-z0-9_]et[^a-z0-9_] /i, " && ")
        .replace(/[^a-z0-9_]ou[^a-z0-9_] /i, " || ")
        .replace(/[^a-z0-9_]dans[^a-z0-9_]/i, " in ")
        .replace(/ +/, " ")
        .replace(/=/, "==")
        .replace(/====/, "==")
        .replace(/ div /, " // ")
        .replace(/ mod /, " % ")
        .replace(/\^/, " ** ")
        .replace(/<--/, '=')

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
    legit.push([start, end])
    full += el.substring(start, end + 1)
    if (opened != null) {
        console.log('unformatted string')
    }
    console.log(full)
    return full
}
function translateLines(res) {
    newres = []
    for (const [i, v] of Object.entries(res)) {
        key = Object.keys(res[i])
        console.log(key, res[i][key])
        res[i][key] = replaceInString(res[i][key])
        console.log(key, res[i][key])
        // res[i][key] = res[i][key].replace(/([^:]*)(:+)$/, /$1/)
        res[i][key] = res[i][key].replace(/^(selon) (.+)/, "match $2:")
        let starter = res[i][key].split(' ')[0].toLowerCase().trim()
        if (re.match("^pour[ ]+", starter, re.IGNORECASE)) {
            test = isBoucleFor(res[i][key])
            if (test) {
                newres.append(test + '{/*' + str(key) + '*/') 
            } else {
                console.error("pour invalide")
            }
        }
    }
    console.log(newres)
    return newres
}