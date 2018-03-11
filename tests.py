import unittest
import datetime
from xmldict import xml_to_dict, dict_to_xml

class TestXmlutils(unittest.TestCase):
    def test_xml_to_dict_simple(self):
        test = '''
        <payment_method>
        <created_at type="datetime">2011-02-12T20:20:46Z</created_at>
        <is_retained type="boolean">true</is_retained>
        <first_name>Bob</first_name>
        <expiry_month type="integer">1</expiry_month>
        <address_1 nil="true"></address_1>
        </payment_method>
        '''

        expected = {'payment_method': {'address_1': {'nil': 'true'},
                                       'created_at': datetime.datetime(2011, 2, 12, 20, 20, 46),
                                       'expiry_month': 1,
                                       'first_name': 'Bob',
                                       'is_retained': True}}

        self.assertEqual(expected, xml_to_dict(test, strict=False))

    def test_xml_to_dict_list(self):
        test = '''
        <messages>
        <message>message1</message>
        <message>message2</message>
        </messages>
        '''

        expected = {'messages': {'message': ['message1', 'message2']}}
        self.assertEqual(expected, xml_to_dict(test, strict=False))

    def test_xml_to_dict_strict(self):
        test = '''
        <payment_method>
        <created_at type="datetime">2011-02-12T20:20:46Z</created_at>
        <is_retained type="boolean">true</is_retained>
        <messages>
            <message class="error" context="input.cvv" key="too_long" />
            <message class="error" context="input.card_number" key="failed_checksum" />
        </messages>
        </payment_method>
        '''

        expected = {'payment_method': {
            'created_at': {
                '@type': 'datetime',
                '#value': datetime.datetime(2011, 2, 12, 20, 20, 46),
                '#text': '2011-02-12T20:20:46Z'
            },
            'is_retained': {
                '@type': 'boolean',
                '#value': True,
                '#text': 'true'
            },
            'messages': {'message': [{'@class': 'error',
                                      '@context': 'input.cvv',
                                      '@key': 'too_long'},
                                     {'@class': 'error',
                                      '@context': 'input.card_number',
                                      '@key': 'failed_checksum'}]},
        }}

        self.assertEqual(expected, xml_to_dict(test, strict=True))

    def test_xml_to_dict_and_reverse(self):

        test = '''<messages>
<message id="1">
a
b
...
</message>
<message id="2">
c
d
...
</message>
</messages>'''

        expected = {'messages':
                     {'message':
                        [
                            {'@id': '1',
                             '#value': 'a\nb\n...',
                             '#text': '\na\nb\n...\n',
                            },
                            {'@id': '2',
                             '#value': 'c\nd\n...',
                             '#text': '\nc\nd\n...\n',
                            },
                        ]
                    }
                  }

        self.assertEqual(expected, xml_to_dict(test, strict=True))

        # once converted to dict, go back to xml (do not care about extra blanks)
        def _remove_blanks(content):

            from lxml import etree
            parser = etree.XMLParser(remove_blank_text=True)
            elem = etree.XML(content, parser=parser)
            return etree.tostring(elem)

        self.assertEqual(_remove_blanks(test), dict_to_xml(expected))

    def test_xml_to_dict_order(self):
        order1 = '<a><c>2</c><c>3</c><b>1</b></a>'
        order2 = '<a><b>1</b><c>2</c><c>3</c></a>'
        expected ={'a': {'c': ['2', '3'], 'b': '1'}}
        self.assertEqual(expected, xml_to_dict(order1))
        self.assertEqual(expected, xml_to_dict(order2))

    def test_xml_to_dict_namespace(self):
        xml_str1 = """<root id="1" xmlns="somenamespace"><items><item>1</item><item>2</item></items></root>"""
        xml_str2 = """<root id="1"><items><item>1</item><item>2</item></items></root>"""
        expected1 = {'{somenamespace}root': {'{somenamespace}items': {'{somenamespace}item': ['1', '2']}}}
        expected2 = {'root': {'items': {'item': ['1', '2']}}}
        self.assertEqual(expected1, xml_to_dict(xml_str1, strict=False))
        self.assertEqual(expected1, xml_to_dict(xml_str1))
        self.assertEqual(expected2, xml_to_dict(xml_str1, False, True))
        self.assertEqual(expected2, xml_to_dict(xml_str1, remove_namespace=True))
        self.assertEqual(expected2, xml_to_dict(xml_str2, strict=False))
        self.assertEqual(expected2, xml_to_dict(xml_str2))
        self.assertEqual(expected2, xml_to_dict(xml_str2, False, True))
        self.assertEqual(expected2, xml_to_dict(xml_str2, remove_namespace=True))

    def test_dict_to_xml_simple(self):
        dict_xml = {'transaction': {'amount': '100.00', 'currency_code': 'USD'}}
        expected = '<transaction><amount>100.00</amount><currency_code>USD</currency_code></transaction>'
        self.assertEqual(expected, dict_to_xml(dict_xml))

    def test_dict_to_xml_empty(self):
        dict_xml = {'messages': {'message': None}}
        expected = '<messages><message>null</message></messages>'
        self.assertEqual(expected, dict_to_xml(dict_xml))

    def test_dict_to_xml_lists(self):
        dict_xml = {'messages': {'message': ['message1', 'message2'], 'flag': True}}
        expected = '<messages><message>message1</message><message>message2</message><flag>true</flag></messages>'
        self.assertEqual(expected, dict_to_xml(dict_xml))

    def test_dict_to_xml_attributes(self):
        dict_xml = {'messages': {
            'message': [{'@foo': 'bar1', 'baz': 'baz1', '#text': 'message1'},
                        {'@foo': 'bar2', 'baz': 'baz2', '#text': 'message2'}],
            'flag': True
        }}
        expected = '<messages><message foo="bar1"><baz>baz1</baz>message1</message><message foo="bar2"><baz>baz2</baz>message2</message><flag>true</flag></messages>'
        self.assertEqual(expected, dict_to_xml(dict_xml))

if __name__ == '__main__':
    unittest.main()
