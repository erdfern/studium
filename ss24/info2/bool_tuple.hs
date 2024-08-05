--XOR operator
(<+>) :: Bool -> Bool -> Bool
(<+>) a b = (a || b) && (not (a && b))

-- Formatierung einer Tabellenzeile 
table_rowA :: (Bool -> Bool -> Bool) -> (Bool, Bool) -> String
table_rowA f xt = show xt ++ " : " ++ show(f (fst xt) (snd xt))

-- Formatierung einer Tabellenzeile 
table_row :: (Bool -> Bool -> Bool) -> (Bool, Bool) -> String
table_row f (x,y) = show (x,y) ++ " : " ++ show (f x y)

-- Formatierung einer Tabelle 
table :: (Bool -> Bool -> Bool) -> [(Bool, Bool)] -> String
table f []      = []
table f (x:xs)  = table_row f x ++ "\n" ++ table f xs

-- Input/Output benoetigt in Haskel ein wenig mehr Grundlagen zu Monaden. Wir schauen uns bei Gelegenheit und Zeit Monaden an. GHCI sollte erstmal ausreichen für diese Vorlesung.
main :: IO()
main = do
    let bool_duo = [(a,b) | a <- [False, True], b <- [False, True]]
    putStrLn (table (<+>) bool_duo)
