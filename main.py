from __future__ import annotations


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

securities = [
    {
        "characteristics":
            {
                "name": "",
                "identifier": "",
                "term": 1,
                "interest": 1.15 / 100.,
                "entry": 0.25 / 100.,
                "hold": 0.12 / 100,
                "final": 0,
            },
        "capital": 185_000
    },
    {
        "characteristics":
            {
                "name": "",
                "identifier": "",
                "term": 3,
                "interest": 2.5 / 100.,
                "entry": 0.55 / 100.,
                "hold": 0.12 / 100,
                "final": 0,
            },
        "capital": 355_000
    },
    {
        "characteristics":
            {
                "name": "",
                "identifier": "",
                "term": 5,
                "interest": 0 / 100.,
                "entry": 1.5 / 100.,
                "hold": 0.12 / 100,
                "final": 5 / 100,
            },
        "capital": 160_000
    }
]


class Portfolio:
    instruments: [Fixed]
    capitals: [float]

    def __init__(self, instruments: [Fixed], capitals: [float]):
        self.instruments = instruments
        self.capitals = capitals

    @staticmethod
    def from_object(object_array: [dict], years: int) -> Portfolio:
        instruments = [Fixed(**instrument["characteristics"], length=years) for instrument in object_array]
        capitals = [instrument["capital"] for instrument in object_array]

        return Portfolio(instruments, capitals)

    def flow(self):
        return Fixed.accumulate_flow(self.instruments, self.capitals)

    def total(self):
        return Fixed.accumulate_total(self.instruments, self.capitals)

    def total_capital(self):
        return sum(self.capitals)

class Fixed:
    name: str
    identifier: str
    term: int
    interest: float
    entry: float
    hold: float
    final: float

    length: int
    padding: int

    def __init__(self, name: str, identifier: str, term: int, interest: float, entry: float, hold: float,
                 final: float = 0., length: int = 0):
        self.name = name
        self.identifier = identifier

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

    def total(self, capital: float) -> float:
        return sum(self.flow(capital))

    def get_length(self):
        return self.length

    def full_name(self):
        return self.name + " " + self.identifier

    @staticmethod
    def accumulate_flow(instruments: [Fixed], capitals: [float]):
        flow_array = [instrument.flow(capital) for [instrument, capital] in zip(instruments, capitals)]

        accumulate = []
        for period in range(0, len(flow_array[0])):
            accumulate.append(sum([row[period] for row in flow_array]))

        return accumulate

    @staticmethod
    def accumulate_total(instruments: [Fixed], capitals: [float]):
        return sum(Fixed.accumulate_flow(instruments, capitals))


portfolio = Portfolio.from_object(securities, 5)

print(portfolio.total_capital())
print(portfolio.flow())
print(portfolio.total())
