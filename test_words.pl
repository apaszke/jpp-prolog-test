grammar(ex1, gramatyka('E', [prod('E', [[nt('E'),+,nt('T')], [nt('T')]]),
                             prod('T', [[id], ['(', nt('E'), ')']]) ])).

parseWords(Automat) :-
    read(Word),
    ( Word = end_of_file ->
        true
    ;
        (accept(Automat, Word) -> write('YES\n'); write('NO\n')),
        parseWords(Automat)
    ).


:-  consult('auto.pl'),
    read(G),
    createLR(G, Automat, yes),
    parseWords(Automat),
    halt.
