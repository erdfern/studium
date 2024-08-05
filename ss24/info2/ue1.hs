toDigits::Int->[Int]
toDigits 0 = []
toDigits x
 |x < 0 = []
 |otherwise = toDigits z ++ [y]
 where
  y= x `mod` 10
  z= x `div` 10

toDigitsRev::Int->[Int]
toDigitsRev = reverse.toDigits

doubleEveryOther::[Int]->[Int]
doubleEveryOther xs = reverse [if i `mod`2 == 1 then x*2 else x
                              | (i,x)<- zip [0..] (reverse xs)]

sumDigits::[Int]->Int
sumDigits=sum

validate::Int->Bool
validate x = sumDigits [(sumDigits.toDigits) y
           | y<-(doubleEveryOther.toDigits) x] `mod` 10 == 0
