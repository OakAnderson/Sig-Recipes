# -*- coding: utf-8 -*-

from unicodedata import normalize
from random import randint
import os
import pickle
import smtplib
import validators
from email.mime.text import MIMEText

smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465

username = 'sig.recipes@gmail.com'
password = 'receitas123'

from_addr = 'sig.recipes@gmail.com'

def valida_email(email):
  if (email.find('@') == -1 or email.find('@') == 0):
    return False
  elif email.find('.') == -1 or email.find('.') == 0:
    return False
  else:
    return True
def remover_acentos(txt):
  return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
def pesquisar(pesquisa,modo):
  encontrados = []
  receita = pesquisa.split()
  if 'de' in receita:
    receita.remove('de')
  if 'para' in receita:
    receita.remove('para')
  if 'com' in receita:
    receita.remove('com')
  if len(receita) > 1:
    for i in receitas:
      for p in range(len(receita)-1):
        if receita[p] in receitas[i][1]:
          if receita[p+1] in receitas[i][1]:
            if i not in encontrados:
              encontrados.append(i)
  elif len(receita) == 1:
    for i in receitas:
      arquivo = open(receitas[i][3], 'r', encoding='utf8')
      receita = ''.join(receita)
      for p in receitas[i][1]:
        if p.lower().find(receita.lower()) >= 0 or receita in receitas[i][1]:
          if i not in encontrados:
            encontrados.append(i)
      for l in arquivo.readlines():
        if l.lower().find(receita.lower()) > -1 and not receita.lower().isdigit() and len(receita) >= 3:
          if i not in encontrados:
            encontrados.append(i)
      arquivo.close()
        
  count = 0
  for i in encontrados:
    count += 1
    print(f'#{count} - {receitas[i][0]}  {receitas[i][2]}min')
  if count == 0 and pesquisa == '':
    return ''
  elif count == 0:
    print('Nenhuma receita foi encontrada! Tente novamente com outra palavra chave.')
    return ''
  elif count > 0:
    done = False
    while not done:
      print()
      escolha = input(f'{modo} receita n°: ')
      if escolha == '':
        print()
        done = True
      elif escolha.lower() == 'ajuda':
          menu()
      elif escolha.isdigit():
        if int(escolha) > count:
          print('Digite apenas os valores apresentados acima.')
        else:
          if modo == 'Editar':
            abrirEdit(open(receitas[encontrados[int(escolha)-1]][3], 'r', encoding='utf8'))
          else:
            abrir(open(receitas[encontrados[int(escolha)-1]][3], 'r', encoding='utf8'), receitas[encontrados[int(escolha)-1]][3], modo)
            return receitas[encontrados[int(escolha)-1]][3]
          done = True
      else:
        print('Digite ajuda para saber os comandos ou aperte enter para voltar.')  
def menu():
  os.system('cls')
  print('|%s|'%('-'*70))
  print('SIG-Recipes'.center(72))
  print('|%s|'%('-'*70))
  print('OPERAÇÕES'.center(72))
  print()
  print(' Clique o botão enter para voltar para o menu anterior')
  print(' Utilize apenas "s" e "n" para sim ou não.')
  print(' Digite ajuda para mostrar esse menu novamente.')
  print(' 1 - Pesquisar')
  print(' 2 - Todas as Receitas')
  print(' 3 - Criar')
  print(' 4 - Editar')
  print(' 5 - Deletar')
  print(' Para sair digite "sair" no campo operação. ')
  print('|%s|'%('-'*70))
  print()
def abrir(receita,arquivo,modo):
  cont = 0
  arquivoEmail = []
  for linha in receita.readlines():
    if linha[0] == '*':
      print()
      arquivoEmail.append(f'\n{linha[1:].upper().center(72)}\n')
      print(linha[1:].upper().center(72))
    elif linha[0] == ';':
      print()
      arquivoEmail.append(f'{linha[1:].title().center(72)}')
      print(linha[1:].title().center(72))
    elif linha[0] == '/':
      print()
      arquivoEmail.append(f'\n{linha[1:].capitalize().center(72)}\n')
      print(linha[1:].capitalize().center(72))
    else:
      arquivoEmail.append(linha)
      print(linha,end='')
    cont += 1
  print()
  receita.close()
  if modo.lower() == 'vizualizar' or modo.lower() == 'v':
    for i in receitas:
      if arquivo in receitas[i] and len(receitas[i]) > 4:
        decisao = input('\nDeseja vizualizar o site da receita? ')
        arquivoEmail.append(f'\n\n{receitas[i][4]}')
        if decisao.lower() == 's':
          os.startfile(receitas[i][4])
        elif decisao == 'ajuda':
          menu()
      if arquivo in receitas[i]:
        nomeReceita = receitas[i][0]
    decisao = input('\nDeseja receber esta receita por email? ')
    if decisao.lower() == 's':
      to_addrs = input('Digite o seu e-mail: ')
      if to_addrs == '':
        print()
      elif to_addrs == 'ajuda':
        menu()
      else:
        while not valida_email(to_addrs):
          print('\nEmail inválido! '.center(10))
          print('Tente algo como: fulano@dominio.com')
          to_addrs = input('\nDigite o seu e-mail: ')
        if valida_email(to_addrs):
          print('\nA receita será enviada para este email.')
          mensagem = ''.join(arquivoEmail)
          message = MIMEText(mensagem)
          message['subject'] = nomeReceita
          message['from'] = from_addr
          message['to'] = to_addrs

          server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
          server.login(username, password)
          server.sendmail(from_addr, to_addrs, message.as_string())
          server.quit()
          print('\n\nReceita enviada com sucesso. Verifique sua caixa de entrada.\n')
