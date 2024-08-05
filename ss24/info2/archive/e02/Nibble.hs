type Nibble = (Bool, Bool, Bool, Bool)

boolToInt :: Bool -> Int
boolToInt True = 1
boolToInt False = 0

-- 2.1
bitsToInt :: [Bool] -> Int
bitsToInt = foldl (\acc x -> acc * 2 + boolToInt x) 0

twosComplement :: Nibble -> Int
twosComplement (b1, b2, b3, b4) =
  let value = bitsToInt [b2, b3, b4]
   in if b1
        then value - 8
        else value

nibbleToString :: Nibble -> String
nibbleToString (b1, b2, b3, b4) = map (\x -> if x then '1' else '0') [b1, b2, b3, b4]

showNibble :: Nibble -> String
showNibble nibble@(b1, b2, b3, b4) =
  let bitString = nibbleToString nibble
      dualValue = bitsToInt [b1, b2, b3, b4]
      twosValue = twosComplement nibble
   in bitString ++ " " ++ show dualValue ++ " " ++ show twosValue

-- 2.2
bitAdder :: Bool -> Bool -> Bool -> (Bool, Bool)
bitAdder a b cin =
  let xor x y = (x || y) && not (x && y)
      sumBit = xor cin (xor a b)
      carryBit = (a && b) || (cin && xor a b)
   in (sumBit, carryBit)

-- 2.3
nibbleAdder :: Nibble -> Nibble -> (Bool, Nibble)
nibbleAdder (a3, a2, a1, a0) (b3, b2, b1, b0) =
  let (sum0, carry0) = bitAdder a0 b0 False
      (sum1, carry1) = bitAdder a1 b1 carry0
      (sum2, carry2) = bitAdder a2 b2 carry1
      (sum3, carry3) = bitAdder a3 b3 carry2
   in (carry3, (sum3, sum2, sum1, sum0))

tableAdder :: (Nibble -> Nibble -> (Bool, Nibble)) -> [(Nibble, Nibble)] -> String
tableAdder f args = unlines $ map (\(a, b) -> showAddition f a b) args
  where
    showAddition f a b =
      let (carry, sumNibble) = f a b
          carryStr = show carry
       in showNibble a ++ " + " ++ showNibble b ++ " = " ++ carryStr ++ " " ++ showNibble sumNibble

main :: IO ()
main = do
  putStrLn $ showNibble (True, False, False, True)
  putStrLn $ tableAdder nibbleAdder [((True, False, False, True), (False, False, False, True))]
