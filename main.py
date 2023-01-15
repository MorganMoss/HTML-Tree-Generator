from functools import reduce
import urllib.request
from urllib.parse import unquote

def get_html_as_string_from_url(url:str, encoding:str="utf8") -> str:
    """
    This will fail if the URL is not a text document of some kind, the preference of course being .html

    Args:
        URL (str): The URL to be opened. 
        encoding (str, optional): The encoding of the bytes received from opening the URL. Defaults to "utf8".

    Returns:
        str: The string consiting of the decoded bytes from the opened URL. 
    """

    page_reader = urllib.request.urlopen(url)
    page_as_bytes = page_reader.read()
    page_reader.close()

    return page_as_bytes.decode("utf8")


def get_href_from_link_element(raw_element:str) -> str:
    """
    Args:
        raw_element (str): A messy string with <a href = "etc" >...</a> buried somewhere in it, the tags are optional

    Returns:
        str: A cleaned up version, keeping only the href, unquoted in url form
    """
    href:int = raw_element.find("href")
    start:int = raw_element.find("\"", href)
    end:int = raw_element.find("\"", start+1)

    if start == -1:
        return ""

    return raw_element[start+1:end]


def get_all_links_in_html_form(html:str) -> list[str]:
    """
    This will get all the <a ...>...</a> element's href urls as a list of strings

    Args:
        html (str): An HTML form (Assuming nested links are illegal)

    Returns:
        list[str]: A list of all link elements href (<a href=...>...</a>) in the same order they appear on the form
    """
    if html == None:
        return []

    raw_list:str = html.split("</a>")
    return list(filter(lambda x : x != "" , map(get_href_from_link_element, raw_list)))


def url_tree_explorer(url:str, folder_template:str, file_template:str, parent_url="", level=0, last = False):
    name = unquote(url.replace(parent_url, ""))

    if last:
        prefix = ("| "*(level-1)).strip() + " `-- "
    else:
        prefix = ("| "*level).strip() + "-- "


    if url.endswith("/"):
        print(prefix + name)
        html:str = folder_template.replace("{{url}}", url).replace("{{name}}", name)
        page:str =  get_html_as_string_from_url(url)
        children:list[str] = get_all_links_in_html_form(page)

        children_html:str = ""
        child_count =  len(children)
        for i in range(child_count):
            is_last = (i == child_count-1)
            children_html += url_tree_explorer(url + children[i], folder_template, file_template, url, level+1,is_last)

        html = html.replace("{{children}}", children_html)

        return html

    else:
        print(prefix + f"\u001b]8;;{url}\u001b\\{name}\u001b]8;;\u001b\\")
        return file_template.replace("{{url}}", url).replace("{{name}}", name)
    

def main():
    parent_url:str = input("Input URL to start tree (traverses from html form with the <a> tags) : \n")
    html_file:str = input("Input destination name : \n")

    with open("folder_template.html", "r", encoding="utf-8") as folder_template_file:
        folder:list[str] = folder_template_file.readlines()

    folder_as_str = reduce(lambda line1, line2 : line1 + line2, folder)

    with open("file_template.html", "r", encoding="utf-8") as file_template_file:
        file:list[str] = file_template_file.readlines()

    file_as_str = reduce(lambda line1, line2 : line1 + line2, file)

    with open("layout.html", "r", encoding="utf-8") as layout_file:
        layout:list[str] = layout_file.readlines()

    layout_as_str = reduce(lambda line1, line2 : line1 + line2, layout)
    tree:str = url_tree_explorer(parent_url, folder_as_str, file_as_str)
    layout_as_str = layout_as_str.replace("{{tree}}", tree)

    with open(html_file, "w", encoding="utf-8") as output_file:
        output_file.write(
            layout_as_str
        )
   
if __name__ == "__main__":
    main()