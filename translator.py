#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RimWorld Mod Translator (Enhanced Version)
Extract translatable strings from RimWorld mods and generate Japanese translation templates.
Supports: DefInjected, Keyed, Patches, LoadFolders.xml, Translation Reports
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse
from datetime import datetime


class RimWorldModTranslator:
    def __init__(self, mod_path, output_path="./output", merge_existing=False):
        self.mod_path = Path(mod_path)
        self.output_path = Path(output_path)
        self.defs_path = self.mod_path / "Defs"
        self.languages_path = self.mod_path / "Languages"
        self.patches_path = self.mod_path / "Patches"
        self.merge_existing = merge_existing
        
        # Extended translatable field list
        self.translatable_tags = [
            "label", "labelShort", "labelMale", "labelFemale",
            "description", "descriptionShort", "descriptionHyperlinks",
            "jobString", "gerund", "verb",
            "pawnSingular", "pawnsPlural",
            "customLabel", "skillLabel",
            "chargeNoun", "destroyedLabel"
        ]
        
    def extract_translatable_strings(self):
        """Extract translatable strings from Defs XML files"""
        if not self.defs_path.exists():
            print(f"Warning: Defs folder not found at {self.defs_path}")
            return {}
            
        translations = {}
        
        for xml_file in self.defs_path.rglob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                for def_element in root:
                    def_name = None
                    
                    # Get defName for context
                    defname_elem = def_element.find("defName")
                    if defname_elem is not None:
                        def_name = defname_elem.text
                    
                    # Extract translatable fields
                    for field in self.translatable_tags:
                        field_elem = def_element.find(f".//{field}")
                        if field_elem is not None and field_elem.text:
                            if def_name:
                                key = f"{def_element.tag}.{def_name}.{field}"
                            else:
                                key = f"{def_element.tag}.{field}"
                            translations[key] = field_elem.text
                        
            except ET.ParseError as e:
                print(f"Warning: Could not parse {xml_file}: {e}")
            except Exception as e:
                print(f"Error processing {xml_file}: {e}")
                
        return translations
    
    def extract_keyed_strings(self):
        """Extract Keyed strings from Languages/English/Keyed folder"""
        keyed_path = self.languages_path / "English" / "Keyed"
        if not keyed_path.exists():
            return {}
        
        keyed_translations = {}
        
        for xml_file in keyed_path.rglob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                for element in root:
                    if element.text:
                        keyed_translations[element.tag] = element.text
                        
            except ET.ParseError as e:
                print(f"Warning: Could not parse Keyed file {xml_file}: {e}")
                
        return keyed_translations
    
    def extract_from_patches(self):
        """Extract translatable content from Patches folder"""
        if not self.patches_path.exists():
            return {}
        
        patch_translations = {}
        
        for xml_file in self.patches_path.rglob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Look for PatchOperationAdd and similar operations
                for operation in root.findall(".//value"):
                    for field in self.translatable_tags:
                        field_elem = operation.find(f".//{field}")
                        if field_elem is not None and field_elem.text:
                            key = f"Patch.{xml_file.stem}.{field}"
                            patch_translations[key] = field_elem.text
                            
            except ET.ParseError as e:
                print(f"Warning: Could not parse Patch file {xml_file}: {e}")
                
        return patch_translations
    
    def generate_japanese_template(self, translations, folder_name="DefInjected"):
        """Generate Japanese translation XML template"""
        if not translations:
            return
            
        output_dir = self.output_path / "Japanese" / folder_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Group by def type or file name
        grouped = {}
        for key, value in translations.items():
            parts = key.split(".")
            def_type = parts[0] if parts else "Unknown"
            if def_type not in grouped:
                grouped[def_type] = []
            grouped[def_type].append((key, value))
        
        # Generate XML files
        for def_type, items in grouped.items():
            output_file = output_dir / f"{def_type}.xml"
            
            # Merge with existing if requested
            existing_translations = {}
            if self.merge_existing and output_file.exists():
                existing_translations = self._load_existing_translations(output_file)
            
            root = ET.Element("LanguageData")
            for key, original_text in items:
                # Use existing translation if available
                if key in existing_translations:
                    text_value = existing_translations[key]
                else:
                    text_value = f"TODO: {original_text}"
                
                # Create nested structure for proper DefInjected format
                element = ET.SubElement(root, key)
                element.text = text_value
            
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            
        print(f"Generated {len(grouped)} files in {output_dir}")
    
    def generate_keyed_template(self, keyed_translations):
        """Generate Japanese Keyed translation template"""
        if not keyed_translations:
            return
            
        output_dir = self.output_path / "Japanese" / "Keyed"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "Keys.xml"
        
        root = ET.Element("LanguageData")
        for key, original_text in keyed_translations.items():
            element = ET.SubElement(root, key)
            element.text = f"TODO: {original_text}"
        
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        
        print(f"Generated Keyed translation file: {output_file}")
    
    def generate_loadfolders_xml(self):
        """Generate LoadFolders.xml for version-specific translations"""
        loadfolders_file = self.output_path / "LoadFolders.xml"
        
        loadfolders_content = '''<?xml version="1.0" encoding="utf-8"?>
<loadFolders>
  <v1.6>
    <li>/</li>
    <li>1.6</li>
  </v1.6>
</loadFolders>'''
        
        loadfolders_file.write_text(loadfolders_content, encoding="utf-8")
        print(f"Generated LoadFolders.xml: {loadfolders_file}")
    
    def generate_translation_report(self, all_translations):
        """Generate translation progress report"""
        report_file = self.output_path / "TranslationReport.txt"
        
        total = len(all_translations)
        translated = sum(1 for v in all_translations.values() if not str(v).startswith("TODO:"))
        untranslated = total - translated
        percentage = (translated / total * 100) if total > 0 else 0
        
        report = f"""RimWorld Mod Translation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

Total strings: {total}
Translated: {translated} ({percentage:.1f}%)
Untranslated: {untranslated}

{'='*60}
Untranslated strings:
"""
        
        for key, value in all_translations.items():
            if str(value).startswith("TODO:"):
                report += f"\n{key}: {value[6:]}"
        
        report_file.write_text(report, encoding="utf-8")
        print(f"\nTranslation report saved: {report_file}")
        print(f"Progress: {translated}/{total} ({percentage:.1f}%)")
    
    def _load_existing_translations(self, xml_file):
        """Load existing translations from file"""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            return {elem.tag: elem.text for elem in root if elem.text}
        except:
            return {}


