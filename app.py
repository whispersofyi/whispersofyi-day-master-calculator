<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

/* Global styles */
.stApp {
    background-color: #fafafa;
    font-family: 'Inter', sans-serif;
    color: #2c3e50; /* Added text color */
}

/* Typography */
h1, h2, h3 {
    font-family: 'Crimson Text', serif;
    color: #2c3e50 !important; /* Added !important to ensure it overrides */
}

h1 {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    text-align: center;
    border-bottom: 1px solid #e8e8e8;
    padding-bottom: 1rem;
    color: #2c3e50 !important; /* Explicit color */
}

.subtitle {
    font-style: italic;
    color: #6c757d;
    text-align: center;
    margin-bottom: 2rem;
    font-size: 1.1rem;
    line-height: 1.6;
}

/* Sidebar styling */
.stSidebar {
    background-color: #ffffff;
    border-right: 1px solid #e8e8e8;
    box-shadow: 0 0 10px rgba(0,0,0,0.05);
    color: #2c3e50; /* Added text color */
}

.stSidebar .stSelectbox label,
.stSidebar .stNumberInput label {
    font-weight: 500;
    color: #495057;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

/* Form elements */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    color: #495057;
}

.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: #6c757d;
    box-shadow: 0 0 0 0.1rem rgba(108, 117, 125, 0.25);
}

/* Button styling - FIXED HOVER ISSUE */
.stButton > button {
    background-color: #495057;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.75rem 2rem;
    font-weight: 500;
    width: 100%;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #343a40 !important; /* Added !important */
    color: white !important; /* Ensure text stays visible */
    transform: translateY(-1px);
}

/* Content containers */
.result-container {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border-left: 4px solid #6c757d;
    color: #2c3e50; /* Added text color */
}

.day-master-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e8e8e8;
}

.day-master-title {
    font-size: 2rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
    font-family: 'Crimson Text', serif;
}

.day-master-element {
    font-size: 1.2rem;
    color: #6c757d;
    font-weight: 300;
}

.description-text {
    line-height: 1.8;
    color: #495057;
    margin-bottom: 2rem;
    font-size: 1.1rem;
    text-align: justify;
}

/* Trait sections */
.trait-section {
    margin: 1.5rem 0;
    background-color: #f8f9fa;
    border-radius: 6px;
    padding: 1.5rem;
    color: #2c3e50; /* Added text color */
}

.trait-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
    font-family: 'Crimson Text', serif;
}

.trait-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.trait-item {
    padding: 0.5rem 0;
    border-bottom: 1px solid #e9ecef;
    color: #495057;
    line-height: 1.6;
}

.trait-item:last-child {
    border-bottom: none;
}

/* Four Pillars display */
.pillars-container {
    display: flex;
    justify-content: space-between;
    margin: 2rem 0;
    gap: 1rem;
}

.pillar-card {
    flex: 1;
    background-color: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 6px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    color: #2c3e50; /* Added text color */
}

.pillar-title {
    font-size: 0.9rem;
    color: #6c757d;
    font-weight: 500;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.pillar-content {
    font-size: 1.5rem;
    color: #2c3e50;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.pillar-description {
    font-size: 0.85rem;
    color: #6c757d;
}

/* Instructions */
.instructions {
    background-color: #e7f3ff;
    border: 1px solid #b8daff;
    border-radius: 6px;
    padding: 1.5rem;
    margin: 2rem 0;
    color: #004085;
}

/* Error and success messages */
.error-message {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
    padding: 1rem;
    margin: 1rem 0;
}

.success-message {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
    border-radius: 4px;
    padding: 1rem;
    margin: 1rem 0;
}

/* Responsive design */
@media (max-width: 768px) {
    .pillars-container {
        flex-direction: column;
    }
    
    h1 {
        font-size: 2rem;
    }
}

/* Additional global text color fixes */
.stMarkdown, .stText, .stNumberInput, .stSelectbox {
    color: #2c3e50;
}
</style>
