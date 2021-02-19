import re, markdown2

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def add_tag(split_content, tag):
    before, content, after = split_content
    return f'{before}<{tag}>{content}</{tag}>{after}'


def md_to_html(text):
    return markdown2.markdown(text)
    
    # TODO: consider converting to my on implementation as below

    # Don't forget escape char ('\' before each md char)
    
    # headings: # largest, ###### smallest
    # TODO: this only works if there's only 1 heading...
    # before, n, content, after = re.split(r'([#]{1,6}) (\w+)', text)
    # n = len(n)
    # text = add_tag([before,content,after], f'h{n}')
    
    # bold: **text** or __text__
    # before, content, after = re.split(r'[*_]{2}(\w+)[*_]{2}')
    # text = f''

    # unordered lists: -item or *item

    # links: [text](url)

    # paragraphs: blank line between

    return(text)