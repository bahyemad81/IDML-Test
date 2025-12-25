# -*- coding: utf-8 -*-
"""
Quick test to verify the translator works with English target
"""

from translator_core import IDMLTranslator
import tempfile
import shutil

# Test with a dummy IDML file path (we'll just test the translator initialization)
translator_ar = IDMLTranslator(target_lang='ar')
translator_en = IDMLTranslator(target_lang='en')

print(f"Arabic translator target_lang: {translator_ar.target_lang}")
print(f"English translator target_lang: {translator_en.target_lang}")

# Test translation function directly
from simple_translator import translate_text

arabic_text = "مصر هي واحدة من أقدم دول العالم"
print(f"\nOriginal Arabic: {arabic_text}")

english_result = translate_text(arabic_text, target_lang='en', source_lang='ar')
print(f"Translated to English: {english_result}")

if english_result != arabic_text and 'Egypt' in english_result:
    print("\n✅ Translation to English WORKS!")
else:
    print("\n❌ Translation to English FAILED!")
    print(f"Expected English text, got: {english_result}")
