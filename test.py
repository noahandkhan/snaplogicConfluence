import fitz  # PyMuPDF

def extract_text_with_positions(pdf_path):
    document = fitz.open(pdf_path)
    text_positions = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block['type'] == 0:  # type 0 indicates text
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_positions.append({
                            "text": span["text"],
                            "x": span["bbox"][0],  # x coordinate
                            "y": span["bbox"][1],  # y coordinate
                            "size": span["size"],  # font size
                            "width": span["bbox"][2] - span["bbox"][0],  # width of the text box
                        })
    return text_positions

def associate_fields_with_values(text_positions, threshold=20):
    associations = {}
    for i, current in enumerate(text_positions):
        # Skip if the text is already part of an association
        if any(current['text'] in value for value in associations.values()):
            continue

        # Look ahead to find the closest possible value
        for j in range(i + 1, len(text_positions)):
            next_text = text_positions[j]

            # Check if the next text is near the current text, assuming they're in the same 'line'
            if abs(next_text["y"] - current["y"]) < threshold and next_text["x"] > current["x"]:
                associations[current["text"]] = next_text["text"]
                break

    return associations

def main(pdf_path):
    # Extract text and their positions from the PDF
    text_positions = extract_text_with_positions(pdf_path)

    # Associate fields with values based on their proximity
    associations = associate_fields_with_values(text_positions)

    # Print the associations
    for field, value in associations.items():
        print(f"{field}: {value}")

if __name__ == "__main__":
    # Specify the path to your PDF document
    pdf_path = "your_order_form.pdf"

    main(pdf_path)
