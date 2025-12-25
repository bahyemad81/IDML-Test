"""
GPS - IDML Translation Tool
Professional translation for Adobe InDesign files with beautiful animations
"""

import streamlit as st
import os
import tempfile
import time
from pathlib import Path
from translator_core import IDMLTranslator

# Page configuration
st.set_page_config(
    page_title="GPS - IDML Translation Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = 'ar'
if 'output_paths' not in st.session_state:
    st.session_state.output_paths = None
if 'translations' not in st.session_state:
    st.session_state.translations = []
if 'current_segment' not in st.session_state:
    st.session_state.current_segment = 0
if 'translation_complete' not in st.session_state:
    st.session_state.translation_complete = False

# Enhanced CSS with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        padding: 2rem;
        min-height: 100vh;
    }
    
    /* Animated Progress Stepper */
    .stepper-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 3rem auto;
        max-width: 700px;
        position: relative;
    }
    
    .step-item {
        flex: 1;
        text-align: center;
        position: relative;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .step-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        margin: 0 auto 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .step-circle.completed {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        animation: scaleIn 0.5s ease-out;
    }
    
    .step-circle.active {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .step-circle.inactive {
        background-color: #e5e7eb;
        color: #9ca3af;
    }
    
    @keyframes scaleIn {
        0% { transform: scale(0.8); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3); }
        50% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.6); }
    }
    
    .step-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        transition: color 0.3s;
        text-align: center;
        max-width: 120px;
        margin: 0 auto;
    }
    
    .step-item.active .step-label {
        color: #3b82f6;
        font-weight: 600;
    }
    
    /* Content Card with slide-in animation */
    .content-card {
        background: white;
        border-radius: 16px;
        padding: 3rem;
        max-width: 800px;
        margin: 2rem auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Enhanced drag-drop area */
    .upload-zone {
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        background: #fafbfc;
    }
    
    .upload-zone:hover {
        border-color: #3b82f6;
        background: #f0f7ff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    
    .upload-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* File display with slide-in */
    .file-display {
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: slideInRight 0.5s ease-out;
        box-shadow: 0 2px 12px rgba(16, 185, 129, 0.1);
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .file-icon {
        font-size: 2.5rem;
        animation: bounce 1s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .file-name {
        font-weight: 600;
        color: #374151;
        font-size: 1.1rem;
    }
    
    .progress-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
        animation: scaleIn 0.5s ease-out;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        border-radius: 10px;
        padding: 0.875rem 2rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }
    
    /* Loading skeleton */
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 8px;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Success animation */
    .success-checkmark {
        width: 80px;
        height: 80px;
        margin: 2rem auto;
        border-radius: 50%;
        display: block;
        stroke-width: 3;
        stroke: #10b981;
        stroke-miterlimit: 10;
        box-shadow: inset 0px 0px 0px #10b981;
        animation: fill 0.4s ease-in-out 0.4s forwards, scale 0.3s ease-in-out 0.9s both;
    }
    
    @keyframes fill {
        100% { box-shadow: inset 0px 0px 0px 40px #10b981; }
    }
    
    @keyframes scale {
        0%, 100% { transform: none; }
        50% { transform: scale3d(1.1, 1.1, 1); }
    }
    
    /* Security message */
    .security-msg {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #6b7280;
        font-size: 0.875rem;
        margin-top: 2rem;
        padding: 1rem;
        background: #f9fafb;
        border-radius: 8px;
        border-left: 3px solid #10b981;
    }
    
    /* Language selector enhancement */
    .stSelectbox {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        background-size: 200% 100%;
        animation: progressGradient 2s ease infinite;
    }
    
    @keyframes progressGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""", unsafe_allow_html=True)

# GPS Branded Header
st.markdown("""
<div style="text-align: center; margin: 2rem 0 1rem 0;">
    <div style="display: inline-flex; align-items: center; gap: 1rem; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 1.5rem 3rem; border-radius: 16px; box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);">
        <div style="font-size: 3rem; animation: rotate 3s linear infinite;">🌐</div>
        <div style="text-align: left;">
            <div style="color: white; font-size: 2rem; font-weight: 700; letter-spacing: 0.5px;">GPS</div>
            <div style="color: #93c5fd; font-size: 0.95rem; font-weight: 500;">IDML Translation Tool</div>
        </div>
    </div>
    <div style="margin-top: 1.5rem; max-width: 600px; margin-left: auto; margin-right: auto;">
        <p style="color: #475569; font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem;">
            Professional Adobe InDesign Translation
        </p>
        <p style="color: #64748b; font-size: 0.95rem; line-height: 1.6;">
            Translate IDML files with perfect formatting • RTL Support • Arabic Typography • Glossary Support
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@keyframes rotate {
    0% { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}
</style>
""", unsafe_allow_html=True)

# Progress Stepper with enhanced animations
def show_stepper(current_step):
    steps = [
        ("Upload file", 1),
        ("Set target language", 2),
        ("Translate & Download", 3),
        ("Edit and enhance text", 4)
    ]
    
    stepper_html = '<div class="stepper-container">'
    
    for i, (label, step_num) in enumerate(steps):
        if step_num < current_step:
            circle_class = "completed"
            item_class = "completed"
            icon = "✓"
        elif step_num == current_step:
            circle_class = "active"
            item_class = "active"
            icon = str(step_num)
        else:
            circle_class = "inactive"
            item_class = "inactive"
            icon = str(step_num)
        
        stepper_html += f'''
        <div class="step-item {item_class}">
            <div class="step-circle {circle_class}">{icon}</div>
            <div class="step-label">{label}</div>
        </div>
        '''
        
        if i < len(steps) - 1:
            line_color = "#3b82f6" if step_num < current_step else "#e5e7eb"
            stepper_html += f'<div style="flex: 0.5; height: 3px; background: {line_color}; margin: 0 -1rem; align-self: flex-start; margin-top: 24px; border-radius: 2px; transition: all 0.5s;"></div>'
    
    stepper_html += '</div>'
    st.markdown(stepper_html, unsafe_allow_html=True)

# STEP 1: Upload File & Select Language (Combined)
if st.session_state.step == 1:
    show_stepper(1)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📁 Upload Your IDML File")
    st.caption("Max: 20 files, 100 MB")
    
    uploaded_file = st.file_uploader(
        "Drag and Drop files",
        type=['idml'],
        help="Supported formats: idml, docx, pptx, xlsx, html, srt, txt, xliff, xlf, xml, json",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.markdown(f'''
        <div class="file-display">
            <span class="file-icon">📄</span>
            <div style="flex: 1;">
                <div class="file-name">{uploaded_file.name}</div>
                <div style="color: #6b7280; font-size: 0.875rem; margin-top: 0.25rem;">
                    {uploaded_file.size / 1024:.2f} KB • IDML File
                </div>
            </div>
            <div class="progress-badge">✓ 100%</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Language selection appears after file upload
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🌐 Select Target Language")
        
        # Display circular flag icons
        st.markdown("""
        <div style="display: flex; gap: 20px; margin: 15px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 35px; height: 35px; border-radius: 50%; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
                    <img src="https://flagcdn.com/eg.svg" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <span style="font-size: 15px; font-weight: 500;">Arabic (العربية)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 35px; height: 35px; border-radius: 50%; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
                    <img src="https://flagcdn.com/gb.svg" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <span style="font-size: 15px; font-weight: 500;">English</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Use radio buttons instead of selectbox for better flag display
        selected_lang = st.radio(
            "Target Language",
            options=["🇪🇬 Arabic (العربية)", "🇬🇧 English"],
            index=0,
            label_visibility="collapsed",
            horizontal=True
        )
        
        # Map selection to language code
        st.session_state.target_lang = 'ar' if 'Arabic' in selected_lang else 'en'
        
    else:
        st.markdown('''
        <div class="upload-zone">
            <div class="upload-icon">📤</div>
            <div style="font-size: 1.1rem; font-weight: 500; color: #374151; margin-bottom: 0.5rem;">
                Drag and drop your IDML file here
            </div>
            <div style="color: #6b7280; font-size: 0.875rem;">
                or click to browse
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div class="security-msg">🔒 Your data is secured with TLS encryption</div>', unsafe_allow_html=True)
    
    if uploaded_file:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 1])
        with col3:
            if st.button("Continue →", type="primary", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: Translate & Download
elif st.session_state.step == 2:
    show_stepper(3)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    
    if st.button("← Back"):
        st.session_state.step = 2
        st.rerun()
    
    st.markdown("### 🚀 Ready to Translate")
    
    if st.session_state.uploaded_file:
        st.info(f"📄 **File:** {st.session_state.uploaded_file.name}")
        st.info(f"🌐 **Target:** {'Arabic (العربية)' if st.session_state.target_lang == 'ar' else 'English'}")
    
    if not st.session_state.translation_complete:
        if st.button("✨ Start Translation", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Save uploaded file to temp location
                temp_path = os.path.join(tempfile.gettempdir(), f"upload_{st.session_state.uploaded_file.name}")
                with open(temp_path, 'wb') as f:
                    f.write(st.session_state.uploaded_file.getvalue())
                    f.flush()  # Ensure data is written to disk
                    os.fsync(f.fileno())  # Force write to disk
                
                # Small delay to ensure file system has processed the write
                time.sleep(0.1)
                
                def update_progress(message, percentage):
                    progress_bar.progress(percentage / 100)
                    status_text.markdown(f"**{message}** ({percentage}%)")
                
                translator = IDMLTranslator(target_lang=st.session_state.target_lang)
                output_paths = translator.translate_idml(temp_path, update_progress)
                
                st.session_state.output_paths = output_paths
                st.session_state.translations = output_paths.get('translations', [])
                st.session_state.translation_complete = True
                
                os.remove(temp_path)
                
                progress_bar.progress(100)
                status_text.markdown("**✅ Translation complete!**")
                
                # Success animation
                st.markdown('''
                <svg class="success-checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                    <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                    <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                </svg>
                ''', unsafe_allow_html=True)
                
                time.sleep(1)
                st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Translation failed: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    # After translation - offer to edit or download
    if st.session_state.translation_complete and st.session_state.output_paths:
        st.success("🎉 **Translation completed successfully!**")
        
        # === TRANSLATION REPORT ===
        st.markdown("### 📊 Translation Report")
        
        # Calculate statistics
        total_segments = len(st.session_state.translations)
        total_words = sum(len(t['original'].split()) for t in st.session_state.translations)
        total_chars = sum(len(t['original']) for t in st.session_state.translations)
        unique_segments = len(set(t['original'] for t in st.session_state.translations))
        
        # Statistics grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Text segments", total_segments)
        
        with col2:
            st.metric("Unique segments", unique_segments)
        
        with col3:
            st.metric("Words", total_words)
        
        with col4:
            st.metric("Characters", total_chars)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 🎯 Next Steps")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Review & Edit Translations", type="primary", use_container_width=True):
                st.session_state.step = 4  # Go to editing page
                st.rerun()
        
        with col2:
            if st.button("🔄 Translate Another File", use_container_width=True, key="translate_another_top"):
                st.session_state.step = 1
                st.session_state.translation_complete = False
                st.session_state.uploaded_file = None
                st.session_state.output_paths = None
                st.session_state.translations = []
                st.rerun()
        
        # Show download section
        st.markdown("---")
        st.markdown("### 📥 Download Your Files")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with open(st.session_state.output_paths['idml'], 'rb') as f:
                st.download_button(
                    label="📄 Download IDML File",
                    data=f.read(),
                    file_name=Path(st.session_state.output_paths['idml']).name,
                    mime="application/octet-stream",
                    use_container_width=True
                )
        
        with col2:
            with open(st.session_state.output_paths['word'], 'rb') as f:
                st.download_button(
                    label="📝 Download Word Document",
                    data=f.read(),
                    file_name=Path(st.session_state.output_paths['word']).name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Translate Another File", use_container_width=True, key="translate_another_bottom"):
            st.session_state.step = 1
            st.session_state.translation_complete = False
            st.session_state.uploaded_file = None
            st.session_state.output_paths = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 4: Edit and Enhance Text
elif st.session_state.step == 4:
    show_stepper(4)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    
    st.markdown("### ✏️ Review & Edit Translations")
    
    if not st.session_state.translations:
        st.warning("No translations available to edit.")
        if st.button("← Back"):
            st.session_state.step = 3
            st.rerun()
    else:
        total_segments = len(st.session_state.translations)
        
        # Navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("← Previous", disabled=st.session_state.current_segment == 0):
                st.session_state.current_segment = max(0, st.session_state.current_segment - 1)
                st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center;'><strong>Segment {st.session_state.current_segment + 1} of {total_segments}</strong></div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("Next →", disabled=st.session_state.current_segment >= total_segments - 1):
                st.session_state.current_segment = min(total_segments - 1, st.session_state.current_segment + 1)
                st.rerun()
        
        st.markdown("---")
        
        # Current segment
        current = st.session_state.translations[st.session_state.current_segment]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original:**")
            st.info(current['original'])
        
        with col2:
            st.markdown("**Translation:**")
            edited_text = st.text_area(
                "Edit",
                value=current['translated'],
                height=150,
                key=f"edit_{st.session_state.current_segment}",
                label_visibility="collapsed"
            )
            
            if edited_text != current['translated']:
                if st.button("💾 Save", type="primary"):
                    st.session_state.translations[st.session_state.current_segment]['translated'] = edited_text
                    st.success("✅ Saved!")
                    time.sleep(0.3)
                    st.rerun()
        
        st.markdown("---")
        
        # === TRANSLATION STATISTICS ===
        st.markdown("### 📊 Translation Statistics")
        
        total_segments = len(st.session_state.translations)
        total_original_words = sum(len(t['original'].split()) for t in st.session_state.translations)
        total_translated_words = sum(len(t['translated'].split()) for t in st.session_state.translations)
        total_translated_chars = sum(len(t['translated']) for t in st.session_state.translations)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Segments", total_segments)
        
        with col2:
            st.metric("Original Words", total_original_words)
        
        with col3:
            st.metric("Translated Words", total_translated_words)
        
        with col4:
            st.metric("Characters", total_translated_chars)
        
        # === DOWNLOAD SECTION ===
        st.markdown("---")
        st.markdown("### 📥 Download Edited Files")
        # Apply Edits Button
        if st.button("🔄 Apply All Edits to Files", type="primary", use_container_width=True, key="apply_edits_step4"):
            with st.spinner("Applying your edits to files..."):
                try:
                    from translator_core import IDMLTranslator
                    from word_generator import create_word_document
                    
                    # Add IDs to translations if missing
                    translations_with_ids = []
                    for idx, t in enumerate(st.session_state.translations):
                        trans_copy = t.copy()
                        if 'id' not in trans_copy:
                            trans_copy['id'] = idx + 1
                        translations_with_ids.append(trans_copy)
                    
                    translator = IDMLTranslator(target_lang=st.session_state.get('target_lang', 'ar'))
                    translator.translation_pairs = translations_with_ids
                    
                    # Get IDML path and convert to absolute path
                    idml_path = st.session_state.output_paths.get('idml')
                    if not isinstance(idml_path, str):
                        st.error(f"Invalid IDML path type: {type(idml_path)}. Expected string.")
                        st.code(f"output_paths: {st.session_state.output_paths}")
                        raise TypeError("IDML path must be a string")
                    
                    # Convert to absolute path if it's relative
                    if not os.path.isabs(idml_path):
                        idml_path = os.path.abspath(idml_path)
                    
                    # Apply edits to IDML
                    edited_idml = translator.apply_translation_edits(
                        translations_with_ids,
                        idml_path
                    )
                    st.session_state.output_paths['idml'] = edited_idml
                    
                    # Regenerate Word
                    edited_word = create_word_document(translations_with_ids, edited_idml)
                    st.session_state.output_paths['word'] = edited_word
                    
                    st.success("✅ All edits applied to files!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error applying edits: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
        
        st.info("💡 Click 'Apply All Edits' above to update files with your changes, then download below.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with open(st.session_state.output_paths['idml'], 'rb') as f:
                st.download_button(
                    label="📄 Download IDML File",
                    data=f.read(),
                    file_name=Path(st.session_state.output_paths['idml']).name,
                    mime="application/octet-stream",
                    use_container_width=True,
                    type="primary",
                    key="download_idml_edit"
                )
        
        with col2:
            with open(st.session_state.output_paths['word'], 'rb') as f:
                st.download_button(
                    label="📝 Download Word Document",
                    data=f.read(),
                    file_name=Path(st.session_state.output_paths['word']).name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    type="primary",
                    key="download_word_edit"
                )
        
        # === NAVIGATION ===
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("← Back to Report", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
        
        with col2:
            if st.button("🔄 Translate Another File", use_container_width=True, key="translate_another_edit"):
                st.session_state.step = 1
                st.session_state.translation_complete = False
                st.session_state.uploaded_file = None
                st.session_state.output_paths = None
                st.session_state.translations = []
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.875rem; padding: 1rem;">
    Built with ❤️ | FREE Translation | No API Key Required
</div>
""", unsafe_allow_html=True)
