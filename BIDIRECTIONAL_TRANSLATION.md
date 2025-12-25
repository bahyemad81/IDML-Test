# Bidirectional Translation Support

## Overview

The IDML Translation Tool now supports **bidirectional translation**:
- ✅ **English → Arabic** (with RTL formatting)
- ✅ **Arabic → English** (with LTR formatting)

## How It Works

### Language Detection

The translator automatically applies the correct formatting based on the **target language**:

```python
translator = IDMLTranslator(target_lang='ar')  # For Arabic
translator = IDMLTranslator(target_lang='en')  # For English
```

### Arabic → English Translation

**What happens:**
1. Text is translated from Arabic to English
2. **LTR (Left-to-Right)** direction is applied
3. **English language ID** is set in InDesign
4. **Standard Adobe Paragraph Composer** is used
5. **Left alignment** is applied
6. Letters display correctly (no disconnection)

**InDesign Attributes Set:**
```xml
<ParagraphStyleRange 
    Composer="Adobe Paragraph Composer"
    StoryDirection="LeftToRightDirection"
    Justification="LeftAlign"
    AppliedLanguage="Language:$ID/English: USA"
/>

<CharacterStyleRange
    AppliedLanguage="Language:$ID/English: USA"
    KerningMethod="Optical"
/>
```

### English → Arabic Translation

**What happens:**
1. Text is translated from English to Arabic
2. **RTL (Right-to-Left)** direction is applied
3. **Arabic language ID** is set in InDesign
4. **World-Ready Paragraph Composer** is used (for Arabic letter joining)
5. **Right alignment** is applied
6. **Kashida** and **DigitsType** are configured for Arabic typography

**InDesign Attributes Set:**
```xml
<ParagraphStyleRange 
    Composer="Adobe World-Ready Paragraph Composer"
    StoryDirection="RightToLeftDirection"
    Justification="RightAlign"
    AppliedLanguage="Language:$ID/Arabic"
    DigitsType="DefaultDigits"
/>

<CharacterStyleRange
    AppliedLanguage="Language:$ID/Arabic"
    DigitsType="DefaultDigits"
    KashidaWidth="Medium"
    KerningMethod="Optical"
/>
```

## Key Differences

| Feature | English | Arabic |
|---------|---------|--------|
| **Text Direction** | LTR (Left-to-Right) | RTL (Right-to-Left) |
| **Composer** | Adobe Paragraph Composer | Adobe World-Ready Paragraph Composer |
| **Alignment** | LeftAlign | RightAlign |
| **Language ID** | Language:$ID/English: USA | Language:$ID/Arabic |
| **Letter Joining** | Not needed | Critical (via World-Ready Composer) |
| **Kashida** | Not used | Medium (for justification) |
| **Digits** | Standard | DefaultDigits |

## Why This Matters

### Problem Before Fix

When translating Arabic → English, the tool was applying Arabic formatting:
- ❌ RTL direction (text flows right-to-left)
- ❌ World-Ready Composer (unnecessary for English)
- ❌ Arabic language ID
- ❌ Result: Disconnected letters, wrong direction

### Solution After Fix

Now the tool detects the target language and applies appropriate formatting:
- ✅ English gets LTR + standard composer
- ✅ Arabic gets RTL + World-Ready composer
- ✅ Proper letter rendering in both languages
- ✅ Correct text direction

## Usage in Streamlit App

The Streamlit app already has a language selector:

```python
target_language = st.selectbox(
    "🌐 Target Language",
    options=[
        ("Arabic (العربية)", "ar"),
        ("English", "en")
    ]
)
```

Users can now:
1. Upload an Arabic IDML file
2. Select "English" as target language
3. Get properly formatted English text (LTR, connected letters)

OR

1. Upload an English IDML file
2. Select "Arabic" as target language
3. Get properly formatted Arabic text (RTL, joined letters)

## Technical Implementation

### Files Modified

1. **translator_core.py**
   - `_fix_styles_xml()` - Now conditional based on target_lang
   - `_translate_stories()` - Applies language-specific formatting
   - `_translate_text()` - Passes target_lang to translator

2. **simple_translator.py**
   - Already supported bidirectional translation
   - Uses `deep-translator` library

3. **requirements.txt**
   - Changed from `googletrans` to `deep-translator`
   - More reliable and actively maintained

## Testing

### Test Arabic → English

1. Upload an Arabic IDML file
2. Select "English" as target language
3. Download translated file
4. Open in InDesign
5. Verify:
   - ✅ Text flows left-to-right
   - ✅ Letters are connected properly
   - ✅ Alignment is left
   - ✅ Language shows as "English"

### Test English → Arabic

1. Upload an English IDML file
2. Select "Arabic" as target language
3. Download translated file
4. Open in InDesign
5. Verify:
   - ✅ Text flows right-to-left
   - ✅ Arabic letters join correctly
   - ✅ Alignment is right
   - ✅ Language shows as "Arabic"

## Benefits

✅ **True bidirectional support** - Works both ways
✅ **Proper formatting** - Each language gets correct settings
✅ **No manual fixes needed** - InDesign opens files correctly
✅ **Professional results** - Typography rules respected
✅ **User-friendly** - Just select target language in dropdown

## Future Enhancements

Potential additions:
- Support for more languages (French, Spanish, etc.)
- Custom font mapping per language
- Preserve original alignment (if centered, keep centered)
- Language-specific typography rules
