{-# LANGUAGE OverloadedStrings #-}

module Day4 (part2) where

import Control.Monad.State
import qualified Data.ByteString as B
import qualified Data.Foldable as F
import Data.Set
import qualified Data.Set as S
import Data.Vector.Unboxed
import qualified GHC.List as L
import Paths_aoc_hs (getDataFileName)

type Grid = Set (Int, Int)

type Coordinate = (Int, Int)

parseGrid :: String -> Grid
parseGrid input = S.fromList coordinates
  where
    n = F.length input
    rows = lines input
    coordinates = [(y, x) | (y, row) <- L.zip [0 .. n - 1] rows, (x, symbol) <- L.zip [0 .. n - 1] row, symbol == '@']

neighborhood :: Coordinate -> Grid
neighborhood (y, x) = S.fromList $ [(y + dy, x + dx) | dx <- [-1, 0, 1], dy <- [-1, 0, 1], (dx /= 0) || (dy /= 0)]

prepend :: [a] -> [a] -> [a]
prepend [] l = l
prepend l [] = l
prepend (x : xs) l = (x : prepend xs l)

checkRoll :: State (Grid, [Coordinate], Int) (Maybe Int)
checkRoll = do
  (grid, working_set, score) <- get
  case working_set of
    [] -> pure $ Just score
    (roll : rest) -> do
      case (member roll grid) of
        False -> do
          put (grid, rest, score)
          pure $ Nothing
        True -> do
          let neighbors = neighborhood roll
          let effectiveNeighbors = intersection grid neighbors
          let removeRoll = (F.length effectiveNeighbors) < 4
          case removeRoll of
            True -> do
              let new_working_set = prepend (S.toList effectiveNeighbors) rest
              let new_grid = delete roll grid
              let new_score = score + 1
              put (new_grid, new_working_set, new_score)
              pure Nothing
            False -> do
              put (grid, rest, score)
              pure Nothing

indexGrid :: Vector Char -> Int -> (Int, Int) -> Char
indexGrid v n (y, x) = v ! (y * n + x)

runUntilDone :: State (Grid, [Coordinate], Int) (Maybe Int) -> State (Grid, [Coordinate], Int) Int
runUntilDone action = do
  result <- action
  case result of
    Just n -> return n
    Nothing -> runUntilDone action

solveGrid :: Grid -> Int
solveGrid grid = evalState (runUntilDone checkRoll) (grid, S.toList grid, 0)

solve :: String -> Int
solve = solveGrid . parseGrid

part2 :: IO Int
part2 = do
  path <- getDataFileName "data/day4/input.txt"
  input <- readFile path
  pure $ solve input
