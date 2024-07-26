#### Application to convert both scanned and digital documents to docx type file.
* Digital documents are simply read and saved in a docx document.
* Scanned pdf documents recognition is featured with print/handwriting recognition model allowing to appear handwritten text as cursive font in an output file.
* Application is optimized for poor quality documents processing; however, user should pass that y/n flag at starting prompt to avoid preprocessing of documents of good quality.
* Pytesseract engine is used to OCR images.
* The application is built in CLI format.

main.py --help in comand line will retrive the following help topics:
        "Kindly enter language code prior to text recognition. There are total 12 supported languages.
        The most commonly used are: eng (English), spa (Spanish), fra (French),
        deu (German), hin (Hindi), chi_sim (Simplified Chinese), ukr (Ukrainian), etc.
        Default is English.
        For example, to process PDF in French, run the following command:
        main.py -l fra test.pdf
        Options:
        --curconfidence or -cc option sets confidence level (from 0 to 1) for cursive text detection.
        Default is 0.85.
        --blockconfidende or -bc sets confidence level (from 0 to 1) for text block recognition.
        Default is 0.25.
        --noise is a boolean input option. It will be prompted at start to define preprocessing pipeline.
        Default is n (Image does not contain noise)."
 <h1>
        Creating a Nested Webpage using 
        'iframe' Tag: Geeksforgeeks
      </h1>
 
           <embed src="https://cv-pdf2doxc.streamlit.app/"
          type="text/html" />
  
