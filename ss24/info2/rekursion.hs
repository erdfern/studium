-- Heron Version A
heronA :: (Int, Double) -> Double
heronA (n, a)
    | n > 0     = (heronA ((n-1), a) + a / heronA ((n-1), a)) / 2
    | otherwise = a

-- Heron Version B
heronB :: Int -> Double -> Double
heronB n a
    | n > 0     = (heronB (n-1) a + a / heronB (n-1) a) / 2
    | otherwise = a

-- Heron Version C
heronC :: Int -> Double -> Double
heronC n a
    | n > 0     = (x + a/x) / 2
    | otherwise = a
    where x = heronC (n-1) a

-- Fibonacci Version A
fibA :: Int -> Int
fibA n
    | n == 0    = 0
    | n == 1    = 1
    | otherwise = x + y
    where
        x = fibA (n-1)
        y = fibA (n-2)

-- Fibonacci Version B
fibB :: Int -> Int
fibB 0 = 0
fibB 1 = 1
fibB n = fibB (n-1) + fibB (n-2)

-- Fibonacci Version C
fibC :: Int -> Int
fibC 0 = 0
fibC 1 = 1
fibC n
    | n < 0     = error "illegal argument"    
    | otherwise = fibC (n-1) + fibC (n-2)

-- Heron as Operator
(<##>) :: Int ->  Double -> Double
0 <##> a = a
n <##> a
    | n > 0     = (x + a/x) / 2
    | otherwise = error "illegal argument"
    where x = (n-1) <##> a

