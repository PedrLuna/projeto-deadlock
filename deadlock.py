processo_recurso = []
recursos_existentes = []
recursos_disponiveis = []
matriz_alocacao = []
matriz_requisicao = []
zero_array = []
    
#counter de processos
contador_ok = 0


def subtrair_recursos(indice2, recursos, matriz, matriz2, zero_array):
    aux = matriz2[indice2 - 1]
    aux2 =  matriz[indice2 - 1]
    recursos_anteriores = recursos
    nova = []
    nova2 = []

    #subtrai
    for i in range(0, len(recursos)):
        valor = int(recursos[i]) - int(aux[i])
        nova.append(str(valor))
    
    #A recebe a subtração
    recursos = nova

    #soma A com Ci
    for j in range(0, len(recursos)):
        valor2 = int(recursos_anteriores[j]) + int(aux2[j])
        nova2.append(str(valor2))

    #linha do processo na matriz de alocação recebe nova2
    matriz[indice2 - 1] = nova2

    #valores do processo executado zeram
    matriz[indice2 -1] = zero_array
    matriz2[indice2 -1] = zero_array

    
    return nova2



def carregar(escolha):
    if escolha == 1:
        arquivo = open("arquivo1.txt","r")
    elif escolha == 2:
        arquivo = open("arquivo2.txt", "r")
    elif escolha == 3:
        arquivo = open("arquivo3.txt", "r")
    conteudo = arquivo.readlines()
    for i in range(len(conteudo)):
        linha_arquivo = conteudo[i].split()
        if(i == 0):
            processo_recurso = linha_arquivo
        elif(i == 2):
            recursos_existentes = linha_arquivo
        elif(i == 4):
            recursos_disponiveis = linha_arquivo
        elif(i in range(6, 6 + int(processo_recurso[0]))):
            matriz_alocacao.append(linha_arquivo)
        elif(i in range((6 + int(processo_recurso[0]) + 1), ((6 + int(processo_recurso[0]) + 1) + int(processo_recurso[0])))):
            matriz_requisicao.append(linha_arquivo)
    for i in range(0, int(processo_recurso[1])):
        zero_array.append('0')
    print("Quantidade de Processos: ",processo_recurso[0])
    print("Quantidade de Recursos: ", processo_recurso[1])
    print("Recursos Existentes: \n", recursos_existentes)
    print("Recursos Disponíveis: \n", recursos_disponiveis)
    print("\nMatriz de Alocação: ")
    for i in matriz_alocacao:
        print(i)
    print("\nMatriz de Requisição: ")
    for i in matriz_requisicao:
        print(i)

    
    print("\nVerificando fórmula :")
    valor_coluna = 0
    indice = 0
    for i in range(0, int(processo_recurso[0]) + 1):
        for item in matriz_alocacao:
            if(indice == i):
                 valor_coluna = valor_coluna + int(item[i])
            elif(indice != i):
                if(valor_coluna + int(recursos_disponiveis[indice]) == int(recursos_existentes[indice])):
                    print("Coluna ", indice + 1, ": OK")
                valor_coluna = 0
                indice = i
                valor_coluna = valor_coluna + int(item[i])

    if(valor_coluna + int(recursos_disponiveis[indice]) == int(recursos_existentes[indice])):
                    print("Coluna ", indice + 1, ": OK")
    
    print("\nVerificando possibilidade de execução dos processos: \n")

    contador_item = 0
    contador_erro = []
    indice2 = 1
    for i in range(0, int(processo_recurso[0])):
        contador_erro.clear()
        indice2 = 1
        print("=>  Rodada ", i + 1)
        lista_retorno = verificar_possibilidade(contador_erro=contador_erro, indice2=indice2, contador_item=contador_item, processo_recurso=processo_recurso, matriz_requisicao=matriz_requisicao, recursos_disponiveis=recursos_disponiveis, matriz_alocacao=matriz_alocacao, rodada= i + 1, zero_array=zero_array)
        recursos_disponiveis = lista_retorno[0]
        print("\n")

    #ultima verificação
    if(lista_retorno[2] != []):
        for i in range(0, int(processo_recurso[1])):
            if(int(lista_retorno[2][i]) > int(recursos_disponiveis[i])):
                resultado = int(lista_retorno[2][i]) - int(recursos_disponiveis[i])
                print("P" + str(lista_retorno[1]) + " está aguardando " + str(resultado) + " instâncias de R" + str(i + 1))
    else:
        print("Sucesso! Todos os processos foram finalizados.\n")

    sair()
    
def verificar_possibilidade(contador_erro, indice2, contador_item, processo_recurso, matriz_requisicao, recursos_disponiveis, matriz_alocacao, rodada, zero_array):
    
    ultimo = 0
    ultima_linha = []
    #laço da matriz
    for i in range(0, int(processo_recurso[0])):
        for j in range(0, int(processo_recurso[1])):
            #se a linha da matriz não estiver zerada
            if(matriz_alocacao[i] != zero_array):
                #se o contador de ítens for menor que 4
                if(contador_item < int(processo_recurso[1])):
                    #se o ítem da matriz for maior que o valor do recurso disponível 
                    if(int(matriz_requisicao[i][j]) > int(recursos_disponiveis[j])):
                        contador_erro.append(0)
                        if(rodada < int(processo_recurso[0])):
                            resultado = int(matriz_requisicao[i][j]) - int(recursos_disponiveis[j])
                            print("P" + str(indice2) + " está aguardando " + str(resultado) + " instâncias de R" + str(j + 1))
                        else:
                            ultimo = indice2
                            ultima_linha = matriz_requisicao[i]
                        
                    else:
                        contador_erro.append(1)
                    
                #se não se o contador de ítens for igual a quatro   
                elif(contador_item == int(processo_recurso[1])):
                    print("P" + str(indice2), 'está aguardando recursos')
                    if(sum(contador_erro) == int(processo_recurso[1])):
                        
                        recursos_disponiveis = subtrair_recursos(indice2=indice2, recursos=recursos_disponiveis, matriz=matriz_alocacao, matriz2=matriz_requisicao,zero_array=zero_array)
                    
                    contador_erro.clear()
                    indice2 = indice2 + 1
                    contador_item = 0
                    
                contador_item = contador_item + 1
                    
    recursos_disponiveis = subtrair_recursos(indice2=indice2, recursos=recursos_disponiveis, matriz=matriz_alocacao, matriz2=matriz_requisicao,zero_array=zero_array)

    return [recursos_disponiveis, ultimo, ultima_linha]


def menu(): 
    print("Escolha uma matriz: 1 | 2 | 3 \n Selecione 0 para acabar o programa")
    escolha = int(input("Digite a sua escolha: "))
    arquivo1 = open("arquivo1.txt")
    arquivo2 = open("arquivo2.txt")
    arquivo3 = open("arquivo3.txt")
    if escolha < 0 or escolha > 4:
        return
    elif escolha == 0:
        return 0 
    else:
        carregar(escolha)

def sair():
    escolha = int(input("\n\nDigite 0 para sair: "))

menu()