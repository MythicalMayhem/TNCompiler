let codeArea = document.querySelector('#main').querySelector('#textarea')
let tdo = document.getElementById('tdo')
let tdnt = document.getElementById('tdnt')
let outputtbtn = document.getElementById('output')
let convertbtn = document.getElementById('convert')
let writebtn = document.getElementById('write')
let runbtn = document.getElementById('run')
let terminalText = document.getElementById('innerTerminal')


let Convert = []
let Write = []
let output = []

function getTDNT(el) {
    let kids = document.getElementById(el).children
    let TABLE = []
    for (const i in kids) {
        if (String(kids[i].tagName) == 'DIV') {
            let kids1 = kids[i].children
            let k, v
            for (const j of kids1) {
                if (j.id == 'name') { k = j.value.trim() }
                if (j.id == 'textarea') { v = j.innerText.trim() }
            }
            let splitVals = v.split('\n')
            splitVals[0] = k + ':' + splitVals[0]
            splitVals.forEach(el => {
                let TD = {}
                TD[String(i)] = el
                TABLE.push(TD)
            });
        }
    }
    return TABLE
}
// ? add counter for each line passed for error checking if necessary 

function getTDO(el) {
    let kids = document.getElementById(el).children
    let TABLE = []
    for (const i in kids) {
        if (String(kids[i].tagName) == 'DIV') {
            let kids1 = kids[i].children
            let k, v
            for (const j of kids1) {
                if (j.id == 'name') { k = j.value.trim() }
                if (j.id == 'textarea') { v = j.innerText.trim() }
            }
            let temp = {}
            temp[i] = k + ':' + v
        }
    }
    return TABLE
}
function run() {
    let f = []
    let lines = []
    if (codeArea.hasChildNodes()) {
        let children = codeArea.childNodes;
        for (const node of children) {
            let text = node.textContent.trim() || node.innerText.trim()
            f.push(text)
        }
    } else {
        f = [codeArea.innerText]
    }
    for (const i in f) {
        let line = f[i]
        let key = `${(i.toString())}`
        let item = {}
        item[key] = line
        lines.push(item)
    }

    Convert = translateLines(lines)
    Write = INDENT(translateLines(lines))
    output = Write.join(';')
}

convertbtn.addEventListener('click', () => { terminalText.innerText = Write.join(''); navigator.clipboard.writeText(Write.join('')) })
outputtbtn.addEventListener('click', () => { terminalText.innerText = output })
writebtn.addEventListener('click', () => { terminalText.innerText = Write.join('\n') })
runbtn.addEventListener('click', () => {

    formatTDO(getTDO('tdo'), formatTDNT(getTDNT('tdnt')))
    run()
    const time = new Intl.DateTimeFormat('fr-fr', { timeStyle: 'medium' }).format(new Date())
    terminalText.innerText = time + '\n'
    try { eval(output) }
    catch (error) { terminalText.innerText = time + '\n' + error }
})