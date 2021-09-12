# -*- coding: utf-8 -*-

import csv
import random

#funcao que calcula os valores: tp, fp, tn e fn e retorna os resultados
def calcularClassificacoes(theta, thetaZero, numeroDeEpocas, v, coluna1):    
    #inicializa a lista classificacoes tudo a 0
    classificacoes = [0] * len(coluna1)
    #percorrer cada mensagem do conjunto de teste
    for i in range(len(v)):
        aux = 0
        #fazer o produto interno de theta com v
        for j in range(len(v[i])):
            aux = aux + theta[j] * v[i][j]
        aux = aux + thetaZero
        #se for positivo é classificado como ham, se der negativo é classificado como spam
        if(aux >= 0):               
            classificacoes[i] = 1
        else:
            classificacoes[i] = -1        
    
    hC = 0
    hE = 0
    sC = 0
    sE = 0
    #classificar as classifições: se for 1 é ham, se for -1 é spam
    for i in range(len(coluna1)):
        if(coluna1[i] == "ham"):            
            if(classificacoes[i] == 1):
                hC = hC + 1
            else:
                hE = hE + 1
        elif(coluna1[i] == "spam"):
            if(classificacoes[i] == -1):
                sC = sC + 1
            else:
                sE = sE + 1
                
    print("\nAcabou de verificar as classificações para ", numeroDeEpocas, " numeros de épocas:\n")
    #mostrar quantos valores de ham e de spam acertou e errou
    print("Ham corretos: ", hC)
    print("Ham errados: ", hE)
    print("Spam corretos: ", sC)
    print("Spam errados: ", sE)
    #hC = ham correto = tp = true positive
    #hE = ham errado = fp = false positive
    #sC = spam correto = tn = true negative
    #sE = spam errado = fn = false negative
    valores = [hC, hE, sC, sE]
    #retorna os valores calculados
    return valores

#funcao que vai testar o algoritmo com o todos os valores de todos os calculos que foram reunidos até agora
def funcaoValidacao(validacao, valores):
    coluna1 = validacao[0]
    coluna2 = validacao[1]
    p = valores[0]
    conjuntoDeThetas = valores[1]
    
    #chama a funcao calcularXi que recebe o p e o coluna2 e calcula as frequencias absolutas 
    #de cada palavra em cada mensagem do conjunto de validacao
    v = calcularXi(p, coluna2)
    
    numeroDeEpocas = valores[2]
    t = valores[3]
    
    #a partir dos valores retornados da funcaoTeste já se sabe quais são os melhores thetas e thetaZeros
    theta = conjuntoDeThetas[t.index(numeroDeEpocas)][0]
    thetaZero = conjuntoDeThetas[t.index(numeroDeEpocas)][1]
    
    #chama uma funcao que calcula os valores: tp, fp, tn e fn e retorna os resultados
    calcularClassificacoes(theta, thetaZero, numeroDeEpocas, v, coluna1)

#funcao que trata da escolha do melhor T dependendo de determinados metricas de classificacao
def funcaoTeste(teste, valores):
    coluna1 = teste[0]
    coluna2 = teste[1]
    p = valores[0]
    conjuntoDeThetas = valores[1]    
    t = valores[2] 
    
    #chama a funcao calcularXi que recebe o p e o coluna2 e calcula as frequencias absolutas 
    #de cada palavra em cada mensagem do conjunto de teste
    v = calcularXi(p, coluna2)
    
    
    
    #criar as listas que vao verificar qual é o melhor T
    calcularMinimosErradosT = []    
    calcularAccuracyT = []
    calcularErrorRateT = []
    calcularPrecisaoT = []
    
    #vamos classificar os dados de validacao com os diferentes valores de T para escolhermos o melhor
    for cT in range(len(t)):
        numeroDeEpocas = t[cT]
        theta = conjuntoDeThetas[cT][0]
        thetaZero = conjuntoDeThetas[cT][1]
        #chama a funcao que calcula os valores: tp, fp, tn e fn e retorna os resultados
        valores = calcularClassificacoes(theta, thetaZero, numeroDeEpocas, v, coluna1)        
        tp = valores[0]
        fp = valores[1]
        tn = valores[2]
        fn = valores[3]
        
        #mostra o resultado das métricas e adiciona às listas supostas os resultados
        calcularMinimosErradosT.append(fp + fn)
        print("Erradas: ", (fp + fn))
        
        calcularAccuracyT.append((tp + tn)/(tp + fp + tn + fn))
        print("Accuracy: ", (tp + tn)/(tp + fp + tn + fn))
        
        calcularErrorRateT.append((fp + fn)/(tp + fp + tn + fn))
        print("Error Rate: ", (fp + fn)/(tp + fp + tn + fn))
                
        calcularPrecisaoT.append(tp/(tp + fp))
        print("Precisão: ", (fp + fn)/(tp + fp + tn + fn))
        
    #calcula os melhores valores de T para as determinadas métricas
    MinimosErradosT = calcularMinimosErradosT.index(min(calcularMinimosErradosT))
    MaxAccT = calcularAccuracyT.index(max(calcularAccuracyT))
    MinErrT = calcularErrorRateT.index(min(calcularErrorRateT))
    MaxPreT = calcularPrecisaoT.index(max(calcularPrecisaoT))
    
    #Mostra quais foram os melhores valores de T para as determinadas Métricas
    print("\n\nErrou menos: ", t[MinimosErradosT])
    print("Maior Acc: ", t[MaxAccT])
    print("Menor taxa de erros: ", t[MinErrT])
    print("Maior precisão: ", t[MaxPreT])
    
    #cada uma das 4 posições representa um valor de T, dependendo de qual receber mais votos ganha
    escolha = [0] * len(t)
    votos = []
    votos.append(MinimosErradosT)
    votos.append(MaxAccT)
    votos.append(MinErrT)
    votos.append(MaxPreT)
    
    #faz os votos
    for i in range(len(votos)):
        escolha[votos[i]] = escolha[votos[i]] + 1
    print("\n\nVotos: ", escolha)
    #o melhor T é o valor que tiver mais votos
    melhorT = t[escolha.index(max(escolha))]
    
    print("\n\nO melhor T foi: ", melhorT)
    
    retorno = [p, conjuntoDeThetas, melhorT, t]
    #retorna o melhor valor de T
    return retorno


