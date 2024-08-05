module Main2 where

import Data.Char (toLower)

-- 2.1
containsList :: [Int] -> Int -> Bool
containsList [] _ = False
containsList (x : xs) y
  | x == y = True
  | otherwise = containsList xs y

-- 2.2
countList :: [Char] -> Char -> Int
countList [] _ = 0
countList (x : xs) y
  | toLower x == toLower y = 1 + countList xs y
  | otherwise = countList xs y
