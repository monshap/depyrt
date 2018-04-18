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

    def calc_v(self, p, T, root='vapor'):
        """ c1 * v^3 + c2 * v^2 + c3 * v + c4 = 0 """
        # if Tc is set to 0, EOS behaves as Ideal Gas
        if self.Tc == 0:
            a = b = alpha = dadT = 0
        else:
            a = 0.45724 * (self.R * self.Tc)**2 / self.pc
            b = 0.07780 * self.R * self.Tc / self.pc
            Tr = T / self.Tc
            alpha = (1 + self.kappa * (1 - np.sqrt(Tr)))**2
<<<<<<< HEAD
            dadT = -0.45724 * (self.R**2 * self.Tc**2) * self.kappa / self.pc \
                * np.sqrt(alpha / (T * self.Tc))
=======
            dadT = (-a * self.kappa) * np.sqrt(alpha / (T * self.Tc))
>>>>>>> dev/eos

        # set p, T, a, b, and alpha attributes
        self.p = p
        self.T = T
        self.a = a
        self.b = b
        self.alpha = alpha
        self.dadT = dadT
        self.root = root

        c1 = p
        c2 = p * b - self.R * T
        c3 = a * alpha - 3 * p * b**2 - 2 * self.R * T * b
        c4 = p * b**3 - a * alpha * b + self.R * T * b**2
        roots = np.roots([c1, c2, c3, c4])

        # filter negative and complex numbers
        vs = []
        for val in roots:
            if val <= 0:
                continue
            elif isinstance(val, complex):
                if val.imag:
                    continue
                else:
                    val = val.real
            vs.append(val)

        # return appropriate root depending on phase
        if not root:
            return vs
        else:
            self.v = max(vs) if root.lower() in 'vapor' else min(vs)
            self.z = p * self.v / (self.R * T)
            return self.v

if __name__ == '__main__':
    # Ammonia (NH_3) props
    pc = 113.53  # bar
    Tc = 405.4   # K
    omega = 0.257

    # standard pressure and temperature
    p = 1.01325  # bar
    T = 273.15   # K

    peng = PengRobinsonEOS(pc, Tc, omega)

    # calculates volume in L
    vol = peng.calc_v(p, T, 'vapor')
