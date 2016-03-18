"""
viewPdf - simple script to open a pdf, convert to text, and display
"""
import argparse, sys, PyPDF2, re

verboseOutput = False


def main( argv ):
    filename = "e:\\Statements\\PNC\\PNC 2011 SEP.pdf"

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
    print("===========================================================================================")
    #  Account Number
    location = fullText.find("Primary account number:")
    fullText = fullText[location+ len("Primary account number:"):] # trim first part of text
    acctNumber = fullText[:12]
    #  Statement Period
    period = fullText[26:48]
    #  Balance information
    location = fullText.find("Endingbalance"); length = len("Endingbalance")
    fullText = fullText[location+length:]
    endlocation = fullText.find("Average monthlybalance");
    balanceInfo = fullText[:endlocation]
    #  Number of Deposits
    location = fullText.find("DetailDeposits and Other Additions"); length = len("DetailDeposits and Other Additions")+10
    print(fullText[location:location+length]); endlocation = location+length
    print(fullText[endlocation:endlocation+15])
    numDeposits = re.search( r'[ 0-9]*', fullText[endlocation:] )
    #print( numDeposits )
    print( "numDeposits = " + numDeposits.group(0) )
    #  Deposit Transactions
    location = fullText.find("DateAmountDescription"); length=len("DateAmountDescription")
    print(fullText[location:location+length])
    endlocation = fullText.find("Banking/Check Card Withdrawals"); length=len("Banking/Check Card Withdrawals")
    depositTrans = fullText[location+21:endlocation]
    print("Deposit Transactions: " + depositTrans)
    #
    # Find bank machine withdrawals
    #
    atm = re.search( r'Check Card Withdrawals and PurchasesThere were[ 0-9]* Banking Machinewithdrawals ', fullText[location:])
    print( "atm= " + atm.group(0))
    foo = [int(s) for s in fullText[location:].split() if s.isdigit()][0]
    print( "foo=" + str(foo) )
    print( "atm= " + atm.group(0))
    location = endlocation + len("Banking/Check Card Withdrawals and PurchasesThere were ")
    numCards = re.search( r'[ 0-9]*', fullText[location:] )
    #print( numCards )
    print( "numCards = " + numCards.group(0) )
    #  Number of other BankingMachine/Card deductions
    otherCardDeductions = re.search( r'There were[ 0-9]*other BankingMachine/Check Card deductions', fullText[location:])
    print( otherCardDeductions.group(0) )
    foo = [int(s) for s in otherCardDeductions.group(0).split() if s.isdigit()][0]
    print( "Other Card Deductions = " +  str(foo) )
    fullText = fullText[location:]
    #  Banking Machine Withdrawals
    location = fullText.find("DateAmountDescription")
    print( "location " + str(location) + " : " + fullText[location:location+150])

    print( "fullText: " + fullText[:50])
    endlocation = fullText.find("Online and Electronic Banking Deductions")
    bankMachineWithdrawals = fullText[location+len("DateAmountDescription"):endlocation]
    print( "bankMachineWithdrawals: " + bankMachineWithdrawals)
    #  Other Banking Machine/Check Card withdrawals
    fullText = fullText[endlocation+len("Online and Electronic Banking Deductions"):]
    print( fullText[:50])
    onlineDeductions = re.search( r'There were[ 0-9]*Online or ElectronicBanking Deductions ', fullText )
    print( onlineDeductions.group(0) )
    foo = [int(s) for s in onlineDeductions.group(0).split() if s.isdigit()][0]
    print( "Other Card Deductions = " +  str(foo) )
    location = fullText.find("DateAmountDescription")
    print( "location: " + str(location) + "fullText: " + fullText[location:location+50])
    endlocation = fullText[location:].find("OtherDeductions")
    onlineTransactions = fullText[location+len("DateAmountDescription"):endlocation]
    print( "onlineTransaction: " + onlineTransactions )
    #  Number other deductions

    #  Other deduction transactions
    print("=====================================================================")
    print("Statement Summary")
    print( "Account number: " + acctNumber )
    print("Statement Period: " + period)
    print("Balance Info: " + balanceInfo )

if __name__ == '__main__':

    main(sys.argv[1:])
