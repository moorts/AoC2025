{-# LANGUAGE OverloadedStrings #-}

module Day5 (part1, part2, mergeRanges) where

import Data.Attoparsec.Text (Parser)
import qualified Data.Attoparsec.Text as P
import Data.List
import qualified Data.Text.IO as T
import Paths_aoc_hs (getDataFileName)

parseRange :: Parser (Int, Int)
parseRange = do
  start <- P.decimal
  _ <- P.char '-'
  end <- P.decimal
  return (start, end)

parseInput :: Parser ([(Int, Int)], [Int])
parseInput = do
  ranges <- P.many' $ parseRange <* P.endOfLine
  P.endOfLine
  ids <- P.decimal `P.sepBy` P.endOfLine

  return (ranges, ids)

readInput :: IO ([(Int, Int)], [Int])
readInput = do
  path <- getDataFileName "data/day5/input.txt"
  input <- T.readFile path
  case P.parseOnly parseInput input of
    Left _ -> error "Invalid Input"
    Right (a, b) -> return (a, b)

inRange :: Int -> (Int, Int) -> Bool
inRange x (start, end) = start <= x && x <= end

isFresh :: [(Int, Int)] -> Int -> Bool
isFresh ranges x = any (inRange x) ranges

countFresh :: [(Int, Int)] -> [Int] -> Int
countFresh ranges = length . (filter (isFresh ranges))

part1 :: IO ()
part1 = do
  (ranges, ids) <- readInput
  let result = countFresh ranges ids
  putStrLn $ show result

mergeRanges :: [(Int, Int)] -> [(Int, Int)]
mergeRanges [] = []
mergeRanges [r] = [r]
mergeRanges ((s1, e1) : (s2, e2) : rs)
  | s2 <= e1 = mergeRanges ((s1, max e1 e2) : rs)
  | otherwise = (s1, e1) : (mergeRanges ((s2, e2) : rs))

part2 :: IO ()
part2 = do
  (ranges, _) <- readInput

  let merged_ranges = mergeRanges $ sort ranges
  putStrLn $ show merged_ranges
  let result = sum $ (\(s, e) -> e - s + 1) <$> merged_ranges
  putStrLn $ show result
