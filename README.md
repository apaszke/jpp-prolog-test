# Testy do zadania z Prologu

Program zakłada że implementacja obu funkcji z zadania znajduje się w pliku `auto.pl` (można to zmienić w `test_words.pl`).
Testy generują wszystkie słowa o wyprowadzeniach do zadanej głębokości, oraz dla każdego takiego słowa dokonują losowych przekształceń, i sprawdzają czy automat nie przyjmuje takiego słowa (jeżeli nie należy już do języka).

## Zależności

Python odpala interpreter `swipl` zamiast `sicstus`a (`swipl` jest darmowy, więc można go u siebie łatwo zainstalować).

```bash
pip install nltk
```

# Uruchamianie

```bash
python test_words.py
```

Długość testów można edytować zmieniając parametr `depth=8` w `test_words.py` (oczywiście liczba słów rośnie wtedy wykładniczo).
