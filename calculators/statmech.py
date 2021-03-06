import math
from operator import mul
from functools import reduce

""" CONSTANTS """
# pi
pi = math.pi

# e
e = math.e

# e^()
exp = math.exp

# ln()
ln = math.log

# avogadro's number (# / mol)
Na = 6.022E23

# boltzmann constant (m^2 kg / s^2 K) || (J / K)
kb = 1.38065E-23

# planck's constant (m^2 kg / s)
h = 6.6261E-34
h_bar = h / (2 * pi)

# molecular data required to calc thermodynamic properties
props_needed = ['theta_v', 'theta_r', 'sigma', 'W0', 'D0', 'Mw', 'type']

""" Ammonia (NH3) Properties """
# characteristic vibrational temperatures
theta_v = [1360, 4800, 4880, 4880, 2330, 2330]

# characteristic rotational temperatures
theta_r = [13.6, 13.6, 8.92]

# symmetry constant
sigma = 3

# electronic ground state degeneracy
W0 = 1

# dissociation energy (J / mol)
D0 = 276.8 * 4186.8

# molecular weight (g / mol)
Mw = 17.

# summary dict
ammonia = {'theta_v': theta_v,
           'theta_r': theta_r,
           'sigma': sigma,
           'W0': W0,
           'D0': D0,
           'Mw': Mw,
           'type': 'nonlinear'
           }


def statmech_calculator(props_dict):
    """General function to create a property calculator for a molecule"""
    # use BaseProps to ensure all keys are present in dict
    b = BaseProps(props_dict)
    typ = props_dict['type'].lower()
    if typ == 'linear':
        return LinearProps(props_dict)
    elif typ == 'nonlinear':
        return NonlinearProps(props_dict)
    else:
        raise ValueError('Invalid molecule type')


class BaseProps(object):
    def __init__(self, props_dict):
        # ensure all required molecular properties are passed in
        missing = ', '.join([i for i in props_needed if i not in props_dict])
        if missing:
            raise KeyError("Missing %s from molecular properties!" % missing)

        for k in props_dict:
            if k != 'type':
                if isinstance(props_dict[k], list):
                    props_dict[k] = list(map(float, props_dict[k]))
                else:
                    props_dict[k] = float(props_dict[k])
        # create props attribute
        self.props = props_dict

        # calc Mw (kg / molecule) and D0 (J / molecule)
        self.props['Mwm'] = self.props['Mw'] / (1000. * Na)
        self.props['D0m'] = self.props['D0'] / Na

        # create specific attributes for each value
        for p in self.props:
            setattr(self, p, self.props[p])

        self.methods = [i for i in dir(self) if i.startswith('get_')]

    def get_A(self, T, V):
        """Returns Helmholtz Free Energy"""
        return 1

    def get_U(self, T, *args):
        """Returns Internal Energy"""
        return 1

    def get_Cv(self, T, *args):
        """Returns Constant V Heat Capacity"""
        return 1

    def get_S(self, T, V):
        """Returns Entropy"""
        return 1

    def get_H(self, T, *args):
        """Returns Enthalpy"""
        return self.get_U(T, *args) + Na * kb * float(T)

    def get_G(self, T, V):
        """Returns Gibbs Free Energy"""
        return self.get_A(T, V) + Na * kb * float(T)

    def get_Cp(self, T, *args):
        """Returns Constant p Heat Capacity"""
        return self.get_Cv(T) + Na * kb

    def calc_all(self, T, V):
        """Returns dictionary of all thermodynmic properties"""
        sol = {m.split('_')[-1]: getattr(self, m)(T, V)
               for m in self.methods}
        sol['type'] = self.type
        return sol


