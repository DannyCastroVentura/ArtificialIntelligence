# -*- coding: utf-8 -*-
import csv
import math
import random

#chama uma funcao que calcula os valores: tp, fp, tn e fn e retorna os resultados
def calcularClassificacoes(coluna1, coluna2 ,mHam, mSpam, p, c):
    b = math.log(c) + math.log(mHam) - math.log(mSpam)
        
    classificacoes = [] 
    for i in coluna2:
        #chama a funcao classify que retorna a classificacao de uma determinada mensagem
        #levando como parametros a mensagem, o b (treshold) e o p (bag of words)
        classificacao = classify(i, b, p)
        classificacoes.append(classificacao)


    print("\nAcabou de classificar as mensagens\n")
    
    #faz as contas de quais foram os hams e os spams que erraram e acertaram para o determinado c
    hC = 0
    hE = 0
    sC = 0
    sE = 0
    for i in range(len(classificacoes)):
        if(coluna1[i] == "ham"):            
            if("ham" == classificacoes[i]):
                hC = hC + 1
            else:
                hE = hE + 1
        else:
            if("spam" == classificacoes[i]):
                sC = sC + 1
            else:
                sE = sE + 1
    print("\nAcabou de verificar as classificações com c igual a ", c, ":\n")
    
    print("Ham corretos: ", hC)
    print("Ham errados: ", hE)
    print("Spam corretos: ", sC)
    print("Spam errados: ", sE)
    #hC = ham correto = tp = true positive
    #hE = ham errado = fp = false positive
    #sC = spam correto = tn = true negative
    #sE = spam errado = fn = false negative
    valores = [hC, hE, sC, sE]
    return valores

#funcao que vai testar o algoritmo com o todos os valores de todos os calculos que foram reunidos até agora
def funcaoValidacao(validacao, valores):
    coluna1 = validacao[0]
    coluna2 = validacao[1]
    mHam = valores[0]
    mSpam = valores[1]
    p = valores[2]
    a = valores[3]
    
    #chama uma funcao que calcula os valores: tp, fp, tn e fn e retorna os resultados
    calcularClassificacoes(coluna1, coluna2 ,mHam, mSpam, p, a)
    
#chama a funcao classify que retorna a classificacao de uma determinada mensagem
#levando como parametros a mensagem, o b (treshold) e o p (bag of words)
def classify(mensagem, b, p):  
    t = -b
    split = mensagem.split()
    #vai calcular palavra a palavra o logaritmo das vezes que aparecem no spam - (menos) o logaritmo das vezes que aparecem no ham
    #(dados em frequencia relativa) e vai somando o resultado ao t para no final se t for superior a 0, o email é classificado como
    #spam, senão o email é classificado como ham.
    for k in split:
        if(k in p[0]):
            t = t + (math.log(p[2][p[0].index(k)]) - math.log(p[1][p[0].index(k)]))
        
    if(t>0):
        return "spam"
    else:
        return "ham"

#funcao que trata da escolha do melhor c dependendo de determinados metricas de classificacao
def funcaoTeste(teste, valores):    
    
    coluna1 = teste[0]
    coluna2 = teste[1]
    mHam = valores[0]
    mSpam = valores[1]
    p = valores[2]
    
    #vamos testar o c com os seguintes valores e vamos verificar qual dos 11 valores é o melhor para ser usado
    c = [0.05, 0.1, 0.5, 1, 5, 10, 20, 30, 50, 75, 100]
    
    #criar as listas que vao verificar qual é o melhor c
    calcularMinimosErradosC = []    
    calcularAccuracyC = []
    calcularErrorRateC = []
    calcularPrecisaoC = []

    #vamos classificar os dados de validacao com os diferentes valores de c para escolhermos o melhor
    for a in c:        
        #chama uma funcao que calcula os valores: tp, fp, tn e fn e retorna os resultados
        valores = calcularClassificacoes(coluna1, coluna2, mHam, mSpam, p, a)
        tp = valores[0]
        fp = valores[1]
        tn = valores[2]
        fn = valores[3]
        
        #mostra o resultado das métricas e adiciona às listas supostas os resultados
        calcularMinimosErradosC.append(fp + fn)
        print("Erradas: ", (fp + fn))
        
        calcularAccuracyC.append((tp + tn)/(tp + fp + tn + fn))
        print("Accuracy: ", (tp + tn)/(tp + fp + tn + fn))
        
        calcularErrorRateC.append((fp + fn)/(tp + fp + tn + fn))
        print("Error Rate: ", (fp + fn)/(tp + fp + tn + fn))
                
        calcularPrecisaoC.append(tp/(tp + fp))
        print("Precisão: ", (fp + fn)/(tp + fp + tn + fn))
        
    #calcula os melhores valores de c para as determinadas métricas
    MinimosErradosC = calcularMinimosErradosC.index(min(calcularMinimosErradosC))
    MaxAccC = calcularAccuracyC.index(max(calcularAccuracyC))
    MinErrC = calcularErrorRateC.index(min(calcularErrorRateC))
    MaxPrec = calcularPrecisaoC.index(max(calcularPrecisaoC))
    
    #Mostra quais foram os melhores valores de C para as determinadas Métricas
    print("\n\nErrou menos: ", c[MinimosErradosC])
    print("Maior Acc: ", c[MaxAccC])
    print("Menor taxa de erros: ", c[MinErrC])
    print("Maior precisão: ", c[MaxPrec])
    
    #cada uma das 11 posições representa um valor de c, dependendo de qual receber mais votos ganha
    escolha = [0] * len(c)
    votos = []
    votos.append(MinimosErradosC)
    votos.append(MaxAccC)
    votos.append(MinErrC)
    votos.append(MaxPrec)
    
    #faz os votos
    for i in range(len(votos)):
        escolha[votos[i]] = escolha[votos[i]] + 1
    print("\n\nVotos: ", escolha)
    #o melhor c é o valor que tiver mais votos
    melhorC = c[escolha.index(max(escolha))]
    
    print("\n\nO melhor C foi: ", melhorC)
    #retorna o melhor valor de C
    return melhorC


