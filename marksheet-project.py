from PIL import Image
import pytesseract
import re

# Set the tesseract executable path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Try to enhance image for better OCR (convert to grayscale, increase contrast)
    image = Image.open(image_path).convert('L')
    # Optionally, apply thresholding for binarization
    # image = image.point(lambda x: 0 if x < 140 else 255, '1')
    text = pytesseract.image_to_string(image)
    return text

def extract_specific_fields(text):
    # Try to extract name and register number from the line after 'NAME OF THE CANDIDATE'
    name, reg_no = None, None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if 'NAME OF THE CANDIDATE' in line.upper():
            # Look for the next non-empty line
            for j in range(i+1, min(i+4, len(lines))):
                next_line = lines[j].strip()
                if next_line:
                    # Try to split name and reg no if both are present
                    match = re.match(r'([A-Z ]+)[^A-Z0-9]*([A-Z0-9]{6,})?', next_line, re.IGNORECASE)
                    if match:
                        name = match.group(1).strip()
                        if match.lastindex and match.lastindex >= 2:
                            reg_no = match.group(2)
                    else:
                        name = next_line
                    break
    # Fallback: Try to find register number anywhere
    if not reg_no:
        reg_match = re.search(r'REGISTER\s*NUMBER[^A-Z0-9]*([A-Z0-9]{6,})', text, re.IGNORECASE)
        if reg_match:
            reg_no = reg_match.group(1)
    # Programme/Branch: Try to find a line with 'PROGRAMME' or 'BRANCH'
    programme = None
    for line in lines:
        if 'PROGRAMME' in line.upper() or 'BRANCH' in line.upper():
            programme = line.strip()
            break
    return name, programme, reg_no

def extract_subjects_and_marks(text):
    subjects = []
    marks = []
    in_table = False
    table_lines = []
    for line in text.splitlines():
        # Detect start of table
        if re.search(r'SUBJECT TITLE', line, re.IGNORECASE):
            in_table = True
            continue
        if in_table:
            # End of table (heuristic: empty line or end marker)
            if not line.strip() or 'End of Statement' in line:
                break
            table_lines.append(line)
            # Extract subject: look for a pattern after a code (e.g., 24LAFO} French-I ...)
            subject_match = re.search(r'\|?\s*([A-Za-z\-: ]{3,})\s+\d', line)
            # Extract marks: last integer before a grade (O P, P, etc.)
            mark_candidates = [int(s) for s in re.findall(r'\b\d{1,3}\b', line)]
            grade_match = re.search(r'(O\s*P|P|A\+|B\+|TP|d|\|P)', line)
            if subject_match and mark_candidates:
                subject = subject_match.group(1).strip()
                # Heuristic: pick the last integer before the grade
                if grade_match:
                    grade_pos = grade_match.start()
                    # Find the last integer before the grade
                    mark = None
                    for m in re.finditer(r'\b\d{1,3}\b', line):
                        if m.start() < grade_pos:
                            mark = int(m.group())
                        else:
                            break
                    if mark is not None:
                        subjects.append(subject)
                        marks.append(mark)
                else:
                    # Fallback: last integer in the line
                    subjects.append(subject)
                    marks.append(mark_candidates[-1])
    return subjects, marks, table_lines

if __name__ == "__main__":
    image_path = "test-marksheet.jpg"
    text = extract_text_from_image(image_path)
    print("--- OCR Output ---")
    print(text)

    name, programme, reg_no = extract_specific_fields(text)
    print("--- Extracted Fields ---")
    print(f"Name: {name}")
    print(f"Programme & Branch: {programme}")
    print(f"Register Number: {reg_no}")

    subjects, marks, table_lines = extract_subjects_and_marks(text)
    print("--- Subjects and Marks ---")
    for subj, mark in zip(subjects, marks):
        print(f"{subj}: {mark}") 