xmldict
========

Convert xml to python dictionaries, and vice-versa.

Installation
------------

    pip install xmldict

On most of the systems, you will need the `sudo` permissions if you are doing a system wide
install.

    sudo pip install xmldict


Example
---------------------


    # Converting xml to dictionary
    >>> xmldict.xml_to_dict('''
    ... <root>
    ...   <persons>
    ...     <person>
    ...       <name first="foo" last="bar" />
    ...     </person>
    ...     <person>
    ...       <name first="baz" last="bar" />
    ...     </person>
    ...   </persons>
    ... </root>
    ... ''')
    {'root': {'persons': {'person': [{'name': {'last': 'bar', 'first': 'foo'}}, {'name': {'last': 'bar', 'first': 'baz'}}]}}}

    # Removing namespace during convertion to dictionary is optional
    >>> xmldict.xml_to_dict("""<root id="1" xmlns="somenamespace"><items><item>1</item><item>2</item></items></root>""", remove_namespace=True)
    {'root': {'items': {'item': ['1', '2']}}}

    # Converting dictionary to xml 
    >>> xmldict.dict_to_xml({'root': {'persons': {'person': [{'name': {'last': 'bar', 'first': 'foo'}}, {'name': {'last': 'bar', 'first': 'baz'}}]}}})
    '<root><persons><person><name><last>bar</last><first>foo</first></name></person><person><name><last>bar</last><first>baz</first></name></person></persons></root>'
