"""
IDML Arabic Translation Tool - Core Translation Module
Handles IDML extraction, translation, font mapping, and reconstruction
Using FREE Google Translate (no API key required)
"""

import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from lxml import etree
from simple_translator import translate_text
from word_generator import create_word_document


class IDMLTranslator:
    def __init__(self, api_key=None, target_lang='ar'):
        """Initialize the translator (API key not needed for free version)"""
        self.temp_dir = None
        self.target_lang = target_lang
        self.translation_pairs = []  # Store all translations for review
        
    def translate_idml(self, idml_path, progress_callback=None):
        """
        Main translation workflow
        
        Args:
            idml_path: Path to the input IDML file
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dictionary with paths to translated IDML and Word files
        """
        try:
            # Step 1: Extract IDML
            if progress_callback:
                progress_callback("Extracting IDML file...", 10)
            self.temp_dir = tempfile.mkdtemp()
            self._extract_idml(idml_path)
            
            # DEBUG: Print target language
            print(f"DEBUG: Target language is: {self.target_lang}")
            
            # Step 2: Apply World-Ready Composer fixes
            if progress_callback:
                progress_callback("Applying formatting rules...", 20)
            self._fix_styles_xml()
            
            # Step 3: Translate Stories
            if progress_callback:
                progress_callback("Translating text content...", 30)
            self._translate_stories(progress_callback)
            
            # Step 4: Map fonts
            if progress_callback:
                progress_callback("Mapping fonts for Arabic compatibility...", 80)
            self._map_fonts()
            
            # Step 5: Reconstruct IDML
            if progress_callback:
                progress_callback("Reconstructing IDML file...", 90)
            idml_output_path = self._reconstruct_idml(idml_path)
            
            # Step 6: Generate Word document
            if progress_callback:
                progress_callback("Generating Word document...", 95)
            word_output_path = self._generate_word_document(idml_path)
            
            if progress_callback:
                progress_callback("Translation complete!", 100)
            
            # Store results before any cleanup
            result = {
                'idml': idml_output_path,
                'word': word_output_path,
                'translations': self.translation_pairs
            }
            
            # Note: Temp directory cleanup is intentionally skipped here
            # The files need to remain accessible for download
            # Streamlit will handle cleanup when the session ends
            
            return result
            
        except Exception as e:
            # Cleanup temp directory on error
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir)
                except:
                    pass  # Ignore cleanup errors
            
            # Provide detailed error information
            import traceback
            error_details = traceback.format_exc()
            print(f"Translation error details:\n{error_details}")
            raise Exception(f"Translation failed: {str(e)}")
    
    def _extract_idml(self, idml_path):
        """Extract IDML archive to temporary directory"""
        # Ensure file exists and is readable
        if not os.path.exists(idml_path):
            raise Exception(f"IDML file not found: {idml_path}")
        
        if not os.path.isfile(idml_path):
            raise Exception(f"Path is not a file: {idml_path}")
        
        # Check if file is accessible
        try:
            with open(idml_path, 'rb') as test_file:
                test_file.read(4)  # Read first 4 bytes to test
        except Exception as e:
            raise Exception(f"Cannot read IDML file: {str(e)}")
        
        # Extract the IDML archive
        try:
            with zipfile.ZipFile(idml_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
        except zipfile.BadZipFile:
            raise Exception("Invalid IDML file: Not a valid ZIP archive")
        except Exception as e:
            raise Exception(f"Failed to extract IDML: {str(e)}")
        
        # Validate structure
        stories_dir = os.path.join(self.temp_dir, 'Stories')
        resources_dir = os.path.join(self.temp_dir, 'Resources')
        
        if not os.path.exists(stories_dir):
            raise Exception("Invalid IDML: Stories folder not found")
        if not os.path.exists(resources_dir):
            raise Exception("Invalid IDML: Resources folder not found")
    
    def _fix_styles_xml(self):
        """Apply World-Ready Composer and RTL alignment to paragraph styles"""
        styles_path = os.path.join(self.temp_dir, 'Resources', 'Styles.xml')
        
        if not os.path.exists(styles_path):
            return  # No styles to fix
        
        # Parse XML
        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(styles_path, parser)
        root = tree.getroot()
        
        # Apply language-specific formatting to styles
        if self.target_lang == 'ar':
            # Arabic-specific style fixes
            for para_style in root.iter('ParagraphStyle'):
                para_style.set('Composer', 'Adobe World-Ready Paragraph Composer')
                
                # Set right alignment for RTL
                current_justification = para_style.get('Justification', '')
                if 'Center' not in current_justification:
                    para_style.set('Justification', 'RightAlign')
                
                para_style.set('AppliedLanguage', 'Language:$ID/Arabic')
                para_style.set('DigitsType', 'DefaultDigits')
            
            # CRITICAL: Also fix CharacterStyle elements for proper letter joining
            for char_style in root.iter('CharacterStyle'):
                char_style.set('AppliedLanguage', 'Language:$ID/Arabic')
                char_style.set('KerningMethod', 'Optical')
        
        elif self.target_lang == 'en':
            # English-specific style fixes
            for para_style in root.iter('ParagraphStyle'):
                para_style.set('Composer', 'Adobe Paragraph Composer')
                
                # Set left alignment for LTR
                current_justification = para_style.get('Justification', '')
                if 'Center' not in current_justification:
                    para_style.set('Justification', 'LeftAlign')
                
                para_style.set('AppliedLanguage', 'Language:$ID/English: USA')
            
            # Fix CharacterStyle elements
            for char_style in root.iter('CharacterStyle'):
                char_style.set('AppliedLanguage', 'Language:$ID/English: USA')
                char_style.set('KerningMethod', 'Optical')
        
        # Write back to file
        tree.write(styles_path, encoding='UTF-8', xml_declaration=True, pretty_print=False)
    
    def _translate_stories(self, progress_callback=None):
        """Translate all text in Stories XML files"""
        stories_dir = os.path.join(self.temp_dir, 'Stories')
        story_files = [f for f in os.listdir(stories_dir) if f.endswith('.xml')]
        
        total_stories = len(story_files)
        
        for idx, story_file in enumerate(story_files):
            story_path = os.path.join(stories_dir, story_file)
            
            # Update progress
            if progress_callback:
                progress = 30 + int((idx / total_stories) * 50)
                progress_callback(f"Translating story {idx + 1}/{total_stories}...", progress)
            
            # Parse XML
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(story_path, parser)
            root = tree.getroot()
            
            # Apply language-specific formatting based on target language
            if self.target_lang == 'ar':
                # Arabic-specific formatting
                for para_range in root.iter('ParagraphStyleRange'):
                    para_range.set('Composer', 'Adobe World-Ready Paragraph Composer')
                    para_range.set('StoryDirection', 'RightToLeftDirection')
                    para_range.set('Justification', 'RightAlign')
                    para_range.set('AppliedLanguage', 'Language:$ID/Arabic')
                    para_range.set('DigitsType', 'DefaultDigits')
                
                # CRITICAL: Also apply to CharacterStyleRange for proper letter joining
                for char_range in root.iter('CharacterStyleRange'):
                    char_range.set('AppliedLanguage', 'Language:$ID/Arabic')
                    char_range.set('DigitsType', 'DefaultDigits')
                    char_range.set('KashidaWidth', 'Medium')
                    char_range.set('KerningMethod', 'Optical')
            
            elif self.target_lang == 'en':
                # English-specific formatting
                for para_range in root.iter('ParagraphStyleRange'):
                    para_range.set('Composer', 'Adobe Paragraph Composer')
                    para_range.set('StoryDirection', 'LeftToRightDirection')
                    para_range.set('Justification', 'LeftAlign')
                    para_range.set('AppliedLanguage', 'Language:$ID/English: USA')
                
                # Set English language on character ranges
                for char_range in root.iter('CharacterStyleRange'):
                    char_range.set('AppliedLanguage', 'Language:$ID/English: USA')
                    char_range.set('KerningMethod', 'Optical')
            
            # Extract and translate Content tags
            for idx, content in enumerate(root.iter('Content')):
                if content.text and content.text.strip():
                    original_text = content.text
                    translated_text = self._translate_text(original_text)
                    content.text = translated_text
                    
                    # Store translation pair for review
                    self.translation_pairs.append({
                        'id': len(self.translation_pairs) + 1,
                        'original': original_text,
                        'translated': translated_text,
                        'story_file': story_file,
                        'element_index': idx
                    })
            
            # Write back to file
            tree.write(story_path, encoding='UTF-8', xml_declaration=True, pretty_print=False)
    
    def _translate_text(self, text):
        """Translate text using free Google Translate"""
        print(f"DEBUG: Translating to {self.target_lang}: {text[:50]}...")
        result = translate_text(text, target_lang=self.target_lang, source_lang='auto')
        print(f"DEBUG: Result: {result[:50]}...")
        return result
    
    def _map_fonts(self):
        """Map English fonts to Arabic-compatible fonts"""
        stories_dir = os.path.join(self.temp_dir, 'Stories')
        story_files = [f for f in os.listdir(stories_dir) if f.endswith('.xml')]
        
        # Comprehensive font mapping dictionary - map common fonts to Arabic-compatible ones
        font_map = {
            'Minion Pro': 'Adobe Arabic',
            'Myriad Pro': 'Adobe Arabic',
            'Times New Roman': 'Arial',
            'Times': 'Arial',
            'Helvetica': 'Arial',
            'Helvetica Neue': 'Arial',
            'Calibri': 'Arial',
            'Verdana': 'Arial',
            'Georgia': 'Arial',
            'Garamond': 'Adobe Arabic',
            'Palatino': 'Adobe Arabic',
            'Baskerville': 'Adobe Arabic',
            'Futura': 'Arial',
            'Avenir': 'Arial',
        }
        
        for story_file in story_files:
            story_path = os.path.join(stories_dir, story_file)
            
            # Parse XML
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(story_path, parser)
            root = tree.getroot()
            
            # Find and update font references
            for elem in root.iter():
                if 'AppliedFont' in elem.attrib:
                    current_font = elem.get('AppliedFont')
                    
                    # Check if font needs mapping
                    font_replaced = False
                    for old_font, new_font in font_map.items():
                        if old_font in current_font:
                            elem.set('AppliedFont', current_font.replace(old_font, new_font))
                            font_replaced = True
                            break
                    
                    # If no specific mapping found, default to Arial for safety
                    # This ensures ALL text uses an Arabic-compatible font
                    if not font_replaced and 'Adobe Arabic' not in current_font and 'Arial' not in current_font:
                        # Extract font style (Regular, Bold, Italic, etc.) if present
                        if '\t' in current_font:
                            parts = current_font.split('\t')
                            elem.set('AppliedFont', f"Arial\t{parts[1] if len(parts) > 1 else 'Regular'}")
                        else:
                            elem.set('AppliedFont', 'Arial')
            
            # Write back to file
            tree.write(story_path, encoding='UTF-8', xml_declaration=True, pretty_print=False)
    
    def _reconstruct_idml(self, original_path):
        """Zip the modified directory back into IDML format"""
        # Generate output filename in uploads folder
        original_name = Path(original_path).stem
        # Save to uploads folder to ensure it persists
        uploads_dir = Path('uploads')
        uploads_dir.mkdir(exist_ok=True)
        output_path = uploads_dir / f"{original_name}_AR.idml"
        
        # Create zip archive
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    zipf.write(file_path, arcname)
        
        # Don't clean up temp directory yet - Word generator needs it
        # Cleanup will happen in translate_idml() after Word generation
        
        return str(output_path)
    
    def _generate_word_document(self, original_path):
        """Generate Word document from translated content"""
        # Generate output filename
        original_name = Path(original_path).stem
        uploads_dir = Path('uploads')
        uploads_dir.mkdir(exist_ok=True)
        word_output_path = uploads_dir / f"{original_name}_AR.docx"
        
        # Create Word document from translated IDML content
        create_word_document(self.temp_dir, str(word_output_path))
        
        return str(word_output_path)
    
    def apply_translation_edits(self, edited_translations, output_idml_path):
        """
        Apply edited translations back to the IDML file
        
        Args:
            edited_translations: List of translation dicts with 'id', 'translated' fields
            output_idml_path: Path to the IDML file to update
        
        Returns:
            Path to the updated IDML file
        """
        # Create a mapping of translation IDs to edited text
        edits_map = {t['id']: t['translated'] for t in edited_translations}
        
        # Extract the IDML
        temp_edit_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(output_idml_path, 'r') as zip_ref:
            zip_ref.extractall(temp_edit_dir)
        
        # Apply edits to each story file
        stories_dir = os.path.join(temp_edit_dir, 'Stories')
        
        for translation in self.translation_pairs:
            trans_id = translation['id']
            
            # Skip if this translation wasn't edited
            if trans_id not in edits_map:
                continue
            
            story_file = translation['story_file']
            element_idx = translation['element_index']
            new_text = edits_map[trans_id]
            
            # Parse the story file
            story_path = os.path.join(stories_dir, story_file)
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(story_path, parser)
            root = tree.getroot()
            
            # Find and update the specific Content element
            for idx, content in enumerate(root.iter('Content')):
                if idx == element_idx and content.text:
                    content.text = new_text
                    break
            
            # Write back
            tree.write(story_path, encoding='UTF-8', xml_declaration=True, pretty_print=False)
        
        # Reconstruct the IDML
        # Convert to string and ensure proper path handling
        output_path_str = str(output_idml_path)
        if output_path_str.endswith('.idml'):
            edited_idml_path = output_path_str.replace('.idml', '_edited.idml')
        else:
            edited_idml_path = output_path_str + '_edited.idml'
        
        with zipfile.ZipFile(edited_idml_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root_dir, dirs, files in os.walk(temp_edit_dir):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, temp_edit_dir)
                    zipf.write(file_path, arcname)
        
        # Clean up
        shutil.rmtree(temp_edit_dir)
        
        return edited_idml_path
