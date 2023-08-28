from tkinter import filedialog

portas = ["and", "nand", "not", "and"]
circuit = {
        "entradas": {},
        "gates": {}
    }

#Lê o arquivo .txt e o retorna em formato de string única
def readLocal_file()->str:
    directory = filedialog.askopenfilename()
    with open(directory, "r", encoding="utf8") as file:
        strText = file.read()
        strText = strText.replace('\n', ' ')
        return strText.lower()
    
#Recebe a string com o texto e retorna substrings em uma lista
def fragment_strText(strText: str)->str:
    strText = strText.translate({ord(i): ' ' for i in ':,={}[]()""'})
    content = strText.split(' ')
    while '' in content:
        content.remove('')
    return content

#Recebe uma lista, fatia em sublistas e organiza no dicionario
def sliceContent_toDict(content: str, circuit: dict)->None:
    index_input = content.index('entradas')
    index_output = content.index('saidas')
    index_gate = content.index('gates')
    for i in content[index_input+1:index_output]:
        while True:
            cin = int(input(f"Digite um nivel lógico 0 ou 1 para a entrada {i}: "))
            if cin == 0 or cin == 1:
                break
        circuit["entradas"][i.upper()] = cin
    
    for i in content[index_output+1:index_gate]:
        circuit["saidas"] = i.upper()
    content = content[index_gate+1:]
    
    for i in content:
        content = content[content.index(i):]
        if i not in portas:
            for j in range(len(content)-1):
                if content[j] in portas:
                    if content[j] == 'not':
                        circuit["gates"][i] = content[j:j+3]
                        break
                    else: 
                        circuit["gates"][i] = content[j:j+4]
                        break
        

krl = fragment_strText(readLocal_file())
sliceContent_toDict(krl, circuit)

print(circuit)