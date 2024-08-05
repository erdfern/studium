## Nicht-rekursiver Parser II

### Parse-Tabelle

|      | 0     | 1     | $neg$   | $vv$     | $^^$     | §§      |
| :--- | :---  | :---  | :---    | :---     | :---     | :---    |
| <1>  | <2>   | <2>   | <2>     |          |          |         |
| <2>  | <3><4>| <3><4>| <3><4>  |          |          |         |
| <3>  | 0     | 1     | $neg$<2>|          |          |         |
| <4>  |       |       |         |$vv$<3><4>|$^^$<3><4>|$epsilon$|


### Parsing

| Stapel           | Eingabe                       | Aktion          |
| ---:             | ---:                          | :---            | 
|<1>$gamma$        | $neg$0$vv$0$^^$1$vv$$neg$1 §§ |<1>$rarr$<2>     |
|<2>$gamma$        | $neg$0$vv$0$^^$1$vv$$neg$1 §§ |<2>$rarr$<3><4>  |
|<3><4>$gamma$     | $neg$0$vv$0$^^$1$vv$$neg$1 §§ |<3>$rarr$$neg$<2>|
|$neg$<2><4>$gamma$| $neg$0$vv$0$^^$1$vv$$neg$1 §§ |match            |
|<2><4>$gamma$     |      0$vv$0$^^$1$vv$$neg$1 §§ |                 |
