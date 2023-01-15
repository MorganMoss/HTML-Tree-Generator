## HTML-Tree-Generator

### Author
<a href=https://github.com/MorganMoss> Morgan Moss </a>


### Summary
This was created to make my life easier when navigating websites that have a lot of links to pdfs


### Installation Requirements
To use this, you require Python and Flask to be installed. 
You also require a browser with a pdf viewer. Firefox was used in testing

Use Python 3.11 or later
https://www.python.org/downloads/

<ol>
<li>
Create a virutal environment and install Flask from there

```python3 -m venv /path/to/new/virtual/environment```

</li>
<li>
Activate that environment

On Unix or MacOS, using the bash shell: 
    ```source /path/to/venv/bin/activate```

On Unix or MacOS, using the csh shell: 
    ```source /path/to/venv/bin/activate.csh```

On Unix or MacOS, using the fish shell: 
    ```source /path/to/venv/bin/activate.fish```   

On Windows using the Command Prompt: 
    ```path\to\venv\Scripts\activate.bat```

On Windows using PowerShell: 
    ```path\to\venv\Scripts\Activate.ps1```

</li>
<li>
Install Flask:

```pip install Flask```

</li>
</ol>

### To Run
<ol>
<li>
In your terminal (opened in this directory) enter:

```python3 main.py```

</li>
<li>
In your browser open the url: <a href="http://127.0.0.1:5000">http://127.0.0.1:5000</a>

</li>
</ol>

### Usage

Once opened, you can choose to enter and submit a URL or choose a file from a dropdown list (will be empty on first use)

When submitting a URL, it should end with '/' for it to be considered a directory. It will take some time depending on how big the directory is,
you can check the progress in the console you opened this in. It will then open automatically when it's done.

You can choose to see trees generated in the past via the drop down menu