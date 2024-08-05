--XOR operator
(<+>) :: Bool -> Bool -> Bool
(<+>) a b = (a || b) && (not (a && b))

-- Nor auf einer Liste von Bools
nor :: [Bool] -> Bool
nor = not . or

-- Typ-Synonym für 4-Tupel von Bools
type Nibble = (Bool, Bool, Bool, Bool)

-- Check von zwei Nibble auf Gleichheit
equals :: Nibble -> Nibble -> Bool
equals (a3, a2, a1, a0) (b3, b2, b1, b0) = nor [a3 <+> b3, a2 <+> b2, a1 <+> b1, a0 <+> b0]

-- Input/Output benoetigt in Haskel ein wenig mehr Grundlagen zu Monaden. Wir schauen uns bei Gelegenheit und Zeit Monaden an. GHCI sollte erstmal ausreichen für diese Vorlesung.
main :: IO()
main = do
    let nibbleA = (True, False, False, False)
    let nibbleB = (True, False, False, False)
    let nibbleC = (False, False, False, False)
    putStrLn $ show $ equals nibbleA nibbleC

