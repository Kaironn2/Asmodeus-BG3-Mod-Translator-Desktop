import xml.etree.ElementTree as ET
import pandas as pd


class XmlUtils:

    @staticmethod
    def xml_to_dataframe(xml_path: str) -> pd.DataFrame:
        
        tree = ET.parse(xml_path)
        root = tree.getroot()

        data = []

        for content in root.findall('.//content'):
            entry = {
                'contentuid': content.get('contentuid'),
                'version': content.get('version'),
                'text': content.text if content.text else ''
            }
            data.append(entry)

        return pd.DataFrame(data)


    @staticmethod
    def dataframe_to_xml(df: pd.DataFrame, output_path: str) -> None:
        
        root = ET.Element('contentList')

        for _, row in df.iterrows():
            attrs = {}

            if 'contentuid' in row and pd.notna(row['contentuid']):
                attrs['contentuid'] = row['contentuid']

            if 'version' in row and pd.notna(row['version']):
                attrs['version'] = row['version']

            content = ET.SubElement(root, 'content', **attrs)

            if 'text' in row and pd.notna(row['text']):
                content.text = row['text']

        tree = ET.ElementTree(root)

        ET.indent(tree, space='  ')

        tree.write(output_path, encoding='utf-8', xml_declaration=True)
