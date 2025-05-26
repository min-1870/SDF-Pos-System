# transactions/management/commands/populate_transactions.py

import random
import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from groups.models import Group
from products.models import Product
from transactions.models import (
    Transaction, TransactionProduct, TransactionCurrency, Currency, Till
)

class Command(BaseCommand):
    help = "Create dummy Transactions with Products and Currency splits"

    def handle(self, *args, **options):
        fake       = Faker()
        groups     = list(Group.objects.all())
        products   = list(Product.objects.all())
        currencies = list(Currency.objects.all())
        tills      = list(Till.objects.all())

        if not (groups and products and currencies and tills):
            self.stderr.write("🔴 Please create at least one Group, Product, Currency and Till first.")
            return

        for _ in range(20):
            # 1) Create Transaction
            tx = Transaction.objects.create(
                group     = random.choice(groups),
                receipt   = fake.bothify(text="RCPT-#####"),
                tax_free  = random.choice([True, False]),
                till      = random.choice(tills),
                date_time = fake.date_time_between(start_date='-30d', end_date='now',
                                                   tzinfo=timezone.get_current_timezone()),
            )
            tx.transaction_number = str(uuid.uuid4())
            tx.save()

            # 2) Add 1–5 line‐items
            subtotal = Decimal('0.00')
            gst_total = Decimal('0.00')
            for i in range(random.randint(1, 5)):
                prod     = random.choice(products)
                qty      = random.randint(1, 10)
                # randomly apply promotion 20% of time
                promo    = random.random() < 0.2
                price    = prod.price
                # if on promotion, 100% discount for demo
                discount = Decimal('1.00') if promo else prod.discount_rate or Decimal('0.00')

                tp = TransactionProduct.objects.create(
                    transaction   = tx,
                    product       = prod,
                    price         = price,
                    discount_rate = discount,
                    quantity      = qty,
                    promotion     = promo,
                )
                # it will auto-compute final_price, final_gst, total in save()
                subtotal += tp.final_price
                gst_total += tp.final_gst

            # 3) Add 1–3 currency splits summing to total
            grand_total = subtotal + gst_total
            remaining   = grand_total
            split_count = random.randint(1, min(3, len(currencies)))
            random.shuffle(currencies)
            for idx in range(split_count):
                cur = currencies[idx]
                if idx == split_count - 1:
                    pay = remaining
                else:
                    # random portion
                    pay = min(remaining, (grand_total * Decimal(random.random())).quantize(Decimal('0.01')))
                    remaining -= pay
                TransactionCurrency.objects.create(
                    transaction = tx,
                    currency    = cur,
                    payment     = pay * cur.currency_rate,
                )

            # 4) Recalculate the transaction summary
            tx.recalculate_summary()

            self.stdout.write(f"✔️ Created Transaction #{tx.pk} | items={tx.transactionproduct_set.count()} | total={tx.total}")
