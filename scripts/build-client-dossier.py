from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "public" / "pilot" / "client-deliverable"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "Красная_сосна_3А_концепция_и_спецификация.pdf"

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
pdfmetrics.registerFont(TTFont("ProjectSans", str(FONT_DIR / "Arial.ttf")))
pdfmetrics.registerFont(TTFont("ProjectSans-Bold", str(FONT_DIR / "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("ProjectSans-Italic", str(FONT_DIR / "Arial Italic.ttf")))

PAGE_W, PAGE_H = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 16 * mm
MARGIN_BOTTOM = 16 * mm
CONTENT_W = PAGE_W - 2 * MARGIN_X

BONE = colors.HexColor("#F4F0E8")
INK = colors.HexColor("#1E1C19")
MUTED = colors.HexColor("#6F685F")
WALNUT = colors.HexColor("#4A3224")
LINE = colors.HexColor("#D7CFC3")
PALE = colors.HexColor("#FBF9F5")
TERRACOTTA = colors.HexColor("#9B5138")


class ProjectDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=MARGIN_X,
            rightMargin=MARGIN_X,
            topMargin=MARGIN_TOP,
            bottomMargin=MARGIN_BOTTOM,
            title="Красная сосна, 3А — концепция интерьера",
            author="Пилотный интерьерный проект",
            subject="Визуализации, реальные товары и ограничения точности",
        )
        frame = Frame(
            MARGIN_X,
            MARGIN_BOTTOM,
            CONTENT_W,
            PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
            id="normal",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=draw_page_chrome))


def draw_page_chrome(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN_X, 11 * mm, PAGE_W - MARGIN_X, 11 * mm)
        canvas.setFont("ProjectSans", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN_X, 6.5 * mm, "КРАСНАЯ СОСНА, 3А · КОНЦЕПЦИЯ")
        canvas.drawRightString(PAGE_W - MARGIN_X, 6.5 * mm, str(doc.page))
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ProjectTitle",
        fontName="ProjectSans-Bold",
        fontSize=28,
        leading=31,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=5 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="RoomTitle",
        fontName="ProjectSans-Bold",
        fontSize=20,
        leading=23,
        textColor=INK,
        spaceAfter=3 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        fontName="ProjectSans-Bold",
        fontSize=10.5,
        leading=13,
        textColor=WALNUT,
        spaceBefore=3 * mm,
        spaceAfter=1.8 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyRU",
        fontName="ProjectSans",
        fontSize=8.6,
        leading=11.4,
        textColor=INK,
        spaceAfter=1.5 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="SmallRU",
        fontName="ProjectSans",
        fontSize=7.3,
        leading=9.3,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="TableRU",
        fontName="ProjectSans",
        fontSize=7.2,
        leading=8.6,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHeadRU",
        fontName="ProjectSans-Bold",
        fontSize=7.1,
        leading=8.4,
        textColor=BONE,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverMeta",
        fontName="ProjectSans",
        fontSize=11,
        leading=15,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="CenterSmall",
        fontName="ProjectSans",
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_CENTER,
    )
)


def p(text: str, style: str = "BodyRU") -> Paragraph:
    # Arial on this macOS runtime lacks a usable ruble glyph in embedded PDFs.
    # Keep the client file portable by using the unambiguous textual abbreviation.
    return Paragraph(text.replace("₽", "руб."), styles[style])


def render_image(path: Path, width=CONTENT_W) -> Image:
    img = Image(str(path))
    ratio = img.imageHeight / img.imageWidth
    img.drawWidth = width
    img.drawHeight = width * ratio
    return img


