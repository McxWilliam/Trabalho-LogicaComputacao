import sys
from semantics import *
from formula import *
import csv

sys.setrecursionlimit(2000)

"""
atributos = ['pi<=42.09', 'pi<=48.12', 'pi<=54.92', 'pi<=63.52', 'pi<=70.62', 'pi<=80.61',
             'pt<=8.31', 'pt<=12.36', 'pt<=14.55', 'pt<=17.44', 'pt<=21.06', 'pt<=28.8',
             'la<=32.59', 'la<=39.63', 'la<=46.33', 'la<=52.68', 'la<=61.27', 'la<=74.10',
             'ss<=29.51', 'ss<=34.38', 'ss<=39.81', 'ss<=44.44', 'ss<=50.55', 'ss<=56.31',
             'rp<=104.70', 'rp<=111.98', 'rp<=116.59', 'rp<=120.08', 'rp<=124.89', 'rp<=130.30',
             'gs<=-0.74', 'gs<=2.10', 'gs<=6.42', 'gs<=25.36', 'gs<=37.89', 'gs<=57.55']
"""
atributos = ['pi<=42.09', 'la<=39.63', 'gs<=37.89']
regras = 2

significado = ['p', 'n', 's']


def lerarquivo(caminho):
    lista = []
    with open(caminho, 'r') as entrada:
        arquivo = csv.reader(entrada)
        next(arquivo)
        for linha in arquivo:
            lista.append(linha)
    return lista

def and_all(list_formulas):
    """
    Returns a BIG AND formula from a list of formulas
    For example, if list_formulas is [Atom('1'), Atom('p'), Atom('r')], it returns
    And(And(Atom('1'), Atom('p')), Atom('r')).
    :param list_formulas: a list of formulas
    :return: And formula
    """
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = And(first_formula, formula)
    return first_formula


def or_all(list_formulas):
    """
    Returns a BIG OR of formulas from a list of formulas.
    For example, if list_formulas is [Atom('1'), Atom('p'), Atom('r')], it returns
    Or(Or(Atom('1'), Atom('p')), Atom('r')).
    :param list_formulas: a list of formulas
    :return: Or formula
    """
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = Or(first_formula, formula)

    return first_formula;


def restricao_um(atributos, regras):
    list_and1 = []
    for p in range(regras):
        list_and2 = [] # para cada regra, uma nova lista de AND é criada.
        for atr in atributos:
            list_or = []  # para cada atributo, uma nova lista de OU será criada.

            list_or.append(And(And(Atom('X' + atr + ',' + str(p + 1) + ',' + 'p'), Not(Atom('X' + atr + ',' + str(p + 1) + ',' + 'n'))),
                                        Not(Atom('X' + atr + ',' + str(p + 1) + ',' + 's'))))

            list_or.append(And(And(Not(Atom('X' + atr + ',' + str(p + 1) + ',' + 'p')), Atom('X' + atr + ',' + str(p + 1) + ',' + 'n')),
                                               Not(Atom('X' + atr + ',' + str(p + 1) + ',' + 's'))))

            list_or.append(And(And(Not(Atom('X' + atr + ',' + str(p + 1) + ',' + 'p')), Not(Atom('X' + atr + ',' + str(p + 1) + ',' + 'n'))),
                                               Atom('X' + atr + ',' + str(p + 1) + ',' + 's')))
            or_form = or_all(list_or)
            list_and2.append(or_form)
        list_and1.append(and_all(list_and2))


    return and_all(list_and1)

def restricao_dois(atributos, regras):
    list_and = []
    for i in range(regras):
        list_or = [] # para cada atributo, uma nova lista de OU será criada.
        for atr in atributos:
            list_or.append(Not(Atom('X' + atr + ',' + str(i+1) + ',' + 's')))

        or_form = or_all(list_or)
        list_and.append(or_form)

    return and_all(list_and)

