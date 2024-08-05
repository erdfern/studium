{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}

{-# HLINT ignore "Use camelCase" #-}
module Main where

import Data.List (partition, sortOn)
import System.Exit (exitSuccess)

data Constants = Constants
  { idle_pid :: String,
    idle_arrival :: Int,
    idle_burst :: Int
  }

constants :: Constants
constants = Constants {idle_pid = "IDLE", idle_arrival = -1, idle_burst = -1}

data Process = Process
  { pid :: String,
    arrival :: Int,
    burst :: Int
  }
  deriving (Show)

instance Eq Process where
  (==) :: Process -> Process -> Bool
  Process {burst = a} == Process {burst = b} = a == b

instance Ord Process where
  compare :: Process -> Process -> Ordering
  compare x y
    | burst x < burst y = LT
    | burst x > burst y = GT
    | burst x == burst y = EQ

data State = State
  { new :: [Process],
    running :: Process,
    ready :: [Process],
    time :: Int,
    chart :: String
  }

instance Show State where
  show :: State -> String
  show s =
    "-- new\n"
      ++ unlines (map show (new s))
      ++ "-- run\n"
      ++ show (running s)
      ++ "\n"
      ++ "-- ready\n"
      ++ unlines (map show (ready s))
      ++ "-- time : "
      ++ show (time s)
      ++ "\n"
      ++ "-- chart : \n"
      ++ chart s

-- updateReadyFCFS adds processes that have arrived to the ready queue in First-Come-First-Serve order
splitByArrivalTime :: [Process] -> Int -> ([Process], [Process])
splitByArrivalTime ps t = partition (\p -> arrival p <= t) ps

-- updateReadySJF adds processes that have arrived to the ready queue in Shortest Job First order
updateReadyFCFS :: State -> State
updateReadyFCFS s =
  let (arrived, notArrived) = splitByArrivalTime (new s) (time s)
   in s {new = notArrived, ready = ready s ++ arrived} -- add arrived processes to ready queue

-- updateReadySJF adds processes that have arrived to the ready queue in Shortest Job First order
updateReadySJF :: State -> State
updateReadySJF s =
  let (arrived, notArrived) = splitByArrivalTime (new s) (time s)
   in s {new = notArrived, ready = sortOn burst (ready s ++ arrived)} -- add arrived processes to the ready queue and sort by burst time

-- updateReadySRTF adds processes that have arrived to the ready queue in Shortest Remaining Time First order
updateReadySRTF :: State -> State
updateReadySRTF s =
  let (arrived, notArrived) = splitByArrivalTime (new s) (time s)
      newReady = ready s ++ arrived -- add arrived processes to the ready queue
      newRunning = running s -- by default, the running process remains the same
   in if not (null newReady) && burst newRunning > minimum (map burst newReady) -- if there's a shorter job in the ready queue
        then -- preempt running process if a shorter job has arrived

          let shortestJob = minimum newReady -- find the shortest job
              newNewReady = filter (/= shortestJob) newReady -- remove the shortest job from the ready queue
           in s {new = notArrived, running = shortestJob, ready = sortOn burst (newRunning : newNewReady)} -- update the state
        else s {new = notArrived, ready = sortOn burst newReady} -- if no preemption is needed, simply sort the ready queue

-- update_running selects a new process to run if the current process is idle
update_running :: State -> State
update_running s
  | pid (running s) == idle_pid constants && not (null (ready s)) -- if the running process is idle and there are processes in the ready queue
    =
      s {running = head (ready s), ready = tail (ready s)} -- run the first process in the ready queue
  | otherwise = s -- if the running process is not idle or the ready queue is empty, do nothing

-- increment time by 1, decrement burst of running process by 1
-- save the PID of running process to chart. If the burst of running process is 0, set running process to idle
update_time :: State -> State
update_time s =
  let newTime = time s + 1
      newChart = chart s ++ pid (running s) ++ " | t" ++ show newTime ++ "\n"
      currentProcess = running s
      newRunning =
        if burst currentProcess <= 1
          then Process {pid = idle_pid constants, arrival = idle_arrival constants, burst = idle_burst constants}
          else currentProcess {burst = burst currentProcess - 1}
   in s {time = newTime, chart = newChart, running = newRunning}

-- simulate scheduling by calling update_ready, update_running, and update_time until there is no process in new and ready queue
-- simulate :: (State -> State) -> State -> State
-- simulate updateReady s
--   | null (new s) && null (ready s) = s
--   | otherwise = simulate updateReady (update_time (update_running (updateReady s)))

-- simulate scheduling by calling update_ready, update_running, and update_time until all processes are finished
simulate :: (State -> State) -> State -> State
simulate updateReady s
  | null (new s) && null (ready s) && pid (running s) == idle_pid constants = s
  | otherwise = simulate updateReady (update_time (update_running (updateReady s)))

main :: IO ()
main = do
  let idle = Process {pid = idle_pid constants, arrival = idle_arrival constants, burst = idle_burst constants}
  let p1 = Process {pid = "P1", arrival = 0, burst = 6}
  let p2 = Process {pid = "P2", arrival = 2, burst = 6}
  let p3 = Process {pid = "P3", arrival = 4, burst = 5}
  let p4 = Process {pid = "P4", arrival = 12, burst = 4}
  let p5 = Process {pid = "P5", arrival = 16, burst = 3}
  let p6 = Process {pid = "P6", arrival = 19, burst = 6}

  let ps = [p1, p2, p3, p4, p5, p6]
  let s = State {new = ps, running = idle, ready = [], time = 0, chart = ""}

  let s_fcfs = simulate updateReadyFCFS s
  let s_sjf = simulate updateReadySJF s
  let s_srtf = simulate updateReadySRTF s

  putStrLn "Initial state:"
  print s

  putStrLn "Final state:"
  putStrLn "FCFS"
  print s_fcfs
  putStrLn "SJF"
  print s_sjf
  putStrLn "SRTF"
  print s_srtf

  exitSuccess
