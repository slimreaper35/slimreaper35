#!/usr/bin/env python3

import pendulum
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

# date configuration
START_YEAR = 2025
START_MONTH = 1
START_DAY = 27

# document configuration
HEADING = "PLÁN UPRATOVANIA"
HEADING_FONT_SIZE = 36

FONT_NAME = "AgaveNerdFont-Regular.ttf"
FONT_SIZE = 24

PAGE_SIZE = A4
OUTPUT_FILENAME = "upratovanie.pdf"

NAMES = [
    "Poníková",
    "Kolarčík",
    "Kofrit",
    "Šoltis",
    "Jančuš",
    "Kóczi",
    "Sekerák",
    "Liška",
    "Kundrák",
    "Tkáčik",
    "Korem",
    "Drap",
    "Železník",
    "Závadský",
    "Antal",
    "Duch",
]


def main():
    initial_monday = pendulum.datetime(year=START_YEAR, month=START_MONTH, day=START_DAY)
    assert initial_monday.day_of_week == pendulum.MONDAY

    registerFont(TTFont(name=FONT_NAME, filename=FONT_NAME))
    canvas = Canvas(filename=OUTPUT_FILENAME, pagesize=A4, initialFontName=FONT_NAME)
    width, height = A4

    x = width / 2
    y = height - 150

    canvas.setFontSize(HEADING_FONT_SIZE)
    canvas.drawCentredString(x, y, HEADING)
    canvas.setFontSize(FONT_SIZE)

    y -= 50

    for i, name in enumerate(NAMES):
        from_date = initial_monday.add(weeks=i).format("DD.MM")
        to_date = initial_monday.add(weeks=i + 1).subtract(days=1).format("DD.MM")

        record = f"{name:.<20} {from_date} - {to_date}"
        canvas.drawCentredString(x, y, record)

        y -= 30

    canvas.save()


if __name__ == "__main__":
    main()
