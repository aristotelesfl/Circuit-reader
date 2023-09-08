all_gates = ["AND", "NAND", "NOT", "OR", "NOR", "XOR", "XNOR"]
output_file = "Tabela.txt"
circuit = {
        "entradas": {},
        "gates": {}
    }
 
#Gera as entradas do circuito
def inputs(n: int)->list:
    all_inputs = []
    for i in range(2**n):
        binario = list(bin(i)[2:].zfill(n))
        all_inputs.append([int(bit) for bit in binario])
    return all_inputs

#Cria uma sublista com as saídas dos gates
def list_outputs(dicio: dict)->list:
    out = []
    for value in dicio["gates"]:
        out.append(dicio['gates'][value][1])
    return out

#Faz as operações lógicas
def logical(gate: str, a:bool, b:bool)->int:
    if gate == "AND" or gate == "NAND":
        return a and b
    elif gate == "OR" or gate == "NOR":
        return a or b
    elif gate == "XOR" or gate == "XNOR":
        return a ^ b

#Faz o complemento das operações lógicas
def gate_not(a: bool)->int:
        return not(a)

#Encontra os gates e separa numa sublista
def list_gates(content: list, all_gates: list)->list:
    content = content[content.index('GATES'):]
    gates = []
    for i in content:
        if i in all_gates:
            gates = content[1:content.index(i)-1]
            break
    gates.sort()
    return gates

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

#---------------------------------------------------------------

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
    keys = content[index_input+1:index_output]
    gate_input = inputs(len(keys))
    for i in keys:
        value = []
        key, index = i, keys.index(i)
        for j in gate_input:
            value.append(j[index])
        circuit['entradas'][key] = value
    outputs = []
    for i in content[index_output+1:index_gate]:
        outputs.append(i)
    circuit["saidas"] = outputs
    
    gates = list_gates(content, all_gates)
    content = content[index_gate:]
    sliceContent_byGates (content, gates)

#Gera as saídas dos gates
def generate_outputs(dicio: dict)->None:
    lista = list_outputs(dicio)
    outputs = dicio["saidas"]
    dicio["saidas"] = {}
    for key in dicio['gates']:
        values, output = [], []
        gate, out = dicio['gates'][key][0], dicio['gates'][key][1]
        for value in dicio['gates'][key]:
            index = dicio['gates'][key].index(value)
            if value in dicio['entradas']:
                values.append(dicio['entradas'][value])
            elif index!=1 and value in lista:
                i = lista.index(value)
                current_list = list_outputs(dicio)
                values.append(current_list[i][value])
        
        if gate == "NOT":
            a = values
            for l in range(len(a[0])):
                output.append(int(gate_not(a[0][l])))

        else:
            cout = False
            for i in range(len(values)-1):
                if cout is False:
                    a, b = values[0], values[1]
                    for l in range(len(a)):
                        output.append(int(logical(gate, a[l], b[l])))
                    cout = True
                else:
                    a, b = output, values[i+1]
                    output = []
                    for l in range(len(a)):
                        output.append(int(logical(gate, a[l], b[l])))
            if gate == "NOR" or gate == "XNOR" or gate == "NAND":
                current_output = []
                for i in output:
                    current_output.append(int(gate_not(i)))
                output = current_output

        dicio['gates'][key][1] = {
            out: output
        }

        if out in outputs:
            dicio['saidas'][out] = dicio['gates'][key][1][out]
    

#Cria uma lista com as entradas e saída do circuito
def create_table(circuit: dict)->list:
    matriz = []
    for i in circuit["entradas"].values():
        matriz.append(i)
    for i in circuit["saidas"].values():
        matriz.append(i)
    return matriz

#Imprime a tabela verdade do circuito num arquivo "Tabela.txt"
def write_matriz(matriz:list, dicio:dict)->None:
    table = open("Tabela.txt", "w+")
    for index_i in dicio['entradas']:
        table.write(f"{index_i} ")
    for index_o in dicio['saidas']:
        table.write(f"{index_o} ")
    table.write("\n")
    for i in range(len(matriz[0])):
        for j in range(len(matriz)):
            table.write(f"{matriz[j][i]} ")
        table.write("\n")
    table.close()

strTXT = readLocal_file()
content = fragment_strText(strTXT)
sliceContent_toDict(content, circuit)
generate_outputs(circuit)
matriz = create_table(circuit)
write_matriz(matriz, circuit)