import numpy as np


class PengRobinsonEOS():
    """
        p = [RT / (v - b)] - [a * alpha / (v^2 + 2bv - b^2)]
    """
    name = 'Peng Robinson EOS'
    # set default R value (L bar / K mol)
    R = 8.314E-2

    def __init__(self, pc, Tc, omega, R=None):
        if R:
            self.R = float(R)

        self.pc = pc
        self.Tc = Tc
        self.kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2

    def solve_v(self, p, T, root='liquid'):
        """ c1 * v^3 + c2 * v^2 + c3 * v + c4 = 0 """
        a = 0.45724 * (self.R * self.Tc)**2 / self.pc
        b = 0.07780 * self.R * self.Tc / self.pc
        Tr = T / self.Tc
        alpha = (1 + self.kappa * (1 - np.sqrt(Tr)))**2

        c1 = p
        c2 = p * b - self.R * T
        c3 = a * alpha - 3 * p * b**2 - 2 * self.R * T * b
        c4 = p * b**3 - a * alpha * b + self.R * T * b**2
        vs = np.roots([c1, c2, c3, c4])
        vs = [i for i in vs if i > 0]

        # return appropriate root depending on phase
        return min(vs) if root.lower() in 'liquid' else max(vs)

if __name__ == '__main__':
    # Ammonia (NH_3) props
    pc = 113.53  # bar
    Tc = 405.4  # K
    omega = 0.257

    # standart pressure and temperature
    p = 1.01325
    T = 273.15

    peng = PengRobinsonEOS(pc, Tc, omega)
    x = peng.solve_v(p, T)
