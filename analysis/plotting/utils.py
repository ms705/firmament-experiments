from matplotlib import use, rc
use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# plot saving utility function
def writeout(filename_base, tight=True):
  for fmt in ['pdf']:
    if tight:
      plt.savefig("%s.%s" % (filename_base, fmt), format=fmt, bbox_inches='tight', pad_inches=0.01)
    else:
      plt.savefig("%s.%s" % (filename_base, fmt), format=fmt)

def set_leg_fontsize(size):
  rc('legend', fontsize=size)

def set_paper_rcs():
  rc('font', family='serif', size=9)
  rc('text.latex', preamble=['\usepackage{times,mathptmx}'])
  rc('text', usetex=True)
  rc('legend', fontsize=8)
  rc('figure', figsize=(3.33,2.22))
#  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  rc('lines', linewidth=0.5)

def set_rcs():
#  rc('font',**{'family':'sans-serif','sans-serif':['Times'],
#               'serif':['Times'],'size':10})
  rc('font', family='serif')
  rc('text.latex', preamble=['\usepackage{times,mathptmx}'])
  rc('text', usetex=True)
  rc('legend', fontsize=10)
  rc('figure', figsize=(6,4))
  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  rc('lines', linewidth=0.5)

def append_or_create(d, i, e):
  if not i in d:
    d[i] = [e]
  else:
    d[i].append(e)

def add_or_create(d, i, e):
  if not i in d:
    d[i] = e
  else:
    d[i] = d[i] + e


paper_figsize_small = (1.1, 1.1)
paper_figsize_small_square = (1.5, 1.5)
paper_figsize_medium = (2, 1.33)
paper_figsize_medium_square = (2, 2)
#paper_figsize_medium = (1.66, 1.1)
paper_figsize_large = (3, 2)
paper_figsize_bigsim3 = (2.4, 1.7)

# -----------------------------------

def think_time_fn(x, y, s):
  return x + y * s

# -----------------------------------

def get_mad(median, data):
  devs = [abs(x - median) for x in data]
  mad = np.median(devs)
  return mad

# -----------------------------------
