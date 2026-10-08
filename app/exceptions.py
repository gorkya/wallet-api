class WalletNotFoundError(Exception):
    """Кошелёк с указанным UUID не существует."""


class InsufficientFundsError(Exception):
    """На кошельке недостаточно средств для списания."""
