import wikipedia
from main_startup.core.decorators import electron_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@electron_on_cmd(
    ["wiki", "wikipedia"],
    is_official=False,
    cmd_help={
        "help": "Wikipedia Makalelerini Alın!",
        "example": "{ch}wiki (sorgu)",
    },
)
async def wikipediasearch(Client, message):
    event = await edit_or_reply(message, "`Aranıyor..`")
    query = get_text(message)
    if not query:
        await event.edit("Geçersiz Söz dizimi Bu komutu nasıl kullanacağınızı öğrenmek için yardım menüsüne bakın")
        return
    results = wikipedia.search(query)
    result = ""
    for s in results:
        try:
            page = wikipedia.page(s)
            url = page.url
            result += f"> [{s}]({url}) \n"
        except BaseException:
            pass
    await event.edit(
        "WikiPedia Araması: {} \n\n Sonuç: \n\n{}".format(query, result),
        disable_web_page_preview=True,
    )
