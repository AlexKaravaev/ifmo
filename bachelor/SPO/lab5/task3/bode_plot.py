import numpy as np
from scipy import signal as s
from matplotlib import pyplot as plt


class plotter:
    # coeffs numerator and denumerator of transfer function
    def __init__(self, num, denum):
        self.num = num
        self.denum = denum
        self.plot()

    def plot(self):

        # magnitude plot
        func = plt.figure()
        signal = s.lti(self.num, self.denum)
        w, magnitude, phase = s.bode(signal, np.arange(0.1, 5, 0.01).tolist())
        plt.semilogx(w, magnitude, color="blue", linewidth="1")
        plt.title("АЧХ")
        plt.xlabel("Frequency")
        plt.ylabel("Magnitude")
        plt.savefig('mag.png',dpi=300,format='png')

        # amplitude plot
        plt.figure()
        signal = s.lti(self.num, self.denum)
        w, magnitude, phase = s.bode(signal, np.arange(0.1, 10, 0.01).tolist())
        plt.semilogx(w, phase, color="red", linewidth="1")
        plt.title("ФЧХ")
        plt.xlabel("Frequency")
        plt.ylabel("Amplitude")
        plt.savefig("phase.png", dpi=300, format='png')

if __name__ == '__main__':
    #coeffs of W(S)
    p = plotter([1], [1/(4000*3.1415), 1])
