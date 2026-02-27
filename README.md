This small software retrieves PDF files containing the votes cast by various deputies on proposals discussed in the Portuguese Republic Assembly. Then, it processes each document, getting all the desired proposals and associated votes, to then publish them on social media.

(As of today, the scraping of documents from the Portuguese Republic Assembly archive has not been implemented)

The two main modules are:
    - readPtARprops.py - Gets all the documents with the votes between the desired dates, stores them in the 'documents/' folder and processes them. Results are stored in the output file requested by the user
    - blueSkyBot.py (in development) - Runs readPtARprops.py and posts them to BlueSky. Username and password are introduced as input on the terminal

Additionally, 3 input files must be provided:
    - parties.txt - Parties and the associated number of deputees, from most to least deputees. If the number of deputees is tied, check one of the tables for the order
    - vote_types.txt - Different types of proposals discussed (e.g., deliberations, final votes) for the document to be able to locate them. The user can exclude proposal types if he deems them irrelevant for the purpose ('0'), or include them ('1') otherwise. The file follows:
        0 - vote_type1
        1 - vote_type2
        ...        
    - col_width.txt (band-aid fix) - helps the PyMuPDF locate the columns within the table. A solution that better defines the dividing line will be developed after

Developed on Python 3.12.3. Required pip libraries can be found in pip_libs_to_install.txt

Relevant links:
    - Voting archive - https://www.parlamento.pt/ArquivoDocumentacao/Paginas/Arquivodevotacoes.aspx

Some inspirations (no association with them):
    - https://www.twitter.com/ArVotacoes - similar idea
    - https://www.votacoes.pt/ - website with all the proposals organised, with available filters

Contact information:
    - Bruno Cotrim - https://www.linkedin.com/in/brunorcotrim/

Side note 1 - I developed this as a way to learn Python while doing something that could be useful in its own right. Feel free to check the code and suggest improvements

Side note 2 - My ability to develop this code freely is a testament to the development of our Democracy in these past 50+ years. It's our ability to scrutinise and take people accountable for their actions that makes democracy possible, not some left/right ideologies. And, for that, we need the most accurate representation of reality possible, in other words, truth. Some far-right populists may say some outrageous things for shock-value, but that does not fundamentally undermines democracy. Dismissing truth, lying, discrediting credible reports, that is the real threat to democracy, and that can come from everywhere, whether an extreme or centre politician, unethical journalist or friend.

Copyright (c) 2026 Bruno Ribeiro Cotrim

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
