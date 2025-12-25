# -*- coding: utf-8 -*-
"""
Simple Translation Module using FREE Google Translate
Supports bidirectional translation (English ↔ Arabic)
No API key required!
"""

import sys
import io

# Fix Windows encoding issues (handle closed file gracefully)
# Only apply when not running in Streamlit (Streamlit manages its own streams)
if sys.platform == 'win32' and not hasattr(sys.stdout, '_is_wrapped'):
    try:
        if hasattr(sys.stdout, 'buffer') and not sys.stdout.closed:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stdout._is_wrapped = True
        if hasattr(sys.stderr, 'buffer') and not sys.stderr.closed:
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
            sys.stderr._is_wrapped = True
    except (ValueError, AttributeError, OSError):
        pass  # Ignore if already closed or no buffer

from deep_translator import GoogleTranslator

def translate_text(text, target_lang='ar', source_lang='auto'):
    """
    Translate text to target language using free Google Translate
    
    Args:
        text: Text to translate
        target_lang: Target language code ('ar' for Arabic, 'en' for English)
        source_lang: Source language code ('auto' for auto-detect)
    
    Returns:
        Translated text
    """
    try:
        if not text or not text.strip():
            return text
        
        # Use Google Translate (free, no API key needed)
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        
        return translated
    except Exception as e:
        # Silently return original text if translation fails
        return text


def translate_to_arabic(text):
    """Translate text to Arabic (backward compatibility)"""
    return translate_text(text, target_lang='ar', source_lang='auto')


def translate_to_english(text):
    """Translate text to English"""
    return translate_text(text, target_lang='en', source_lang='auto')
