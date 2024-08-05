match :: String -> [String] -> [String]
match _ [] = error "End of input reached, match failed"
match expected (x : xs)
  | expected == x = xs
  | otherwise = error ("Expected" ++ expected ++ " but found " ++ x)

id_list_tail :: [String] -> [String]
id_list_tail [] = error "Unexpected end of input in id_list_tail"
id_list_tail tokens@(x : _)
  | x == "," = id_list (match "," tokens)
  | x == ";" = match "$$" (match ";" tokens)
  | otherwise = error ("unexpeced token " ++ x ++ " in id_list_tail")

id_list :: [String] -> [String]
id_list [] = error "Unexpected end of input in id_list"
id_list tokens = id_list_tail (match "id" tokens)

main :: IO ()
main = do
  print (id_list ["id", ",", "id", ";", "$$"])
  print (id_list ["id", "$$"])