def abrirEdit(receita):
  count = 1
  for linha in receita.readlines():
    if linha[0] == '*':
      print()
      print(count,linha[1:].upper().center(72))
    elif linha[0] == ';':
      print()
      print(count,linha[1:].title().center(72))
    elif linha[0] == '/':
      print()
      print(count,linha[1:].capitalize())
    else:
      print(count,linha,end='')
    count += 1
  print()
  receita.close()
def seguranca():
  letrasSeguranca = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'w', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  senha = []
  for i in range(5):
    i = i
    x = randint(0, 60)
    senha += [letrasSeguranca[x]]
  return senha
def converterb_d(n):
    decimal = 0
    n = str(n)
    n = n[::-1]
    tam = len(n)
    for i in range(tam):
        if n[i] == "1":
            decimal = decimal + 2**i
    return decimal
def editInstructions():
  print('Instruções para editar uma receita'.title().center(72,'-'))
  print('''
    1 - primeiro você vai pesquisar a receita a ser editada pelo nome
    2 - em seguida você escolherá a sua receita pelo número
    3 - após isso sua receita será apresentada linha à linha, você irá
    editar digitando a nova parte abaixo da apresentada.
    4 - caso não queira editar a linha apresentada apenas dê um enter
    que você irá para a próxima linha.
    Boa sorte :)
    ''')

arquivo = open('receitas.pck', 'rb')
receitas = pickle.load(arquivo)
arquivo.close()

