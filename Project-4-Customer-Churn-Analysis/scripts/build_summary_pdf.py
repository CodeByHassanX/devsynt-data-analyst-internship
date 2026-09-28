from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

doc = SimpleDocTemplate("Task4_Final_Summary.pdf", pagesize=letter,
                         topMargin=0.45*inch, bottomMargin=0.45*inch,
                         leftMargin=0.7*inch, rightMargin=0.7*inch)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=17, spaceAfter=2)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=10,
                                 textColor=colors.HexColor('#555555'), spaceAfter=10)
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12.5, spaceBefore=7, spaceAfter=3,
                     textColor=colors.HexColor('#1a1a2e'))
body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.3, leading=12.5, alignment=TA_LEFT)
small = ParagraphStyle('Small', parent=styles['Normal'], fontSize=8.7, leading=11.5)
cell_style = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=8.3, leading=10.5, alignment=TA_LEFT)
cell_center = ParagraphStyle('CellCenter', parent=cell_style, alignment=1)
header_style = ParagraphStyle('Header', parent=styles['Normal'], fontSize=8.3, leading=10.5,
                               textColor=colors.white, fontName='Helvetica-Bold', alignment=1)
header_left = ParagraphStyle('HeaderLeft', parent=header_style, alignment=TA_LEFT)

story = []

story.append(Paragraph("Customer Churn &amp; Retention Analysis — Final Summary", title_style))
story.append(Paragraph("Telco Customer Churn dataset (7,043 customers) — Data Analyst Internship, Task 4",
                        subtitle_style))

# ---- KPI table ----
story.append(Paragraph("Headline Numbers", h2))
kpi_header_style = ParagraphStyle('KpiHeader', parent=header_style, fontSize=8.0)
kpi_data = [
    [Paragraph(t, kpi_header_style) for t in
     ["Total Customers", "Churned", "Churn Rate", "Avg. Monthly<br/>Charges", "Revenue at Risk"]],
    [Paragraph(v, cell_center) for v in
     ["7,043", "1,869", "26.54%", "$64.76", "$139,130.85 /<br/>month"]],
]
kpi_table = Table(kpi_data, colWidths=[1.25*inch, 1.1*inch, 1.1*inch, 1.55*inch, 1.7*inch])
kpi_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a2e')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#eef1fb')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(kpi_table)
story.append(Spacer(1, 4))

# ---- Statistical results ----
story.append(Paragraph("Statistical Results (α = 0.05)", h2))
stat_data = [
    [Paragraph(t, header_left) for t in ["Test", "Result", "Decision"]],
    [Paragraph("Chi-Square: Contract vs. Churn", cell_style),
     Paragraph("Chi-Square stat = 1,184.60, p &#8776; 5.9e-258", cell_style),
     Paragraph("Reject H0 &mdash; associated", cell_style)],
    [Paragraph("T-Test: Monthly Charges vs. Churn", cell_style),
     Paragraph("t = 18.41, p &#8776; 8.6e-73<br/>(churned avg $74.44 vs. retained $61.27)", cell_style),
     Paragraph("Reject H0 &mdash; significant difference", cell_style)],
]
stat_table = Table(stat_data, colWidths=[1.7*inch, 3.15*inch, 2.25*inch])
stat_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a2e')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7f7fb')]),
]))
story.append(stat_table)
story.append(Spacer(1, 4))

# ---- Most important segment ----
story.append(Paragraph("Segment Needing the Most Retention Attention", h2))
story.append(Paragraph(
    "<b>New customers (tenure ≤ 12 months)</b> — 2,186 customers, <b>47.0% churn rate</b> "
    "(highest of any segment) and <b>$68,954/month revenue at risk</b> (also the highest of any "
    "segment, ahead of High-Value's $62,760/month). This group is large, newly acquired, and not "
    "yet committed to a longer contract, making it the highest-leverage target for retention "
    "investment.", body))
story.append(Spacer(1, 4))

# ---- Findings ----
story.append(Paragraph("Key Findings", h2))
findings = [
    "Overall churn is 26.54% (1,869 of 7,043 customers) — a material share of the customer base.",
    "Contract length is the strongest churn driver: month-to-month churn (42.7%) is ~4x one-year "
    "(11.3%) and ~15x two-year (2.8%); confirmed statistically significant (Chi-Square test, p &lt; 0.001).",
    "Churn risk is front-loaded by tenure: first-year customers churn at 47.4% vs. 9.5% for "
    "customers with 49+ months tenure.",
    "Churned customers pay more, not less — $74.44/month average vs. $61.27/month for retained "
    "customers, a statistically significant gap (t-test, p &lt; 0.001).",
    "Manual payment and missing services compound risk: Electronic check users churn at 45.3% "
    "(vs. ~15-17% for automatic payments), and customers without Tech Support churn at 41.6% "
    "(vs. 15.2% with it).",
]
story.append(ListFlowable(
    [ListItem(Paragraph(f, body), leftIndent=10, spaceAfter=3) for f in findings],
    bulletType='1', start=1, leftIndent=14
))
story.append(Spacer(1, 3))

# ---- Recommendations ----
story.append(Paragraph("Recommendations", h2))
recs = [
    "Incentivize contract upgrades — offer a discount for month-to-month customers who switch to "
    "a one-year contract, directly targeting the strongest churn driver found.",
    "Build a structured first-year onboarding/retention program — front-load engagement "
    "(check-ins, early offers, proactive support) during the highest-risk 0-12 month tenure window.",
    "Review fiber/high-tier pricing and value communication — test bundling a retention perk with "
    "the priciest plans, since churned customers pay $13/month more on average and Fiber churns at 41.9%.",
    "Push electronic check users onto automatic payment — offer a small discount for switching to "
    "bank transfer or credit card autopay, cutting churn from a method carrying 3x the risk.",
    "Bundle a free Tech Support trial into first-year onboarding for New-segment customers — this "
    "segment carries the highest churn rate and the most revenue at risk of any segment.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(r, body), leftIndent=10, spaceAfter=3) for r in recs],
    bulletType='1', start=1, leftIndent=14
))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "Full analysis, charts, and statistical test code: Task4_Customer_Churn_Analysis.ipynb. "
    "Dashboard data and build guide: power_bi/ folder.", small))

doc.build(story)
print("PDF built.")
