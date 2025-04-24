import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Union
from uuid import uuid4


class LsxParser:

    @classmethod
    def load_lsx(cls, lsx_path: Union[str, Path]) -> ET.ElementTree:
        return ET.parse(lsx_path)


    @classmethod
    def save_lsx(cls, tree: ET.ElementTree, file_path: Union[str, Path]) -> None:
        output_path = Path(file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        return Path(file_path)


    @classmethod
    def find_attribute_by_id(cls, root: ET.Element, attribute_id: str) -> Optional[ET.Element]:
        for attribute in root.findall(f".//attribute[@id='{attribute_id}']"):
            return attribute
        return None


    @classmethod
    def update_attribute_value(cls, root: ET.Element, attribute_id: str, new_value: str) -> bool:
        attribute = cls.find_attribute_by_id(root, attribute_id)
        if attribute is not None:
            attribute.set('value', new_value)
            return True
        return False


    @classmethod
    def update_multiple_attributes(cls, root: ET.Element, updates: Dict[str, str]) -> Dict[str, bool]:
        return {attr_id: cls.update_attribute_value(root, attr_id, val) for attr_id, val in updates.items()}


    @classmethod
    def find_node_by_id(cls, root: ET.Element, node_id: str) -> Optional[ET.Element]:
        for node in root.findall(f".//node[@id='{node_id}']"):
            return node
        return None


    @classmethod
    def create_meta(
        cls,
        mod_name: str,
        meta_file_path: Union[str, Path],
        meta_output_path: Union[str, Path],
        author: str,
        description: str,
    ) -> str:

        tree = cls.load_lsx(meta_file_path)
        root = tree.getroot()

        module_info = cls.find_node_by_id(root, 'ModuleInfo')
        if module_info is None:
            raise ValueError('ModuleInfo node not found in the XML file.')
        
        
        attr = cls.find_attribute_by_id(module_info, 'Name')

        updates = {
            'Name': mod_name,
            'Folder': mod_name,
            'Author': author,
            'Description': description,
            'UUID': str(uuid4()),
        }

        for attr_id, new_value in updates.items():
            if new_value is not None:
                attr = cls.find_attribute_by_id(module_info, attr_id)
                if attr is not None:
                    attr.set('value', new_value)
                    print(f'Attribute {attr_id} updated to: {new_value}')
                else:
                    print(f'Attribute {attr_id} not found in ModuleInfo node.')

        cls.save_lsx(tree, meta_output_path)

        return mod_name
