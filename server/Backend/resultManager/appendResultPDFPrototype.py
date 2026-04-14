import PyPDF2

# List of PDF filenames to append
pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']

# Create a PDF writer object
pdf_writer = PyPDF2.PdfFileWriter()

# Loop through all PDF files
for filename in pdf_files:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(filename)
    # Loop through all the pages of the current PDF
    for page_num in range(pdf_reader.numPages):
        # Get the page
        page = pdf_reader.getPage(page_num)
        # Add it to the writer object
        pdf_writer.addPage(page)

# Save the combined PDF to a file
with open('combined_pdf.pdf', 'wb') as out_file:
    pdf_writer.write(out_file)
