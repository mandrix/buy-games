# Generated by Django 4.2.2 on 2023-08-01 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_alter_product_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessory',
            name='console',
            field=models.CharField(choices=[('na', 'N/A'), ('ps1', 'PS1'), ('ps2', 'PS2'), ('ps3', 'PS3'), ('ps4', 'PS4'), ('ps5', 'PS5'), ('xbox', 'Xbox'), ('xbox360', 'Xbox360'), ('xbox-one', 'XboxOne'), ('xbox-series-s', 'XboxSeriesS'), ('xbox-series-x', 'XboxSeriesX'), ('psvita', 'PSVita'), ('psp', 'PSP'), ('wii', 'Wii'), ('wiiu', 'Wii U'), ('n64', 'N64'), ('snes', 'SNES'), ('nes', 'Nes'), ('atari2600', 'Atari 2600'), ('sega-genesis', 'Sega Genesis'), ('sega-dreamcast', 'Sega Dreamcast'), ('sega-saturn', 'Sega Saturn'), ('sega-nomad', 'Sega Nomad'), ('sega-gamegear', 'Sega GameGear'), ('gameboy', 'Gameboy'), ('gameboy-color', 'Gameboy Color'), ('gameboy-pocket', 'Gameboy Pocket'), ('gameboy-advanced', 'Gameboy Advanced'), ('gameboy-advanced-sp', 'Gameboy Advanced SP'), ('gamecube', 'Gamecube'), ('ds', 'DS'), ('dsi', 'DSi'), ('3ds', '3DS'), ('switch', 'Nintendo Switch')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='console',
            name='title',
            field=models.CharField(choices=[('na', 'N/A'), ('ps1', 'PS1'), ('ps2', 'PS2'), ('ps3', 'PS3'), ('ps4', 'PS4'), ('ps5', 'PS5'), ('xbox', 'Xbox'), ('xbox360', 'Xbox360'), ('xbox-one', 'XboxOne'), ('xbox-series-s', 'XboxSeriesS'), ('xbox-series-x', 'XboxSeriesX'), ('psvita', 'PSVita'), ('psp', 'PSP'), ('wii', 'Wii'), ('wiiu', 'Wii U'), ('n64', 'N64'), ('snes', 'SNES'), ('nes', 'Nes'), ('atari2600', 'Atari 2600'), ('sega-genesis', 'Sega Genesis'), ('sega-dreamcast', 'Sega Dreamcast'), ('sega-saturn', 'Sega Saturn'), ('sega-nomad', 'Sega Nomad'), ('sega-gamegear', 'Sega GameGear'), ('gameboy', 'Gameboy'), ('gameboy-color', 'Gameboy Color'), ('gameboy-pocket', 'Gameboy Pocket'), ('gameboy-advanced', 'Gameboy Advanced'), ('gameboy-advanced-sp', 'Gameboy Advanced SP'), ('gamecube', 'Gamecube'), ('ds', 'DS'), ('dsi', 'DSi'), ('3ds', '3DS'), ('switch', 'Nintendo Switch')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='console',
            field=models.CharField(choices=[('na', 'N/A'), ('ps1', 'PS1'), ('ps2', 'PS2'), ('ps3', 'PS3'), ('ps4', 'PS4'), ('ps5', 'PS5'), ('xbox', 'Xbox'), ('xbox360', 'Xbox360'), ('xbox-one', 'XboxOne'), ('xbox-series-s', 'XboxSeriesS'), ('xbox-series-x', 'XboxSeriesX'), ('psvita', 'PSVita'), ('psp', 'PSP'), ('wii', 'Wii'), ('wiiu', 'Wii U'), ('n64', 'N64'), ('snes', 'SNES'), ('nes', 'Nes'), ('atari2600', 'Atari 2600'), ('sega-genesis', 'Sega Genesis'), ('sega-dreamcast', 'Sega Dreamcast'), ('sega-saturn', 'Sega Saturn'), ('sega-nomad', 'Sega Nomad'), ('sega-gamegear', 'Sega GameGear'), ('gameboy', 'Gameboy'), ('gameboy-color', 'Gameboy Color'), ('gameboy-pocket', 'Gameboy Pocket'), ('gameboy-advanced', 'Gameboy Advanced'), ('gameboy-advanced-sp', 'Gameboy Advanced SP'), ('gamecube', 'Gamecube'), ('ds', 'DS'), ('dsi', 'DSi'), ('3ds', '3DS'), ('switch', 'Nintendo Switch')], max_length=20, null=True),
        ),
    ]
