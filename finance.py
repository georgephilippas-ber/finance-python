from __future__ import annotations

import pandas as pd


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

    def get_name(self):
        return self.name

    def get_identifier(self):
        return self.identifier

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

    def initial(self):
        return Fixed.accumulate_flow(self.instruments, self.capitals)[0]

    def to_df(self) -> pd.DataFrame:
        dataframe_ = pd.DataFrame(
            ([instrument.get_identifier(), instrument.get_name(), capital, *instrument.flow(capital)] for
             instrument, capital in
             zip(self.instruments, self.capitals)))

        return dataframe_.append([["", "Gesamtmenge", self.total_capital(), *self.flow()]]).set_index(0)