class LinearProps(BaseProps):
    def __init__(self, props_dict):
        super(LinearProps, self).__init__(props_dict)
        if isinstance(self.props['theta_r'], list):
            self.props['theta_r'] = float(self.props['theta_r'][0])
            self.theta_r = float(self.theta_r[0])

    def get_A(self, T, V):
        T, V = list(map(float, [T, V]))
        kbT = kb * T

        term1 = ln((2 * pi * self.Mwm * kbT / h**2)**(1.5) * (V * e / Na))
        term2 = ln(T / (self.sigma * self.theta_r))
        term3 = self.D0m / kbT
        term4 = ln(self.W0)
        term5 = -sum([ln(1 - exp(-vj / T))
                      for vj in self.theta_v])

        return -sum([term1, term2, term3, term4, term5]) * Na * kbT

    def get_U(self, T, *args):
        T = float(T)

        term1 = 1.5
        term2 = 1.
        term3 = -self.D0m / (kb * T)
        term4 = sum([(vj / T) / (exp(vj / T) - 1)
                     for vj in self.theta_v])

        return sum([term1, term2, term3, term4]) * Na * kb * T

    def get_Cv(self, T, *args):
        T = float(T)

        term1 = 1.5
        term2 = 1.
        term3 = sum([(vj / T)**2 * (exp(vj / T) / (exp(vj / T) - 1)**2)
                     for vj in self.theta_v])

        return sum([term1, term2, term3]) * Na * kb

    def get_S(self, T, V):
        T, V = list(map(float, [T, V]))

        term1 = ln(((2 * pi * self.Mwm * kb * T) / h**2)**(1.5) *
                   (V * exp(2.5) / Na)
                   )
        term2 = ln(T * e / (self.sigma * self.theta_r))
        term3 = ln(self.W0)
        term4 = sum([((vj / T) / ((exp(vj / T) - 1))) - ln(1 - exp(-vj / T))
                     for vj in self.theta_v])

        return sum([term1, term2, term3, term4]) * Na * kb


class NonlinearProps(BaseProps):
    def __init__(self, props_dict):
        super(NonlinearProps, self).__init__(props_dict)
        if not isinstance(props_dict['theta_v'], list):
            props_dict['theta_v'] = [props_dict['theta_v']]

        # product of rotational temperatures
        self.theta_r3 = reduce(mul, self.theta_r)

    def get_A(self, T, V):
        T, V = list(map(float, [T, V]))
        kbT = kb * T

        term1 = ln((2 * pi * self.Mwm * kbT / h**2)**(1.5) * (V * e / Na))
        term2 = ln((1 / self.sigma) * ((pi * T**3 / self.theta_r3)**0.5))
        term3 = self.D0m / kbT
        term4 = ln(self.W0)
        term5 = -sum([ln(1 - exp(-vj / T))
                      for vj in self.theta_v])

        return -sum([term1, term2, term3, term4, term5]) * Na * kbT

    def get_U(self, T, *args):
        T = float(T)

        term1 = 1.5
        term2 = 1.5
        term3 = - self.D0m / (kb * T)
        term4 = sum([(vj / T) / (exp(vj / T) - 1)
                     for vj in self.theta_v])

        return sum([term1, term2, term3, term4]) * Na * kb * T

    def get_Cv(self, T, *args):
        T = float(T)

        term1 = 1.5
        term2 = 1.5
        term3 = sum([(vj / T)**2 * (exp(vj / T) / (exp(vj / T) - 1)**2)
                     for vj in self.theta_v])

        return sum([term1, term2, term3]) * Na * kb

    def get_S(self, T, V):
        T, V = list(map(float, [T, V]))

        term1 = ln((2 * pi * self.Mwm * kb * T / h**2)**(1.5) *
                   (V * exp(2.5) / Na)
                   )
        term2 = ln((1 / self.sigma) * (pi * T**3 * e**3 / self.theta_r3)**0.5)
        term3 = ln(self.W0)
        term4 = sum([((vj / T) / (exp(vj / T) - 1)) - ln(1 - exp(-vj / T))
                     for vj in self.theta_v])

        return sum([term1, term2, term3, term4]) * Na * kb

if __name__ == '__main__':
    t1 = 200.
    p1 = 0.06
    v1 = 8.314 * t1 / (p1 * 1E5)

    t2 = 450.
    p2 = 2.09
    v2 = 8.314 * t2 / (p2 * 1E5)
    b = statmech_calculator(ammonia)
    sol = b.calc_all(t1, v1)
    sol2 = b.calc_all(t2, v2)
