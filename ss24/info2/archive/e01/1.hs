module Main1 where

-- 1.1
quadratic :: (Int, Int, Int) -> Int -> Int
quadratic (a, b, c) x = a * x * x + b * x + c


-- 1.2
square :: Int -> Int
square n
  | n < 0 = square (-n)
  | n == 0 = 0
  | otherwise = sum [2 * i - 1 | i <- [1 .. n]]

-- 1.3a
sumList :: [Int] -> Int
sumList [] = 0
sumList (x : xs) = x + sumList xs

-- 1.3b
foldList :: (Double -> Double -> Double) -> [Double] -> Double
foldList _ [] = 0
foldList f (x : xs) = f x (foldList f xs)

-- 1.3c
mapList :: (Int -> Int) -> [Int] -> [Int]
mapList _ [] = []
mapList f (x : xs) = f x : mapList f xs

-- 1.4
tableInt :: (Int -> Int) -> [Int] -> String
tableInt _ [] = ""
tableInt f (x : xs) = show x ++ " -> " ++ show (f x) ++ "\n" ++ tableInt f xs
