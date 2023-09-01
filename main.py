
all_gates = ["AND", "NAND", "NOT", "OR", "NOR", "XOR", "XNOR"]
output_file = "Tabela.txt"
circuit = {
        "entradas": [],
        "gates": {}
    }

def logical(gate: str, a:bool, b:bool)->bool:
    if gate == "AND":
        if a == True and b == True:
            return True
        else:
            return False
    elif gate == "OR":
        if a == False and b == False:
            return False
        else:
            return True
    elif gate == "XOR":
        if ((a and gate_not(b)) or (gate_not(a) and b)) == True:
            return True
        else:
            return False

def gate_not(gate, a: bool)->bool:
    if gate == "AND":
        if a == True:
            return False
        else:
            return True
    
#Fatia uma parte da lista separando-a a partir dos gates    
def sliceContent_byGates(content: list, gates: list)->None:
    current_key = None
    current_sublist = []

    for i in content:
        if i in gates:
            if current_key is not None:
                circuit["gates"][current_key] = current_sublist
                current_sublist = []
            current_key = i
        else:
            current_sublist.append(i)

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
    with open("exemplo_1.txt", "r", encoding="utf8") as file:
        strText = file.read()
        strText = strText.replace('\n', ' ')
        return strText.upper()
    
#Recebe a string com o texto e retorna substrings em uma lista
def fragment_strText(strText: str)->str:
    strText = strText.translate({ord(i): ' ' for i in ':,={}[]()""“”'})
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
        circuit["entradas"].append(i)
    
    for i in content[index_output+1:index_gate]:
        circuit["saidas"] = i
    
    gates = list_gates(content, all_gates)
    content = content[index_gate+len(gates):]
    sliceContent_byGates (content, gates)

def create_table(circuit: dict)->list:
    pass





krl = fragment_strText(readLocal_file())
sliceContent_toDict(krl, circuit)

print(circuit)