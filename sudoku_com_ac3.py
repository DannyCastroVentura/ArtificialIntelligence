# -*- coding: utf-8 -*-
import queue

#função usada para dadas as coordenadas de um quadrado, guardar numa lista quais são os quadrados vizinhos e retorna-la
def neighbors(linha, coluna, q):
    neighborsAux = []
    for linhaAux in range(9):
        for colunaAux in range(9):
            if((linhaAux == linha) and (colunaAux == coluna)):
                pass
            else:
                if(linhaAux == linha) or (colunaAux == coluna) or (verificarSeEstaoNoMesmoQuadrado(linha, coluna, linhaAux, colunaAux)):
                        neighborsAux.append([linhaAux, colunaAux])
    return neighborsAux
    

#função usada para a partir do csp e de dois quadrados, verificar se o segundo quadrado tem apenas uma opção para ser preenchido
#se sim retira-se esse valor do domínio de valores possíveis do primeiro quadrado 
def revise(csp, quadrado1, quadrado2):    
    linha1 = quadrado1[0]
    coluna1 = quadrado1[1]
    linha2 = quadrado2[0]
    coluna2 = quadrado2[1]
    revised = False
    aux = [linha1, coluna1]
    for i in csp[1][csp[0].index(aux)]:
        i = [i]
        if(len(csp[1][csp[0].index([linha2, coluna2])]) == 1) and (i == csp[1][csp[0].index([linha2, coluna2])]):
            csp[1][csp[0].index([linha1, coluna1])].pop(csp[1][csp[0].index([linha1, coluna1])].index(i[0]))
            revised = True
    return revised
            
            


#função que recebe como parâmetro o sudoku original e retorna o csp resolvido
def ac3(sudoku):
    q = queue.Queue()
    csp = [[], []]    
    #[0] = Linha & Coluna
    #[1] = ValoresPossiveis
    
    #adicionar os valores possiveis ao dominio dos diferentes quadrados
    for linha in range(9):
        for coluna in range(9):
            if(sudoku[linha][coluna] == 0):                
                csp[0].append([linha, coluna])
                csp[1].append([1,2,3,4,5,6,7,8,9])
            else:
                csp[0].append([linha, coluna])
                csp[1].append([sudoku[linha][coluna]])
                
    #CRIAR A PRIMEIRA FILA DE ARCOS
    #andar pelo sudoku com o primeiro quadrado
    for linhaA in range(9):
        for colunaA in range(9):
            #andar pelo sudoku com o segundo quadrado
            for linhaB in range(9):
                for colunaB in range(9):
                    #se estiverem na mesma posição passa a frente (um quadrado não pode ser arco dele próprio)
                    if((linhaA == linhaB) and (colunaA == colunaB)):
                        pass
                    else:
                        #verificar se têm ou a mesma linha, ou a mesma coluna ou se pretencem à mesma região
                        if(linhaA == linhaB) or (colunaA == colunaB) or (verificarSeEstaoNoMesmoQuadrado(linhaA, colunaA, linhaB, colunaB)):
                            q.put([[linhaA, colunaA], [linhaB, colunaB]])

    #percorrer a fila de arcos
    while not q.empty():
        arc = q.get()
        quadrado1 = arc[0]
        linha = quadrado1[0]
        coluna = quadrado1[1]
        quadrado2 = arc[1]
        #chama a função revise para verificar se o segundo quadrado tem apenas uma opção para ser preenchido, se sim retira-se esse valor do dominio do primeiro quadrado
        if(revise(csp, quadrado1, quadrado2)):
            #verificar se o dominio do primeiro quadrado ficou vazio, se sim retorna falso pois é impossivel de resolver com o ac-3
            if(len(csp[1][csp[0].index(quadrado1)]) == 0):
                return False
            else:
            #se não vai verificar os vizinhos do quadrado 1 pois como alterou o seu domínio já pode ter disponíbilizado novas oportunidades
                neighborsAux = neighbors(linha, coluna, q)
                for i in neighborsAux:
                    q.put([i, quadrado1])
                    q.put([quadrado1, i])
       
    #formata de forma a que seja mais visivel a trasnformação e retorna o sudoku resolvido
    k = 0
    for i in range (9):
        for j in range (9):
            sudoku[i][j] = csp[1][k]
            k = k + 1
    return sudoku
    
