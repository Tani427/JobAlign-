import argparse
import os
import re

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

AI_MARKERS = [
    "delve", "testament", "orchestrated", "spearheaded", "tapestry", 
    "seamlessly", "unwavering", "meticulous", "synergy", "pivotal", 
    "navigate", "fostered", "realm", "profound", "multifaceted", "dynamic"
]

SCAM_MARKERS = [
    "western union", "wire transfer", "processing fee", "upfront payment", 
    "money order", "kindly", "guaranteed income", "crypto", "bitcoin",
    "confidential company", "undisclosed client", "account detail"
]

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == '.pdf':
        if PyPDF2 is None:
            print("Error: PyPDF2 is not installed. Run 'pip install PyPDF2' to read PDFs.")
            return ""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
        except Exception as e:
            print(f"Error reading PDF: {e}")
    elif ext in ['.doc', '.docx']:
        if docx is None:
            print("Error: python-docx is not installed. Run 'pip install python-docx' to read DOCX files.")
            return ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "
        except Exception as e:
            print(f"Error reading DOCX: {e}")
    elif ext == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
    else:
        print(f"Unsupported file format: {ext}")
    return text

def analyze_text(text):
    text_lower = text.lower()
    
    ai_matches = {}
    for marker in AI_MARKERS:
        # Match whole words only
        count = len(re.findall(r'\b' + re.escape(marker) + r'\b', text_lower))
        if count > 0:
            ai_matches[marker] = count
            
    scam_matches = {}
    for marker in SCAM_MARKERS:
        count = len(re.findall(r'\b' + re.escape(marker) + r'\b', text_lower))
        if count > 0:
            scam_matches[marker] = count
            
    return ai_matches, scam_matches

def generate_report(ai_matches, scam_matches, total_words):
    print("=" * 50)
    print("RESUME ANALYSIS REPORT")
    print("=" * 50)
    
    print(f"\nTotal Words Analyzed: {total_words}")
    
    print("\n--- AI Generation Markers ---")
    ai_total = sum(ai_matches.values())
    if ai_total == 0:
        print("No obvious AI markers found. (Low Risk)")
    else:
        print(f"Found {ai_total} instances of common AI buzzwords.")
        for word, count in ai_matches.items():
            print(f"  - '{word}': {count} time(s)")
            
        if ai_total > 5:
            print("Risk Level: HIGH (Likely AI-assisted or generated)")
        elif ai_total > 2:
            print("Risk Level: MEDIUM (Possible AI assistance)")
        else:
            print("Risk Level: LOW (Minimal AI markers)")

    print("\n--- Scam/Fraud Indicators ---")
    scam_total = sum(scam_matches.values())
    if scam_total == 0:
        print("No obvious scam indicators found. (Low Risk)")
    else:
        print(f"Found {scam_total} suspicious phrases.")
        for word, count in scam_matches.items():
            print(f"  - '{word}': {count} time(s)")
            
        if scam_total > 2:
            print("Risk Level: HIGH (Strong indications of a scam)")
        else:
            print("Risk Level: MEDIUM (Suspicious language present)")
            
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description="Analyze a resume for AI generation and scam markers.")
    parser.add_argument("file_path", help="Path to the resume file (.pdf, .docx, .txt)")
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"File not found: {args.file_path}")
        return
        
    print(f"Analyzing {args.file_path}...")
    text = extract_text(args.file_path)
    
    if not text.strip():
        print("Could not extract any text from the file.")
        return
        
    words = text.split()
    total_words = len(words)
    
    ai_matches, scam_matches = analyze_text(text)
    generate_report(ai_matches, scam_matches, total_words)

if __name__ == "__main__":
    main()
