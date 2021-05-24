from invoke import task
import time

@task(aliases=['del'])
def delete(c):
    c.run("rm *mykmeanssp*.so")


@task
def build(c):
    c.run("python setup.py build_ext --inplace")


@task
def run(c, k=-1 , n=-1 , Random=True):
  #  print("For 2 dimensions and 5 minutes run, maximum points 300, maximum centers 20")
   # print("For 3 dimensions and 5 minutes run, maximum points 300, maximum centers 20")
    c.run("python setup.py build_ext --inplace")
    start = time.time()
    c.run("python main.py {0} {1} {2}".format(k, n, Random))
    end = time.time()
    print(end - start)
