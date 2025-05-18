import pypandoc
output = pypandoc.convert_file('your_doc.docx', 'md')
print(output)
