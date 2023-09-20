let codeArea = document.querySelector('#main').querySelector('#textarea')
let tdo = document.getElementById('tdo')
let tdnt = document.getElementById('tdnt')
let outputtbtn = document.getElementById('output')
let copybtn = document.getElementById('copy')
let writebtn = document.getElementById('write')
let runbtn = document.getElementById('run')
let terminalText = document.getElementById('innerTerminal')


let Write = []
let output = []

function getTDNT() {
    let kids = document.getElementById('tdnt').children
    let TABLE = []
    for (const i in kids) {
        if (String(kids[i].tagName) == 'DIV') {
            let kids1 = kids[i].children
            let k, v
            for (const j of kids1) {
                if (j.id == 'name') { k = j.value.trim() }
                if (j.id == 'textarea') { v = j.innerText.trim() }
            }
            if (k.length == 0 && v.length == 0) {
                continue
            } else if (k.length == 0 || v.length == 0) {
                console.error(`TDNT ${i} not valid`)
                continue
            } else {
                let splitVals = v.split('\n')
                splitVals[0] = k + ':' + splitVals[0]
                splitVals.forEach(el => {
                    let TD = {}
                    TD[String(i)] = el
                    TABLE.push(TD)
                });
            }
        }
    }
    return TABLE
}
// ? add counter for each line passed for error checking if necessary 

function getTDO() {
    let kids = document.getElementById('tdo').children
    let TABLE = []
    for (const i in kids) {
        if (String(kids[i].tagName) == 'DIV') {
            let kids1 = kids[i].children
            let k, v
            for (const j of kids1) {
                if (j.id == 'name') { k = j.value.trim() }
                if (j.id == 'textarea') { v = j.innerText.trim() }
            }
            if (k.length == 0 && v.length == 0) {
                continue
            } else if (k.length == 0 || v.length == 0) {
                console.error(`TDNT ${i} not valid`)
                continue
            } else {
                let temp = {}
                temp[i] = `${k}:${v}`
                TABLE.push(temp)
            }
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
    let objs = formatTDO(getTDO(), getTDNT())
    Write = INDENT(translateLines(lines))
    output = objs.join('') + Write.join(';')

}

copybtn.addEventListener('click', () => { terminalText.innerText = Write.join(''); navigator.clipboard.writeText(Write.join('')) })
outputtbtn.addEventListener('click', () => { terminalText.innerText = output })
writebtn.addEventListener('click', () => { terminalText.innerText = Write.join('\n') })
runbtn.addEventListener('click', () => {
    formatTDO(getTDO(), getTDNT())
    run()
    const time = new Intl.DateTimeFormat('fr-fr', { timeStyle: 'medium' }).format(new Date())
    terminalText.innerText = time + '\n'
    console.log(output)
    try { eval(output ) }
    catch (error) { terminalText.innerText = time + '\n' + error }
})