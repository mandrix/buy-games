import datetime
import decimal

from django.contrib import admin
from django.db import models
import django.conf as conf
import shortuuid

from helpers.payment import price_formatted, commission_price, factor_tasa_0, factor_card, PaymentMethodEnum


class RegionEnum(models.TextChoices):
    Japan = "jp", "Japan"
    USA = "usa", "USA"
    Europe = "eu", "Europe"


class StateEnum(models.TextChoices):
    sold = "sold", "Vendido"
    available = "available", "Disponible"
    reserved = "reserved", "Apartado"
    na = "na", "N/A"


class OwnerEnum(models.TextChoices):
    Joseph = "joseph", "Joseph"
    Mauricio = "mauricio", "Mauricio"
    Business = "business", "Business"


class ProviderEnum(models.TextChoices):
    ebay = "ebay", "Ebay"
    tecnoplay = "tecnoplay", "Tecnoplay"
    ali_express = "aliexpress", "AliExpress"
    cliente = "cliente", "Cliente"
    otros = "otros", "Otros"


class ConsoleEnum(models.TextChoices):
    NA = "na", "N/A"
    PlayStation1 = "ps1", "PS1"
    PlayStation2 = "ps2", "PS2"
    PlayStation3 = "ps3", "PS3"
    PlayStation4 = "ps4", "PS4"
    PlayStation5 = "ps5", "PS5"
    Xbox = "xbox", "Xbox"
    Xbox360 = "xbox360", "Xbox 360"
    XboxOne = "xbox-one", "Xbox One"
    XboxSeriesS = "xbox-series-s", "Xbox Series S"
    XboxSeriesX = "xbox-series-x", "Xbox Series X"
    PSVita = "psvita", "PSVita"
    PSP = "psp", "PSP"
    Wii = "wii", "Wii"
    WiiU = "wiiu", "Wii U"
    N64 = "n64", "N64"
    Snes = "snes", "SNES"
    Nes = "nes", "NES"
    Atari2600 = "atari2600", "Atari 2600"
    SegaGenesis = "sega-genesis", "Sega Genesis"
    SegaDreamcast = "sega-dreamcast", "Sega Dreamcast"
    SegaSaturn = "sega-saturn", "Sega Saturn"
    SegaNomad = "sega-nomad", "Sega Nomad"
    SegaGameGear = "sega-gamegear", "Sega GameGear"
    Gameboy = "gameboy", "Gameboy"
    GameboyColor = "gameboy-color", "Gameboy Color"
    GameboyPocket = "gameboy-pocket", "Gameboy Pocket"
    GameboyAdvanced = "gameboy-advanced", "Gameboy Advanced"
    GameboyAdvancedSP = "gameboy-advanced-sp", "Gameboy Advanced SP"
    Gamecube = "gamecube", "Gamecube"
    DS = "ds", "DS"
    DSi = "dsi", "DSi"
    _3DS = "3ds", "3DS"
    Switch = "switch", "Nintendo Switch"


class WarrantyType(models.TextChoices):
    STANDARD = "standard", "Standard"
    EXTENDED = "extended", "Extended"


class Console(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    title = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )

    def __str__(self):
        return self.get_title_display()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.product.amount > 1:
            self.product.duplicate()


class VideoGame(models.Model):
    title = models.CharField(max_length=100, default="")
    console = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.product.amount > 1:
            self.product.duplicate()


