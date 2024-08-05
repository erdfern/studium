-- Formatierung einer Tabellenzeile
table_row :: ([Bool] -> Bool) -> [Bool] -> String
table_row f xs = show xs ++ " : " ++ show (f xs)

-- Formatierung einer Tabelle
tableA :: ([Bool] -> Bool) -> [[Bool]] -> String
tableA f xs
    | null xs   = ""
    | otherwise = table_row f (head xs) ++ "\n" ++ tableA f (tail xs)

-- Formatierung einer Tabelle
table :: ([Bool] -> Bool) -> [[Bool]] -> String
table f [] = ""
table f (x:xs) = table_row f x ++ "\n" ++ table f xs

