"""The goal in this module is to define functions that take a formula as input and
do some computation on its syntactic structure. """

from copy import deepcopy
from formula import *


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


def length(formula):
    """Determines the length of a formula in propositional logic."""
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return length(formula.inner) + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return length(formula.left) + length(formula.right) + 1


def subformulas(formula):
    """Returns the set of all subformulas of a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for subformula in subformulas(my_formula):
        print(subformula)

    This piece of code prints p, s, (p v s), (p → (p v s))
    (Note that there is no repetition of p)
    """

    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, Not):
        return {formula}.union(subformulas(formula.inner))
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        sub1 = subformulas(formula.left)
        sub2 = subformulas(formula.right)
        return {formula}.union(sub1).union(sub2)

#  we have shown in class that, for all formula A, len(subformulas(A)) <= length(A).


def atoms(formula):
    """Returns the set of all atoms occurring in a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for atom in atoms(my_formula):
        print(atom)

    This piece of code above prints: p, s
    (Note that there is no repetition of p)
    """
    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, Not):
        return atoms(formula.inner)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return atoms(formula.left).union(atoms(formula.right))


def number_of_atoms(formula):
    """Returns the number of atoms occurring in a formula.
    For instance,
    number_of_atoms(Implies(Atom('q'), And(Atom('p'), Atom('q'))))

    must return 3 (Observe that this function counts the repetitions of atoms)
    """
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return number_of_atoms(formula.inner)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return number_of_atoms(formula.left) + number_of_atoms(formula.right)


def number_of_connectives(formula):
    """Returns the number of connectives occurring in a formula."""

    if isinstance(formula, Atom):
        return 0
    if isinstance(formula, Not):
        return number_of_connectives(formula.inner) + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return number_of_connectives(formula.left) + number_of_connectives(formula.right) + 1


def is_literal(formula):
    """Returns True if formula is a literal. It returns False, otherwise"""

    if isinstance(formula, Atom):
        return True

    if isinstance(formula, Not):
        return is_literal(formula.inner)

    return False


def substitution(formula, old_subformula, new_subformula):
    """Returns a new formula obtained by replacing all occurrences
    of old_subformula in the input formula by new_subformula."""

    if isinstance(formula, Atom):
        if formula == old_subformula:
            return new_subformula
        else:
            return formula

    if isinstance(formula, Or):
        if formula == old_subformula:
            form = new_subformula
        else:
            form = Or(substitution(formula.left, old_subformula, new_subformula),
                      substitution(formula.right, old_subformula, new_subformula))

    if isinstance(formula, And):
        if formula == old_subformula:
            form = new_subformula
        else:
            form = And(substitution(formula.left, old_subformula, new_subformula),
                       substitution(formula.right, old_subformula, new_subformula))

    if isinstance(formula, Implies):
        if formula == old_subformula:
            form = new_subformula
        else:
            form = Implies(substitution(formula.left, old_subformula, new_subformula),
                           substitution(formula.right, old_subformula, new_subformula))

    if isinstance(formula, Not):
        if formula == old_subformula:
            form = new_subformula
        elif formula.inner == old_subformula:
            form = Not(new_subformula)
        else:
            form = Not(substitution(formula.inner, old_subformula, new_subformula))

    return form


def is_clause(formula):
    """Returns True if formula is a clause. It returns False, otherwise"""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_negation_normal_form(formula):
    """Returns True if formula is in negation normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_cnf(formula):
    """Returns True if formula is in conjunctive normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_term(formula):
    """Returns True if formula is a term. It returns False, otherwise"""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_dnf(formula):
    """Returns True if formula is in disjunctive normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_decomposable_negation_normal_form(formula):
    """Returns True if formula is in decomposable negation normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def cnf(formula):
    b = implication_free(formula)
    b = negation_normal_form(b)
    b = distributive(b)
    return b


def implication_free(formula):
    if isinstance(formula, Implies):
        b1 = implication_free(formula.left)
        b2 = implication_free(formula.right)
        return Or(Not(b1), b2)

    if isinstance(formula, And):
        b1 = implication_free(formula.left)
        b2 = implication_free(formula.right)
        return And(b1, b2)

    if isinstance(formula, Or):
        b1 = implication_free(formula.left)
        b2 = implication_free(formula.right)
        return Or(b1, b2)

    if isinstance(formula, Not):
        b1 = implication_free(formula.inner)
        return Not(b1)

    if isinstance(formula, Atom):
        return formula


def negation_normal_form(formula):
    if is_literal(formula):
        return formula

    if isinstance(formula, Not):
        b1 = formula.inner
        if isinstance(b1, Not):
            return negation_normal_form(b1.inner)

    if isinstance(formula, And):
        b1 = negation_normal_form(formula.left)
        b2 = negation_normal_form(formula.right)
        return And(b1, b2)

    if isinstance(formula, Or):
        b1 = negation_normal_form(formula.left)
        b2 = negation_normal_form(formula.right)
        return Or(b1, b2)

    if isinstance(formula, Not) and isinstance(formula.inner, And):
        a = formula.inner
        b1 = negation_normal_form(Not(a.left))
        b2 = negation_normal_form(Not(a.right))
        return Or(b1, b2)

    if isinstance(formula, Not) and isinstance(formula.inner, Or):
        a = formula.inner
        b1 = negation_normal_form(Not(a.left))
        b2 = negation_normal_form(Not(a.right))
        return And(b1, b2)


