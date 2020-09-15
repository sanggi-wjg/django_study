from apps.third_party.fdr.finance_data import FinanceData


class FinanceDataList(FinanceData):
    _symbol_list = None

    def get_fd_data(self, symbol_list: list):
        """
        :param symbol_list: 주식코드들
        :return:
        """
        self._symbol_list = symbol_list
        for symbol in self._symbol_list:
            print(symbol)
