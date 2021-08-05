from functools import wraps

def coroutine(func):
  """[summary]

  Args:
      func ([type]): [description]
  """
  @wraps(func)
  def primer(*args, **kwargs):
    gen = func(*args, **kwargs)
    next(gen)
    return gen
  return primer

@coroutine
def grep(pattern):
  print("looking for", pattern)
  try:
    while True:
      line = (yield)
      if pattern in line:
        print(line)
  except GeneratorExit:
    print("Good Bye.")

g = grep("python")
g

g.send("python is good")
g.send("elixir is good")
g.close()
# g.throw(RuntimeError, "closed earlier")

def countdown(n):
  print("counting down from", n)
  while(n >= 0):
    new_value = yield n
    if new_value is not None:
      n = new_value
    else:
      n -= 1

c = countdown(5)
for n in c:
  print(n)
  if n==5:
    c.send(3)




