import logging
from repositories import ProductRepository
# Challenge 13
from services import IPaymentProcessor, ShoppingCart, CashPayment, DebitCardPayment
from models import Product

LOGGER = logging.getLogger('MAIN_APP')

class PosApp:
    """Kelas Orchestrator (Aplikasi Utama). Hanya mengkoordinasi flow dan menerapkan DI."""
    
    def __init__(self, repository: ProductRepository, payment_processor: IPaymentProcessor):
        self.repository = repository
        self.payment_processor = payment_processor
        self.cart = ShoppingCart()
        LOGGER.info("POS Application Initialized.")

    def _display_menu(self):
        LOGGER.info("\n--- DAFTAR PRODUK ---")
        for p in self.repository.get_all():
            LOGGER.info(f"[{p.id}] {p.name} - Rp{p.price:,.0f}")

    def _handle_add_item(self):
        product_id = input("Masukkan ID Produk: ").strip().upper()
        product = self.repository.get_by_id(product_id)
        if not product:
            LOGGER.warning("Produk tidak ditemukan.")
            return
        
        try:
            qty_input = input("Jumlah (default 1): ")
            quantity = int(qty_input) if qty_input else 1
            if quantity <= 0: raise ValueError
            self.cart.add_item(product, quantity)
        except ValueError:
            LOGGER.error("Jumlah tidak valid.")

    def _handle_checkout(self):
        total = self.cart.total_price
        if total == 0:
            LOGGER.warning("Keranjang kosong.")
            return
            
        LOGGER.info(f"\nTotal Belanja: Rp{total:,.0f}")
        success = self.payment_processor.process(total)
        if success:
            LOGGER.info("TRANSAKSI BERHASIL.")
            self._print_receipt()
            self.cart = ShoppingCart()
        else:
            LOGGER.error("TRANSAKSI GAGAL.")

    def _print_receipt(self):
        LOGGER.info("\n--- STRUK PEMBELIAN ---")
        for item in self.cart.get_items():
            LOGGER.info(f"{item.product.name} x{item.quantity} - Rp{item.subtotal:,.0f}")
        LOGGER.info("-" * 20)
        LOGGER.info(f"TOTAL AKHIR: Rp{self.cart.total_price:,.0f}")
        LOGGER.info("-" * 20)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    
    repo = ProductRepository()
    
    # Challenge 13
    payment_method = DebitCardPayment()
    
    app = PosApp(repository=repo, payment_processor=payment_method)
    
    while True:
        print("\nMenu:")
        print("1. Tampilkan Produk")
        print("2. Tambah ke Keranjang")
        print("3. Checkout")
        print("4. Keluar")
        
        choice = input("Pilih opsi (1-4): ")
        
        if choice == "1":
            app._display_menu()
        elif choice == "2":
            app._handle_add_item()
        elif choice == "3":
            app._handle_checkout()
        elif choice == "4":
            LOGGER.info("Aplikasi dihentikan.")
            break
        else:
            LOGGER.warning("Pilihan tidak valid.")