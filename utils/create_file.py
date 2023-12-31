from data.objects import PeriodReport
from pathlib import Path

from weasyprint import HTML


def send_report(period: PeriodReport, bot, id):
    html = period.get_report(file=True)
    filename = f"{period.master}_{period.get_filename()}"

    with open(filename, "wb") as f:
        HTML(string=html).write_pdf(f)

    with open(filename, "rb") as f:
        bot.send_document(id, f)

    file = Path(f"./{filename}")
    file.unlink()
