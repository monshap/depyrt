from __future__ import absolute_import
import numpy as np
if __name__ == '__main__':
    from peng import PengRobinsonEOS
else:
    from .peng import PengRobinsonEOS


class Departure(PengRobinsonEOS):
    def __init__(self, pc, Tc, omega):
        # Initialize molar properties
        super(Departure, self).__init__(pc, Tc, omega)

        # List of methods to calculate individual departure functions
        self.methods = [i for i in dir(self) if i.startswith('calc_') and
                        i != 'calc_v']

    def check_peng(self, p, T, root='vapor'):
        # Check if state has changed and if so, recalculate PR EOS properties
        try:
            if (self.p == p) and (self.T == T) and (self.root == root):
                return
            else:
                raise KeyError()
        except:
            self.calc_v(p, T, root)

    def prereq(self, potentials, *args):
        for J in potentials:
            try:
                exec('return self.d%s' % (J))
            except:
                exec('self.calc_%s(*args)' % (J))

    def calc_S(self, p, T, root='vapor'):
        """Calculate entropy residual:\n
        dS' = -R ln(Z - B) - [(da/dT) / (2^(3/2) b)] * ln[J],\n
        J = (Z + (1 + sqrt(2)) B) / (Z + (1 - sqrt(2)) B)"""

        # Check if state changed
        self.check_peng(p, T, root)

        # Calculate residual
        B = self.p * self.b / (self.R * self.T)
        f2 = (self.z + (1 + np.sqrt(2)) * B) / (self.z + (1 - np.sqrt(2)) * B)
        s1 = self.R * np.log(self.z - B)
        s2 = self.dadT * np.log(f2) / (2**(3/2) * self.b)
        ds = (-s1 - s2) * 1e2  # J/mol*K
        self.dS = ds
        return ds

    def calc_H(self, p, T, root='vapor'):
        """Calculate enthalpy residual:\n
        dH' = RT(1 - Z) +\n
        \t[(a - T(da/dT)) / (2^(3/2) * b)] * ln[J],\n
        J = (Z + (1 + sqrt(2)) * B) / (Z + (1 - sqrt(2)) * B)"""

        # Check if state changed
        self.check_peng(p, T, root)

        # Calculate residual
        B = self.p * self.b / (self.R * self.T)
        f2 = (self.z + (1 + np.sqrt(2)) * B) / (self.z + (1 - np.sqrt(2)) * B)
        h1 = self.R * self.T * (1 - self.z)
        c2 = (self.a * self.alpha - self.T * self.dadT) / (2**(3/2.) * self.b)
        h2 = c2 * np.log(f2)
        dh = (h1 + h2) * 1e2  # J/mol*K
        self.dH = dh
        return dh

    def calc_V(self, p, T, root='vapor'):
        """Calculate volume residual:\n
        dV' = V_{ig} - V"""

        # Check if state changed
        self.check_peng(p, T, root)

        # Calculate residual
        v_id = self.R * self.T / self.p
        v = self.v
        dv = v_id - v
        self.dV = dv
        return dv

    def calc_A(self, p, T, root='vapor'):
        """Calculate Helmholtz free engergy residual:\n
        dA' = dU' - TdS'"""

        # Check if state changed
        self.check_peng(p, T, root)
        self.prereq(['U', 'S'], p, T, root)

        # Calculate residual
        da = self.dU - self.T * self.dS
        self.dA = da
        return da

    def calc_U(self, p, T, root='vapor'):
        """Calculate interntal energy residual:\n
        dU' = dH' - pdV'"""

        # Check if state changed
        self.check_peng(p, T, root)
        self.prereq(['H', 'V'], p, T, root)

        # Calculate residual
        du = self.dH - self.p * self.dV
        self.dU = du
        return du

    def calc_G(self, p, T, root='vapor'):
        """Calculate Gibbs free energy residual:\n
        dG' = dH' - TdS'"""

        # Check if state changed
        self.check_peng(p, T, root)
        self.prereq(['H', 'S'], p, T, root)

        # Calculate residual
        dg = self.dH - self.T * self.dS
        self.dG = dg
        return dg

    def get_all(self, p, T, root='vapor'):
        # Make dictionary of all potential residuals
        self.check_peng(p, T, root)
        sol = {}
        for m in self.methods:
            sol[m[-1]] = getattr(self, m)(p, T, root)
        return sol

if __name__ == '__main__':
    # Ammonia (NH_3) props
    pc = 113.53  # bar
    Tc = 405.4   # K
    omega = 0.257

    # standard pressure and temperature
    p = 1.01325  # bar
    T = 273.15   # K

    me_sleepy = Departure(pc, Tc, omega)
    x = me_sleepy.get_all(0.06, 200, 'liquid')
    x2 = me_sleepy.get_all(2.09, 450)

    id_diff = {'U': 7024,
               'H': 9102,
               'A': -43507,
               'G': -41429,
               'S': -0.336,
               'V': 0}

    diff = {i: x[i] - x2[i] for i in x}
    diff_real = {j: diff[j] + id_diff[j] for j in diff}
    print('\nDeparture Differences')
    for d in diff:
        print('%s: %.3f' % (d, diff[d]))
    print('\n\nReal Differences')
    for d in diff_real:
        print('%s: %.3f' % (d, diff_real[d]))
