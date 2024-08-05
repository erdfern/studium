## Deterministischer endlicher Automat (DEA)

$A = (Sigma, Q, s, F, delta)$

- Alphabet $Sigma = {a,b}$ 
- Zustände $Q = {{q_0}, ... }$
- Startzustand $s = {q_0}$
- Akzeptierende Zustände $F = { ... }$
- Überführungsfunktion $delta : Q xx Sigma -> Q$

### Überführungsfunktion

| $p in Q$          | $delta_p(a)$ | $delta_p(b)$ |
| :---              | :---         | :---         |
| ${q_0}$           | ${q_0, q_1}$ | ${q_1}$      |
| ${q_1}$           |              |              |
| ${q_2}$           |              |              |
| ${q_3}$           |              |              |
| ${q_0, q_1}$      |              |              |
| ${q_0, q_2}$      |              |              |
| ${q_0, q_3}$      |              |              |
| ${q_1, q_2}$      |              |              |
| ${q_1, q_3}$      |              |              |
| ${q_2, q_3}$      |              |              |
| ${q_0, q_1, q_2}$ |              |              |
| ${q_0, q_2, q_3}$ |              |              |
| ${q_1, q_2, q_3}$ |              |              |
| $O/$              |              |              |