def restricao_tres(atributos, regras):
    datas = lerarquivo('arquivos/column_bin_compacto.csv')
    list_and1 = []
    for paciente in datas:
        if paciente[3] == '0':
            list_and2 = [] # para cada nova linha do arquivo, uma nova lista de AND é criada.
            for r in range(regras):
                list_or = []
                for i in range(len(paciente) - 1): # quantidade de colunas do arquivo compactado;
                    if paciente[i] == '0':
                        list_or.append(Atom('X' + atributos[i] + ',' + str(r + 1) + ',' + 'p'))
                    elif paciente[i] == '1':
                        list_or.append(Atom('X' + atributos[i] + ',' + str(r + 1) + ',' + 'n'))

                or_form = or_all(list_or)
                list_and2.append(or_form)
            and_form = and_all(list_and2)
            list_and1.append(and_form)

    return and_all(list_and1)

def restricao_quatro(atributos, regras):
    datas = lerarquivo('arquivos/column_bin_compacto.csv')
    list_and = []
    for r in range(regras):
        enfermo = 0
        for paciente in datas:
            list_implies = []
            if paciente[3] == '1':
                enfermo += 1
                for j in range(len(paciente) - 1):
                    if paciente[j] == '0':
                        list_implies.append(Implies(Atom('X' + atributos[j] + ',' + str(r+1) + ',' + 'p'),
                                                    Not(Atom('C' + str(r+1) + ',' + str(enfermo)))))
                    elif paciente[j] == '1':
                        list_implies.append(Implies(Atom('X' + atributos[j] + ',' + str(r + 1) + ',' + 'n'),
                                                    Not(Atom('C' + str(r + 1) + ',' + str(enfermo)))))
                and_form = and_all(list_implies)
                list_and.append(and_form)

    return and_all(list_and)

def restricao_cinco(regras):
    datas = lerarquivo('arquivos/column_bin_compacto.csv')
    list_and = []
    enfermo = 0
    for paciente in datas:
        if paciente[3] == '1':
            enfermo += 1
            list_or = []
            for i in range(regras):
                list_or.append(Atom('C' + str(i + 1) + ',' + str(enfermo)))

            or_form = or_all(list_or)
            list_and.append(or_form)

    return and_all(list_and)

def pathology_solution(atributos, regras):
    final_formula = And(
        And(
            And(
                restricao_um(atributos, regras),
                restricao_dois(atributos, regras)
            ),
            And(
                restricao_tres(atributos, regras),
                restricao_quatro(atributos, regras)
            ),
        ),
        restricao_cinco(regras)
    )
    solution = is_satisfiable(final_formula)
    if solution:
        print(solution)
        rules = defined_attribute(solution) # matriz em que cada elemento é uma regra;
        print("-- Regras --")
        for rule in rules:
            print(rule)
        taxa_acerto = porcentege_of_correct_answers(rules)
        print(f"Taxa de acerto - {taxa_acerto}%")
    else:
        print("Insatisfatível.")


def defined_attribute(solution):
    list_atoms = []
    for k, v in solution.items():
        if(v == True):
            list_atoms.append(k)
    return make_rules(list_atoms)

def make_rules(list_atomicas):
    rules = []
    atomicas = []
    for atom in list_atomicas:
        atomicas.append(atom.split(','))
    for r in range(1, regras + 1):
        rule = []
        for atom in atomicas:
            if len(atom) > 2 and atom[1] == str(r):
                if atom[2] == 'p':
                    rule.append(Atom(atom[0]))
                elif atom[2] == 'n':
                    rule.append(Not(Atom(atom[0])))
        rules.append(and_all(rule))

    return rules


def porcentege_of_correct_answers(rules):
    dados = lerarquivo('arquivos/column_bin_test_compacto.csv')
    count = 0
    for paciente in dados:
        atendido = False
        interpretation = dict()
        for i in range(len(paciente) - 1):
            if paciente[i] == '0':
                interpretation['X' + atributos[i]] = False
            elif paciente[i] == '1':
                interpretation['X' + atributos[i]] = True
        #print(interpretation)

        for rule in rules:
            if truth_value(rule, interpretation):
                if paciente[len(paciente) - 1] == '1':
                    count += 1
                    atendido = True
                elif paciente[len(paciente) - 1] == '0':
                    atendido = True
        if (not atendido) and paciente[len(paciente) - 1] == '0':
            count += 1
    return (count/len(dados))*100


pathology_solution(atributos, regras)



