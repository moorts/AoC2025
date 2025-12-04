import Control.Monad.Identity
import Control.Monad.State
import Data.Maybe
import Data.Set
import qualified Data.Set as S

type Grid = Set (Int, Int)

type Coordinate = (Int, Int)

parseGrid :: String -> Grid
parseGrid input = fromList coordinates
  where
    n = length input
    rows = lines input
    coordinates = [(y, x) | (y, row) <- zip [0 .. n - 1] rows, (x, symbol) <- zip [0 .. n - 1] row, symbol == '@']

neighborhood :: Coordinate -> Grid
neighborhood (y, x) = fromList $ [(y + dy, x + dx) | dx <- [-1, 0, 1], dy <- [-1, 0, 1], (dx /= 0) || (dy /= 0)]

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
          let removeRoll = (length effectiveNeighbors) < 4
          case removeRoll of
            True -> do
              let new_working_set = rest ++ (toList effectiveNeighbors)
              let new_grid = delete roll grid
              let new_score = score + 1
              put (new_grid, new_working_set, new_score)
              pure Nothing
            False -> do
              put (grid, rest, score)
              pure Nothing

runUntilDone :: State (Grid, [Coordinate], Int) (Maybe Int) -> State (Grid, [Coordinate], Int) Int
runUntilDone action = do
  result <- action
  case result of
    Just n -> return n
    Nothing -> runUntilDone action

solve :: Grid -> Int
solve grid = evalState (runUntilDone checkRoll) (grid, toList grid, 0)

main :: IO ()
main = do
  input <- readFile "input.txt"
  let grid = parseGrid input
  let score = solve grid
  putStrLn $ show score
