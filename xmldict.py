"""
    xmldict
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Convert xml to python dictionaries.
"""
import datetime

def xml_to_dict(root_or_str, strict=True):
    """
    Converts `root_or_str` which can be parsed xml or a xml string to dict.

    """
    root = root_or_str
    if isinstance(root, str):
        import xml.etree.cElementTree as ElementTree
        root = ElementTree.XML(root_or_str)
    return {root.tag: _from_xml(root, strict)}

def dict_to_xml(dict_xml):
    """
    Converts `dict_xml` which is a python dict to corresponding xml.
    """
    return _to_xml(dict_xml)

# Functions below this line are implementation details.
# Unless you are changing code, don't bother reading.
# The functions above constitute the user interface.

def _to_xml(el):
    """
    Converts `el` to its xml representation.
    """
    val = None
    if isinstance(el, dict):
        val = _dict_to_xml(el)
    elif isinstance(el, bool):
        val = str(el).lower()
    else:
        val = el
    if val is None: val = 'null'
    return val

def _extract_attrs(els):
    """
    Extracts attributes from dictionary `els`. Attributes are keys which start
    with '@'
    """
    if not isinstance(els, dict):
        return ''
    return ''.join(' %s="%s"' % (key[1:], value) for key, value in els.iteritems()
                   if key.startswith('@'))

def _dict_to_xml(els):
    """
    Converts `els` which is a python dict to corresponding xml.
    """
    def process_content(tag, content):
        attrs = _extract_attrs(content)
        text = isinstance(content, dict) and content.get('#text', '') or ''
        return '<%s%s>%s%s</%s>' % (tag, attrs, _to_xml(content), text, tag)

    tags = []
    for tag, content in els.iteritems():
        # Text and attributes
        if tag.startswith('@') or tag == '#text':
            continue
        elif isinstance(content, list):
            for el in content:
                tags.append(process_content(tag, el))
        elif isinstance(content, dict):
            tags.append(process_content(tag, content))
        else:
            tags.append('<%s>%s</%s>' % (tag, _to_xml(content), tag))
    return ''.join(tags)

def _is_xml_el_dict(el):
    """
    Returns true if `el` is supposed to be a dict.
    This function makes sense only in the context of making dicts out of xml.
    """
    if len(el) == 1  or el[0].tag != el[1].tag:
        return True
    return False

def _is_xml_el_list(el):
    """
    Returns true if `el` is supposed to be a list.
    This function makes sense only in the context of making lists out of xml.
    """
    if len(el) > 1 and el[0].tag == el[1].tag:
        return True
    return False

def _str_to_datetime(date_str):
    try:
        val = datetime.datetime.strptime(date_str,  "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        val = date_str
    return val

def _str_to_boolean(bool_str):
    if bool_str.lower() != 'false' and bool(bool_str):
        return True
    return False

def _from_xml(el, strict):
    """
    Extracts value of xml element element `el`.
    """
    val = None
    # Parent node.
    if el:
        if _is_xml_el_dict(el):
            val = _dict_from_xml(el, strict)
        elif _is_xml_el_list(el):
            val = _list_from_xml(el, strict)
    # Simple node.
    else:
        attribs = el.items()
        # An element with attributes.
        if attribs and strict:
            val = dict(('@%s' % k, v) for k, v in dict(attribs).iteritems())
            if el.text:
                converted = _val_and_maybe_convert(el)
                val['#text'] = el.text
                if converted != el.text:
                    val['#value'] = converted
        elif el.text:
            # An element with no subelements but text.
            val = _val_and_maybe_convert(el)
        elif attribs:
            val = dict(attribs)
    return val

def _val_and_maybe_convert(el):
    """
    Converts `el.text` if `el` has attribute `type` with valid value.
    """
    text = el.text.strip()
    data_type = el.get('type')
    convertor = _val_and_maybe_convert.convertors.get(data_type)
    if convertor:
        return convertor(text)
    else:
        return text
_val_and_maybe_convert.convertors = {
    'boolean': _str_to_boolean,
    'datetime': _str_to_datetime,
    'integer': int
}

def _list_from_xml(els, strict):
    """
    Converts xml elements list `el_list` to a python list.
    """
    res = []
    tag = els[0].tag
    for el in els:
        res.append(_from_xml(el, strict))
    return {tag: res}

def _dict_from_xml(els, strict):
    """
    Converts xml doc with root `root` to a python dict.
    """
    # An element with subelements.
    res = {}
    for el in els:
        res[el.tag] = _from_xml(el, strict)
    return res
