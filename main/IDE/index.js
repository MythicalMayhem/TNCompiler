

let codeArea = document.querySelector('#main').querySelector('textarea')
let convertbtn = document.getElementById('convert')
let writebtn = document.getElementById('write')
let runbtn = document.getElementById('run')
let terminalText = document.getElementById('innerTerminal')


let Convert = []
let Write = []


function run() {
    let f = codeArea.value.split('\n')
    let lines = []
    for (const i in f) {
        let line = f[i]
        key = `${(i.toString())}`
        let item = {}
        item[key] = line
        lines.push(item)
    } 
    Convert = translateLines(lines) 
    Write = INDENT(translateLines(lines)) 
    console.log(Write)
}
convertbtn.addEventListener('click', () => {
    terminalText.innerText = Convert.join('\n')
})
writebtn.addEventListener('click', () => {
    terminalText.innerText = Write.join('\n')
})
runbtn.addEventListener('click', () => {
    run()
})