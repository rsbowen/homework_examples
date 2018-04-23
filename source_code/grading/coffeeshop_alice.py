# Alice is a model student; her code is identical to the solution!

# Please see instructions.txt for the description of this problem.
from exceptions import NotImplementedError

def busiest_time(customer_entry_data):
  # customer_entry_data is a list of tuples:
  # (entry_time, exit_time).
  # entry_time and exit_time are integers (think of them as minutes past some reference, if you like).
  # Your code should return a triple of integers:
  # (start, end, number)
  # which indicate the period during which the coffeeshop was most busy, and how many people were there.
  # In case of a tie, your code should return the first busy period.

  # YOUR CODE HERE!
  entry_times = [(d[0], 1) for d in customer_entry_data]
  exit_times = [(d[1], -1) for d in customer_entry_data]
  interleaved = (entry_times + exit_times)
  interleaved.sort()

  num_patrons = 0
  max_num_patrons = 0
  busy_start = 0
  busy_end = 0
  for i in range(len(interleaved)):
    num_patrons += interleaved[i][1]
    if num_patrons > max_num_patrons:
      max_num_patrons = num_patrons
      busy_start = interleaved[i][0]
      busy_end = interleaved[i+1][0]

  return (busy_start, busy_end, max_num_patrons)
