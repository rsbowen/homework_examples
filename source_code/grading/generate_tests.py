import random
import multiprocessing
import sys

# Generative tests for coffeeshop problem.
def generate_test_cases(num_cases):
  #Be deterministic.
  random.seed(0)
  max_num_intervals = 5 
  num_generated = 0
  while num_generated < num_cases:
    num_intervals = random.randint(1,max_num_intervals)
    timepoints = range(2*num_intervals)
    random.shuffle(timepoints)
    pairs = [sorted([timepoints[2*i], timepoints[2*i + 1]]) for i in range(num_intervals)]
    num_generated += 1
    yield pairs

def test_runner(student_soln, soln, tc_gen, result_pipe):
  for (index, testcase) in enumerate(tc_gen):
    student_answer = None
    right_answer = soln(testcase)
    try:
      student_answer = student_soln(testcase)
      if not right_answer == student_answer:
        result_pipe.send((index, testcase, student_answer, right_answer))
        result_pipe.close()
        return
    except:
      result_pipe.send((index, testcase, sys.exc_info()[0], right_answer))
      result_pipe.close()
      return

  result_pipe.send(-1)
  result_pipe.close()

from coffeeshop_alice import busiest_time as busiest_time_alice
from coffeeshop_bob import busiest_time as busiest_time_bob
from coffeeshop_carol import busiest_time as busiest_time_carol
from coffeeshop_dan import busiest_time as busiest_time_dan
from coffeeshop_eve import busiest_time as busiest_time_eve

student_solutions = [busiest_time_alice, busiest_time_bob, busiest_time_carol, busiest_time_dan, busiest_time_eve]

from coffeeshop_solution import busiest_time as busiest_time_soln

# This could be better, but for now, just run until they pass 10000 tests or fail at least one test.

timeout_seconds = 10

for (student_index, student_soln) in enumerate(student_solutions):
  [recv, send] = multiprocessing.Pipe()
  tc_gen = generate_test_cases(10000)
  p = multiprocessing.Process(target = test_runner, args=(student_soln, busiest_time_soln, tc_gen, send))

  p.start()
  p.join(timeout_seconds)

  if p.is_alive():
    p.terminate()

  pipe_contents = []
  while recv.poll():
    pipe_contents.append(recv.recv())

  if len(pipe_contents) != 1:
    print "Student %d timed out" % (student_index)
  elif pipe_contents[0] == -1:
    print "Student %d passed all tests" % (student_index)
  else:
    print "Student %d failed test %d, with input %s and output %s and correct output %s" % (student_index, pipe_contents[0][0], pipe_contents[0][1], pipe_contents[0][2], pipe_contents[0][3])