#função usada para verificar se dois quadrados estão na mesma região ou não
def verificarSeEstaoNoMesmoQuadrado(linhaA, colunaA, linhaB, colunaB):
    if(linhaA < 3) and (colunaA < 3) and (linhaB < 3) and (colunaB < 3):
        return True
    elif((linhaA < 6) and (linhaA >= 3)) and (colunaA < 3) and ((linhaB < 6) and (linhaB >= 3)) and (colunaB < 3):
        return True
    elif((linhaA < 9) and (linhaA >= 6)) and (colunaA < 3) and ((linhaB < 9) and (linhaB >= 6)) and (colunaB < 3):
        return True
    elif(linhaA < 3) and ((colunaA < 6) and (colunaA >= 3)) and (linhaB < 3) and ((colunaB < 6) and (colunaB >= 3)):
        return True
    elif((linhaA < 6) and (linhaA >= 3)) and ((colunaA < 6) and (colunaA >= 3)) and ((linhaB < 6) and (linhaB >= 3)) and ((colunaB < 6) and (colunaB >= 3)):
        return True
    elif((linhaA < 9) and (linhaA >= 6)) and((colunaA < 6) and (colunaA >= 3)) and ((linhaB < 9) and (linhaB >= 6)) and ((colunaB < 6) and (colunaB >= 3)):
        return True
    elif(linhaA < 3) and ((colunaA < 9) and (colunaA >= 6)) and (linhaB < 3) and ((colunaB < 9) and (colunaB >= 6)):
        return True
    elif((linhaA < 6) and (linhaA >= 3)) and ((colunaA < 9) and (colunaA >= 6)) and ((linhaB < 6) and (linhaB >= 3)) and ((colunaB < 9) and (colunaB >= 6)):
        return True
    elif((linhaA < 9) and (linhaA >= 6)) and ((colunaA < 9) and (colunaA >= 6)) and ((linhaB < 9) and (linhaB >= 6)) and ((colunaB < 9) and (colunaB >= 6)):
        return True
    else:
        return False
    
#coluna / linha
linha1 = [0] * 9
linha2 = [0] * 9
linha3 = [0] * 9
linha4 = [0] * 9
linha5 = [0] * 9
linha6 = [0] * 9
linha7 = [0] * 9
linha8 = [0] * 9
linha9 = [0] * 9

# primeira linha
linha1[2] = 3
linha1[4] = 2
linha1[6] = 6

# segunda linha
linha2[0] = 9
linha2[3] = 3
linha2[5] = 5
linha2[8] = 1

# terceira linha
linha3[2] = 1
linha3[3] = 8
linha3[5] = 6
linha3[6] = 4

# quarta linha
linha4[2] = 8
linha4[3] = 1
linha4[5] = 2
linha4[6] = 9

# quinta linha
linha5[0] = 7
linha5[8] = 8

# sexta linha
linha6[2] = 6
linha6[3] = 7
linha6[5] = 8
linha6[6] = 2

# setima linha
linha7[2] = 2
linha7[3] = 6
linha7[5] = 9
linha7[6] = 5

# oitava linha
linha8[0] = 8
linha8[3] = 2
linha8[5] = 3
linha8[8] = 9

# nona linha
linha9[2] = 5
linha9[4] = 1
linha9[6] = 3



sudoku = [linha1, linha2, linha3, linha4, linha5, linha6, linha7, linha8, linha9]



#mostrar como está o sudoku antes da sua resolução
for item in range(9):
    print(sudoku[item])




#iniciar o processo de resolução do sudoku
sudoku = ac3(sudoku)


#mostrar o sudoku resolvido
print("\nAspecto final do Sudoku: \n")
for item in range(9):
    print(sudoku[item])
    