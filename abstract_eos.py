from abc import ABC, abstractmethod
from scipy.optimize import fsolve


class EOS(ABC):
    """
        Equation of state abstract class
        - __init__ should take EOS params
        - gas constant must be defined
        - eos function must be defined and set equal to 0
          ------------------------------------------------
          e.g.
            class MyEOS(EOS):
                def __init__(self, <<EOS-Dependent Variables>>):
                    <<Assign EOS variables here - to be used in self.eos>>

                @property
                def R(self):
                    return <<R value>>

                def eos(self, p, v, T):
                    return <<EOS function set equal to 0>>
          ------------------------------------------------
    """
    def __init__(self):
        self.__p = None
        self.__v = None
        self.__T = None

    @property
    @abstractmethod
    def R(self):
        """
            Define gas constant here
              - use appropriate units
        """
        pass

    @abstractmethod
    def eos(self, p, v, T):
        """
            Define EOS here
              - return value should equal 0
        """
        pass

    def get_state(self, T=None, p=None, v=None):
        """
            Returns a dict with defined props of state
        """
        pvT = [p, v, T]

        # ensure only two props are defined
        if sum(map(bool, pvT)) != 2:
            raise ValueError("Must define exactly two properties")
        else:

            # create state dict and convert props to floats
            try:
                state = {prop: 0 if not val else float(val)
                         for prop, val in zip(['p', 'v', 'T'], pvT)}
            except (TypeError, ValueError):
                raise ValueError("Properties given must be numbers")

            # set known props
            for prop in state:
                if state[prop] != 0:
                    setattr(self, '_EOS__%s' % prop, state[prop])
                else:
                    solve_for = prop

            # call method to solve for other prop
            state[solve_for] = getattr(self, '__get%s__' % solve_for)()

            # solve for compressibility, z
            state['z'] = (state['p'] * state['v']) / (self.R * state['T'])
            return state

    def __getp__(self):
        p_ideal = self.R * self.__T / self.__v
        p = fsolve(lambda p: self.eos(p, self.__v, self.__T), p_ideal)[0]
        return p

    def __getv__(self):
        v_ideal = self.R * self.__T / self.__p
        v = fsolve(lambda v: self.eos(self.__p, v, self.__T), v_ideal)[0]
        return v

    def __getT__(self):
        T_ideal = self.__p * self.__v / self.R
        T = fsolve(lambda T: self.eos(self.__p, self.__v, T), T_ideal)[0]
        return T
