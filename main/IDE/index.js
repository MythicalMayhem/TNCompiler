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
            let text = node.textContent.trim() || node.innerText.trim() 
            f.push(text)
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
    Convert = translateLines(lines)
    Write = INDENT(translateLines(lines))
    output = Write.join(';')
}
convertbtn.addEventListener('click', () => {
    terminalText.innerText = Write.join('')
    navigator.clipboard.writeText(Write.join(''))
})
outputtbtn.addEventListener('click', () => {
    terminalText.innerText = output
})
writebtn.addEventListener('click', () => {
    terminalText.innerText = Write.join('\n')
})
runbtn.addEventListener('click', () => {
    run() 
    const d = new Date(); 
    const time = new Intl.DateTimeFormat('fr-fr',{timeStyle:'medium'}).format(d)
    terminalText.innerText = time+'\n'
    eval(output)
})