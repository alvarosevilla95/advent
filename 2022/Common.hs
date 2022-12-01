module Common (
getInput,
getInputLines,
) where

getInput n = readFile $ "inputs/day" ++ show n ++ ".txt"

getInputLines n = lines <$> getInput n
