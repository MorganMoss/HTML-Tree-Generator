from functools import reduce
import urllib.request
from urllib.parse import unquote
from flask import Flask, render_template, request, url_for, redirect
from os import path

TEMPLATE_FOLDER:str = "templates/"
OUTPUT_FOLDER:str = "static/output/"
app = Flask(__name__)

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


def url_tree_explorer(url:str, folder_template:str, file_template:str, parent_url="", level=0, last = False) -> str:
    """
    Recursively looks through links, prints out progress and returns a string to represent it, using the templates to 
    render folders and files

    Args:
        url (str): of the parent
        folder_template (str): a string with {{url}}, {{name}}, {{children}} within. 
        Replaces those tags with the link to the given content,
        simplified name of the content and the children of the content respectively
        file_template (str): a string with {{url}}, {{name}} within. 
        Replaces those tags with the link to the given content,
        simplified name of the content.
        
        parent_url (str, optional): previous url, used for recursion purposes. Defaults to "".
        level (int, optional): depth of the current url from parent, for recursion purposes. Defaults to 0.
        last (bool, optional): a boolean to show that the current url is the last 
        in a list of children or not, for recursion purposes. Defaults to False.

    Returns:
        str: rendered template for this tree
    """
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
    

def get_templates() -> tuple[str, str, str]:
    """
    Pulls from hard coded sources: layout.html, folder_template, file_template

    Returns:
        tuple[str, str, str]: the layout of the form, the template for a folder and the template of the file.
    """
    with open(TEMPLATE_FOLDER + "folder_template.html", "r", encoding="utf-8") as folder_template_file:
            folder:list[str] = folder_template_file.readlines()

    folder_as_str = reduce(lambda line1, line2 : line1 + line2, folder)

    with open(TEMPLATE_FOLDER + "file_template.html", "r", encoding="utf-8") as file_template_file:
        file:list[str] = file_template_file.readlines()

    file_as_str = reduce(lambda line1, line2 : line1 + line2, file)

    with open(TEMPLATE_FOLDER + "layout.html", "r", encoding="utf-8") as layout_file:
        layout:list[str] = layout_file.readlines()

    layout_as_str = reduce(lambda line1, line2 : line1 + line2, layout)

    return layout_as_str, folder_as_str, file_as_str


def generate_tree_page(parent_url:str, html_file:str):
    layout_as_str, folder_as_str, file_as_str = get_templates()

    tree:str = url_tree_explorer(parent_url, folder_as_str, file_as_str)
    layout_as_str = layout_as_str.replace("{{tree}}", tree)

    with open(OUTPUT_FOLDER + html_file, "w", encoding="utf-8") as output_file:
        output_file.write( layout_as_str )
   

def get_list_of_trees() -> list[str]:
    return list(map(lambda file : file.name, path.os.scandir(OUTPUT_FOLDER)))


def main():
    parent_url:str = input("Input URL to start tree (traverses from html form with the <a> tags) : \n")
    html_file:str = input("Input destination name : \n")
    generate_tree_page(parent_url, html_file)


@app.route('/tree', methods=['POST'])
def tree():
    url = request.form['url']

    file = url.split('/')[-2] + ".html"
    generate_tree_page(url, url.split('/')[-2] + ".html")
    return redirect(url_for('static', filename="output/" + file))
        

@app.route('/open', methods=['POST'])
def open_file():
    file = request.form['file']
    return redirect(url_for('static', filename="output/" + file))


@app.route('/')
def index():
    files = get_list_of_trees()
    return render_template('index.html', files=files)

if __name__ == '__main__':
   app.run()