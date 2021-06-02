"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import atoms


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    # Implementação da função;
    pass
    # ======== YOUR CODE HERE ========
    if isinstance(formula, Atom):
        return interpretation[Atom.__str__(formula)]
    if isinstance(formula, Not):
        return not truth_value(formula.inner, interpretation)
    if isinstance(formula, And):
        return truth_value(formula.left, interpretation) and truth_value(formula.right, interpretation)
    if isinstance(formula, Or):
        return truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)
    if isinstance(formula, Implies):
        return not truth_value(formula.left, interpretation) or (truth_value(formula.right, interpretation))


def is_logical_consequence(premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    pass
    # ======== YOUR CODE HERE ========


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    pass
    # ======== YOUR CODE HERE ========


def defined_values(formula):
    """Auxiliary function that returns an interpretation with some defined values """

    interpretation = dict()
    list_formula = defined_list(formula)

    for form in list_formula:
        if isinstance(form, Atom):
            interpretation[Atom.__str__(form)] = True
        if isinstance(form, Not) and isinstance(form.inner, Atom):
            interpretation[Atom.__str__(form.inner)] = False

    return interpretation


def defined_list(formula):
    """Returns a list with some formulas"""

    list_and = list()
    if isinstance(formula, Atom):
        list_and.append(formula)
    if isinstance(formula, Not) and isinstance(formula.inner, Atom):
        list_and.append(formula)
    if isinstance(formula, And):
        list_and += defined_list(formula.left)
        list_and += defined_list(formula.right)

    return list_and


def is_satisfiable(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    pass
    list_atoms = atoms(formula)
    interpretation = defined_values(formula)

    for k in interpretation.keys():
        list_atoms.remove(Atom(k))

    return sat(formula, list_atoms, interpretation)


def sat(formula, list_atoms, interpretation):
    if len(list_atoms) == 0:
        if truth_value(formula, interpretation):
            return interpretation
        else:
            return False

    atom = list_atoms.pop()

    list1 = list_atoms.copy()
    list2 = list_atoms.copy()

    interpretation1 = interpretation.copy()
    interpretation1[Atom.__str__(atom)] = True

    interpretation2 = interpretation.copy()
    interpretation2[Atom.__str__(atom)] = False

    result = sat(formula, list1, interpretation1)

    if result:
        return result
    return sat(formula, list2, interpretation2)