def distributive(formula):
    if is_literal(formula):
        return formula

    if isinstance(formula, And):
        b1 = distributive(formula.left)
        b2 = distributive(formula.right)
        return And(b1, b2)

    if isinstance(formula, Or):
        b1 = distributive(formula.left)
        b2 = distributive(formula.right)
        if isinstance(b1, And):
            c1 = b1.left
            c2 = b1.right
            return And(distributive(Or(c1, b2)), distributive(Or(c2, b2)))
        if isinstance(b2, And):
            c1 = b2.left
            c2 = b2.right
            return And(distributive(Or(b1, c1)), distributive(Or(b1, c2)))
        return Or(b1, b2)


def dpll(formulas):
    valoracao = dict()
    return dpll_check(formulas, valoracao)


def dpll_check(formulas, valoracao):
    formulas, valoracao = unit_propagation(formulas, valoracao)
    if len(formulas) == 0:
        return valoracao
    if [] in formulas:
        return False
    atomic = get_atomic(formulas)

    formulas1 = deepcopy(formulas)
    formulas1.append([atomic])

    formulas2 = deepcopy(formulas)
    formulas2.append([Not(atomic)])

    result = dpll_check(formulas1, valoracao)
    if result != False:
        return result
    return dpll_check(formulas2, valoracao)


def unit_propagation(formulas, valoracao):
    while has_unit_clause(formulas):
        literal = literal_unit(formulas)
        valoracao[literal.__str__()] = True
        formulas = remove_clauses_with_literal(formulas, literal)
        if isinstance(literal, Atom):
            literal = Not(literal)
        elif isinstance(literal, Not):
            literal = literal.inner
        formulas = remove_complement_literal(formulas, literal)

    return formulas, valoracao


def get_atomic(formulas):
    for clausula in formulas:
        if len(clausula) != 0:
            return clausula[0]


def has_unit_clause(formulas):
    for clausula in formulas:
        if len(clausula) == 1:
            return True
    return False


def literal_unit(formulas):
    for clausula in formulas:
        if len(clausula) == 1:
            return clausula[0]


def remove_clauses_with_literal(formulas, literal):
    new_clauses = []
    for clasula in formulas:
        if literal not in clasula:
            new_clauses.append(clasula)
    return new_clauses


def remove_complement_literal(formulas, literal):
    new_clauses = []
    for clausula in formulas:
        if literal in clausula:
            clausula.remove(literal)
            new_clauses.append(clausula)
        else:
            new_clauses.append(clausula)
    return new_clauses


def tseitin(formula):
    list_subformulas = subformulas(formula)
    formula = tseitin_transformation(formula, list_subformulas)

    return cnf(formula)


def tseitin_transformation(formula, list_subformulas):
    new_subformulas = []
    cont = 0
    for subformula in list_subformulas:
        if not is_literal(subformula):
            while isinstance(subformula, Not):
                subformula = subformula.inner
            if is_literal(subformula.left) and is_literal(subformula.right):
                cont += 1
                new_subformulas.append(Implies(Atom(f"z{cont}"), subformula))
                new_subformulas.append(Implies(subformula, Atom(f"z{cont}")))
                formula = substitution(formula, subformula, Atom(f"z{cont}"))

    new_subformulas.append(formula)
    return and_all(new_subformulas)


def formula_in_clauses(formula):
    list_formulas = []
    list_formulas = break_form1(formula, list_formulas)

    list_clausulas = []
    for formula in list_formulas:
        clausula = []
        clausula = break_form2(formula, clausula)
        list_clausulas.append(clausula)

    return list_clausulas


def break_form1(formula, list_formulas):
    if isinstance(formula, And) and isinstance(formula.right, Or):
        list_formulas.append(formula.right)
        return break_form1(formula.left, list_formulas)
    elif isinstance(formula, And) and isinstance(formula.left, Or):
        list_formulas.append(formula.left)
        return break_form1(formula.right, list_formulas)
    elif isinstance(formula, And) and isinstance(formula.right, And):
        list_formulas = break_form1(formula.right, list_formulas)
        return break_form1(formula.left, list_formulas)
    elif isinstance(formula, And) and isinstance(formula.left, And):
        list_formulas = break_form1(formula.left, list_formulas)
        return break_form1(formula.right, list_formulas)
    elif isinstance(formula, And) and isinstance(formula.left, Atom) and isinstance(formula.right, Atom):
        list_formulas.append(formula.left)
        list_formulas.append(formula.right)
    else:
        list_formulas.append(formula)
    return list_formulas


def break_form2(formula, clausula):
    if isinstance(formula, Or) and is_literal(formula.right):
        clausula.append(formula.right)
        return break_form2(formula.left, clausula)
    elif isinstance(formula, Or) and not is_literal(formula.right):
        clausula = break_form2(formula.right, clausula)
        return break_form2(formula.left, clausula)
    else:
        clausula.append(formula)
    return clausula
