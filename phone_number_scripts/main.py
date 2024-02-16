import re
import pypdf


def extract_phone_numbers_from_pdf(pdf_path):
    phone_numbers = []

    try:
        # Attempt to read the PDF with UTF-8 encoding. Adjust if needed based on your PDF's encoding.
        pdf_reader = pypdf.PdfReader(pdf_path)
        num_pages = len(pdf_reader.pages)

        # Extract text from all pages (replace with page-specific extraction if needed)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]

            # Check for potential truncation errors before decoding:
            page_text = page.extract_text().strip()
            if '\\U' in page_text:  # Check for escape sequences
                raise ValueError("Truncated escape sequences might exist. Adjust encoding or handle manually.")

            # Decode text based on PDF encoding (replace 'latin-1' with actual encoding):
            page_text = page_text.encode('latin-1', errors='replace')

            # Handle remaining encoding issues (replace if needed):
            page_text = page_text.decode('utf-8', errors='replace')

            # Handle non-breaking spaces:
            page_text = page_text.replace('\x0c', ' ')

            # Find phone numbers (adjust the regex if needed):
            phone_numbers.extend(re.findall(r"((?:\+?\d{1,2}[ \.-])?\d{3}[ \.-]?(\d{3}[ \.-]?\d{4})|((\(\d{3}\) )?\d{"
                                            r"3}[ \.-]?\d{4}))"
                                          r"[ \/]?(x\w*|ext\.\w*|[ \.-]?\d+)?", page_text))

    except pypdf.errors.PdfReadError as e:
        print(f"Error reading PDF: {e}")
        return []
    except ValueError as e:
        print(f"Error: {e}")
        return []
    except re.error as e:
        print(f"Error finding phone numbers: {e}")
        return []

    top_phone_number = phone_numbers[0]

    # Remove duplicates while preserving order
    return list(set(phone_numbers))[0]
