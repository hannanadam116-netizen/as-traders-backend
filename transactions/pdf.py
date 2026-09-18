from decimal import Decimal
from io import BytesIO

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from company.models import Company
from .models import SalesInvoice


# ==========================================================
# STYLES
# ==========================================================

TITLE_STYLE = ParagraphStyle(
    name="Title",
    fontName="Helvetica-Bold",
    fontSize=18,
    alignment=TA_CENTER,
    spaceAfter=10,
)

SUBTITLE_STYLE = ParagraphStyle(
    name="Subtitle",
    fontName="Helvetica",
    fontSize=10,
    alignment=TA_CENTER,
)

HEADER_STYLE = ParagraphStyle(
    name="Header",
    fontName="Helvetica-Bold",
    fontSize=12,
    alignment=TA_LEFT,
)

TEXT_STYLE = ParagraphStyle(
    name="Text",
    fontName="Helvetica",
    fontSize=9,
    alignment=TA_LEFT,
)

BOLD_STYLE = ParagraphStyle(
    name="Bold",
    fontName="Helvetica-Bold",
    fontSize=9,
    alignment=TA_LEFT,
)


# ==========================================================
# HELPER
# ==========================================================

def money(value):
    if value is None:
        value = Decimal("0.00")

    return f"₹ {value:,.2f}"


# ==========================================================
# PDF GENERATOR
# ==========================================================

