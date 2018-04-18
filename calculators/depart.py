from __future__ import absolute_import
from peng import PengRobinsonEOS
import numpy as np


class Departure(PengRobinsonEOS):
    def __init__(self, pc, Tc, omega):
        # Initialize molar properties
        super(Departure, self).__init__(pc, Tc, omega)

        # List of methods to calculate individual departure functions
        self.methods = [i for i in dir(self) if i.startswith('calc_')]

    def check_peng(self, p, T):
        # Check if state has changed and if so, recalculate PR EOS properties
        try:
            if (self.p == p) and (self.T == T):
                return
            else:
                raise KeyError()
        except:
            self.calc_v(p, T)

    def calc_S(self, p, T):
        # Calculate entropy residual
        self.check_peng(p, T)
        B = self.b
        return 1

    def calc_H(self, p, T):
        # Calculate entropy residual
        self.check_peng(p, T)
        return 1

    def calc_V(self, p, T):
        # Calculate entropy residual
        self.check_peng(p, T)
        return 1

    def calc_A(self, p, T):
        # Calculate entropy residual
        self.check_peng(p, T)
        return 1

    def calc_U(self, p, T):
        # Calculate entropy residual
        self.check_peng(p, T)
        return 1

    def calc_G(self, p, T):
        # Calculate entropy residual
        self.check_peng(p, T)
        return 1

    def get_all(self, p, T):
        # Make dictionary of all potential residuals
        self.check_peng(p, T)
        sol = {}
        for m in self.methods:
            sol[m[-1]] = getattr(self, m)(p, T)
        return sol

if __name__ == '__main__':
    # Ammonia (NH_3) props
    pc = 113.53  # bar
    Tc = 405.4   # K
    omega = 0.257

    # standard pressure and temperature
    p = 1.01325  # bar
    T = 273.15   # K

    me_sleepy = Departure({'pc': pc, 'Tc': Tc, 'omega': omega})
    x = me_sleepy.get_all(p, T)
