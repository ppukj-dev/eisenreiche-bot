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


def split_string_at_index(text: str, max_length: int):
    if len(text) <= max_length:
        return text, None

    # Find the nearest newline character before the max_length
    split_index = text.rfind('\n', 0, max_length)

    if split_index == -1:
        # No newline found, just split at max_length
        split_index = max_length

    # Split the string at the determined index
    first_part = text[:split_index]
    second_part = text[split_index:]

    return first_part, second_part
