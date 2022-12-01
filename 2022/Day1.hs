import Common
import Data.List

main = do 
    input <- getInputLines 1
    let caloriesByElf = map (map read) $ splitWhen (== "") input
    let caloriesByElfSum = reverse $ sort $ map sum caloriesByElf
    print $ head caloriesByElfSum
    print $ take 3 caloriesByElfSum

splitWhen :: (a -> Bool) -> [a] -> [[a]]
splitWhen pred xs = splitWhen' xs [] where 
    splitWhen' [] agg = [agg]
    splitWhen' (y : ys) agg
        | pred y = agg : splitWhen' ys []
        | otherwise = splitWhen' ys (agg ++ [y])
