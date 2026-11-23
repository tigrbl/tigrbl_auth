"""DNS zone transaction configuration and limits."""


class TooManyChanges(ValueError):
    """The zone transaction reached its configured change limit."""


class TransactionLimiter:
    """Count dataset writes, dataset deletions, and whole-name deletions."""

    def __init__(self, limit: int):
        self.limit = limit
        self.changes = 0

    def __call__(self, txn):
        txn.check_put_rdataset(self._count)
        txn.check_delete_rdataset(self._count)
        txn.check_delete_name(self._count)

    def _count(self, txn, name, *details):
        self.changes += 1
        if self.changes >= self.limit:
            raise TooManyChanges(f"limit is {self.limit} changes")
