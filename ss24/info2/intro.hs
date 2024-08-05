-- parabola
f :: Int -> Int
f   x = x * x + x + x

--logarithm to base 2
log2 :: Float -> Float
log2 = logBase 2

--implication praefix
(==>) :: Bool -> Bool -> Bool
(==>) a b = not a || b

--implication infix
(===>) :: Bool -> Bool -> Bool
a ===> b = not a || b

-- euler number
e :: Float
e = exp 1
