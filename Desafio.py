#  --------------------------------------------------------  Funções utilizadas  ----------------------------------------------------------
def main():
    #  ----------------------------------------------------------  Diagramação do menu  -------------------------------------------------------

    menu = """

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Cadastrar Cliente
    [5] Cadastrar Conta
    [6] Mostrar Contas
    [7] Sair

    => """

    #  --------------------------------------------   Variaveis, listas e dicionarios de escopo global  -------------------------------------------------
    LIMITE_SAQUES = 3

    contador_conta = 0
    saldo = 0
    limite = 500
    numero_saques = 0
    extrato = ''
    clientes = []
    contas = []

    # --------------------------------------------------------------   Loop do menu   -----------------------------------------------------------

    while True:
        opcao = input(menu)
        if opcao == "1":  # Deposita
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposita(valor, saldo, extrato)

        elif opcao == "2":  # Saca
            valor = float(input("Informe o valor do saque: "))
            try:
                numero_saques, extrato, saldo = saca(valor=valor, saldo=saldo, extrato=extrato, numero_saques=numero_saques,
                                                     LIMITE_SAQUES=LIMITE_SAQUES, limite=limite)
            except:
                continue

        elif opcao == "3":  # Extrato
            imprime_extrato(saldo, extrato=extrato)

        elif opcao == "4":  # Cadastro de Cliente
            nome = str(input("Digite seu nome: ")).strip().title()
            cpf = int(input("Digite seu CPF: "))
            cadastro(nome, cpf, clientes)

        elif opcao == "5":  # Cadastrod e conta
            nome = str(input("Digite seu nome: ")).strip().title()
            cpf = int(input("Digite seu CPF: "))
            contas, contador_conta = nova_conta(nome, cpf, contas, clientes, contador_conta)

        elif opcao == "6":  # mostra listagem de contas
            mostra_conta(contas)

        elif opcao == "7":
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada.")


def cadastro(nome, cpf, clientes):
    """_Cadastro de cliente. Necessário para o cadastro de contas_

    Args:
        nome (_str_): _Nome do usuário_
        cpf (_int_): _Número do cpf do cliente_
        clientes (_list_): _Lista de clientes_

    Returns:
        _list_: _Lista atualizada de clientes_
    """
    data = str(input("Data de nascimento: "))
    endereco = input(
        "Endereço: sugestão -> logradouro - bairro - cidade/sigla ")
    existe = False
    valida = [int(dict_cliente["cpf"]) for dict_cliente in clientes]
    if cpf in valida:
        existe = True
        print(f"Falha ao Cadastrar! Já existe um cliente com o cpf: {cpf}!")
    if existe == False:
        dict_cliente = {"nome": f"{nome}", "data_nascimento": f"{data}",
                        "cpf": f"{cpf}", "endereco": f"{endereco}"}
        clientes.append(dict_cliente.copy())
        print("Cliente Cadastrado com sucesso!")
    return clientes


def nova_conta(nome, cpf, contas, clientes, contador_conta):
    """Funçao cria conta caso o cpf do cliente já esteja cadastrado na lista de clientes, permite a criação de mais de uma conta em mesmo cpf
    onde o campo contas é uma lista que permite a inclusão de novos numeros de contas

    Args:
        nome (_srt_): _Nome do usuário_
        cpf (_int_): _Conjunto de numéros que identifica o cliente sem repetição_
        contas (_list_): _Lista de contas_
        clientes (_list_): _Lista de clientes_
        contador_conta (_int_): _Contador que gera o número de contas de forma sequêncial

    Returns:
        _list/int_: _Retorna lista de clientes atualizada e validada de acordo com os requisitos do sistema e contador de numero de conta atualizado_
    """
    ja_tem_conta = False
    valida = [int(dict_cliente["cpf"]) for dict_cliente in clientes]
    if cpf in valida:
        for dict_conta in contas:
            if dict_conta["cpf"] == cpf:
                contador_conta += 1
                (dict_conta["conta"]).append(contador_conta)
                print(
                    f"Nova conta de numero {contador_conta} criada em nome de {nome}!")
                return contas, contador_conta
            else:
                ja_tem_conta = False
        if ja_tem_conta == False:
            conta = []
            contador_conta += 1
            conta.append(contador_conta)
            dict_conta = {"agencia": "0001",
                          "nome": f"{nome}", "cpf": cpf, "conta(s)": conta}
            contas.append(dict_conta)
            print(
                f"Conta de numero {contador_conta} criada em nome de {nome}!")
            return contas, contador_conta
    else:
        print("É preciso fazer o cadastro como cliente antes de criar uma conta! ")


def deposita(valor, saldo, extrato, /):
    """_Função que organiza os depositos e devolvendo a informação a ser incluida no extrato e o saldo atualizado_

    Args:
        valor (_float_): _Valor do depósito_
        saldo (_float_): _Saldo resultante da movimentação_
        extrato (_str_): _historico de movimentações realizadas_

    Returns:
        _float/str_: _retorna saldo disponivel e extrato alterado_
    """
    extrato = extrato
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        return saldo, extrato
    else:
        print("Operação falhou! O valor informado é inválido.")


def saca(*, valor, saldo, extrato, numero_saques, LIMITE_SAQUES, limite):
    """_Função que debita a quantidade valor do saldo disponível, devolvendo saldo atualizado e informações sobre o número de saques realizados_

    Args:
        valor (_float_): _valor a ser debitado_
        saldo (_float_): _valor disponível para ser debitado_
        extrato (_str_): _Histórico de movimentações de saques e depositos_
        numero_saques (_int_): _Quantidade de saques, define se a movimentação será posivel ou se excedeu o numero limite_

    Returns:
        _int/str/float_: _Retorna o incremento do número de saques, seguido do extrato atualizado e por fim o saldo atualizado_
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        return numero_saques, extrato, saldo
    else:
        print("Operação falhou! O valor informado é inválido.")


def imprime_extrato(saldo, /, *, extrato):
    """_Funçao que cria estrato diagramado para melhor intendimento do usuário_

    Args:
        extrato (_str_): _histórico de movimentações de saque e deposito_
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print("==========================================")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def mostra_conta(contas):
    """_Função para mostrar contas cadastradas_

    Args:
        contas (_list_): _Lista de contas criadas_
    """
    for conta in contas:
        print("\n-------------------------\n")
        for k, v in conta.items():
            print(f"{k} -> {v}")
        print("\n-------------------------\n")


#  --------------------------------------------------------  inicializador  ---------------------------------------------------------------
if __name__ == "__main__":
    main()
