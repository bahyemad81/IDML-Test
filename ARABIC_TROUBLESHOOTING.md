# Arabic Text Rendering - Troubleshooting Guide

## Latest Fixes Applied

### 1. Correct Language ID Format
Changed from `Language:Arabic` to `Language:$ID/Arabic` (InDesign's internal format)

### 2. Removed Invalid Attributes
- Removed `Composer` from `CharacterStyleRange` (it only belongs on `ParagraphStyleRange`)

### 3. Added Critical Arabic Attributes
```python
# On ParagraphStyleRange:
- AppliedLanguage: 'Language:$ID/Arabic'
- DigitsType: 'DefaultDigits'
- Composer: 'Adobe World-Ready Paragraph Composer'
- StoryDirection: 'RightToLeftDirection'

# On CharacterStyleRange:
- AppliedLanguage: 'Language:$ID/Arabic'
- DigitsType: 'DefaultDigits'
- KashidaWidth: 'Medium'
- KerningMethod: 'Optical'
```

### 4. Aggressive Font Mapping
- ALL fonts now mapped to Arabic-compatible fonts (Adobe Arabic or Arial)
- Prevents any font from blocking Arabic letter joining

## If Still Not Working

### Check in InDesign:
1. Open the file
2. Select the Arabic text
3. Go to **Character Panel** (Ctrl+T / Cmd+T)
4. Check the **Language** setting - should show "Arabic"
5. Go to **Paragraph Panel**
6. Check **Composer** - should show "Adobe World-Ready Paragraph Composer"

### Manual Fix in InDesign:
1. Select all text (Ctrl+A / Cmd+A)
2. **Character Panel** → Set Language to "Arabic"
3. **Paragraph Panel** → Set Composer to "Adobe World-Ready Paragraph Composer"
4. **Character Panel** → Set Font to "Adobe Arabic" or "Arial"

## Common Causes

1. **Font doesn't support Arabic** → Use Adobe Arabic or Arial
2. **Language not set** → Must be "Arabic" for letter shaping
3. **Wrong Composer** → Must be "World-Ready" not "Single-line"
4. **Missing font** → InDesign substitutes with incompatible font

## Re-translate Your File

The latest version of the translator includes all these fixes. Re-translate your IDML file to apply them.
