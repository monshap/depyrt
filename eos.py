from abstract_eos import EOS
import numpy as np


class IdealGasEOS(EOS):
    @property
    def R(self):
        """L bar / K mol"""
        return 8.314E-2

    def eos(self, p, v, T):
        return p * v - self.R * T


class PengRobinsonEOS(EOS):
    """
        p = [RT / (v - b)] - [a * alpha / (v^2 + 2bv - b^2)]
    """
    def __init__(self, Tc, pc, omega):
        self.Tc = Tc
        self.a = 0.45724 * (self.R * Tc)**2 / pc
        self.b = 0.07780 * self.R * Tc / pc
        self.kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2

    @property
    def R(self):
        """L bar / K mol"""
        return 8.314E-2

    def eos(self, p, v, T):
        Tr = T / self.Tc
        alpha = (1 + self.kappa * (1 - np.sqrt(Tr)))**2
        term1 = self.R * T / (v - self.b)
        term2 = self.a * alpha / (v**2 + 2 * self.b * v - self.b**2)
        return p - term1 + term2

if __name__ == '__main__':
    # Ammonia (NH_3) props
    Tc = 405.4  # K
    pc = 113.53  # bar
    omega = 0.257

    # standart pressure and temperature
    p = 1.01325
    T = 273.15

    # initialize ideal and real gas objects
    nh3_ideal = IdealGasEOS()
    nh3_real = PengRobinsonEOS(Tc, pc, omega)

    stp_real = nh3_real.get_state(p=p, T=T)
    stp_ideal = nh3_ideal.get_state(p=p, T=T)

    print('at STP:\nReal State:')
    print(stp_real)
    print('Ideal State:')
    print(stp_ideal)