#funcao que normaliza o p(bag of words)
def normalizar(p, wHam, wSpam):
    for i in range(len(p[0])):        
        p[1][i] = p[1][i]/ wHam
        p[2][i] = p[2][i]/ wSpam
    print("\nAcabou de normalizar o P\n")
    
#funcao que calcula o p (bag of words)
def calcularPalavras(m, mHam, mSpam):    
    
    #bag of words
    p = [[], [], []]
    #[0] -> palavra
    #[1] -> numero de vezes que aparece no ham
    #[2] -> numero de vezes que aparece no spam
    
    wHamList = []
    wSpamList = []
    wHam = 0
    wSpam = 0
    #precorre cada uma das mensagens
    for i in range(m):
        #dividir as frases em palavras
        split = coluna2[i].split()
        #precorrer as palavras das frases e adiciona-las ao P
        #se já existem no p apenas incrementa-se o numero de vezes que a palavra 
        #aparece no ham ou no spam dependendo do suposto
        for j in range (len(split)):
            if(coluna1[i] == "ham"):
                if(split[j] in wHamList):
                    p[1][p[0].index(split[j])] = p[1][p[0].index(split[j])] + 1
                else:
                    p[0].append(split[j])
                    p[1].append(2)
                    p[2].append(1)
                    wHamList.append(split[j])
                    wHam = wHam + 1
                    
            elif(coluna1[i] == "spam"):
                if(split[j] in wSpamList):
                    p[2][p[0].index(split[j])] = p[2][p[0].index(split[j])] + 1
                else:
                    p[0].append(split[j])
                    p[1].append(1)
                    p[2].append(2)
                    wSpamList.append(split[j])                    
                    wSpam = wSpam + 1
    
    print('\nAcabou de calcular as palavras das mensagens.\n')
    
    #função que normaliza os dados do p (bag of words)
    normalizar(p, wHam, wSpam)
    return p
    
#funcao que trata do conjunto de treino
def funcaoTreino(treino):
    coluna1 = treino[0]
    m = 0
    mHam = 0
    mSpam = 0
    #precorrer a coluna1
    for i in range(len(coluna1)):
        #contar emails ham/spam
        if(coluna1[i] == "ham"):
            mHam = mHam + 1
        elif(coluna1[i] == "spam"):
            mSpam = mSpam + 1
        m = m + 1
    
    print('\nAcabou de calcular as mensagens.\n')
    
    #Funcao que recebe o m, mHam, mSpam e p e que calcula o p (bag of words)
    p = calcularPalavras(m, mHam, mSpam)
    
    #agrupa variaveis para retornar e retorna-as
    retorno = [mHam, mSpam, p]
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
            linha.append(split[0] + "," + split[1].lower())
            i = i + 1
    #baralhar as linhas
    random.shuffle(linha)
    #depois de baralhadas vamos adicionar cada linha ao par de colunas
    for i in linha:
        split = i.split(',', 1)
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
#e retorna para a variavel valores o melhorC para ser utilizado no conjunto de teste
print("\n\n\tCONJUNTO DE TESTE\n")
valores.append(funcaoTeste(teste, valores))

#chamar a funcao funcaoValidacao que leva como parametros a variavel validacao e os valores retornados das funcoes anteriores
print("\n\n\tCONJUNTO DE VALIDAÇÃO\n")
funcaoValidacao(validacao, valores)