def generate_sales_invoice(invoice):

    company = Company.objects.first()

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    elements = []

    # ======================================================
    # COMPANY HEADER
    # ======================================================

    if company:

        elements.append(
            Paragraph(
                company.company_name,
                TITLE_STYLE,
            )
        )

        address = (
            f"{company.address}<br/>"
            f"{company.city}, {company.state} - {company.pin_code}"
        )

        elements.append(
            Paragraph(
                address,
                SUBTITLE_STYLE,
            )
        )

        contact = (
            f"Mobile : {company.mobile}"
        )

        if company.email:
            contact += f" | Email : {company.email}"

        elements.append(
            Paragraph(
                contact,
                SUBTITLE_STYLE,
            )
        )

        if company.gst_number:

            elements.append(
                Paragraph(
                    f"GSTIN : {company.gst_number}",
                    SUBTITLE_STYLE,
                )
            )

    elements.append(
        Spacer(
            1,
            8,
        )
    )

    # ======================================================
    # INVOICE TITLE
    # ======================================================

    elements.append(
        Paragraph(
            "TAX INVOICE",
            HEADER_STYLE,
        )
    )

    elements.append(
        Spacer(
            1,
            5,
        )
    )

        # ======================================================
    # INVOICE INFORMATION
    # ======================================================

    customer = invoice.customer

    left_data = [
        ["Customer", customer.name],
        [
            "Mobile",
            customer.mobile if customer.mobile else "-"
        ],
        [
            "GST No",
            customer.gst_number if customer.gst_number else "-"
        ],
        [
            "Address",
            (
                f"{customer.address}, "
                f"{customer.city}, "
                f"{customer.state} - "
                f"{customer.pin_code}"
            )
        ],
    ]

    right_data = [
        [
            "Invoice No",
            invoice.display_invoice_number,
        ],
        [
            "Invoice Date",
            invoice.invoice_date.strftime(
                "%d-%m-%Y"
            ),
        ],
        [
            "Payment",
            invoice.payment_type,
        ],
    ]

    left_table = Table(
        left_data,
        colWidths=[35 * mm, 75 * mm],
    )

    left_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.30,
                colors.grey,
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.whitesmoke,
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica",
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold",
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),
        ])
    )

    right_table = Table(
        right_data,
        colWidths=[35 * mm, 40 * mm],
    )

    right_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.30,
                colors.grey,
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.whitesmoke,
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica",
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold",
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),
        ])
    )

    info_table = Table(
        [
            [
                left_table,
                right_table,
            ]
        ],
        colWidths=[115 * mm, 60 * mm],
    )

    info_table.setStyle(
        TableStyle([
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
        ])
    )

    elements.append(info_table)

    elements.append(
        Spacer(
            1,
            10,
        )
    )

        # ======================================================
    # ITEMS TABLE
    # ======================================================

    table_data = [
        [
            "Sl No",
            "Product",
            "Qty",
            "Rate",
            "Amount",
        ]
    ]

    for index, item in enumerate(
        invoice.items.all(),
        start=1,
    ):

        table_data.append(
            [
                str(index),
                item.product.product_name,
                str(item.quantity),
                money(item.selling_price),
                money(item.total),
            ]
        )

    items_table = Table(
        table_data,
        colWidths=[
            15 * mm,
            80 * mm,
            20 * mm,
            30 * mm,
            35 * mm,
        ],
    )

    items_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.30,
                colors.grey,
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey,
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica",
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9,
            ),

            (
                "ALIGN",
                (2, 1),
                (-1, -1),
                "CENTER",
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                8,
            ),

        ])
    )

    elements.append(items_table)

    elements.append(
        Spacer(
            1,
            10,
        )
    )

    # ======================================================
    # TOTALS
    # ======================================================

    totals_data = [

        [
            "Subtotal",
            money(invoice.subtotal),
        ],

        [
            "Discount",
            money(invoice.discount),
        ],

        [
            f"GST ({invoice.gst_percent}%)",
            money(invoice.gst_amount),
        ],

        [
            "Transport Charge",
            money(invoice.transport_charge),
        ],

        [
            "Grand Total",
            money(invoice.grand_total),
        ],

    ]

    totals_table = Table(
        totals_data,
        colWidths=[
            45 * mm,
            35 * mm,
        ],
    )

    totals_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.30,
                colors.grey,
            ),

            (
                "BACKGROUND",
                (0, 4),
                (-1, 4),
                colors.lightgrey,
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica-Bold",
            ),

            (
                "ALIGN",
                (1, 0),
                (1, -1),
                "RIGHT",
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),

        ])
    )

    totals_wrapper = Table(
        [
            [
                "",
                totals_table,
            ]
        ],
        colWidths=[
            95 * mm,
            80 * mm,
        ],
    )

    totals_wrapper.setStyle(
        TableStyle([
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
        ])
    )

    elements.append(totals_wrapper)

    elements.append(
        Spacer(
            1,
            12,
        )
    )

        # ======================================================
    # AMOUNT IN WORDS
    # ======================================================

    try:
        from num2words import num2words

        amount_words = (
            num2words(
                invoice.grand_total,
                lang="en_IN"
            ).title()
            + " Rupees Only"
        )

    except Exception:

        amount_words = str(invoice.grand_total)

    elements.append(
        Paragraph(
            "<b>Amount in Words :</b>",
            BOLD_STYLE,
        )
    )

    elements.append(
        Paragraph(
            amount_words,
            TEXT_STYLE,
        )
    )

    elements.append(
        Spacer(
            1,
            8,
        )
    )

    # ======================================================
    # BANK DETAILS
    # ======================================================

    if company:

        bank_data = [

            [
                "Bank",
                company.bank_name or "-",
            ],

            [
                "Account No",
                company.account_number or "-",
            ],

            [
                "IFSC",
                company.ifsc_code or "-",
            ],

            [
                "UPI",
                company.upi_id or "-",
            ],

        ]

        bank_table = Table(
            bank_data,
            colWidths=[
                35 * mm,
                70 * mm,
            ],
        )

        bank_table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.30,
                    colors.grey,
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.whitesmoke,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),

            ])
        )

        elements.append(bank_table)

        elements.append(
            Spacer(
                1,
                10,
            )
        )

    # ======================================================
    # TERMS
    # ======================================================

    if company and company.terms:

        elements.append(
            Paragraph(
                "<b>Terms & Conditions</b>",
                HEADER_STYLE,
            )
        )

        elements.append(
            Paragraph(
                company.terms,
                TEXT_STYLE,
            )
        )

        elements.append(
            Spacer(
                1,
                12,
            )
        )

    # ======================================================
    # SIGNATURE
    # ======================================================

    signature = Table(

        [
            [
                "",
                "For " + (
                    company.company_name
                    if company
                    else ""
                ),
            ],

            [
                "",
                "",
            ],

            [
                "",
                "Authorized Signatory",
            ],

        ],

        colWidths=[
            110 * mm,
            65 * mm,
        ],

    )

    signature.setStyle(

        TableStyle([

            (
                "ALIGN",
                (1, 0),
                (1, -1),
                "CENTER",
            ),

            (
                "FONTNAME",
                (1, 0),
                (1, -1),
                "Helvetica-Bold",
            ),

        ])

    )

    elements.append(signature)

    # ======================================================
    # BUILD PDF
    # ======================================================

    document.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response[
        "Content-Disposition"
    ] = (
        f'inline; filename="Invoice-{invoice.display_invoice_number}.pdf"'
    )

    return response