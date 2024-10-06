import pendulum
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

initial_monday = pendulum.datetime(year=2024, month=10, day=7)
assert initial_monday.day_of_week == pendulum.MONDAY

font = "AgaveNerdFont-Regular.ttf"
registerFont(TTFont(name=font, filename=font))

output = "upratovanie.pdf"
canvas = Canvas(filename=output, pagesize=A4, initialFontName=font)
width, height = A4

x = width / 2
y = height - 150

heading = "PLÁN UPRATOVANIA"
canvas.setFontSize(36)
canvas.drawCentredString(x, y, heading)
canvas.setFontSize(24)

y -= 50

names = [
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

for i, name in enumerate(names):
    from_date = initial_monday.add(weeks=i).format("DD.MM")
    to_date = initial_monday.add(weeks=i + 1).subtract(days=1).format("DD.MM")

    record = f"{name:.<20} {from_date} - {to_date}"
    canvas.drawCentredString(x, y, record)

    y -= 30

canvas.save()
