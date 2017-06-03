import random
import subprocess
from collections import defaultdict

import nltk
from nltk.parse.generate import generate
from nltk import CFG

grammars = [
    CFG.fromstring("""
        E -> E '+' T | T
        T -> 'id' | '(' E ')'
    """),
    CFG.fromstring("""
        A -> A 'x' | 'x'
    """),
    CFG.fromstring("""
        E -> E '*' B
        E -> E '+' B
        E -> B
        B -> '0'
        B -> '1'
    """)
]


def fuzz(word):
    duplicate = random.uniform(0, 20)
    remove = random.uniform(0, 20)
    while duplicate > 0:
        word.insert(random.randrange(len(word)), random.choice(word))
        duplicate -= 1
    while remove > 0 and len(word) > 0:
        del word[random.randrange(len(word))]
        remove -= 1
    return word

def send(obj):
    data = bytes(str(obj), 'ascii') + b'.\n'
    proc.stdin.write(data)
    proc.stdin.flush()

def check(word):
    send(word)
    response = proc.stdout.readline()
    assert response in {b'YES\n', b'NO\n'}
    return response == b'YES\n'

def dump_grammar(grammar):
    nonterminals = set(p.lhs() for p in grammar.productions())
    productions = defaultdict(list)
    for production in grammar.productions():
        productions[production.lhs()].append(production.rhs())

    nltk.grammar.Nonterminal.__repr__ = lambda self: "nt('" + self.symbol() + "')"

    prod_str = ', '.join("prod('{}', {})".format(lhs, list(map(list, rhs))) for lhs, rhs in productions.items())
    return "gramatyka('{}', [{}])".format(grammar.start(), prod_str)

stats = {True: 0, False: 0}
for grammar in grammars:
    print(grammar)
    parser = nltk.ChartParser(grammar)
    proc = subprocess.Popen(['swipl', '-s', 'test_words.pl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    grammar_term = dump_grammar(grammar)
    send(grammar_term)
    for i, word in enumerate(generate(grammar, depth=8)):
        if i % 100 == 0 and i > 0:
            print('{i:16d}\taccepted: {accepted:8d}\trejected:{rejected:8d}'.format(
                i=i, accepted=stats[True], rejected=stats[False]))
        assert check(word), word
        stats[True] += 1

        word = fuzz(word)
        should_accept = bool(len(list(parser.parse(word))))
        assert check(word) == should_accept, word
        stats[should_accept] += 1
    proc.stdin.close()