class Collectable(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.product.amount > 1:
            self.product.duplicate()


class Accessory(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    console = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.product.amount > 1:
            self.product.duplicate()


class Payment(models.Model):
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    remaining = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(default=PaymentMethodEnum.na, max_length=100, choices=PaymentMethodEnum.choices,
                                      null=True, blank=True)

    def __str__(self):
        return self.payment_method

    def check_payment(self):
        payment_info = {
            "sale_price": self.remaining,
            "payment_method": self.payment_method,
        }
        if self.payment_method == PaymentMethodEnum.na:
            payment_info.update({
                "tasa0": commission_price(self.remaining, factor_tasa_0()),
                "card": commission_price(self.remaining, factor_card()),
            })

        return payment_info

    @property
    @admin.display(description='sale price', ordering='sale_price')
    def sale_price_formatted(self):
        if self.sale_price:
            return price_formatted(self.sale_price)

    @property
    @admin.display(description='precio datafono', ordering='sale_price')
    def sale_price_with_card(self):
        if self.sale_price:
            return price_formatted(commission_price(self.sale_price, factor_card()))

    @property
    @admin.display(description='precio tasa 0', ordering='sale_price')
    def sale_price_with_tasa_0(self):
        if self.sale_price:
            return price_formatted(commission_price(self.sale_price, factor_tasa_0()))


class Product(models.Model):
    sale_price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, null=True, blank=True,
                                     help_text="En colones")
    provider_price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, help_text="En colones")
    provider = models.CharField(max_length=200, null=True, blank=True, choices=ProviderEnum.choices)
    remaining = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, null=True, blank=True,
                                    help_text="En colones")
    barcode = models.CharField(max_length=22, null=True, blank=True, unique=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    provider_purchase_date = models.DateField(default=datetime.date.today)
    sale_date = models.DateField(null=True, blank=True)
    owner = models.CharField(default=OwnerEnum.Business, max_length=100, choices=OwnerEnum.choices, null=True,
                             blank=True)
    description = models.TextField(default="")
    region = models.CharField(default=RegionEnum.USA, max_length=100, choices=RegionEnum.choices, null=True, blank=True)
    image = models.ImageField(upload_to='vents/photos/', null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)
    used = models.BooleanField(default=True)
    state = models.CharField(default=StateEnum.available, max_length=100, choices=StateEnum.choices)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        try:
            return self.get_additional_product_info().get_title_display()
        except:
            try:
                return self.get_additional_product_info().title
            except:
                return "ERROR sin info adicional"

    def generate_barcode(self, *args, **kwargs):
        self.barcode = shortuuid.uuid()

    @property
    @admin.display(description='console')
    def console_type(self):
        try:
            if self.console_set.first():
                return self.console_set.first()
            elif hasattr(self.get_additional_product_info(), "console"):
                return self.get_additional_product_info().console
        except:
            return "ERROR no tiene tipo"

    @property
    @admin.display(description='copies')
    def copies(self):
        try:
            return self.get_additional_product_info().__class__.objects.filter(
                title=self.get_additional_product_info().title, product__sale_date__isnull=not self.sale_date).count()
        except ValueError:
            return "ERROR"

    @property
    @admin.display(description='sale price', ordering='sale_price')
    def sale_price_formatted(self):
        if self.payment:
            return self.payment.sale_price_formatted

    @property
    @admin.display(description='precio datafono', ordering='sale_price')
    def sale_price_with_card(self):
        if self.payment:
            return self.payment.sale_price_with_card

    @property
    @admin.display(description='precio tasa 0', ordering='sale_price')
    def sale_price_with_tasa_0(self):
        if self.payment:
            return self.payment.sale_price_with_tasa_0

    @property
    @admin.display(description='provider price', ordering='provider_price')
    def provider_price_formatted(self):
        if self.provider_price:
            return f'{self.provider_price:,}₡'

    def get_additional_product_info(self):
        if additional_info := VideoGame.objects.filter(product=self).first():
            return additional_info
        elif additional_info := Console.objects.filter(product=self).first():
            return additional_info
        elif additional_info := Accessory.objects.filter(product=self).first():
            return additional_info
        elif additional_info := Collectable.objects.filter(product=self).first():
            return additional_info
        else:
            raise ValueError("Este producto no tiene informacion adicional")

    def get_product_type(self):
        type_mapping = {
            VideoGame: "Videojuego",
            Collectable: "Collecionable",
            Console: "Consola",
            Accessory: "Accesorio"
        }
        return type_mapping[type(self.get_additional_product_info())]

    def duplicate(self):
        amount = self.amount
        self.amount = 1
        self.save()
        for _ in range(amount - 1):
            copy = self

            additional_info = copy.get_additional_product_info()

            copy.pk = None
            copy.payment = None
            copy.amount = 1
            copy.save()

            additional_info.pk = None
            additional_info.product = copy
            additional_info.save()

    def save(self, *args, **kwargs):

        if not self.payment:
            payment = Payment(sale_price=self.sale_price,
                              remaining=self.sale_price)  # TODO falta quitar sle_price de producto
            payment.save()
            self.payment = payment

        if self.state == StateEnum.available:
            self.payment.sale_price = self.sale_price
            self.payment.remaining = self.sale_price
            self.remaining = self.sale_price
            self.payment.payment_method = PaymentMethodEnum.na
            self.payment.save()

        if not self.barcode:
            self.generate_barcode()
        super().save(*args, **kwargs)

        try:
            if self.amount > 1 and self.get_additional_product_info():
                self.duplicate()
        except ValueError as e:
            pass


class Report(models.Model):
    date = models.DateField()

    def __str__(self):
        return self.date.strftime('%d de %B de %Y')


class Sale(models.Model):
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product)
    warranty_type = models.CharField(max_length=100)
    purchase_date_time = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, null=True, blank=True,
                                   help_text="En colones")
    discount = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, null=True, blank=True,
                                   help_text="En colones")
    taxes = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, null=True, blank=True,
                                help_text="En colones")
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, null=True, blank=True,
                                help_text="En colones")
    payment_details = models.TextField(blank=True, default="")
    customer_name = models.CharField(max_length=100, default="Ready")
    customer_mail = models.EmailField(default='readygamescr@gmail.com')
    creation_date_time = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        if not self.report:
            return ""
        products_str = ", ".join(product.description[:30] for product in self.products.all()[:2])
        if not products_str:
            products_str = "Reparación"

        return f"{self.report.date} - {products_str} - ₡{self.total:,}"


class Log(models.Model):
    """
    Saving data to this model about every request
    """

    datetime = models.DateTimeField(auto_now=True)
    status_code = models.PositiveSmallIntegerField()
    status_text = models.TextField()
    response = models.TextField()
    request = models.TextField()
    ipv4_address = models.GenericIPAddressField()
    path = models.CharField(validators=[], max_length=100)
    is_secure = models.BooleanField()

    def __str__(self):
        return f"Log(datetime={self.datetime}, status_code={self.status_code}, path={self.path})"

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Overriding the save method in order to limit the amount of Logs that can be saved in the database.
        The limit is LOGS_LIMIT, after that the first ones inserted will be eliminated
        """
        super().save()
        count = Log.objects.count()
        extra = count - conf.settings.LOGS_LIMIT
        if extra > 0:
            remainder = Log.objects.all()[:extra]
            for log in remainder:
                log.delete()


class Expense(models.Model):  # gastos del negocio ordenados por dia (reporte)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.PositiveIntegerField()
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
