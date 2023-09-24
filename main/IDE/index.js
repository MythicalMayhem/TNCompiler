function setCookie(cName, cValue, time) {
    let date = new Date();
    date.setTime(date.getTime() + (time * 1000));
    date = "expires=" + date.toUTCString()
    document.cookie = cName + "=" + cValue + "; " + date + "; path=/";
}
function getCookie(cName) {
    const name = cName + "=";
    const cDecoded = decodeURIComponent(document.cookie);
    const cArr = cDecoded.split('; ');
    let res;
    cArr.forEach(val => { if (val.indexOf(name) === 0) res = val.substring(name.length); })
    return res;
}
function deleteCookie(name) { setCookie(name, '', -1) }


let codeArea = document.querySelector('#main').querySelector('#textarea')
let tdo = document.getElementById('tdo')
let tdnt = document.getElementById('tdnt')
let outputtbtn = document.getElementById('output')
let copybtn = document.getElementById('copy')
let writebtn = document.getElementById('write')
let runbtn = document.getElementById('run')
let terminalText = document.getElementById('innerTerminal')


codeArea.addEventListener("paste", (e) => {
    e.preventDefault();
    const text = e.clipboardData.getData('text/plain');
    document.execCommand("insertHTML", false, text);
});

let Write = []
let output = []

let tdntSave = []
function getTDNT() {
    let kids = document.getElementById('tdnt').children
    let TABLE = []
    let localtdntSave = []
    for (const i in kids) {
        if (String(kids[i].tagName) == 'DIV') {
            let kids1 = kids[i].children
            let k, v
            for (const j of kids1) {
                if (j.id == 'name') { k = j.value.trim() }
                if (j.id == 'textarea') { v = j.innerText.trim() }
            }
            if (k.length == 0 && v.length == 0) { continue }
            else if (k.length == 0 || v.length == 0) { continue }
            else {
                let splitVals = v.split('\n')
                splitVals[0] = k + ':' + splitVals[0]
                localtdntSave.push(splitVals[0])
                splitVals.forEach(el => {
                    let TD = {}
                    TD[String(i)] = el
                    TABLE.push(TD)
                });
            }
        }
    }
    tdntSave = localtdntSave
    return TABLE
}
// ? add counter for each line passed for error checking if necessary 

let tdoSave = []
function getTDO() {
    let kids = document.getElementById('tdo').children
    let TABLE = []
    let localtdoSave = []
    for (const i in kids) {
        if (String(kids[i].tagName) == 'DIV') {
            let kids1 = kids[i].children
            let k, v
            for (const j of kids1) {
                if (j.id == 'name') { k = j.value.trim() }
                if (j.id == 'textarea') { v = j.innerText.trim() }
            }
            if (k.length == 0 || v.length == 0) {
                continue
            } else {
                let temp = {}
                temp[i] = `${k}:${v}`
                localtdoSave.push(temp[i])
                TABLE.push(temp)
            }
        }
    }
    tdoSave = localtdoSave
    return TABLE
}
function getLines() {
    let f = []
    if (codeArea.hasChildNodes()) {
        let children = codeArea.childNodes;
        for (const node of children) {
            let text = node.textContent.trim() || node.innerText.trim()
            f.push(text)
        }
    } else {
        f = [codeArea.innerText]
    }
    f = codeArea.value.split('\n')
    console.log(f)
    return f
}
function run() {
    let f = getLines()
    let lines = []
    for (const i in f) {
        let key = `${(i.toString())}`
        let item = {}
        item[key] = f[i]
        lines.push(item)
    }
    let objs = formatTDO(getTDO(), getTDNT())
    Write = INDENT(translateLines(lines))
    output = objs.join('') + Write.join(';\n')
}

window.addEventListener('load', () => {
    let a = getCookie('algo')?.split('#') || [] 
    codeArea.value = a.join('\n')

    let b = getCookie('TDO')?.split('#') || []
    let kids = tdo.querySelectorAll('div')
    for (const K of kids) { K.remove() }
    for (const i of b) { if (i.length > 0) { addObjectField(tdo, i.split(':')[0], i.split(':')[1]) } }

    let c = getCookie('TDNT')?.split('#') || []
    let kids1 = tdnt.querySelectorAll('div')
    for (const K of kids1) { K.remove() }
    for (const i of c) { if (i.length > 0) { addObjectField(tdnt, i.split(':')[0], i.split(':')[1]) } }
})
function save() {
    let areas = document.querySelectorAll('#textarea')
    for (const area of areas) {
        area.addEventListener("input", () => { 
            getTDO()
            getTDNT()
            setCookie('TDNT', tdntSave.join('#'), 60 * 60 * 24 * 365)
            setCookie('TDO', tdoSave.join('#'), 60 * 60 * 24 * 365)
            setCookie('algo', getLines().join('#'), 60 * 60 * 24 * 365)
        })
    }
    setTimeout(() => {
        save()
    }, 2000);
}
save()
copybtn.addEventListener('click', () => { terminalText.innerText = Write.join(''); navigator.clipboard.writeText(Write.join('')) })
outputtbtn.addEventListener('click', () => { terminalText.innerText = output })
writebtn.addEventListener('click', () => { terminalText.innerText = Write.join('\n') })
runbtn.addEventListener('click', () => {
    run()
    const time = new Intl.DateTimeFormat('fr-fr', { timeStyle: 'medium' }).format(new Date())
    terminalText.innerText = time + '\n'
    try { eval(output) }
    catch (e) {
        var err = e.constructor('Error in Evaled Script: ' + e.message);
        // +3 because `err` has the line number of the `eval` line plus two.
        err.lineNumber = e.lineNumber - err.lineNumber + 3;
        terminalText.innerText = time + '\n' + err;
        throw err;
    }

})