menu()
print()
comando = ''
while comando != 'sair':
  print('')
  buscando = False
  imprimir = False
  deletar = False
  criar = False
  criarVelha = False
  editar = False
  comando = input('Operação: ')
  if comando.isdigit():
    if int(comando) == 1:
      buscando = True
    elif int(comando) == 2:
      imprimir = True
    elif int(comando) == 3:
      feito = False
      while not feito:
        print('\n1 - Criar nova receita')
        print('2 - Modificar receita já existente')
        escolha = input('')
        if escolha.isdigit():
          if int(escolha) == 1:
            criar = True
            feito = True
          elif int(escolha) == 2:
            criarVelha = True
            feito = True
          else:
            print('Digite apenas 1 ou 2.')
        elif escolha == '':
          feito = True
        elif escolha == 'ajuda':
          menu()
    elif int(comando) == 4:
      editar = True
    elif int(comando) == 5:
      deletar = True
    elif int(comando) <= 0:
      print('Isso não é um comando!')
    else:
      print('Isso não é um comando!')
  elif comando.lower() == 'ajuda' or comando == '':
      menu()
  elif comando != 'sair':
    print('Isso não é um comando!')

  while buscando:
    nome = input('\nPesquisar: ')
    if nome == '':
      buscando = False
    elif nome == 'ajuda':
      menu()
    else:
      pesquisar(nome,'Vizualizar')
      buscando = False
  while imprimir:
    print()
    print('1 - Mostrar todas as receitas')
    print('2 - Mostrar receitas por tempo de preparo')
    print('3 - Mostrar receitas doces ou salgadas')
    print()
    decisao = input('')
    if decisao.isdigit():
      todas = False
      porTempo = False
      porTipo = False

      if int(decisao) == 1:
        todas = True
      elif int(decisao) == 2:
        porTempo = True
      elif int(decisao) == 3:
        porTipo = True
      
      if todas:
        pesquisar('todas','Vizualizar')
        imprimir = False
      while porTempo:
        print()
        print('1 - receitas rápidas')
        print('2 - receitas com tempo médio')
        print('3 - receitas demoradas')
        print()
        tempo = input('')
        if tempo.isdigit():
          if int(tempo) == 1:
            count = 0
            print()
            for i in receitas:
              receita = receitas[i][2]
              if receita <= 30:
                count += 1
                print(f'#{count} - {receitas[i][0]}  {receitas[i][2]}min')
            print()
            escolha = input('Vizualizar receita n°: ')
            if escolha.isdigit():
              if int(escolha) > count or int(escolha) < 1:
                print('Digite apenas os valores apresentados acima!')
              else:
                count2 = 0
                for i in receitas:
                  receita = receitas[i][2]
                  if receita <= 30:
                    count2 += 1
                  if receita <= 30 and count2 == int(escolha):
                    abrir(open(receitas[i][3], 'r', encoding='utf8'), receitas[i][3], 'v')
                    porTempo = False
                    imprimir = False
            elif escolha == '':
              porTempo = False
            elif escolha == 'ajuda':
              menu()
            else:
              print('Comando desconhecido. Tente outra coisa ou digite ajuda para mostrar o menu')
          elif int(tempo) == 2:
            count = 0
            print()
            for i in receitas:
              receita = receitas[i][2]
              if receita > 30 and receita <= 60:
                count += 1
                print(f'#{count} - {receitas[i][0]}  {receitas[i][2]}min')
            print()
            escolha = input('Vizualizar receita n°: ')
            if escolha.isdigit():
              if int(escolha) > count or int(escolha) < 1:
                print('Digite apenas os valores apresentados acima!')
              else:
                count2 = 0
                for i in receitas:
                  receita = receitas[i][2]
                  if receita > 30 and receita <= 60:
                    count2 += 1
                  if (receita > 30 and receita <= 60) and count2 == int(escolha):
                    abrir(open(receitas[i][3], 'r', encoding='utf8'), receitas[i][3], 'v')
                    porTempo = False
                    imprimir = False
            elif escolha == '':
              porTempo = False
            elif escolha == 'ajuda':
              menu()
            else:
              print('Comando desconhecido. Tente outra coisa ou digite ajuda para mostrar o menu')
          elif int(tempo) == 3:
            count = 0
            print()
            for i in receitas:
              receita = receitas[i][2]
              if receita > 60:
                count += 1
                print(f'#{count} - {receitas[i][0]}  {receitas[i][2]}min')
            print()
            escolha = input('Vizualizar receita n°: ')
            if escolha.isdigit():
              if int(escolha) > count or int(escolha) < 1:
                print('Digite apenas os valores apresentados acima!')
              else:
                count2 = 0
                for i in receitas:
                  receita = receitas[i][2]
                  if receita > 60:
                    count2 += 1
                  if receita > 60 and count2 == int(escolha):
                    abrir(open(receitas[i][3], 'r', encoding='utf8'), receitas[i][3], 'v')
                    porTempo = False
                    imprimir = False
            elif escolha == '':
              porTempo = False
            elif escolha == 'ajuda':
              menu()
            else:
              print('Comando desconhecido. Tente outra coisa ou digite ajuda para mostrar o menu')
        elif tempo == '':
          porTempo = False
        elif tempo == 'ajuda':
          menu()
        else:
          print('Comando desconhecido. Tente outra coisa ou digite ajuda para mostrar o menu')
      while porTipo:
        print()
        print('1 - receitas doces')
        print('2 - receitas salgadas')
        decisao = input('')
        if decisao == '':
          porTipo = False
        elif decisao == 'ajuda':
          menu()
        elif decisao.isdigit():
          if int(decisao) == 1:
            count = 0
            print()
            for i in receitas:
              receita = receitas[i][1]
              if 'doce' in receita:
                count += 1
                print(f'#{count} - {receitas[i][0]}  {receitas[i][2]}min')
            print()
            escolha = input('Vizualizar receita n°: ')
            if escolha.isdigit():
              if int(escolha) > count or int(escolha) < 1:
                print('Digite apenas os valores apresentados acima!')
              else:
                count2 = 0
                for i in receitas:
                  receita = receitas[i][1]
                  if 'doce' in receita:
                    count2 += 1
                  if 'doce' in receita and count2 == int(escolha):
                    abrir(open(receitas[i][3], 'r', encoding='utf8'), receitas[i][3], 'v')
                    porTipo = False
                    imprimir = False
            elif escolha == '':
              porTipo = False
            elif escolha == 'ajuda':
              menu()
          elif int(decisao) == 2:
            count = 0
            print()
            for i in receitas:
              receita = receitas[i][1]
              if 'salgado' in receita:
                count += 1
                print(f'#{count} - {receitas[i][0]}  {receitas[i][2]}min')
            print()
            escolha = input('Vizualizar receita n°: ')
            if escolha.isdigit():
              if int(escolha) > count or int(escolha) < 1:
                print('Digite apenas os valores apresentados acima!')
              else:
                count2 = 0
                for i in receitas:
                  receita = receitas[i][1]
                  if 'salgado' in receita:
                    count2 += 1
                  if 'salgado' in receita and count2 == int(escolha):
                    abrir(open(receitas[i][3], 'r', encoding='utf8'), receitas[i][3], 'v')
                    porTipo = False
                    imprimir = False
            elif escolha == '':
              porTipo = False
            elif escolha == 'ajuda':
              menu()

    elif decisao == '':
      imprimir = False
    elif decisao == 'ajuda':
      menu()
    else:
      print('Comando desconhecido. Tente outra coisa ou digite ajuda para mostrar o menu')      
  while criarVelha:
    titulo = 'falso'
    print('Receita a modificar:')
    pesquisa = str(input(''))
    if pesquisa == '':
      criarVelha= False
    elif pesquisa == 'ajuda':
      menu()
    print()
    arquivo = pesquisar(pesquisa, 'Modificar')
    editando = False
    if len(arquivo) > 0:
      receita = open(arquivo, 'r', encoding='utf8')
      receitaEdit = receita.readlines()
      receita.close()
      editando = True
    while editando:
      ingrediente = input('\nDigite o ingrediente que irá substituir: ').lower()
      ingredienteNovo = input('Digite o novo ingrediente: ').lower()
      cont = 0
      for i in range(len(receitaEdit)):
        if receitaEdit[i].lower().find(ingrediente) > -1:
          receitaEdit[i] = receitaEdit[i].replace(ingrediente, ingredienteNovo)
          if receitaEdit[i][0] == ';':
            titulo = ingrediente
            tituloNovo = ingredienteNovo
          cont += 1
      if cont >= 1:
        for linha in receitaEdit:
          if linha[0] == '*':
            print()
            print(linha[1:].upper().center(72))
          elif linha[0] == ';':
            print()
            print(linha[1:].title().center(72))
          elif linha[0] == '/':
            print()
            print(linha[1:].capitalize())
          else:
            print(linha,end='')
          for i in receitas:
            if arquivo in receitas[i]:
              chaves = receitas[i][1]
        if ingrediente in chaves:
          chaves = (' '.join(chaves).replace(ingrediente, ingredienteNovo)).split()
          if remover_acentos(ingredienteNovo) != ingredienteNovo:
            chaves.append(remover_acentos(ingredienteNovo))
          if remover_acentos(ingrediente) != ingrediente:
            chaves.remove(remover_acentos(ingrediente))
        print()
        print('1 - modificar mais um ingrediente')
        print('2 - salvar')
        decisao = input('')
        print()
        if decisao == '1':
          continue
        elif decisao == '2':
          for i in receitas:
            if arquivo in receitas[i]:
              receita = receitas[i][:]
          if titulo != 'falso':
            receita[0] = receita[0].lower().replace(titulo.lower(), tituloNovo.lower())
            receita[0] = receita[0].capitalize()
          else:
            receita[0] = list(receita[0].capitalize())
            receita[0].append(' (modificada)')
            receita[0] = ''.join(receita[0])
          receita[1] = chaves
          receita[3] = list(receita[0])
          receita[3].append('.txt')
          receita[3] = ''.join(receita[3])
          novaReceita = open(receita[3], 'w', encoding='utf8')
          novaReceita.writelines(receitaEdit)
          novo = format(len(receitas),'07b')
          receitas[novo] = receita
          novaReceita.close()
          pickle.dump(receitas, open('receitas.pck', 'wb'))
          print('Receita criada com sucesso!')
          criarVelha = False
          editando = False
      elif cont < 1:
        print()
        print('Seu ingrediente não foi encontrado!')
        print('Tente digitar a palavra corretamente com acentos.')
        print()

  while editar:
    editInstructions()
    recipe = input('Receita a ser editada: ')
    if recipe == '':
      editar = False
    elif recipe == 'ajuda':
      menu()
    else:
      encontrados = []
      receita = recipe.split()
      if 'de' in receita:
        receita.remove('de')
      if 'para' in receita:
        receita.remove('para')
      if 'com' in receita:
        receita.remove('com')
      for i in receitas:
        if len(receita) > 1:
          for p in range(len(receita)-1):
            if receita[p] in receitas[i][1]:
              if receita[p+1] in receitas[i][1]:
                if i not in encontrados:
                  encontrados.append(i)
        elif len(receita) == 1:
          for p in receita:
            if p in receitas[i][1]:
              if i not in encontrados:
                encontrados.append(i)
      count = 0
      print()
      for i in encontrados:
        count += 1
        print(f'#{count} - {receitas[i][0]}  {receitas[i][2]}min')
      if count == 0:
        print('Nenhuma receita foi encontrada! Tente novamente com outra palavra chave.')
      elif count > 0:
        done = False
        while not done:
          print()
          escolha = input('Editar receita n°: ')
          if escolha == '':
            print()
            done = True
          elif escolha.lower() == 'ajuda':
            menu()
          elif escolha.isdigit():
            if int(escolha) > count or int(escolha) < 0:
              print('Digite apenas os valores apresentados acima.')
            else:
              receita = open(receitas[encontrados[int(escolha)-1]][3], 'r', encoding='utf8')
              receitaEdit = receita.readlines()
              receita.close()
              receita = open(receitas[encontrados[int(escolha)-1]][3], 'w', encoding='utf8')
              cont = 0
              while cont < len(receitaEdit):
                linha = receitaEdit[cont]
                if linha[0] == '*':
                  print(linha[1:].upper().center(72))
                  edite = False
                elif linha[0] == ';':
                  print(linha[1:].title().center(72))
                  edite = False
                elif linha[0] == '/':
                  print()
                  edite = True
                  print(linha[1:])
                elif linha[0] == '¬':
                  print()
                  edite = True
                  print(linha[2:])
                elif linha[0].isdigit():
                  print()
                  edite = True
                  if int(linha[0:1]) < 10:
                    num = linha[0]
                    print(linha[4:])
                  else:
                    num = linha[0:1]
                    print(linha[5:])
                if edite:
                  edit = input('').lower()
                else:
                  edit = ''
                if edit == '' or linha[0] == ';' or linha[0] == '*':
                  receita.write(linha)
                elif edit == '+':
                  if linha[0] == '¬':
                    print('\nNovo ingrediente!\n')
                    novaLinhaIngrediente = input('Ingrediente: ')
                    while novaLinhaIngrediente.isspace() or novaLinhaIngrediente == '' or novaLinhaIngrediente.isdigit():
                      print('Ingrediente inválido. Tente novamente.')
                      novaLinhaIngrediente = input('Ingrediente: ')
                    novaLinhaQuantidade = input('Quantidade: ')
                    while novaLinhaQuantidade.isspace() or novaLinhaQuantidade == '':
                      print('\nQuantidade inválida. Tente novamente.\n')
                      novaLinhaQuantidade = input('Quantidade: ')
                    if novaLinhaQuantidade == '0':
                      receita.write(f'¬ {novaLinhaIngrediente.capitalize()} à gosto\n')
                    else:
                      receita.write(f'¬  {novaLinhaQuantidade} {novaLinhaIngrediente.capitalize()}\n')
                  elif linha[0].isdigit():
                    for i in range(len(receitaEdit)):
                      if receitaEdit[i][0].isdigit():
                        if int(receitaEdit[i][0]) >= int(linha[0]):
                          if int(receitaEdit[i][0:1]) < 10:
                            receitaEdit[i] = receitaEdit[i].replace(receitaEdit[i][0], str(int(receitaEdit[i][0])+1))
                          else:
                            receitaEdit[i] = receitaEdit[i].replace(receitaEdit[i][0:1], str(int(receitaEdit[i][0:1])+1))
                    print(f'Passo {int(linha[0:1])}')
                    novaLinha = input('')
                    while novaLinha.isspace() or novaLinha == '':
                      print('\nTexto inserido é inválido. Tente novamente.\n')
                      print(f'Passo {int(linha[0:1])}')
                      novaLinha = input('')
                    receita.write(f'{int(linha[0:1])} - {novaLinha}\n')
                  cont -= 1
                elif edit == 'del':
                  if linha[0].isdigit():
                    for i in range(len(receitaEdit)):
                      if receitaEdit[i][0].isdigit():
                        if int(receitaEdit[i][0]) >= int(linha[0]):
                          if int(receitaEdit[i][0:1]) < 10:
                            receitaEdit[i] = receitaEdit[i].replace(receitaEdit[i][0], str(int(receitaEdit[i][0])-1))
                          else:
                            receitaEdit[i] = receitaEdit[i].replace(receitaEdit[i][0:1], str(int(receitaEdit[i][0:1])-1))
                  else:
                    cont += 1
                else:
                  if linha[0] == '/':
                    receita.write(f'/{edit}\n')
                  elif linha[0] == '¬':
                    receita.write(f'¬ {edit.capitalize()}\n')
                  elif linha[0].isdigit():
                    receita.write(f'{num} - {edit.capitalize()}\n')
                cont += 1
              print('\n\n __________________________________')
              print('|                                  |')
              print('| - Receita editada com sucesso! - |')
              print('|__________________________________|')
              receita.close()
              done = True
        editar = False
  while deletar:
    found = False
    pesquisa = input('Digite o nome da receita que deseja apagar: ')
    if pesquisa == '':
      deletar = False
    elif pesquisa == 'ajuda':
      menu()
      continue
    else:
      count = 0
      print()
      for i in receitas:
        receita = ' '.join(receitas[i][1])
        if receita.find(pesquisa.lower()) > -1:
          count += 1
          print(f'#{count} - {receitas[i][0]}  {receitas[i][2]}min')
      if count == 0:
        print('Nenhuma receita foi encontrada! Tente novamente com outra palavra chave.\n')
      elif count > 0:
        found = True
        done = False
        while not done:
          escolha = input(f'\nApagar receita n°: ')
          if escolha == '':
            print()
            done = True
            found = False
          elif escolha.lower() == 'ajuda':
              menu()
          elif escolha.isdigit():
            if int(escolha) > count:
              print('Digite apenas os valores apresentados acima.')
            else:
              count2 = 0
              for i in receitas:
                receita = ' '.join(receitas[i][1])
                if receita.find(pesquisa.lower()) > -1:
                  count2 += 1
                if receita.find(pesquisa.lower()) > -1 and count2 == int(escolha):
                  abrir(open(receitas[i][3], 'r', encoding='utf8'), receitas[i][3], 'd')
                  arquivo = i
                  done = True
          else:
            print('Digite ajuda para saber os comandos ou aperte enter para voltar.')
    if found:  
      decisao = input('\n\nVocê tem certeza que deseja apagar esta receita? ')
      if decisao.lower() == 's':
        senha = seguranca()
        senha = ''.join(senha)
        print()
        print(f'A receita {receitas[arquivo][0]} será apagada.')
        print()
        print('Digite a senha a seguir para continuar.\n')
        print(senha)
        print()
        digitar = input('')
        print()
        if digitar == senha:
          if (converterb_d(arquivo) +1) == len(receitas):
            os.remove(receitas[arquivo][3])
            del receitas[arquivo]
            pickle.dump(receitas, open('receitas.pck', 'wb'))
            print('Receita apagada.')
            deletar = False
          else:
            os.remove(receitas[arquivo][3])
            for i in receitas:
              if converterb_d(i) >= converterb_d(arquivo) and (converterb_d(i) < (len(receitas) - 1)):
                prox = format(converterb_d(i)+1,'07b')
                receitas[i] = receitas[prox]
            del receitas[i]
            pickle.dump(receitas, open('receitas.pck', 'wb'))
            print('Receita apagada.')
            deletar = False
        else:
          print('Você digitou errado. Tente novamente. ')
          senha = seguranca()
          senha = ''.join(senha)
          print()
          print('Digite a senha a seguir para continuar.\n')
          print(senha)
          print()
          digitar = input('')
          print()
          if digitar == senha:
            if (converterb_d(arquivo) +1) == len(receitas):
              os.remove(receitas[arquivo][3])
              del receitas[arquivo]
              pickle.dump(receitas, open('receitas.pck', 'wb'))
              print('Receita apagada.')
              deletar = False
            else:
              os.remove(receitas[arquivo][3])
              for i in receitas:
                if converterb_d(i) >= converterb_d(arquivo) and (converterb_d(i) < len(receitas) - 1):
                  prox = format(converterb_d(i),'07b')
                  receitas[i] = receitas[prox]
              del receitas[i]
              pickle.dump(receitas, open('receitas.pck', 'wb'))
              print('Receita apagada.')
              deletar = False
          else:
            print ('Não foi possível completar a ação. Tente novamente mais tarde.')
            deletar = False
  while criar:
    existe = False
    nome = input('Digite o nome da sua receita: ')
    for i in receitas:
      if nome.lower() == receitas[i][0].lower():
        print('\nJá existe uma receita com esse nome!\n')
        existe = True
    if nome == 'ajuda':
      menu()
    elif nome == '':
      break
    elif nome.isspace() or len(nome) == 1:
      print('\nDigite um nome válido!\n')
      existe = True
    if not existe:
      decisao = input(f'Sua receita se chamará {nome}, está certo disso? ')
      iniciar = False
      if decisao == 's':
        iniciar = True
      if iniciar:
        titulo = nome.capitalize()
        nome = list(nome.capitalize())
        nome += ['.txt']
        nome = ''.join(nome)
        receita = open(nome,'w', encoding='utf8')
        done = False
        if not done:
          receita.write(f';{titulo}\n')
          receita.write('*ingredientes\n')
          ingrediente = 0
          count = 0
          print()
          print('Ingredientes'.center(72))
          print('Para ingrediente sem quantidade(à gosto) insira 0 em quantidade.')
          while ingrediente != '':
            ingrediente = input('Ingrediente: ')
            if ingrediente != '' and not ingrediente.isspace() and not ingrediente.isdigit():
              quantidade = input('Quantidade: ')
              while quantidade.isspace() or quantidade == '':
                print('\nQuantidade inválida. Tente novamente.\n')
                quantidade = input('Quantidade: ')
              if quantidade == '0':
                receita.write(f'¬ {ingrediente} à gosto\n')
              else:
                receita.write(f'¬ {quantidade} {ingrediente}\n')
            elif ingrediente.isspace() or ingrediente.isdigit():
              print('\nIngrediente inválido não adicionado.\n')
          print('\nDigite o nome de um passo a mais(coisas adicionais como cobertura, recheio ou calda) a seguir ou digite 0 para ir direto para o modo de fazer.')
          passos = 0
          passosAdc = []
          decisao = input('Inserir um passo: ')
          while decisao != '' and decisao != '0':
            passosAdc.append(decisao)
            passos += 1
            decisao = input('Inserir um passo: ')
            while decisao.isspace() or decisao.isdigit():
              print('\nO nome inserido é inválido. Tente novamente.\n')
              decisao = input('Inserir um passo: ')
          passosAdc.reverse()
          print()
          if decisao != '0' or decisao != '':
            contador = passos
            while contador > 0:
              receita.write(f';{passosAdc[contador-1]}(ingredientes)\n')
              ingrediente = 0
              count = 0
              print(f'{passosAdc[contador-1]}(ingredientes)'.center(72))
              print()
              print('Para ingrediente sem quantidade(à gosto) insira 0 em quantidade.')
              while ingrediente != '':
                ingrediente = input('Ingrediente: ')
                if ingrediente != '' and not ingrediente.isspace() and not ingrediente.isdigit():
                  quantidade = input('Quantidade: ')
                  while quantidade.isspace() or quantidade == '':
                    print('\nQuantidade inválida. Tente novamente.\n')
                    quantidade = input('Quantidade: ')
                  if quantidade == '0':
                    receita.write(f'¬ {ingrediente} à gosto\n')
                  else:
                    receita.write(f'¬ {quantidade} {ingrediente}\n')
                elif ingrediente.isspace() or ingrediente.isdigit():
                  print('\nIngrediente inválido não adicionado.\n')
              contador -= 1
          print('Modo de preparo'.center(72))
          receita.write('*modo de preparo\n')
          count = 1
          modo = '0'
          while modo != '':
            print(f'Passo {count}')
            modo = input('')
            if modo != '' and not modo.isspace():
              receita.write(f'{count} - {modo}\n')
            elif modo.isspace():
              print('\nTexto inserido é inválido e não foi adicionado.\n')
              count -= 1
            count += 1
          if len(passosAdc) > 0:
            contador = passos
            while contador > 0:
              receita.write(f';{passosAdc[contador-1]}(modo de preparo)\n')
              print(f'{passosAdc[contador-1]}(Modo de preparo)'.center(72))
              count = 1
              modo = '0'
              while modo != '':
                print(f'Passo {count}') 
                modo = input('')
                if modo.isspace():
                  print('\nTexto inserido é inválido e não foi adicionado.\n')
                elif modo != '':
                  receita.write(f'{count} - {modo}\n')
                count += 1
              contador -= 1
          print('\n\n\n')
          print('Apresentando sua receita...')
          print('\n\n\n')
          receita = open(nome,'r', encoding='utf8')
          abrir(receita, nome, 'c')
          print('\n\n')
          print('Sua receita será salva, mas você poderá editar posteriormente. ')
          print('\n\n')
          for i in receitas:
            print('.',end='')
          print()
          novo = format(len(receitas),'07b')
          chaves = []
          for i in titulo.split():
            if i != 'de' and i != 'para':
              chaves.append(i.lower())
          chave = titulo.split()
          for i in chave:
            i = remover_acentos(i)
            if i not in chaves and i != 'de' and i != 'para' and i != 'com':
              chaves.append(i.lower())
          print('Sua receita é:')
          print('1 - doce')
          print('2 - salgada')
          feito = False
          while not feito:
            sabor = input('')
            if sabor.isdigit():
              if int(sabor) == 1:
                chaves += ['doce']
                feito = True
              elif int(sabor) == 2:
                chaves += ['salgado']
                feito = True
              else:
                print('Digite apenas 1 ou 2.')
            else:
              print('Digite apenas 1 ou 2.')
          while chave != '0' and chave != '':
            chave = input('Digite palavras chave para buscar a receita depois ou "0" para sair: ')
            if chave != '0' and chave != '':
              chaves += [chave.lower()]
          chaves.append('todas')
          tempo = input('Quanto tempo leva a preparação da receita(em minutos)? ')
          while not tempo.isdigit():
            print('\nDigite apenas números!\n')
            tempo = input('Quanto tempo leva a preparação da receita(em minutos)? ')
          site = input('\nVocê deseja adicionar o site dessa receita? ')
          link = False
          if site == 's':
            print('\nCole o link a seguir: ')
            site = input('')
            while not validators.url(site):
              print('url inválida. Confira o link e cole novamente.')
              print('\nCole o link a seguir: ')
              site = input('')
            link = True
          receitas[novo] = [titulo.capitalize(),chaves,int(tempo),nome]
          if link:
            receitas[novo].append(site)
          arquivo_salvar = open('receitas.pck', 'wb')
          pickle.dump(receitas,arquivo_salvar)
          arquivo_salvar.close()
          receita.close()
          print('\n\nReceita cadastrada com sucesso!')
          decisao = input('\nVocê deseja editar sua receita? ')
          while decisao == 's':
            arquivo = open(nome, 'r', encoding='utf8')
            arquivoEdit = arquivo.readlines()
            arquivo.close()
            count = 1
            for linha in arquivoEdit:
              if linha[0] == '*':
                print()
                print(count,linha[1:].upper().center(72))
              elif linha[0] == ';':
                print()
                print(count,linha[1:].title().center(72))
              elif linha[0] == '/':
                print()
                print(count,linha[1:].capitalize())
              else:
                print(count,linha,end='')
              count += 1
            print()
            linha = input('Digite a linha que deseja editar: ')
            if linha.isdigit():
              linha = int(linha)
              if linha > len(arquivoEdit) or linha < 0:
                print('Digite apenas números que correspondem a uma linha da receita.')
              else:
                cont = 1
                if arquivoEdit[linha-1][0] == '¬':
                  print(arquivoEdit[linha-1][1:])
                elif arquivoEdit[linha-1][0] == ';':
                  print(arquivoEdit[linha-1][1:])
                elif arquivoEdit[linha-1][0] == '*':
                  print(arquivoEdit[linha-1][1:])
                elif arquivoEdit[linha-1][0] == '/':
                  print(arquivoEdit[linha-1][1:])
                elif arquivoEdit[linha-1][0].isdigit():
                  if int(arquivoEdit[linha-1][0:1]) < 10:
                    print(arquivoEdit[linha-1][4:])
                  else:
                    print(arquivoEdit[linha-1][5 :])
                print('Escreva a nova linha:')
                if arquivoEdit[linha-1][0] == '*':
                  arquivoEdit.pop(linha-1)
                  novaLinha = input('')
                  arquivoEdit.insert(linha-1,f'*{novaLinha}\n')
                elif arquivoEdit[linha-1][0] == ';':
                  arquivoEdit.pop(linha-1)
                  novaLinha = input('')
                  arquivoEdit.insert(linha-1,f';{novaLinha}\n')
                elif arquivoEdit[linha-1][0] == '/':
                  arquivoEdit.pop(linha-1)
                  novaLinha = input('')
                  arquivoEdit.insert(linha-1,f'/{novaLinha}\n')
                elif arquivoEdit[linha-1][0] == '¬':
                  arquivoEdit.pop(linha-1)
                  novaLinha = input('Ingrediente: ')
                  while novaLinha == '' or novaLinha.isspace() or novaLinha.isdigit():
                    print('\nIngrediente inválido. Tente novamente.\n')
                    novaLinha = input('Ingrediente: ')
                  quantidade = input('Quantidade: ')
                  while quantidade == '' or quantidade.isspace():
                    print('\nQuantidade inválida. Tente novamente.\n')
                    quantidade = input('Quantidade: ')
                  if quantidade == '0':
                    arquivoEdit.insert(linha-1,f'¬ {novaLinha} à gosto\n')
                  else:
                    arquivoEdit.insert(linha-1,f'¬ {quantidade} {novaLinha}\n')
                elif arquivoEdit[linha-1][0].isdigit():
                  num = arquivoEdit[linha-1][0]
                  arquivoEdit.pop(linha-1)
                  novaLinha = input('')
                  arquivoEdit.insert(linha-1,f'{num} - {novaLinha}\n')
                arquivo = open(nome, 'w', encoding='utf8')
                arquivo.writelines(arquivoEdit)
                arquivo.close()
                decisao = input('Editar mais uma linha? ')
            elif linha == '':
              decisao = 'n'
            elif linha == 'ajuda':
              menu()
          done = True
          criar = False
