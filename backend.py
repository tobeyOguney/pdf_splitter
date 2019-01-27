import PyPDF2

def split_pdf(start, end, input, output):
    pdfReader = PyPDF2.PdfFileReader(input)
    pdf_writer = PyPDF2.PdfFileWriter()
    for page in range(pdfReader.getNumPages()-1):
        while start<=end:
            pdf_writer.addPage(pdfReader.getPage(start-1))
            start+=1
        output_filename = output
        with open(output_filename,'wb') as out:
            pdf_writer.write(out)


def interpret_query(inputs, mapping, output):
    pdf_writer = PyPDF2.PdfFileWriter()
    for input in inputs:
        pdf_reader = PyPDF2.PdfFileReader(input)
        queries = [i.strip().split('-') for i in mapping[input].split(',')]
        for query in queries:
            if '*' in query:
                start = 0
                end = pdf_reader.getNumPages()-1
            else:
                if len(query) == 1: query.append(query[0])
                start = int(query[0].replace('.', str(pdf_reader.getNumPages())))
                end = int(query[1].replace('.', str(pdf_reader.getNumPages())))
            for page in range(pdf_reader.getNumPages()-1):
                while start<=end:
                    pdf_writer.addPage(pdf_reader.getPage(start-1))
                    start+=1
    with open(output, 'wb') as out:
        pdf_writer.write(out)