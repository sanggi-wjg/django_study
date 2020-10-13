import sys
import traceback

from apps.third_party.util.colorful import print_red


def print_exception():
    exc_type, exc_value, exc_tb = sys.exc_info()

    print_red("(TYPE) : {}\n (LINE) : {}\n (MSG) : {}\n (FILE) : {}\n (METHOD) : {}\n{}".format(
        exc_type.__name__, exc_tb.tb_lineno, exc_value, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_frame.f_code.co_name, traceback.format_exc())
    )
    # print_red("{}\n{}".format({
    #     'type'       : exc_type.__name__,
    #     'line_no'    : exc_tb.tb_lineno,
    #     'message'    : str(exc_value),
    #     'file_name'  : exc_tb.tb_frame.f_code.co_filename,
    #     'method_name': exc_tb.tb_frame.f_code.co_name,
    # }, traceback.format_exc()))


class HttpException(Exception):
    pass


class AlertError(HttpException):
    pass


class DBError(Exception):
    pass


class TransactionError(DBError):
    pass


class DBSelectNone(DBError):
    pass


class DBInsertError(DBError):
    pass


class DBUpdateError(DBError):
    pass


class DBDeleteError(DBError):
    pass
