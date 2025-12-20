import logging
from abc import ABC, abstractmethod
from typing import List
from models import Product, CartItem

LOGGER = logging.getLogger('SERVICES')

class IPaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CashPayment(IPaymentProcessor):
    def process(self, amount: float) -> bool:
        LOGGER.info(f"Menerima TUNAI sejumlah: Rp{amount:,.0f}")
        return True

class ShoppingCart:
    """Mengelola item, kuantitas, dan total harga pesanan (SRP)."""
    
    def __init__(self):
        self._items: dict[str, CartItem] = {}

    def add_item(self, product: Product, quantity: int = 1):
        if product.id in self._items:
            self._items[product.id].quantity += quantity
        else:
            self._items[product.id] = CartItem(product=product, quantity=quantity)
        LOGGER.info(f"Added {quantity}x {product.name} to cart.")

    def get_items(self) -> List[CartItem]:
        return list(self._items.values())

    @property
    def total_price(self) -> float:
        return sum(item.subtotal for item in self._items.values())
    
# Challenge 13

class DebitCardPayment(IPaymentProcessor):
    """Implementasi pembayaran menggunakan Kartu Debit."""
    
    def process(self, amount: float) -> bool:
        print("--- Memproses Kartu Debit ---")
        card_number = input("Masukkan Nomor Kartu: ")
        LOGGER.info(f"Otorisasi kartu {card_number} berhasil.")
        LOGGER.info(f"Saldo didebit sejumlah: Rp{amount:,.0f}")
        return True