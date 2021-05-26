#----------------------------------------- Sistema Bancário em python -------------------------------------------------
conta = []
guardar_saldos = []
maior_saldo = 0
print('---------- SEJÁ BEM-VINDO -----------')
while True:
    print('1 - DIGITE UM PARA CRIAR UM CADASTROS;')
    print('2 - DIGITE DOIS PARA ACESSAR AS INFORMAÇÕES DO BANCO;')
    choice = int(input('O que gostaria de fazer? '))
    if choice == 1:
        while True:
            num_conta = int(input('Número conta: '))
            for h, valor in enumerate(conta):
                if conta[h][0] == num_conta:
                    print('Este numero de conta já existe, por favor digite outro!')
                    num_conta = int(input('Número conta: '))
            saldo = float(input('Saldo: '))
            if saldo > maior_saldo:
                maior_saldo = saldo
            guardar_saldos.append(saldo)
            nome = str(input('Nome: '))
            conta.append([num_conta, saldo, nome])
            res = str(input('QUER CONTINUAR? [S/N] '))
            if res in 'Nn':
                print('SALVANDO DADOS...')
                break
    if choice == 2 and conta == []:
        while True:
            print('NECESSITA DE CADASTRO PRIMEIRO.')
            voltar = str(input('QUER RETORNAR? [S/N]: '))
            if voltar in 'Ss':
                break
    if choice == 2 and conta != []:
        media_saldos = (sum(guardar_saldos))/(len(guardar_saldos))
        print('--------------------- DIGITE UM NÚMERO PARA VER DETERMINADA INFORMAÇÃO ------------------------')
        print('4 - INFORMAÇÕES DE UMA CONTA;')
        print('5 - MÉDIA SALDO NO BANCO;')
        print('6 - TOTAL DINHEIRO NO BANCO;')
        print('7 - CONTA COM SALDO MAIOR QUE A MÉDIA DE SALDO;')
        print('8 - CONTA BANCÁRIA COM MAIOR SALDO;')
        print('1000 - INFORMAÇÕES DE TODAS AS CONTAS;')
        print('999 - FECHAR;')
        while True:
            opção = int(input('O que deseja visualizar? '))
            if opção == 4:
                conta_usuario = int(input('Conta: '))
                for i, v in enumerate(conta):
                    if conta[i][0] == conta_usuario:
                        print(conta[i])
                        print('1 - DEPÓSITO // 2 - SAQUE // 3 - CANCELAR CONTA')
                        opc = int(input('Opção: '))
                        if opc == 1:
                            deposito = float(input('DEPÓSITO: '))
                            conta[i][1] = conta[i][1] + deposito
                            print(conta[i])
                        if opc == 2:
                            saque = float(input('Saque: '))
                            conta[i][1] = conta[i][1] - saque
                            print(conta[i])
                        if opc == 3:
                            decisao_final = str(input('Gostária mesmo de cancelar sua conta? [S/N] '))
                            if decisao_final in 'Ss':
                                del conta[i]
                                #print('CONTA CANCCELADA.')
                if conta [i][0] != conta_usuario:
                             print('ESSA CONTA NÃO EXISTE OU FOI CANCELADA.')
            if opção == 5:
                print(f'A média bancária é de: {media_saldos}!')
            if opção == 6:
                print(f'O total de dinheiro armazenado no banco é de {sum(guardar_saldos)}')
            if opção == 7:
                for k, value in enumerate(conta):
                    if conta[k][1] >= media_saldos:
                         print(f'A conta com o saldo maior que a média de saldos é de {conta[k][2]}, informações da conta: {conta[k]}')
            if opção == 8:
                for j, elem in enumerate(conta):
                    if conta[j][1] == maior_saldo:
                        print(f'A CONTA DE MAIOR SALDO É DE {conta[j][2]}, INFORMÇÕES DA CONTA: {conta[j]}')
            if opção == 1000:
                print(f'CONTAS-CADASTRADAS: {conta}')
            if opção == 999:
                break