from semantics import *
from formula import *

atributos = ['pi<=42.09', 'pi<=48.12', 'pi<=54.92', 'pi<=63.52', 'pi<=70.62', 'pi<=80.61',
             'pt<=8.31', 'pt<=12.36', 'pt<=14.55', 'pt<=17.44', 'pt<=21.06', 'pt<=28.8',
             'la<=32.59', 'la<=39.63', 'la<=46.33', 'la<=52.68', 'la<=61.27', 'la<=74.10',
             'ss<=29.51', 'ss<=34.38', 'ss<=39.81', 'ss<=44.44', 'ss<=50.55', 'ss<=56.31',
             'rp<=104.70', 'rp<=111.98', 'rp<=116.59', 'rp<=120.08', 'rp<=124.89', 'rp<=130.30',
             'gs<=-0.74', 'gs<=2.10', 'gs<=6.42', 'gs<=25.36', 'gs<=37.89', 'gs<=57.55']
regras = 4

significado = ['p', 'n', 's']


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


def restricao_um(atributos, regras, significado):
    list_and = []
    for i in range(regras):
        list_or = []
        for atr in atributos:
            for sig in significado:
                list_or.append(Atom('X' + atr + ',' + str(i+1) + ',' + sig))
        or_form = or_all(list_or)
        list_and.append(or_form)


    return and_all(list_and)



def restricao_dois(atributos, regras):
    list_and = []
    for i in range(regras):
        list_or = []
        for atr in atributos:
            list_or.append(Not(Atom('X' + atr + ',' + str(i+1) + ',' + 's')))

        or_form = or_all(list_or)
        list_and.append(or_form)

    return and_all(list_and)


print(restricao_um(atributos, regras, significado))
print(restricao_dois(atributos, regras))