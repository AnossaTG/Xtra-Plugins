import os
import time

import pyshorteners
import requests
from bs4 import BeautifulSoup
from faker import Faker
from faker.providers import internet

from main_startup.core.decorators import electron_on_cmd
from main_startup.helper_func.basic_helpers import (
    delete_or_pass,
    edit_or_reply,
    get_text,
    progress,
)


@electron_on_cmd(
    ["fakegen", "fakedata"],
    cmd_help={"help": "Rastgele Sahte Ayrıntılar Oluştur", "example": "{ch}fakegen"},
)
async def gen_fake_details(client, message):
    lel = await edit_or_reply(message, "`İşleniyor...`")
    fake = Faker()
    name = str(fake.name())
    fake.add_provider(internet)
    address = str(fake.address())
    ip = fake.ipv4_private()
    cc = fake.credit_card_full()
    email = fake.ascii_free_email()
    job = fake.job()
    android = fake.android_platform_token()
    pc = fake.chrome()
    await lel.edit(
        f"<b><u> Sahte Bilgi Üretildi</b></u>\n<b>İsim :-</b><code>{name}</code>\n\n<b>Adres:-</b><code>{address}</code>\n\n<b>IP Adresi:-</b><code>{ip}</code>\n\n<b>Kredi Kartı:-</b><code>{cc}</code>\n\n<b>Email kimliği:-</b><code>{email}</code>\n\n<b>İş:-</b><code>{job}</code>\n\n<b>Android Kullanıcı Aracısı:-</b><code>{android}</code>\n\n<b>Bilgisayar Kullanıcı Aracısı:-</b><code>{pc}</code>",
        parse_mode="HTML",
    )


@electron_on_cmd(
    ["short"],
    cmd_help={"help": "URL bağlantısını kısaltın!", "example": "{ch}short {link}"},
)
async def vom(client, message):
    event = await edit_or_reply(message, "`Bağlantıyı kısaltılıyor.....`")
    link = get_text(message)
    if not link:
        await event.edit(
            "``Lütfen Bana Geçerli Bir Girdi Verin. Daha Fazla Bilgi İçin Yardım Menüsüne Bakabilirsiniz!``"
        )
        return
    sed = pyshorteners.Shortener()
    kek = sed.dagd.short(link)
    bestisbest = (
        f"<b>Url Kısaltıldı</b> \n<b><u>Verilen Bağlantı</u></b> ➠ {link}\n"
        f"<b><u>Kısaltılmış Bağlantı</u></b> ➠ {kek}"
    )
    await event.edit(bestisbest)


@electron_on_cmd(
    ["rmeme", "randomeme"],
    cmd_help={"help": "Rastgele Memeler Oluşturun!", "example": "{ch}rmeme"},
)
async def givemememe(client, message):
    hmm_s = "https://some-random-api.ml/meme"
    r = requests.get(url=hmm_s).json()
    image_s = r["image"]
    await message.reply_photo(image_s)
    await delete_or_pass(message)

    
@electron_on_cmd(
    ["iban", "ibaninfo"],
    cmd_help={"help": "IBAN Hakkında Bilgi Alın", "example": "{ch}iban (iban gir)"},
)
async def ibanbanem(client, message):
    stark_m = await edit_or_reply(message, "`Lütfen Bekle!`")
    iban = get_text(message)
    if not iban:
        await stark_m.edit(
            "`Lütfen Bana Geçerli Bir Girdi Verin. Daha Fazla Bilgi İçin Yardım Menüsüne Bakabilirsiniz!`"
        )
        return
    api = f"https://openiban.com/validate/{iban}?getBIC=true&validateBankCode=true"
    r = requests.get(url=api).json()
    if r["valid"] is False:
        await stark_m.edit("Geçersiz IBAN, Geçerli Bir IBAN İle Tekrar Deneyin!")
        return
    banks = r["bankData"]
    kek = (
        f"<b><u>GEÇERLİ</u></b> ➠ <code>{r['valid']}</code> \n"
        f"<b><u>IBAN</u></b> ➠ <code>{r['iban']}</code> \n"
        f"<b><u>BANKA-KODU</u></b> ➠ <code>{banks['bankCode']}</code> \n"
        f"<b><u>BANKA-ADI</u></b> ➠ <code>{banks['name']}</code> \n"
        f"<b><u>POSTA KODU</u></b> ➠ <code>{banks['zip']}</code> \n"
        f"<b><u>ŞEHİR</u></b> ➠ <code>{banks['city']}</code> \n"
        f"<b><u>BIC</u></b> ➠ <code>{banks['bic']}</code> \n"
    )
    await stark_m.edit(kek, parse_mode="html")
