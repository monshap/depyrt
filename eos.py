from abstract_eos import EOS
import numpy as np

"""Default R value for all EOS classes: 8.314E-2 L bar / K mol"""


class IdealGasEOS(EOS):
    """
        pv = RT
    """
    name = 'Ideal Gas EOS'

    def __init__(self, R=None):
        if R:
            self.R = float(R)

    def eos(self, p, v, T):
        return p * v - self.R * T


class PengRobinsonEOS(EOS):
    """
        0 = p - [RT / (v - b)] - [a * alpha / (v^2 + 2bv - b^2)]
    """
    name = 'Peng Robinson EOS'

    def __init__(self, pc, Tc, omega, R=None):
        if R:
            self.R = float(R)

        self.pc = pc
        self.Tc = Tc
        self.kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2

    def eos(self, p, v, T):
        a = 0.45724 * (self.R * self.Tc)**2 / self.pc
        b = 0.07780 * self.R * self.Tc / self.pc
        Tr = T / self.Tc
        alpha = (1 + self.kappa * (1 - np.sqrt(Tr)))**2
        term1 = self.R * T / (v - b)
        term2 = a * alpha / (v**2 + 2 * b * v - b**2)
        return p - term1 + term2


class RedlichKwongEOS(EOS):
    """
        0 = p - [RT / (v - b)] + [a / (sqrt(T) v (v + b))]
    """
    name = 'Redlich Kwong EOS'

    def __init__(self, pc, Tc, R=None):
        if R:
            self.R = float(R)

        self.pc = pc
        self.Tc = Tc

    def eos(self, p, v, T):
        a = (0.42748 * self.R**2 * self.Tc**(5/2.)) / self.pc
        b = (0.08664 * self.R * self.Tc) / self.pc
        term1 = self.R * T / (v - b)
        term2 = a / (np.sqrt(T) * v * (v + b))
        return p - term1 + term2


class VanDerWaalsEOS(EOS):
    """
        (p + a / v^2)(v - b) = RT
    """
    name = 'Van der Waals EOS'

    def __init__(self, pc, Tc, R=None):
        if R:
            self.R = float(R)

        self.pc = float(pc)
        self.Tc = float(Tc)

    def eos(self, p, v, T):
        a = 27 * (self.R * self.Tc)**2 / (64 * self.pc)
        b = self.R * self.Tc / (8 * self.pc)
        return ((p + (a / v**2)) * (v - b)) - self.R * T


if __name__ == '__main__':
    # Ammonia (NH_3) props
    pc = 113.53  # bar
    Tc = 405.4  # K
    omega = 0.257

    # standart pressure and temperature
    p = 1.01325
    T = 273.15

    # initialize gas EOS objects
    nh3_ideal = IdealGasEOS()
    nh3_peng = PengRobinsonEOS(pc, Tc, omega)
    nh3_red = RedlichKwongEOS(pc, Tc)
    nh3_vdw = VanDerWaalsEOS(pc, Tc)

    # state dict is returned
    stp_ideal = nh3_ideal.get_state(p=p, T=T)
    stp_peng = nh3_peng.get_state(p=p, T=T)
    stp_red = nh3_red.get_state(p=p, T=T)
    stp_vdw = nh3_vdw.get_state(p=p, T=T)

    # last calculated state dict is also set as atttribute
    [print(e.state) for e in [nh3_ideal, nh3_peng, nh3_red, nh3_vdw]]
