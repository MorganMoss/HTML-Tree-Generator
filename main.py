import sys
import urllib.request
from urllib.parse import unquote, quote


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


def url_tree_explorer(url:str, out, parent_url="", level=0, last = False):
    cleaned = unquote(url.replace(parent_url, ""))

    if last:
        prefix = ("| "*(level-1)).strip() + " `-- "
    else:
        prefix = ("| "*level).strip() + "-- "



    if url.endswith("/"):
        out.write(f'<li><span class="caret"><b><a href="{url}">{cleaned}</a></b></span>\n <ul class="nested">\n')
        page:str =  get_html_as_string_from_url(url)
        children:list[str] = get_all_links_in_html_form(page)

        print(prefix + cleaned)

        child_count =  len(children)
        for i in range(child_count):
            is_last = (i == child_count-1)
            url_tree_explorer(url+children[i], out, url, level+1,is_last)

        out.write(f'</ul>\n</li>\n') 
    else:
        out.write(f'<li><a href="{url}" class="preview">{cleaned}</a></li>\n')    
        print(prefix + f"\u001b]8;;{url}\u001b\\{cleaned}\u001b]8;;\u001b\\")

    out.write("\n")
    

def main():
    parent_url:str = input("Input URL to start tree (traverses from html form with the <a> tags) : \n")
    html_file:str = input("Input destination name : \n")

    with open(html_file, "w", encoding="utf-8") as output_file:

        output_file.write("""<!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport">
    <style>
    ul, #myUL {
    list-style-type: none;
    }

    #myUL {
    margin: 0;
    padding: 0;
    }

    .caret {
    cursor: pointer;
    -webkit-user-select: none; /* Safari 3.1+ */
    -moz-user-select: none; /* Firefox 2+ */
    -ms-user-select: none; /* IE 10+ */
    user-select: none;
    }

    .caret::before {
    content: "▶";
    color: black;
    display: inline-block;
    margin-right: 6px;
    }

    .caret-down::before {
    -ms-transform: rotate(90deg); /* IE 9 */
    -webkit-transform: rotate(90deg); /* Safari */
    transform: rotate(90deg);  
    }

    .nested {
    display: none;
    }

    .active {
    display: block;
    }

  
    a {
    color: black;
    text-decoration: none;
    }

    .content {
    width: 100%;
    box-sizing: border-box;
}

    * {
    box-sizing: border-box;
    }

    body {
        display: flex;
        width: 100%;
        height: 98%;
    }

    html {
        display: flex;
        width: 100%;
        height: 100%;
    }

    /* Create two equal columns that floats next to each other */
    .column {
    float: left;
    width: 50%;
    padding: 10px;
    height: 100%;
    }

    /* Clear floats after the columns */
    .row:after {
    display: flex;
    content: "";
    display: table;
    clear: both;
    width: auto;
    }   

    </style>
    </head>
<body>
    <div class="row" style="width:100%">
        <div class="column" style="background-color:#bbb;">
            <ul id="myUL">
        """)

        url_tree_explorer(parent_url, output_file)

        output_file.write("""
            </ul>
        </div>
        
        <div class="column" style="background-color:#aaa;">
            <iframe src="" width="100%" height="100%">
                <div>No online PDF viewer installed</div>
            </iframe>
        </div>
    </div>

    <script type="text/javascript" src="https://code.jquery.com/jquery-1.7.1.min.js"></script>
    <script>
        var toggler = document.getElementsByClassName("caret");
        var i;

        for (i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function() {
            this.parentElement.querySelector(".nested").classList.toggle("active");
            this.classList.toggle("caret-down");
        });
        } 

        $(document).ready(function(){
            $(document).on('mouseover','.preview',function(){
                var path_source=$(this).attr('href');
                $("iframe").attr("src",path_source);
            });

            $(document).on('mouseout','.preview',function(){
            });
        });

    </script>
</body>
    </html>
        """)

   
if __name__ == "__main__":
    main()