#funcao que recebe o p e o x e calcula as frequencias absolutas de cada palavra em cada mensagem do conjunto de x
def calcularXi(p, x):
    #inicializa-se o xi a vazio
    xi = []
    
    #percorrer cada mensagem
    for mensagem in x:
        split = mensagem.split()
        #percorrer palavra do lexico
        numeroDePalavrasDoLexico = []
        for lexico in p:
            numero = 0
            #percorrer cada palavra de cada mensagem
            for palavraDaMensagem in split:
                #se a palavra da mensagem for igual a palavra do lexico adiciona-se a variavel numero o valor dela mais 1
                if(palavraDaMensagem == lexico):
                    numero = numero + 1
            #aux vai ter o numero de vezes que uma palavra do lexico aparece numa determinada mensagem
            aux = numero
            #adiciona-se aux à lista numeroDePalavrasDoLexico
            numeroDePalavrasDoLexico.append(aux)
        #no final de correr o lexico de palavras todo, adiciona-se a lista numeroDePalavrasDoLexico à lista xi e passa-se para a prox mensagem
        xi.append(numeroDePalavrasDoLexico)
    print("\nAcabou de calcular o Xi.\n")
    #no final de percorrer todas as mensagens retorna-se xi
    return xi


#funcao que recebe o m e calcula o p (bag of words)
def calcularPalavras(m):
    #inicializa-se o p a vazio
    p = []
    #percorre cada mensagem
    for i in range(m):
        #dividir as frases em palavras
        split = coluna2[i].split()
        #precorrer as palavras nas frases e verificar se a palavra ainda não existe em p, se não adiciona-se
        for j in range (len(split)):
            if(split[j] not in p):
                p.append(split[j])
                    
    print('\nAcabou de calcular o Léxico de palavras (p).\n')
    #retorna p
    return p
    
        
