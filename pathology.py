from semantics import *
from formula import *
from functions import *
from semantics import truth_value
import csv
import time
from pysat.solvers import Glucose3

"""
atributos = ['pi<=42.09', 'pi<=48.12', 'pi<=54.92', 'pi<=63.52', 'pi<=70.62', 'pi<=80.61',
             'pt<=8.31', 'pt<=12.36', 'pt<=14.55', 'pt<=17.44', 'pt<=21.06', 'pt<=28.8',
             'la<=32.59', 'la<=39.63', 'la<=46.33', 'la<=52.68', 'la<=61.27', 'la<=74.10',
             'ss<=29.51', 'ss<=34.38', 'ss<=39.81', 'ss<=44.44', 'ss<=50.55', 'ss<=56.31',
             'rp<=104.70', 'rp<=111.98', 'rp<=116.59', 'rp<=120.08', 'rp<=124.89', 'rp<=130.30',
             'gs<=-0.74', 'gs<=2.10','gs<=6.42', 'gs<=25.36', 'gs<=37.89', 'gs<=57.55']
"""

atributos = ['pi<=42.09', 'la<=39.63', 'gs<=37.89']

regras = 2

significado = ['p', 'n', 's']


#auxiliary functions

def lerArquivo(caminho):
    lista = []
    with open(caminho, 'r') as entrada:
        arquivo = csv.reader(entrada)
        next(arquivo)      #pula a linha de cabeçalho
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
    return first_formula


def restricao_um(atributos, regras):
    list_and1 = []
    for p in range(regras):
        list_and2 = []
        for atr in atributos:
            list_or = []
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
        list_or = []
        for atr in atributos:
            list_or.append(Not(Atom('X' + atr + ',' + str(i+1) + ',' + 's')))
        or_form = or_all(list_or)
        list_and.append(or_form)
    return and_all(list_and)


def restricao_tres(atributos, regras):
    dados = lerArquivo('arquivos/column_bin_compacto.csv')
    list_and1 = []
    for paciente in dados:
        if paciente[3] == '0':
            list_and2 = []
            for r in range(regras):
                list_or = []
                for i in range(len(paciente) - 1):
                    if paciente[i] == '0':
                        list_or.append(Atom('X' + atributos[i] + ',' + str(r+1) + ',' + 'p'))
                    elif paciente[i] == '1':
                        list_or.append(Atom('X' + atributos[i] + ',' + str(r+1) + ',' + 'n'))

                or_form = or_all(list_or)
                list_and2.append(or_form)
            and_form = and_all(list_and2)
            list_and1.append(and_form)
    return and_all(list_and1)


def restricao_quatro(atributos, regras):
    dados = lerArquivo('arquivos/column_bin_compacto.csv')
    list_and = []
    for r in range(regras):
        enfermo = 0
        for paciente in dados:
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
    dados = lerArquivo('arquivos/column_bin_compacto.csv')
    list_and = []
    enfermo = 0
    for paciente in dados:
        if paciente[len(dados) - 1] == '1':
            enfermo += 1
            list_or = []
            for r in range(regras):
                list_or.append(Atom('C' + str(r+1) + ',' + str(enfermo)))

            or_form = or_all(list_or)
            list_and.append(or_form)
    return and_all(list_and)


def create_final_formula(atributos, regras):
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
    return final_formula


def pathology_solution(formula):

    solution = is_satisfiable(formula)

    if solution:
        print(solution)
        rules = defined_attribute(solution)  #matriz em que cada elemento é uma regra.
        print("--Regras--")
        for rule in rules:
            print(rule)
        taxa_acerto = porcentege_of_correct_answers(rules)
        print(f"Taxa de acerto - {taxa_acerto}%")
    else:
        print("Insatisfatível")

    return formula


def dpll_solution(formula):
    tseitin_form = tseitin(formula)
    form_clausal = formula_in_clauses(tseitin_form)

    interpretation = dpll(form_clausal)

    if interpretation:
        print(interpretation)
        rules = defined_attribute(interpretation)
        print("--Regras--")
        for rule in rules:
            print(rule)
        taxa_acerto = porcentege_of_correct_answers(rules)
        print(f"Taxa de acerto - {taxa_acerto}%")
    else:
        print("Insatisfatível")


def pysat_solution(formula):
    tseitin_form = tseitin(formula)
    form_clausal = formula_in_clauses(tseitin_form)

    array_integer, all_clauses = mapping_atoms_integers(tseitin_form, form_clausal)

    solver = Glucose3()
    for clausula in all_clauses:
        solver.add_clause(clausula)
    solver.solve()
    model = solver.get_model()

    interpretation = mapping_integers_atoms(array_integer, model)

    if solver.solve():
        print(interpretation)
        rules = defined_attribute(interpretation)
        print("--Regras--")
        for rule in rules:
            print(rule)
        taxa_acerto = porcentege_of_correct_answers(rules)
        print(f"Taxa de acerto - {taxa_acerto}%")
    else:
        print("Insatisfatível")


def mapping_atoms_integers(tseitin_form, form_clausal):
    atomicas = atoms(tseitin_form)
    array_integer = {}
    cont = 0
    for atom in atomicas:
        cont += 1
        array_integer[atom.__str__()] = cont

    all_clauses = []
    for clausula in form_clausal:
        clause = []
        for literal in clausula:
            if isinstance(literal, Atom):
                clause.append(array_integer[literal.__str__()])
            elif isinstance(literal, Not):
                while isinstance(literal, Not):
                    literal = literal.inner
                inteiro = array_integer[literal.__str__()]
                clause.append(inteiro * (-1))
        all_clauses.append(clause)

    return array_integer, all_clauses


def mapping_integers_atoms(array_integer, model):
    interpretation = {}
    list_of_key = list(array_integer.keys())
    list_of_value = list(array_integer.values())
    for elem in model:
        if elem > 0:
            position = list_of_value.index(elem)
            interpretation[list_of_key[position]] = True
        elif elem < 0:
            position = list_of_value.index(elem * (-1))
            interpretation[Not(list_of_key[position]).__str__()] = True
    return interpretation


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
    dados = lerArquivo('arquivos/column_bin_test_compacto.csv')
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


formula_final = create_final_formula(atributos, regras)


#testando força bruta

start_time = time.time()
print('Solution satisfiability brute force:')
pathology_solution(formula_final)
end_time = time.time()
print("Time: {:.2f}".format(end_time-start_time))


#testando dpll

start_time = time.time()
print('\nSolution DPLL:')
dpll_solution(formula_final)
end_time = time.time()
print("Time: {:.2f}".format(end_time - start_time))


#testando solver

start_time = time.time()
print('\nSolution PySat:')
pysat_solution(formula_final)
end_time = time.time()
print("Time: {:.2f}".format(end_time - start_time))