def main():
    parser = argparse.ArgumentParser(
        description="RimWorld Mod Translation Tool (Enhanced)",
        epilog="Supports DefInjected, Keyed, Patches, and generates LoadFolders.xml"
    )
    parser.add_argument("mod_path", help="Path to the RimWorld mod folder")
    parser.add_argument("-o", "--output", default="./output", 
                        help="Output directory for translation files")
    parser.add_argument("-m", "--merge", action="store_true",
                        help="Merge with existing translations")
    parser.add_argument("-r", "--report", action="store_true",
                        help="Generate translation progress report")
    parser.add_argument("--no-keyed", action="store_true",
                        help="Skip Keyed translation extraction")
    parser.add_argument("--no-patches", action="store_true",
                        help="Skip Patches translation extraction")
    
    args = parser.parse_args()
    
    print(f"RimWorld Mod Translator (Enhanced)")
    print(f"Mod: {args.mod_path}")
    print(f"Output: {args.output}\n")
    
    translator = RimWorldModTranslator(args.mod_path, args.output, args.merge)
    
    # Extract DefInjected translations
    print("Extracting DefInjected translations...")
    def_translations = translator.extract_translatable_strings()
    
    # Extract Keyed translations
    keyed_translations = {}
    if not args.no_keyed:
        print("Extracting Keyed translations...")
        keyed_translations = translator.extract_keyed_strings()
    
    # Extract Patches translations
    patch_translations = {}
    if not args.no_patches:
        print("Extracting Patches translations...")
        patch_translations = translator.extract_from_patches()
    
    # Generate templates
    if def_translations:
        translator.generate_japanese_template(def_translations, "DefInjected")
    
    if keyed_translations:
        translator.generate_keyed_template(keyed_translations)
    
    if patch_translations:
        translator.generate_japanese_template(patch_translations, "Patches")
    
    # Generate LoadFolders.xml
    translator.generate_loadfolders_xml()
    
    # Generate report
    if args.report:
        all_translations = {**def_translations, **keyed_translations, **patch_translations}
        translator.generate_translation_report(all_translations)
    
    # Summary
    total_strings = len(def_translations) + len(keyed_translations) + len(patch_translations)
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  DefInjected: {len(def_translations)} strings")
    print(f"  Keyed: {len(keyed_translations)} strings")
    print(f"  Patches: {len(patch_translations)} strings")
    print(f"  Total: {total_strings} strings")
    print(f"{'='*60}")
    
    if total_strings == 0:
        print("\nNo translatable content found.")
        sys.exit(1)
    else:
        print(f"\nTranslation templates generated successfully!")


if __name__ == "__main__":
    main()
