function INDENT(translated) {
    result = []
    for (let i = 0; i < translated.length; i++) {
        starter = String(translated[i]).replace(/ +/, " ",).trim()
        if (starter.match(/d.but/i)) {
            result.push("/*" + String(starter) + "*/")
        } else if (starter.match(/^((fin[-_ ]?pour)|(fin[-_ ]?si)|(fin)|fin[-_ ]?selon|(fin[-_ ]?tant[-_ ]?que))/i)) {
            result.push("};/*" + String(starter) )
        } else if (starter.match(/^(if|while|function|for|switch)/)) {
            result.push(String(translated[i]))
        } else { 
            result.push(String(starter) + ";")
        }
    }  
    return result
}