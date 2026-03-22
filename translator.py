#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RimWorld Mod Translator
Extract translatable strings from RimWorld mods and generate Japanese translation templates.
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse


class RimWorldModTranslator:
    def __init__(self, mod_path, output_path="./output"):
        self.mod_path = Path(mod_path)
        self.output_path = Path(output_path)
        self.defs_path = self.mod_path / "Defs"
        self.languages_path = self.mod_path / "Languages"
        
    def extract_translatable_strings(self):
        """Extract translatable strings from Defs XML files"""
        if not self.defs_path.exists():
            print(f"Error: Defs folder not found at {self.defs_path}")
            return None
            
        translations = {}
        
        # Walk through all XML files in Defs
        for xml_file in self.defs_path.rglob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Extract def names and labels
                for def_element in root.findall(".//"):
                    if def_element.tag == "defName":
                        def_name = def_element.text
                    
                    # Common translatable fields
                    translatable_tags = ["label", "description", "labelShort", "labelMale", "labelFemale"]
                    if def_element.tag in translatable_tags and def_element.text:
                        key = f"{xml_file.stem}.{def_element.tag}"
                        translations[key] = def_element.text
                        
            except ET.ParseError as e:
                print(f"Warning: Could not parse {xml_file}: {e}")
                
        return translations
    
    def generate_japanese_template(self, translations):
        """Generate Japanese translation XML template"""
        if not translations:
            print("No translations found.")
            return
            
        # Create output directory
        output_dir = self.output_path / "Japanese" / "DefInjected"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Group by def type
        grouped = {}
        for key, value in translations.items():
            def_type = key.split(".")[0]
            if def_type not in grouped:
                grouped[def_type] = []
            grouped[def_type].append((key, value))
        
        # Generate XML files
        for def_type, items in grouped.items():
            output_file = output_dir / f"{def_type}.xml"
            
            root = ET.Element("LanguageData")
            for key, original_text in items:
                element = ET.SubElement(root, key)
                element.text = f"TODO: {original_text}"
            
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            
        print(f"Translation templates generated in {output_dir}")
        print(f"Generated {len(grouped)} translation files with {len(translations)} strings.")


def main():
    parser = argparse.ArgumentParser(description="RimWorld Mod Translation Tool")
    parser.add_argument("mod_path", help="Path to the RimWorld mod folder")
    parser.add_argument("-o", "--output", default="./output", help="Output directory for translation files")
    
    args = parser.parse_args()
    
    translator = RimWorldModTranslator(args.mod_path, args.output)
    translations = translator.extract_translatable_strings()
    
    if translations:
        translator.generate_japanese_template(translations)
    else:
        print("No translatable content found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
