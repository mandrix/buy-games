from django.db import models


class RegionEnum(models.TextChoices):
    Japan = "jp", "Japan"
    USA = "usa", "USA"
    Europe = "eu", "Europe"


class OwnerEnum(models.TextChoices):
    Joseph = "joseph", "Joseph"
    Mauricio = "mauricio", "Mauricio"
    Business = "business", "Business"


class ConsoleEnum(models.TextChoices):
    NA = "na", "N/A"
    PlayStation1 = "ps1", "PS1"
    PlayStation2 = "ps2", "PS2"
    PlayStation3 = "ps3", "PS3"
    PlayStation4 = "ps4", "PS4"
    PlayStation5 = "ps5", "PS5"
    Xbox = "xbox", "Xbox"
    Xbox360 = "xbox360", "Xbox360"
    XboxOne = "xbox-one", "XboxOne"
    XboxSeriesS = "xbox-series-s", "XboxSeriesS"
    XboxSeriesX = "xbox-series-x", "XboxSeriesX"
    PSVita = "psvita", "PSVita"
    PSP = "psp", "PSP"
    Wii = "wii", "Wii"
    WiiU = "wiiu", "Wii U"
    N64 = "n64", "N64"
    Snes = "snes", "SNES"
    Nes = "nes", "Nes"
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
    DS = "ds", "DS"
    DSi = "dsi", "DSi"
    _3DS = "3ds", "3DS"
    Switch = "switch", "Nintendo Switch"


class Product(models.Model):
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="En colones")
    provider_price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, help_text="En colones")
    barcode = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    provider_purchase_date = models.DateField()
    sale_date = models.DateField(null=True, blank=True)
    owner = models.CharField(default=OwnerEnum.Business, max_length=100, choices=OwnerEnum.choices, null=True, blank=True)
    description = models.TextField(default="")
    region = models.CharField(default=RegionEnum.USA, max_length=100, choices=RegionEnum.choices, null=True, blank=True)
    image = models.ImageField(upload_to='vents/photos/', null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)
    used = models.BooleanField(default=True)

    def __str__(self):
        return self.get_additional_product_info().title

    def get_additional_product_info(self):
        if additional_info := VideoGame.objects.filter(product=self).first():
            return additional_info
        elif additional_info := Console.objects.filter(product=self).first():
            return additional_info
        elif additional_info := Accessory.objects.filter(product=self).first():
            return additional_info
        else:
            raise Exception("Este producto no tiene informacion adicional")
        
    def get_product_type(self):
        type_mapping = {
            VideoGame: "Videojuego",
            Collectable: "Collecionable",
            Console: "Consola",
            Accessory: "Accesorio"
        }
        return type_mapping[type(self.get_additional_product_info())]


class Console(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )

    def __str__(self):
        return self.get_title_display()


class VideoGame(models.Model):
    title = models.CharField(max_length=100, default="")
    console = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Collectable(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Accessory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    console = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )

    def __str__(self):
        return self.title
