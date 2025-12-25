// IDML Arabic Translator - Frontend JavaScript

let selectedFile = null;

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const dropzoneContent = document.querySelector('.dropzone-content');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFile');
const translateBtn = document.getElementById('translateBtn');
const downloadBtn = document.getElementById('downloadBtn');
const progressSection = document.getElementById('progressSection');
const progressLabel = document.getElementById('progressLabel');
const progressPercentage = document.getElementById('progressPercentage');
const progressFill = document.getElementById('progressFill');
const messageDiv = document.getElementById('message');
const apiKeyInput = document.getElementById('apiKey');

// Event Listeners
dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('dragover', handleDragOver);
dropzone.addEventListener('dragleave', handleDragLeave);
dropzone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
removeFileBtn.addEventListener('click', handleRemoveFile);
translateBtn.addEventListener('click', handleTranslate);
apiKeyInput.addEventListener('input', validateForm);

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    dropzone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    dropzone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    dropzone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.idml')) {
        showMessage('Please select a valid IDML file', 'error');
        return;
    }
    
    // Validate file size (50MB max)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        showMessage('File size exceeds 50MB limit', 'error');
        return;
    }
    
    selectedFile = file;
    
    // Update UI
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    dropzoneContent.style.display = 'none';
    filePreview.style.display = 'flex';
    
    validateForm();
    hideMessage();
}

function handleRemoveFile(e) {
    e.stopPropagation();
    selectedFile = null;
    fileInput.value = '';
    
    dropzoneContent.style.display = 'block';
    filePreview.style.display = 'none';
    
    validateForm();
    hideProgress();
    hideDownloadButtons();
}

function validateForm() {
    const hasFile = selectedFile !== null;
    // API key is now optional since we're using free translation
    translateBtn.disabled = !hasFile;
}

async function handleTranslate() {
    if (!selectedFile) {
        showMessage('Please select an IDML file', 'error');
        return;
    }
    
    // API key is optional now - using free translation
    const apiKey = apiKeyInput.value.trim();
    
    // Get target language
    const targetLang = document.getElementById('targetLanguage').value;
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('target_lang', targetLang);
    if (apiKey) {
        formData.append('api_key', apiKey);  // Optional
    }
    
    // Update UI
    translateBtn.disabled = true;
    translateBtn.classList.add('loading');
    showProgress();
    hideMessage();
    hideDownloadButtons();
    
    try {
        // Simulate progress (since we can't get real-time progress from the backend easily)
        simulateProgress();
        
        const response = await fetch('/api/translate', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Translation failed');
        }
        
        // Get JSON response with both file names
        const data = await response.json();
        
        if (!data.success) {
            throw new Error('Translation failed');
        }
        
        // Create download buttons for both files
        showDownloadButtons(data.idml_file, data.word_file);
        
        // Update progress to 100%
        updateProgress('Translation complete!', 100);
        
        // Show success message
        showMessage('Translation completed successfully! Download your files below.', 'success');
        
    } catch (error) {
        console.error('Translation error:', error);
        showMessage(error.message || 'Translation failed. Please try again.', 'error');
        hideProgress();
    } finally {
        translateBtn.disabled = false;
        translateBtn.classList.remove('loading');
    }
}

function simulateProgress() {
    const stages = [
        { label: 'Extracting IDML file...', progress: 10 },
        { label: 'Applying Arabic formatting rules...', progress: 20 },
        { label: 'Translating text content...', progress: 40 },
        { label: 'Processing translation...', progress: 60 },
        { label: 'Mapping fonts for Arabic...', progress: 80 },
        { label: 'Reconstructing IDML file...', progress: 90 },
        { label: 'Generating Word document...', progress: 95 }
    ];
    
    let currentStage = 0;
    
    const interval = setInterval(() => {
        if (currentStage < stages.length) {
            const stage = stages[currentStage];
            updateProgress(stage.label, stage.progress);
            currentStage++;
        } else {
            clearInterval(interval);
        }
    }, 2000);
}

function updateProgress(label, progress) {
    progressLabel.textContent = label;
    progressPercentage.textContent = `${progress}%`;
    progressFill.style.width = `${progress}%`;
}

function showProgress() {
    progressSection.style.display = 'block';
    updateProgress('Starting translation...', 0);
}

function hideProgress() {
    progressSection.style.display = 'none';
}

function showDownloadButtons(idmlFile, wordFile) {
    // Create or update download buttons container
    let downloadSection = document.getElementById('downloadButtons');
    if (!downloadSection) {
        downloadSection = document.createElement('div');
        downloadSection.id = 'downloadButtons';
        downloadSection.style.marginTop = '20px';
        downloadSection.style.display = 'flex';
        downloadSection.style.flexDirection = 'column';
        downloadSection.style.gap = '10px';
        downloadBtn.parentNode.insertBefore(downloadSection, downloadBtn.nextSibling);
    }
    
    downloadSection.innerHTML = `
        <a href="/api/download/idml/${idmlFile}" class="btn-download">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            <span>Download IDML File</span>
        </a>
        <a href="/api/download/word/${wordFile}" class="btn-download" style="background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            <span>Download Word Document</span>
        </a>
    `;
    
    downloadSection.style.display = 'flex';
    downloadBtn.style.display = 'none'; // Hide old button
}

function hideDownloadButtons() {
    const downloadSection = document.getElementById('downloadButtons');
    if (downloadSection) {
        downloadSection.style.display = 'none';
    }
    downloadBtn.style.display = 'none';
}

function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
}

function hideMessage() {
    messageDiv.style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
