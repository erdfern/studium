data ProzessA = ProzessA
                    String      -- PID
                    Int         -- arrival
                    Int         -- computing
                    deriving (Show)

data Prozess = Prozess {    pid         :: String
                            ,arrival    :: Int
                            ,computing  :: Int} deriving (Show)

arrivedBefore :: Int -> Prozess -> Bool
arrivedBefore t Prozess {arrival = a} = a < t

