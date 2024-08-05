type Nibble = (Bool, Bool, Bool, Bool)
type Byte = (Nibble, Nibble)

lastBitNibble :: Nibble -> Bool
lastBitNibble (a,b,c,d) = d

lastBitByte :: Byte -> Bool
lastBitByte (a,b) = lastBitNibble b

data Signal = X | O
