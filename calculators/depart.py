from __future__ import absolute_import
from peng import PengRobinsonEOS


class Departure(object):
    def __init__(self, mol_props):
        self.pc = mol_props['pc']
        self.Tc = mol_props['Tc']
        self.omega = mol_props['omega']
        self.peng = PengRobinsonEOS(self.pc, self.Tc, self.omega)
        self.R = self.peng.R

        self.methods = [i for i in dir(self) if i.startswith('calc_')]

    def check_peng(self, p, T):
        try:
            if (self.peng.p == p) and (self.peng.T == T):
                return
            else:
                raise KeyError()
        except:
            self.peng.calc_v(p, T)

    def calc_S(self, p, T):
        self.check_peng(p, T)  # Add to all methods
        return 1

    def calc_H(self, p, T):
        return 1

    def calc_V(self, p, T):
        return 1

    def calc_A(self, p, T):
        return 1

    def calc_U(self, p, T):
        return 1

    def calc_G(self, p, T):
        return 1

    def get_all(self, p, T):
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
