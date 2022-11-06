from __future__ import annotations
import math

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

class Fixed:
    term: int
    interest: float
    entry: float
    hold: float
    final: float

    length: int
    padding: int

    def __init__(self, term: int, interest: float, entry: float, hold: float, final: float = 0., length: int = 0):
        self.term = term
        self.interest = interest
        self.entry = entry
        self.hold = hold
        self.final = final

        self.length = length
        self.padding = max(0, length - self.term)

    def flow(self, capital: float) -> [float]:
        flow_ = [-capital * self.entry]

        for period in range(0, self.term):
            flow_.append(capital * (self.interest - self.hold))

        flow_[-1] += capital * self.final

        flow_.extend(self.padding * [0])

        return flow_

    def get_length(self):
        return self.length

    def accumulate(self, instruments: [Fixed], capitals: [float]):
        for instrument in instruments


certificate = Fixed(5, 0, 0.015, 0.0012, 0.05, 5)
deutsche_bank_3 = Fixed(3, 0.025, 0.0025, 0.0012, 0, 5)
deutsche_bank_1 = Fixed(1, 0.0115, 0.0025, 0.0012, 0, 5)

#print(sum([certificate.flow(160_000), deutsche_bank_1.flow(355_000), deutsche_bank_3.flow(185_000)]))


print(certificate.flow(160_000))
print(deutsche_bank_3.flow(355_000))
print(deutsche_bank_1.flow(185_000))

print(185_000 * 0.0115)

