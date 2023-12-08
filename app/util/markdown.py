import re
import markdownify
import yatg


def to_markdown(html: str) -> str:
    html = table_converter(html)
    md = markdownify.markdownify(html=html)
    return md


def table_converter(html: str) -> str:
    tables = re.findall(r'<table.*>.*</table>', html)
    if len(tables) == 0:
        return html

    for table in tables:
        ascii_table = yatg.html_2_ascii_table(html_content=table, output_style="orgmode")
        html = html.replace(table, "```" + ascii_table + "```")
    return html
