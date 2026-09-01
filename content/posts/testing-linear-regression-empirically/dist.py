import sys
from scipy import stats


distributions = {
    "normal": {
        "type": "continous",
        "parameters": [(0., 0.2), (0., 1.), (0., 5.), (-2, 0.5)],
        "function": stats.norm
    },
    "uniform": {
        "type": "continous",
        "parameters": [(0, 1)],
        "function": stats.uniform
    },
    "cauchy": {
        "type": "continous",
        "parameters": [(0., 0.5), (0., 1.), (0., 2.), (-2., 1.)],
        "function": stats.cauchy
    },
    "t": {
        "type": "continous",
        "parameters": [(1,), (2,), (5,), (sys.maxsize,)],
        "function": stats.t
    },
    "f": {
        "type": "continous",
        "parameters": [(1, 1), (2, 1), (5, 2), (10, 1), (200, 100)],
        "function": stats.f
    },
    "chi2": {
        "type": "continous",
        "parameters": [(1,), (2,), (3,), (4,), (6,), (9,)],
        "function": stats.chi2
    },
    "expon": {
        "type": "continous",
        "parameters": [(0.5,), (1.,), (1.5,)],
        "function": stats.expon
    },
    "weibull": {
        "type": "continous",
        "parameters": [(1., 0.5), (1., 1.), (1., 1.5), (1., 5.)],
        "function": stats.weibull_min
    },
    "lognorm": {
        "type": "continous",
        "parameters": [(0.1, 1.), (0.1, 0.25), (0.1, 0.5)],
        "function": stats.lognorm
    },
    "fatiguelife": {
        "type": "continous",
        "parameters": [(0.5,), (1.,), (2.,), (5.,), (10.,)],
        "function": stats.fatiguelife
    },
    "gamma": {
        "type": "continous",
        "parameters": [(1., 2.), (2., 2.), (3., 2.), (5., 1.), (9., 0.5), (7.5, 1.), (0.5, 1.)],
        "function": stats.gamma
    },
    "doubleexpon": {
        "type": "continous",
        "parameters": [(0., 1.), (0., 2.), (0., 4.), (-5., 4.)],
        "function": stats.laplace
    },
    "powernorm": {
        "type": "continous",
        "parameters": [(0.5,), (1.,), (1.5,), (2.,), (3.,), (8.,)],
        "function": stats.powernorm
    },
    "powerlognorm": {
        "type": "continous",
        "parameters": [(0.5, 1.),(1., 1.),(5., 1.),(10., 1.)],
        "function": stats.powerlognorm
    },
    "tukeylambda": {
        "type": "continous",
        "parameters": [(-1.,), (0.,), (1.,), (2.,)],
        "function": stats.tukeylambda
    },
    "extremetype1": {
        "type": "continous",
        "parameters": [(0.5, 2.), (1., 2.), (1.5, 3), (3., 4.)],
        "function": stats.gompertz
    },
    "beta": {
        "type": "continous",
        "parameters": [(0.5, 0.5), (5., 1.), (1., 3.), (2., 2.), (2., 5.)],
        "function": stats.beta
    },
    "binom": {
        "type": "discrete",
        "parameters": [(20, 0.5), (20, 0.7), (40, 0.5)],
        "function": stats.binom
    }, 
    "poisson": {
        "type": "discrete",
        "parameters": [(1.,), (5.,), (9.,)],
        "function": stats.poisson
    }
}