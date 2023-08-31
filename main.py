from tkinter import filedialog

all_gates = ["AND", "NAND","XAND", "NOT", "OR", "NOR", "XOR"]

circuit = {
        "entradas": {},
        "gates": {}
    }

def gate_not(a: bool)->bool:
    if a == True:
        return False
    else:
        return True

def gate_and(a:bool, b:bool)->bool:
    if a == True and b == True:
        return True
    else:
        return False

def gate_or(a:bool, b:bool)->bool:
    if a == False and b == False:
        return False
    else:
        return True

def gate_xor(a: bool, b: bool)->bool:
    if (gate_and(a,gate_not(b)) or gate_and(gate_not(a), b)) == True:
        return True
    else:
        return False
    
def slice_list_by_indices(input_list, indices):
    current_key = None
    current_sublist = []

    for item in input_list:
        if item in indices:
            if current_key is not None:
                circuit["gates"][current_key] = current_sublist
                current_sublist = []
            current_key = item
        else:
            current_sublist.append(item)

    if current_key is not None:
        circuit["gates"][current_key] = current_sublist

#Encontra os gates e separa numa sublista
def list_gates(content: list, all_gates: list)->list:
    content = content[content.index('GATES'):]
    gates = []
    for i in content:
        if i in all_gates:
            gates = content[1:content.index(i)-1]
            break
    return gates
#Lê o arquivo .txt e o retorna em formato de string única
def readLocal_file()->str:
    directory = filedialog.askopenfilename()
    with open(directory, "r", encoding="utf8") as file:
        strText = file.read()
        strText = strText.replace('\n', ' ')
        return strText.upper()
    
#Recebe a string com o texto e retorna substrings em uma lista
def fragment_strText(strText: str)->str:
    strText = strText.translate({ord(i): ' ' for i in ':,={}[]()""'})
    content = strText.split(' ')
    while '' in content:
        content.remove('')
    return content

#Recebe uma lista, fatia em sublistas e organiza no dicionario
def sliceContent_toDict(content: str, circuit: dict)->None:
    index_input = content.index('ENTRADAS')
    index_output = content.index('SAIDAS')
    index_gate = content.index('GATES')
    for i in content[index_input+1:index_output]:
        while True:
            cin = int(input(f"Digite um nivel lógico 0 ou 1 para a entrada {i}: "))
            if cin == 0 or cin == 1:
                break
        circuit["entradas"][i] = cin
    
    for i in content[index_output+1:index_gate]:
        circuit["saidas"] = i
    
    gates = list_gates(content, all_gates)
    content = content[index_gate+len(gates):]
    slice_list_by_indices (content, gates)




krl = fragment_strText(readLocal_file())
sliceContent_toDict(krl, circuit)

print(circuit)