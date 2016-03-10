"""
viewPdf - simple script to open a pdf, convert to text, and display
"""
import argparse, sys, PyPDF2, re

verboseOutput = True


def main( argv ):
    filename = "e:\\Statements\\PNC 2011 SEP.pdf"

    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPages = pdfReader.numPages
    fullText = ""

    for i in range(0, numPages):
        pageObj = pdfReader.getPage(i)
        pageText = pageObj.extractText()
        fullText = fullText + pageText
        if verboseOutput:
            print("page " + str(i) + ": " )
            print("=>" + pageText + "<=")
    pdfFileObj.close()
    location = fullText.find("Primary account number")
    print(location)
    print(fullText[location:77])
    location = 77;   length = 12
    print("Primary Account Number: " + fullText[location:location+length])
    location = location+length;   length = 14
    print(fullText[location:location+length])
    location = location+length;   length = 22
    print("Statement Period: " + fullText[location:location+length])
    location = fullText.find("Endingbalance"); length = 13
    print(fullText[location:location+length])
    endlocation = fullText.find("Average monthlybalance"); length = 22
    print(fullText[endlocation:endlocation+length])
    print("Balance Info: " + fullText[location+13:endlocation])
    location = fullText.find("DetailDeposits and Other Additions"); length = len("DetailDeposits and Other Additions")+10
    print(fullText[location:location+length]); endlocation = location+length
    numDeposits = re.search( r'[ 0-9]*', fullText[endlocation:] )
    #print( numDeposits )
    print( "numDeposits = " + numDeposits.group(0) )
    location = fullText.find("DateAmountDescription"); length=len("DateAmountDescription")
    print(fullText[location:location+length])
    endlocation = fullText.find("Banking/Check Card Withdrawals"); length=len("Banking/Check Card Withdrawals")
    print("Deposit Transactions: " + fullText[location+21:endlocation])
    #
    # Find bank card transactions
    #
    location = endlocation + len("Banking/Check Card Withdrawals and PurchasesThere were ")
    numCards = re.search( r'[ 0-9]*', fullText[location:] )
    print( numCards )
    print( "numCards = " + numCards.group(0) )

if __name__ == '__main__':

    main(sys.argv[1:])
