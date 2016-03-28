class MalformedTransactionException(Exception):
    def __init__(self):
        message = "Malformed transaction data"
        super(MalformedTransactionException, self).__init__(message)


class InsufficientDataInTransactionException(Exception):
    def __init__(self):
        message = "There is not enough data in the transaction for the " \
                  "algorithm to classify it"
        super(InsufficientDataInTransactionException, self).__init__(message)


class EmptyQueueException(Exception):
    def __init__(self):
        message = "The Transaction queue is empty"
        super(EmptyQueueException, self).__init__(message)

class EnviromentVariablesNotSet(Exception):
    def __init__(self):
        message = "The necessary enviroment variables are not set"
        super(EnviromentVariablesNotSet, self).__init__(message)