def price_table(rows, total_label, total_value):
    data = [
        [p("Позиция", "TableHeadRU"), p("Конфигурация", "TableHeadRU"), p("Кол-во", "TableHeadRU"), p("Цена", "TableHeadRU"), p("Сумма", "TableHeadRU")]
    ]
    for row in rows:
        label = f'<link href="{row[1]}" color="#4A3224"><u>{row[0]}</u></link>' if row[1] else row[0]
        data.append(
            [
                p(label, "TableRU"),
                p(row[2], "TableRU"),
                p(str(row[3]), "TableRU"),
                p(row[4], "TableRU"),
                p(row[5], "TableRU"),
            ]
        )
    data.append(["", p(f"<b>{total_label}</b>", "TableRU"), "", "", p(f"<b>{total_value}</b>", "TableRU")])
    table = Table(data, colWidths=[34 * mm, 74 * mm, 13 * mm, 25 * mm, 28 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), WALNUT),
                ("BACKGROUND", (0, -1), (-1, -1), BONE),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
            ]
        )
    )
    return table


def bullet_list(items):
    return [p(f"• {item}") for item in items]


ROOMS = [
    {
        "title": "Кухня-гостиная 12,90 м²",
        "image": ROOT / "public/pilot/kitchen-living/camera-02-premium-final-v4-sharp.png",
        "layout": "Комната 7. Камера и архитектура сохранены по утверждённому ракурсу. Свет принят нейтральным, поскольку ориентация окон и данные по солнцу не предоставлены.",
        "rows": [
            ("SKDESIGN ЭНЗО", "https://skdesign.ru/product/enzo-divan-krovat?configurationId=2dcb8243-1b5b-11f0-a2b5-00505699dabd&productId=c660a0a6-0fd9-11f0-a2b5-00505699dabd", "Диван-кровать 210 × 100 × 85 см, «Букле Вайт», арт. SK-00042652", 1, "270 900 ₽", "270 900 ₽"),
            ("SKDESIGN ЛАГЕН РАУНД", "https://skdesign.ru/product/lagen-round-stol-obedennyy-razdvizhnoy?configurationId=1fa75564-6e0f-11f0-a2c1-00505699dabd&productId=60cb3603-6e0e-11f0-a2c1-00505699dabd", "Стол 110(153) × 110 × 76 см, натуральный дуб, основание «Домус Мауве», арт. SK-00044285", 1, "150 500 ₽", "150 500 ₽"),
            ("SKDESIGN ТОРИНО", "https://skdesign.ru/product/stul-torino?configurationId=e5054c80-d4b5-11ef-a2a5-00505699dabd&productId=38293a97-546c-11ed-bba8-0050569522e0", "Стул 54 × 61 × 83 см, бежевое букле, дуб «Орех Диккенс», арт. SK-00034579", 4, "53 600 ₽", "214 400 ₽"),
        ],
        "total_label": "Итого подтверждённая мебель",
        "total": "635 800 ₽",
        "custom": [
            "Кухня — индивидуальное изготовление после замера: тёмный дуб, молочная эмаль, столешница и фартук под Calacatta Viola.",
            "Картина сгенерирована для концепции; подвес и декоративная чаша не включены до выбора конкретных моделей.",
        ],
        "limit": "Проверить проходы, раскрытие стола, посадку четырёх стульев, ширину дивана и все привязки кухни по обмерному плану.",
    },
    {
        "title": "Прихожая-коридор 11,20 м²",
        "image": ROOT / "public/pilot/remaining-rooms/hall-01-final.png",
        "layout": "Комната 1. Главный объём — встроенное хранение длиной около 3000 мм; проходы к жилым комнатам и санузлам сохранены.",
        "rows": [
            ("SKDESIGN ФЛЭМ", "https://skdesign.ru/product/zerkalo-flam-simple?productId=56c31007-ede3-11ef-a2b2-00505699dabd", "Зеркало 50 × 140 см, дуб «Орех Диккенс»", 1, "23 700 ₽", "23 700 ₽"),
            ("SKDESIGN ЛУП", "https://skdesign.ru/product/loop-puf-39kh39kh46-sm?configurationId=3e9e268b-8e43-11f0-98f6-005056b45615&productId=d57dbdce-7f24-11f0-a2c1-00505699dabd", "Пуф 39 × 39 × 46 см, кофейное букле, арт. SK-00044565", 1, "33 600 ₽", "33 600 ₽"),
        ],
        "total_label": "Итого подтверждённая мебель",
        "total": "57 300 ₽",
        "custom": [
            "Шкаф 3000 × 600–700 мм до потолка, ниша около 900 мм; внутри правой секции — стиральная и сушильная машины.",
            "Шкаф, камень, подсветка, дорожка и картина требуют отдельного подбора или изготовления.",
        ],
        "limit": "Проверить глубину шкафа, вентиляцию техники, доступ к щиту и инженерным узлам; сохранить проход не менее 900 мм.",
    },
    {
        "title": "Спальня 12,42 м²",
        "image": ROOT / "public/pilot/remaining-rooms/bedroom-04-final.png",
        "layout": "Комната 4. Кровать 180 × 200 см расположена изголовьем к правой стене, окно и вход в гардеробную остаются доступными.",
        "rows": [
            ("SKDESIGN ПАРК", "https://skdesign.ru/product/krovat-parc-na-nozhkax?configurationId=3a1a8c83-73df-11ee-a22e-00505699dabd&productId=0933de71-822b-11ed-bbe5-005056abfb9b", "Кровать, габариты 190 × 230 × 123 см, тёпло-бежевая обивка, арт. SK-00007264", 1, "133 900 ₽", "133 900 ₽"),
            ("SKDESIGN ОЛСОН ВУД", "https://skdesign.ru/product/tumba-prikrovatnaya-olson-wood-2-yashhika", "Тумба 53 × 40 × 50 см, шпон, два ящика, арт. SK-00034455", 2, "36 300 ₽", "72 600 ₽"),
        ],
        "total_label": "Итого подтверждённая мебель",
        "total": "206 500 ₽",
        "custom": [
            "Матрас, ковёр, шторы, постельный текстиль и бра не включены; светильники подобрать после проверки выводов.",
            "Картина сгенерирована для проекта; рекомендуемый формат около 70 × 100 см.",
        ],
        "limit": "Проверить нижнюю тумбу у проёма гардеробной. При недостаточном проходе заменить её моделью шириной 35–42 см.",
    },
    {
        "title": "Детская 10,48 м²",
        "image": ROOT / "public/pilot/remaining-rooms/child-05-final.png",
        "layout": "Комната 5. Односпальная кровать расположена вдоль правой стены, стол 1200 мм — по левой; проход в гардеробную 6 не перекрывается.",
        "rows": [
            ("SKDESIGN ЭМБЕР ЛАЙН", "https://skdesign.ru/product/krovat-odnospalnaya-ember-line-s-podushkami", "Кровать 90 × 200 см, габариты 103,5 × 215 × 87,5 см, кофейное букле", 1, "228 700 ₽", "228 700 ₽"),
            ("SKDESIGN НЕССИ", "https://skdesign.ru/product/nessi-stol-pismennyy", "Стол 120 × 60 × 75 см, шпон дуба «Орех Диккенс»", 1, "55 700 ₽", "55 700 ₽"),
            ("Divan.ru ЭШЛИ", "https://www.divan.ru/product/ofisnoe-kreslo-eshli-textile-beige", "Кресло 59 × 55 × 82 см, бежевая рогожка, арт. 259790", 1, "14 990 ₽", "14 990 ₽"),
        ],
        "total_label": "Итого подтверждённая мебель",
        "total": "299 390 ₽",
        "custom": [
            "Матрас, ковёр, шторы, лампа, прикроватный куб и полки не включены в подтверждённый итог.",
            "Картина сгенерирована для проекта и не является товаром из каталога.",
        ],
        "limit": "Проверить зазор кровати до радиатора, открывание окна и двери гардеробной, а также рабочий проход со стулом.",
    },
    {
        "title": "Гардеробная 2,90 м²",
        "image": ROOT / "public/pilot/remaining-rooms/wardrobe-03-final.png",
        "layout": "Комната 3. Компактная П-образная система при спальне; центральный проход по плану около 700 мм.",
        "rows": [],
        "total_label": "Подтверждённая серийная мебель",
        "total": "нет",
        "custom": [
            "Левый фронт около 690 мм, центральный проём около 700 мм, правый фронт около 760 мм; глубина секций 500–600 мм после обмера.",
            "Тёмный дуб, молочные ящики, тёмно-бронзовые штанги и вертикальная подсветка 3000 K — индивидуальное изготовление.",
        ],
        "limit": "Рабочая документация мебельщика и чистый обмер после отделки имеют приоритет; проверить плечики, ящики и выключатель.",
    },
    {
        "title": "Гардеробная 3,47 м²",
        "image": ROOT / "public/pilot/remaining-rooms/wardrobe-06-final.png",
        "layout": "Комната 6. П-образная система: боковые и дальняя секции глубиной около 500 мм, центральный проход около 1400 мм.",
        "rows": [
            ("SKDESIGN ЛУП", "https://skdesign.ru/product/loop-puf-39kh39kh46-sm?configurationId=3e9e268b-8e43-11f0-98f6-005056b45615&productId=d57dbdce-7f24-11f0-a2c1-00505699dabd", "Пуф 39 × 39 × 46 см, кофейное букле", 1, "33 600 ₽", "33 600 ₽"),
        ],
        "total_label": "Итого подтверждённая мебель",
        "total": "33 600 ₽",
        "custom": [
            "Слева — закрытые молочные фасады; справа и по дальней стене — тёмный дуб, ящики, штанги, полки и верхние шкафы.",
            "Встроенная система, фурнитура и подсветка рассчитываются после деталировки.",
        ],
        "limit": "Проверить чистые размеры, дверь, выключатель, ревизии и возможность вынести пуф без демонтажа мебели.",
    },
    {
        "title": "Санузел 3,30 м²",
        "image": ROOT / "public/pilot/remaining-rooms/bathroom-02-final.png",
        "layout": "Комната 2. Ванна 1700 × 700 мм — по дальней стене; унитаз слева, компактная тумба до 500 мм справа.",
        "rows": [
            ("Cersanit CREA", "https://cersanit.ru/catalog/3d-be/collections/crea_1/", "Акриловая прямоугольная ванна 170 × 70 см", 1, "29 990 ₽", "29 990 ₽"),
            ("Cersanit CREA SQUARE + LINK PRO", "https://cersanit.ru/catalog/3d-be/installyatsii-i-komplekty/komplekty-gotovye-resheniya/komplekt-crea-square-co-dpl-eo-slim-installyaciya-link-pro/", "Подвесной унитаз с инсталляцией, 39,5 × 52 см, арт. A63997", 1, "27 440 ₽", "27 440 ₽"),
            ("Cersanit CREA 50", "https://cersanit.ru/catalog/3d-be/collections/crea_1/", "Керамическая раковина 50 см", 1, "5 490 ₽", "5 490 ₽"),
            ("IDDIS SAM", "https://www.iddis.ru/catalog/bathroom/faucets/SAMBR00i01/", "Смеситель для раковины, матовая бронза", 1, "3 270 ₽", "3 270 ₽"),
            ("IDDIS OLDIE", "https://www.iddis.ru/catalog/bathroom/faucets/OLDBR00i02/", "Смеситель для ванны с ручным душем, матовая бронза", 1, "10 670 ₽", "10 670 ₽"),
        ],
        "total_label": "Итого подтверждённая сантехника",
        "total": "76 860 ₽",
        "custom": [
            "Подвесная тумба до 500 мм, зеркало, экран, полотенцесушитель и отделка подбираются или изготавливаются отдельно.",
            "Керамогранит под известняк и акцентная плита под Calacatta Viola рассчитываются после раскладки.",
        ],
        "limit": "Проверить скрытые части, инсталляцию, привязки тумбы, ревизии и свободный проход. Монтажные схемы важнее визуализации.",
    },
    {
        "title": "Санузел 2,86 м²",
        "image": ROOT / "public/pilot/remaining-rooms/bathroom-08-final.png",
        "layout": "Комната 8. Душ около 1040 × 800 мм по дальней стене; унитаз слева, тумба 50 см справа у входа.",
        "rows": [
            ("Cersanit CREA SQUARE + LINK PRO", "https://cersanit.ru/catalog/3d-be/installyatsii-i-komplekty/komplekty-gotovye-resheniya/komplekt-crea-square-co-dpl-eo-slim-installyaciya-link-pro/", "Подвесной унитаз с инсталляцией, 39,5 × 52 см", 1, "27 440 ₽", "27 440 ₽"),
            ("AQUATON СИЛЬВА 50", "https://aquaton.ru/catalog/mebel-dlya-vannoy/tumby/tumba-pod-rakovinu-aquaton-silva-50-dub-ford-1a211701siw60/", "Тумба 44,5 × 38,7 × 56 см, дуб фьорд", 1, "5 976 ₽", "5 976 ₽"),
            ("Santek НЕО 50", "https://aquaton.ru/catalog/mebel-dlya-vannoy/tumby/tumba-pod-rakovinu-aquaton-silva-50-dub-ford-1a211701siw60/", "Совместимая керамическая раковина 50 см", 1, "4 590 ₽", "4 590 ₽"),
            ("IDDIS DUNA", "https://www.iddis.ru/catalog/bathroom/shower-systems/DUNMG0Ti67/", "Встраиваемая душевая система с термостатом, матовое золото", 1, "64 990 ₽", "64 990 ₽"),
            ("IDDIS SAM", "https://www.iddis.ru/catalog/bathroom/faucets/SAMBR00i01/", "Смеситель для раковины, матовая бронза", 1, "3 270 ₽", "3 270 ₽"),
        ],
        "total_label": "Итого подтверждённая сантехника и мебель",
        "total": "106 266 ₽",
        "custom": [
            "Душевой поддон в строительном исполнении, стекло, трап, зеркало, полотенцесушитель и сервисная ниша — после обмера.",
            "Акцентная вертикальная плитка и керамогранит под известняк рассчитываются после раскладки.",
        ],
        "limit": "Проверить дверь 700 мм, глубину тумбы 387 мм, уклон и отметку трапа, сервисный доступ и скрытую часть душевой системы.",
    },
]


