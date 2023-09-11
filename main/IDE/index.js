

let codeArea = document.querySelector('#main').querySelector('#textarea')
let outputtbtn = document.getElementById('output')
let convertbtn = document.getElementById('convert')
let writebtn = document.getElementById('write')
let runbtn = document.getElementById('run')
let terminalText = document.getElementById('innerTerminal')


let Convert = []
let Write = []
let output = []



function run() {
    let f = []
    let lines = []
    if (codeArea.hasChildNodes()) {
        let children = codeArea.childNodes;
        for (const node of children) {
            if (node.innerText) {
                for (const iter of node.innerText.split('\n')) {
                    f.push(iter)
                }
            } else {
                for (const iter of node.textContent.split('\n')) {
                    f.push(iter)
                }
            }
        }
    } else {
        f = [codeArea.innerText]
    }
    for (const i in f) {
        let line = f[i]
        key = `${(i.toString())}`
        let item = {}
        item[key] = line
        lines.push(item)
    }

    console.log(lines)
    Convert = translateLines(f)
    Write = INDENT(translateLines(lines))
    output = Write.join('').replace(/\/\//, '')
}
convertbtn.addEventListener('click', () => {
    terminalText.innerText = Write.join('')
    navigator.clipboard.writeText(Write.join(''))
})
writebtn.addEventListener('click', () => {
    terminalText.innerText = Write.join('\n')
})
runbtn.addEventListener('click', () => { 
    run()
    terminalText.innerText = Write.join('\n')
})