# Python program to convert 
# text file to pdf file   
  
from fpdf import FPDF 

for story in range(1,248):
    pdf = FPDF()
    pdf.add_page()
    file_in = "story" + str(story) + ".txt"
    file_out = "story" + str(story) + ".pdf"
    # set style and size of font  
    # that you want in the pdf 
    pdf.set_font("Arial", size = 12) 
    
    # open the text file in read mode 
    f = open(file_in, "r") 
    
    # insert the texts in pdf 
    for x in f: 
        x = x.encode('utf-8').decode('latin-1')
        #pdf.cell(200, 10, txt = x, ln = 1, align = 'C') 
        pdf.multi_cell(200, 6, x, 0, 'L', False) 
    
    # save the pdf with name .pdf 
    pdf.output(file_out) 
