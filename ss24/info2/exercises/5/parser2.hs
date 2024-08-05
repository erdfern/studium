match :: Char -> Maybe String -> Maybe String
match _ Nothing = Nothing
match expected (Just (c : cs))
  | c == expected = Just cs
  | otherwise = Nothing

factor :: Maybe String -> Maybe String
factor tokens = match 'c' tokens

ftail :: Maybe String -> Maybe String
ftail Nothing = Nothing
ftail tokens@(Just (c : _))
  | c == '*' = ftail $ factor $ match '*' tokens
  | otherwise = tokens

term :: Maybe String -> Maybe String
term tokens = ftail $ factor tokens

ttail :: Maybe String -> Maybe String
ttail Nothing = Nothing
ttail tokens@(Just (c : _))
  | c == '+' = ttail $ term $ match '+' tokens
  | otherwise = tokens

expr :: Maybe String -> Maybe String
expr tokens = ttail $ term tokens

prog :: String -> Maybe String
prog tokens = match '$' $ expr $ Just tokens

main :: IO ()
main = do
  print (prog "c+c*c$")
  print (prog "c+c-c$")
