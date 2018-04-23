# This is a short test file, given to you to ensure that our grading scripts can grade your file.
# Please do not modify it.
# You should only submit "coffeeshop.py".

# This tests the simplest case: a single interval.

import coffeeshop
import sys

try:
  output = coffeeshop.busiest_time([(0,1)])
  if output is not (0,1,1):
    print "Your code ran, but did NOT output the right answer on the input [(0,1)]."
  else:
    print "Your code ran, and it output the right answer on the input [(0,1)]."
except:
  print "Your code produced this error on the input [(0,1)]"
  print sys.exc_info()[0]
