from apps.third_party.fdr.finance_data_image import FinanceDataImage


class FinanceDataImageStockList(FinanceDataImage):
    save_path = ['finance', 'sector']
