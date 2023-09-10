function isVariable(el) { 
   return el.match(/[_a-z][_a-z0-9]*/i)
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
    el = el.split(" ").slice(1, -1)
    console.log(el)
    var index, start, end = 0
    for (let i = 0; i < el.length; i++) {
        if (el[i] == "de") { index = i }
        if (el[i] == "a") { start = i }
    }

    return `for (let ${el.slice(0, index)}=${el.slice(index + 1, start).join(" ")};i<${el.slice(start + 1, el.length).join(" ")}),i++){`
}
function isSi(el) {
    regex = /si[ ]+(?<arguments>.+)?[ ]+alors:?/i
    var newel = regex.exec(el)
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
    newel = el.match(/fonction[ ]+(?<name>[a-z]([a-z0-9_])*)[ ]*\((?<arguments>.*)\)[ ]*:[ ]*(?<returntype>[a-z]+[0-9]*)/i)
    if (newel) {
        let [alls, unchanges, changes] = getParams(newel[3])
        console.log(alls, unchanges, changes)
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