def build_story():
    story = []
    cover = ROOT / "public/pilot/kitchen-living/camera-02-premium-final-v4-sharp.png"
    story.append(render_image(cover, PAGE_W - 2 * MARGIN_X))
    story.append(Spacer(1, 12 * mm))
    story.append(p("КРАСНАЯ СОСНА, 3А", "ProjectTitle"))
    story.append(p("Концепция интерьера · визуализации · реальные товары", "CoverMeta"))
    story.append(Spacer(1, 6 * mm))
    story.append(p("Пилотный проект по PDF-плану", "Section"))
    story.append(p("Общая площадь помещений по экспликации: 59,53 м². Стиль: тёплый современный интерьер с натуральным дубом, светло-бежевыми стенами, тёмным шпоном, молочными тканями и точечными терракотовыми акцентами."))
    story.append(Spacer(1, 4 * mm))
    story.append(p("05 августа 2026", "SmallRU"))
    story.append(PageBreak())

    story.append(p("Основа проекта", "RoomTitle"))
    plan = ROOT / "tmp/pdfs/electrical-plan-pages/page-2.png"
    story.append(render_image(plan, CONTENT_W))
    story.append(Spacer(1, 3 * mm))
    room_rows = [
        [p("№", "TableHeadRU"), p("Помещение", "TableHeadRU"), p("Площадь", "TableHeadRU")],
        ["1", "Прихожая-коридор", "11,20 м²"],
        ["2", "Санузел", "3,30 м²"],
        ["3", "Гардероб", "2,90 м²"],
        ["4", "Спальня", "12,42 м²"],
        ["5", "Детская", "10,48 м²"],
        ["6", "Гардероб", "3,47 м²"],
        ["7", "Кухня-гостиная", "12,90 м²"],
        ["8", "Санузел", "2,86 м²"],
    ]
    room_table = Table(room_rows, colWidths=[15 * mm, 110 * mm, 45 * mm])
    room_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), WALNUT),
                ("TEXTCOLOR", (0, 0), (-1, 0), BONE),
                ("FONTNAME", (0, 0), (-1, 0), "ProjectSans-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "ProjectSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(room_table)
    story.append(Spacer(1, 3 * mm))
    story.extend(
        bullet_list(
            [
                "PDF использован как источник геометрии и расстановки, но не как миллиметровая рабочая модель.",
                "Ориентация окон и солнечная траектория не предоставлены; во всех кадрах принят мягкий нейтральный дневной свет.",
                "Цены проверены 05.08.2026 и являются ориентиром до повторной проверки перед заказом.",
            ]
        )
    )

    for room in ROOMS:
        story.append(PageBreak())
        story.append(p(room["title"], "RoomTitle"))
        story.append(render_image(room["image"], CONTENT_W))
        story.append(Spacer(1, 2.5 * mm))
        story.append(p(room["layout"], "SmallRU"))
        story.append(p("Реальные товары в визуализации", "Section"))
        if room["rows"]:
            story.append(price_table(room["rows"], room["total_label"], room["total"]))
        else:
            story.append(p("Подтверждённой серийной мебели в кадре нет. Система хранения — индивидуальное изделие без фиктивного артикула и фиксированной цены."))
        story.append(p("Индивидуальные и концептуальные элементы", "Section"))
        story.extend(bullet_list(room["custom"]))
        story.append(p("Ограничение точности", "Section"))
        story.append(p(room["limit"]))

    story.append(PageBreak())
    story.append(p("Итог и границы сметы", "RoomTitle"))
    total_data = [
        [p("Категория", "TableHeadRU"), p("Подтверждённая сумма", "TableHeadRU")],
        ["Кухня-гостиная", "635 800 руб."],
        ["Прихожая", "57 300 руб."],
        ["Спальня", "206 500 руб."],
        ["Детская", "299 390 руб."],
        ["Гардеробная 3", "—"],
        ["Гардеробная 6", "33 600 руб."],
        ["Санузел 2", "76 860 руб."],
        ["Санузел 8", "106 266 руб."],
        [p("<b>Всего подтверждённых товаров</b>", "TableRU"), p("<b>1 415 716 ₽</b>", "TableRU")],
    ]
    total_table = Table(total_data, colWidths=[115 * mm, 55 * mm])
    total_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), WALNUT),
                ("BACKGROUND", (0, -1), (-1, -1), BONE),
                ("TEXTCOLOR", (0, 0), (-1, 0), BONE),
                ("FONTNAME", (0, 0), (-1, 0), "ProjectSans-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "ProjectSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(total_table)
    story.append(Spacer(1, 5 * mm))
    story.append(p("В сумму не входят", "Section"))
    story.extend(
        bullet_list(
            [
                "кухня, встроенные шкафы и гардеробные, индивидуальные тумбы и стекло душевых зон;",
                "отделочные материалы, плитка, камень, сантехнический монтаж и ремонтные работы;",
                "матрасы, текстиль, ковры, большая часть света, зеркала по размеру, декор и искусство;",
                "доставка, подъём, сборка, запас материалов и возможные региональные коэффициенты.",
            ]
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(p("Следующий обязательный этап", "Section"))
    story.append(
        p(
            "Обмер объекта → проверка проходов и инженерных привязок → рабочие чертежи встроенной мебели и сантехники → образцы материалов → повторная проверка наличия и цен → закупочная ведомость. Визуализации показывают концепцию и товарную логику, но не заменяют строительную документацию."
        )
    )
    return story


def main():
    doc = ProjectDocTemplate(str(OUT_PATH))
    doc.build(build_story())
    print(OUT_PATH)


if __name__ == "__main__":
    main()