def funcaoTreino(treino):
    coluna1 = treino[0]
    coluna2 = treino[1]
    m = 0
    #as frequencias absolutas no iesimo x
    xi = []    
    #y tem as labels
    y = []    
    #theta é uma lista de listas
    #cada elemento do theta é uma lista do dicionário de palavras, com o numero de vezes que essa palavra aparece nessa mensagem
    theta = []    
    #bag of words
    p = []
    #[0] -> palavra
    
    #precorrer a coluna1
    for i in range(len(coluna1)):
        #classificar ham como 1 e spam como -1
        if(coluna1[i] == "ham"):
            y.append(1)
        elif(coluna1[i] == "spam"):
            y.append(-1)
        m = m + 1
    
    print('\nAcabou de calcular as mensagens.\n')
    #funcao que recebe o m e calcula o p (bag of words)
    p = calcularPalavras(m)
    
    
    #funcao que recebe o p e o x e calcula as frequencias absolutas de cada palavra em cada mensagem do conjunto de treino
    xi = calcularXi(p, coluna2)
    
    #a lista t tem as opções de numeros de epocas que vão ser avaliadas para se perceber qual é o melhor T
    t = [1, 3, 5, 10]
    #variavel que vai ter os diferentes conjuntos de thetas, [0] = theta, [1] = thetaZero
    conjuntoDeThetas = []
    
    #precorrer o algoritmo do perceptrao para cada opção de T
    for numeroDeEpocas in t:
            
        #preencher o theta a 0
        theta = [0] * len(p)
        
        #inicializar o tetaZero com 0
        thetaZero = 0
        
        #algoritmo do perceptrão:
        #precorrer o algoritmo para cada t igual a numeroDeEpocas
        for epoca in range(numeroDeEpocas):
            #precorrer cada mensagem
            for i in range(len(coluna2)):
                #declarar aux = 0
                aux = 0
                #fazer o produto interno de theta com xi
                for j in range(len(theta)):
                    aux = aux + theta[j] * xi[i][j]
                #adicionar thetaZero ao numero produto interno de theta e xi
                aux = aux + thetaZero
                #verificar se acertou na predição
                if(y[i] * aux <= 0):
                    #se não acertou vai adicionar a cada valor de theta o seu valor
                    #somado com a multiplicacao de cada vez que cada valor de theta aparece em cada mensagem
                    #com 1 ou -1, dependendo da label da mensagem
                    for l in range(len(theta)):
                        theta[l] = theta[l] + y[i] * xi[i][l]
                    thetaZero = thetaZero + y[i]  
        #adicionar o theta e o thetaZero ao conjunto de thetas, para no final de percorrer t, verificar-se qual o melhor t
        conjuntoDeThetas.append([theta, thetaZero])
        print("Acabou agora de calcular o theta e o thetaZero para ", numeroDeEpocas, " número(s) de epocas!\n")
    print('\nAcabou de calcular os diferentes thetas.\n')
    #no final retorna-se o p (bag of words) e o conjuntoDeThetas
    retorno = [p, conjuntoDeThetas, t]
    return retorno
#---------------------------inicio do programa--------------------------------
#criar as listas coluna1, coluna2 e linha
coluna1 = []
coluna2 = []
linha = []

#ir buscar os dados necessários ao ficheiro spam.csv
with open('spam.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='#')
    line_count = 0
    #string que contém os simbolos que vão ser apagados pois não são relevantes
    retirar = '''!()-[]{};:'"\, <>./?@#$%^&*_~0123456789'''
    i = 0
    
    for row in csv_reader:
        #passar a frente o cabeçalho (v1, v2,,,)
        if(i == 0):
            i = i + 1
        else:
            #dividir apenas uma vez para podermos ter a palavra "ham" ou "spam" no split[0] e termos o resto da mensagem no split[1]
            split = row[0].split(',', 1)
            if(len(split[1]) != 0):
                linha.append(split[0] + "-----^^-----" + split[1].lower())
            i = i + 1
    #baralhar as linhas
    random.shuffle(linha)
    #depois de baralhadas vamos adicionar cada linha ao par de colunas
    for i in linha:
        split = i.split("-----^^-----")
        coluna1.append(split[0])
        coluna2.append(split[1])
    print('\nAcabou de ler dados do ficheiro.\n')
    
    #retirar pontuação de cada linha da coluna2 e colocar um espaço em vez disso
    for ele in range(len(coluna2)):
        for ele2 in range(len(coluna2[ele])):            
            if coluna2[ele][ele2] in retirar:
                coluna2[ele] = coluna2[ele].replace(coluna2[ele][ele2], " ")
    
    
#colocar na variavel treino 70 por cento dos dados 
coluna1Aux = coluna1[:int(len(coluna1)*0.7)]
coluna2Aux = coluna2[:int(len(coluna2)*0.7)]
treino = coluna1Aux, coluna2Aux

#colocar na variavel validacao 15 por cento dos dados
coluna1Aux = coluna1[int(len(coluna1)*0.7):int(len(coluna1)*0.85)]
coluna2Aux = coluna2[int(len(coluna2)*0.7):int(len(coluna2)*0.85)]
teste = coluna1Aux, coluna2Aux

#colocar na variavel teste os restantes 15 por cento dos dados
coluna1Aux = coluna1[int(len(coluna1)*0.85):]
coluna2Aux = coluna2[int(len(coluna2)*0.85):]
validacao = coluna1Aux, coluna2Aux

#chamar a funcao funcaoTreino que leva como parametro a variavel treino que é o dicionario de dados do conjunto de treino
#e que retorna para a variavel valores um conjunto de dados importantes para os restantes conjuntos
print("\n\n\tCONJUNTO DE TREINO\n")
valores = funcaoTreino(treino)

#chamar a funcao funcaoTeste que leva como parametros a variavel teste e os valores retornados da funcao anterior
#e retorna para a variavel valores o melhorT para ser utilizado no conjunto de teste
print("\n\n\tCONJUNTO DE TESTE\n")
valores = funcaoTeste(teste, valores)

#chamar a funcao funcaoValidacao que leva como parametros a variavel validacao e os valores retornados das funcoes anteriores
print("\n\n\tCONJUNTO DE VALIDAÇÃO\n")
funcaoValidacao(validacao, valores)