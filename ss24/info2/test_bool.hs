testAND :: String
testAND = 
  show( and[False, False, False] ) ++ "\n" ++ 
  show( and[False, False, True ] ) ++ "\n" ++ 
  show( and[False, True , False] ) ++ "\n" ++ 
  show( and[False, True , True ] ) ++ "\n" ++ 
  show( and[True , False, False] ) ++ "\n" ++ 
  show( and[True , False, True ] ) ++ "\n" ++ 
  show( and[True , True , False] ) ++ "\n" ++ 
  show( and[True , True , True ] ) 

main :: IO()
main = do
  putStrLn testAND
