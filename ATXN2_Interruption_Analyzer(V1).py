'''
#Problems to IMPROVE ON
Flanking Analysis
Comp and NonComp - How to best output interruptions (For ALL LC is Most Interruptions Accurate) - If all interruption then ideal would be an analysis around each specific interruption
Spanning Matrix Validation
Cutstring Shaping
Error/NOTES handling (Improved With New Version)
Check all comp is similiar
 - Clean Code: Iterator, Default, and Number Holders

#HOW IT WORKS
Put log and VCF files in same directory as this .py file
If using a txt file to hold all the names, make sure each CHGVID is on a new line and in the same directory as .py
OPEN this Python File in IDLE (Download Python 3.7 and up) and Run (Press F5)
Type into the Shell that pops up with whatever it asks (Pressing Enter Key Submits)
Output will be a .csv file or printed in the shell

Note:
VLOOKUP still require manual human support by linking target file to csv


'''
#Variables that don't change with each CHGVID
import re
from collections import defaultdict
from pathlib import Path
import csv
substringFlanking = "FLANKING:"
substringATXN2 = "ATXN2:"
substringSpan = "SPANNING_"
substringend = ":"
substringread = "align: |"
substringfstart = "|    "
substringfend = "   |"
substringflanking = "FLANKING:"
substringflankSTOP = "C9ORF72:"
regrepeat = "CTG"
interruption = "GTT"
logcheck="_log.txt"
vcfcheck=".vcf"
substringATXN2 = "ATXN2"
substringSTR = "<STR"
substringEND = ">	."
ShouldIVlookup = 1
selectivity=0.25

CHGVID, File, IGM_SUB, GROUP, BH_GT, EXPHUNT_RESULT, LG_Result, Large, Large_INT_LOC, SM_RESULT, SMALL, SMALL_INT_LOC, NOTES, Flanking_Reads, Error_Reads = "CHGVID", "File", "IGM_SUB", "GROUP", "BH_GT", "EXPHUNT_RESULT", "LG_Result", "Large", "Large_INT_LOC", "SM_RESULT", "SMALL", "SMALL_INT_LOC", "NOTES", "Flanking_Reads", "Error_Reads"
csvRow = [CHGVID, File, IGM_SUB, GROUP, BH_GT, EXPHUNT_RESULT, LG_Result, Large, Large_INT_LOC, SM_RESULT, SMALL, SMALL_INT_LOC, NOTES, Flanking_Reads, Error_Reads]


class spanningreads:
        def __init__(self, spanningsize, reads):
            self.spanningsize = spanningsize
            self.reads = reads
class readFrame:
        def __init__(self, lineRead, frameStart, frameEnd):
            self.lineRead = lineRead
            self.frameStart = frameStart
            self.frameEnd = frameEnd
        def __repr__(self):
                return (str(self.lineRead)+", "+str(self.frameStart)+", "+str(self.frameEnd))
class flankingINPUT:
        def __init__(self, lineRead, frameStart, frameEnd, interruptionlocation, interruptioncount, repeatlocation, repeatcount, frame, LowerCaseLocations):
            self.lineRead = lineRead
            self.frameStart = frameStart
            self.frameEnd = frameEnd
            self.interruptionlocation = interruptionlocation
            self.interruptioncount = interruptioncount
            self.repeatlocation = repeatlocation
            self.repeatcount = repeatcount
            self.frame = frame
            self.LowerCaseLocations = LowerCaseLocations
class interruptioncount:
        def __init__(self, interruptionlocation, LEFTinterruptionlocation,countHolder, LClocations):
            self.interruptionlocation = interruptionlocation
            self.LEFTinterruptionlocation = LEFTinterruptionlocation
            self.countHolder = countHolder
            self.LClocations = LClocations
class fileCharacteristics:
        def __init__(self, filename, existence, EXP_RES):
            self.filename = filename
            self.existence = existence
            self.EXP_RES = EXP_RES
class interpret:
    def __init__(self, interruptionlocation, spanningsize, numsimiliar, percen):
        self.interruptionlocation = interruptionlocation
        self.spanningsize = spanningsize
        self.numsimiliar = numsimiliar
        self.percen = percen
class COMPinterruptionlocationholder:
    def __init__(self, interruptionlocation, spanningsize, numsimiliar, readnumlist, LClocations, interruptionnoncomp, compinterruption, compstatus):
        self.interruptionlocation = interruptionlocation
        self.spanningsize = spanningsize
        self.numsimiliar = numsimiliar
        self.readnumlist = readnumlist
        self.LClocations = LClocations
        self.interruptionnoncomp = interruptionnoncomp
        self.compinterruption = compinterruption
        self.compstatus = compstatus
#Catch all class to streamline data calling for interruptions
class interruptionchecker:
    def __init__(self, spanningsize, readindex, percentagespanning, lineread, interruptionlocations, counts, lowercaselocations, truncatelclocations, flankingchecker, flankingmatchlist):
        self.spanningsize = spanningsize
        self.readindex = readindex
        self.percentagespanning = percentagespanning
        self.lineread = lineread
        self.interruptionlocations = interruptionlocations
        self.counts = counts
        self.lowercaselocations = lowercaselocations
        #Need to calculate the following
        self.truncatelclocations = truncatelclocations
        self.flankingchecker = flankingchecker
        self.flankingmatchlist = flankingmatchlist
class spanningchecker:
    def __init__(self, spanningsize, percentagespanning, reads):
        self.spanningsize = spanningsize
        self.percentagespanning = percentagespanning
        self.reads = reads
rval = input("PRESS ENTER     (if test enter capital T)")
print("(Enter Capital Y for .txt input)(COPY/PASTING: CURSOR DIRECTLY AFTER)(Capital T for Tester Mode)")
val = input("Enter your CHGVID:")
if (val == 'Y') == False:
        print("The hopefully single CHGVID: " + val)
        chgvids = val
        excelinput = 0
        if (rval == 'T')==False:
                excelinput = input("(Input capital N if you don't want to input) What is the name of the excel file to be used for VLOOKUP?")
                testermode = 0
        if rval == 'T':
                testermode = 1
                excelinput = 'N'
        if excelinput == 'N':
                excelinput = "Empty"
                ShouldIVlookup = 0
                outputfile = input("(Input capital N if you don't want to Output)Output file name:")
        if (ShouldIVlookup == 0) == False:
                        sheetpagename = input("(Input capital N if you don't want to) What is the Sheet Page Name for VLOOKUP:")
                        if sheetpagename == 'N':
                                sheetpagename= "1" #
                        columnNumIS = input("(Input capital N if you don't want to) What is the Column Number for IGM_SUB:")
                        if columnNumIS == 'N':
                                columnNumIS = "3" #
                        columnNumG = input("(Input capital N if you don't want to) What is the Column Number for Group:")
                        if columnNumG == 'N':
                                columnNumG = "4" #
                        columnNumBH = input("(Input capital N if you don't want to) What is the Column Number for BH_GT:")
                        if columnNumBH == 'N':
                                columnNumBH = "5" #

                        vlookupfilename=excelinput
                        vlookupn=0
                        outputfile=input("(Input capital N if you don't want to Output)Output file name:")
if (val == 'Y'):
        masterfilename = input("(Must be in Directory) What is the exact filename:")
        f = open(masterfilename,'r')
        mastertxt = f.read()
        chgvids = mastertxt.splitlines()
        if len(chgvids)>0:
                print("Input Successful; Here is the first line: " + chgvids[0])
                if (rval == 'T')==False:
                        excelinput = input("(Input capital N if you don't want to input) What is the name of the excel file to be used for VLOOKUP?")
                        testermode = 0
                if rval == 'T':
                        testermode = 1
                        excelinput = 'N'
                if excelinput == 'N':
                        excelinput = "Empty"
                        ShouldIVlookup = 0
                if (ShouldIVlookup == 0) == False:
                        sheetpagename = input("(Input capital N if you don't want to) What is the Sheet Page Name for VLOOKUP:")
                        if sheetpagename == 'N':
                                sheetpagename= "1" #
                        columnNumIS = input("(Input capital N if you don't want to) What is the Column Number for IGM_SUB:")
                        if columnNumIS == 'N':
                                columnNumIS = "3" #
                        columnNumG = input("(Input capital N if you don't want to) What is the Column Number for Group:")
                        if columnNumG == 'N':
                                columnNumG = "4" #
                        columnNumBH = input("(Input capital N if you don't want to) What is the Column Number for BH_GT:")
                        if columnNumBH == 'N':
                                columnNumBH = "5" #

                        vlookupfilename=excelinput
                        vlookupn=0
                outputfile=input("(Input capital N if you don't want to Output) Output file name:")

        else:
                print("ERROR: File Contains no values")

outputfilecheck = outputfile+".csv"
myfile_OPFC = Path(outputfilecheck)
while myfile_OPFC.is_file():
        outputfile = outputfile+"_COPY"
        outputfilecheck = outputfile+".csv"
        myfile_OPFC = Path(outputfilecheck)

if (outputfile == 'N') == False:
        csvfile = str(outputfile)+".csv"
        with open(csvfile, "a", newline='') as fp:
                wr = csv.writer(fp, dialect='excel')
                wr.writerow(csvRow)

if isinstance(chgvids, str):
        chgvids = [chgvids]
for z in chgvids:
    CHGVID, File, IGM_SUB, GROUP, BH_GT, EXPHUNT_RESULT, LG_Result, Large, Large_INT_LOC, SM_RESULT, SMALL, SMALL_INT_LOC, NOTES, Flanking_Reads, Error_Reads = "CHGVID", "File", "IGM_SUB", "GROUP", "BH_GT", "EXPHUNT_RESULT", "LG_Result", "Large", "Large_INT_LOC", "SM_RESULT", "SMALL", "SMALL_INT_LOC", "NOTES", "Flanking_Reads", "Error_Reads"
    csvRow = [CHGVID, File, IGM_SUB, GROUP, BH_GT, EXPHUNT_RESULT, LG_Result, Large, Large_INT_LOC, SM_RESULT, SMALL, SMALL_INT_LOC, NOTES, Flanking_Reads, Error_Reads]
    if (excelinput == "Empty") == False:
            vlookupn = vlookupn + 1
            IGM_SUB = "=VLOOKUP(A"+str(vlookupn+1)+", '["+vlookupfilename+".xlsx]"+sheetpagename+"'!$1:$1048576,"+columnNumIS+",True)"
            GROUP = "=VLOOKUP(A"+str(vlookupn+1)+", '["+vlookupfilename+".xlsx]"+sheetpagename+"'!$1:$1048576,"+columnNumG+",True)"
            BH_GT = "=VLOOKUP(A"+str(vlookupn+1)+", '["+vlookupfilename+".xlsx]"+sheetpagename+"'!$1:$1048576,"+columnNumBH+",True)"

    spanninglist=[]
    flanking =[]
    flankingfinal=[]
    tempspanninglist=[]
    ATXN2Interruptions = []
    vcflist = []
    Large_INT_LOC = []
    SMALL_INT_LOC = []
    NOTES = []
    ERROR = []
    Flanking_Reads = []
    Error_Reads = []
    interruptioncheckerlist=[]
    runner=[]
    percentages=[]
    interruptionlocations = []
    lowercaselocations = []
    truncatelclocations = []
    flankingmatchlist = []
    spanningcheckerlist=[]
    LClocations = []
    LCHelper = []
    interruptionnoncomp = []
    compinterruption = []
    comp=[]
    notcomp=[]
    compdictransfer=[]
    compdictransfer=[]
    compresolver = []
    interpretor = []
    longest= []
    NOTESINTER = []
    joinertemp = []
    norepeaterfornotes = []
    d=defaultdict(list)
    inter=defaultdict(list)
    LCUSEFUL = defaultdict(list)
    internoncomp = defaultdict(list)
    compdict = defaultdict(list)
    notcompdict = defaultdict(list)
    Existence_Counter = "N"
    EXP_RES = "N/A"
    reads = 0
    spanninglength = "-"
    locationLog = 0
    endlocationLog = 0
    lineholder = "-"
    ReadStart = 0
    ReadEnd = 0
    TotalSpanningReads=0#for interpretator
    index = 0
    flankingstartnum = 0
    flankingreads = 0
    flankingindex = 0
    flankingholder = "-"
    flankingstart = 0
    flankingend = 0
    flankingstring = "-"
    samplestring=""
    fileexistenceholder=""
    exp_res=""
    location=0
    endlocation=0
    count=0
    ERRORnum=0 #DO IT RETROACTIVELY ABOVE
    LG_Result = 0
    LG_HOLDER=""
    Large = 0
    SM_RESULT = 0
    SM_HOLDER=""
    SMALL = 0
    readindexnum=0
    runningindex=0
    spanningindexnum=0
    spanningsize = ""
    readindex = 0
    percentagespanning = 0
    lineread = ""
    counts = 0
    flankingchecker = False
    numsimiliar = 0
    compstatus=True

    holder=z
    holdervcf=holder+vcfcheck
    holderlog=holder+logcheck
    my_fileVCF = Path(holdervcf)
    my_fileLog = Path(holderlog)
    if my_fileVCF.is_file() and my_fileLog.is_file():
        Existence_Counter = "Y"
    if (my_fileVCF.is_file()==False) and (my_fileLog.is_file()==True):
        Existence_Counter = "VCF File Missing"
    if (my_fileVCF.is_file()==True) and (my_fileLog.is_file()==False):
        Existence_Counter = "Log File Missing"
    if (my_fileVCF.is_file()==False) and (my_fileLog.is_file()==False):
        Existence_Counter = "N"
    if my_fileVCF.is_file()==False:
            vcflist.append(fileCharacteristics(holder, Existence_Counter, EXP_RES))
    if my_fileVCF.is_file()==True:
            f = open(my_fileVCF,'r')
            messageVCF = f.read()
            res = messageVCF.splitlines()
            ATXN2list = []
            location = ""
            endlocation = 0
            finalresult = ""
            for i in res:
                if substringATXN2 in i:
                    ATXN2list.append(i)
            for i in ATXN2list:
                if substringSTR in i:
                    location = i.find(substringSTR)
                    if location == -1:
                        finalresult = "N/A"
                        EXP_RES = finalresult
                    else:
                        endlocation = i.find(substringEND)
                        finalresult = i[location:(endlocation+1)]
                        EXP_RES = finalresult
            vcflist.append(fileCharacteristics(holder, Existence_Counter, EXP_RES))
    if my_fileLog.is_file()==False:
            for obj in vcflist:
                    if testermode == 1 or outputfile == 'N':
                            print( obj.filename, obj.existence, obj.EXP_RES, sep =', ' )
                    fileexistenceholder=obj.existence
                    exp_res=obj.EXP_RES
            if (outputfile == 'N') == False:
                    with open(csvfile, "a", newline='') as fp:
                            wr = csv.writer(fp, dialect='excel')
                            wr.writerow([str(z), fileexistenceholder, IGM_SUB, GROUP, BH_GT])
            continue
    filename=holderlog
    f = open(filename,'r')
    messageLOG = f.read()
    resLog = messageLOG.splitlines()
    if((substringATXN2 in resLog[0]) ++ (substringSpan in resLog[1]))==False:
        Error_Reads.appends("LogFile_FormatError: ATXN2 Not Found + Spanning Label Not Found")
    if((substringATXN2 in resLog[0]) ++ (substringSpan in resLog[1])): #Based on format
            for i in resLog:
                    index = index + 1
                    if (i.rfind(substringFlanking)> -1): #Based on format
                        spanninglist.append(spanningreads(spanninglength, reads))
                        break
                    if substringread in i:
                        reads = reads + 1
                        lineHolder = resLog[index]
                        ReadStart = resLog[index+1].rfind(substringfstart)#Based on format
                        ReadEnd = resLog[index+1].rfind(substringfend)#Based on format
                        tempspanninglist.append((spanninglength, readFrame(lineHolder, ReadStart, ReadEnd)))
                        TotalSpanningReads = TotalSpanningReads + 1
                    if substringSpan in i:
                        if(reads == 0):
                            if((spanninglength == "-")== False):
                                    spanninglist.append(spanningreads(spanninglength, reads))
                            locationLog = i.find(substringSpan)
                            endlocationLog = i.find(substringend)
                            spanninglength = i[(locationLog+9):(endlocationLog)]#Based on format
                            reads = 0
                        if(reads>0):
                            spanninglist.append(spanningreads(spanninglength, reads))
                            locationLog = i.find(substringSpan)
                            endlocationLog = i.find(substringend)
                            spanninglength = i[(locationLog+9):(endlocationLog)]#Based on format
                            reads = 0
            for i in resLog:
                flankingindex = flankingindex + 1
                if substringflankSTOP in i:
                    flankingstartnum = 0
                    break
                if substringflanking in i:
                    flankingstartnum = 1
                if flankingstartnum == 1:
                    if substringread in i:
                        flankingreads = flankingreads + 1
                        flankingholder = resLog[flankingindex]
                        if (resLog[flankingindex+1].rfind(substringfstart)==-1)==True: #Based on format
                            flankingend = resLog[flankingindex+1].rfind(substringfend)
                            flankingstart = 8 #Based on format
                        if (resLog[flankingindex+1].rfind(substringfend)==5)==True: #Based on format
                            flankingstart = resLog[flankingindex+1].rfind(substringfstart)+2
                            flankingend =161 #Based on format
                        flankingstring = flankingholder[(flankingstart):(flankingend + 3)] #Based on format
                        flanking.append(readFrame(flankingstring, flankingstart, flankingend))
    for k, v in tempspanninglist:
            d[k].append(v)
    tempspanninglist.clear()
    for obj in spanninglist:
            tempspanninglist.append(obj.spanningsize)
    for i in tempspanninglist:
            for obj in d[i]:
                    lowercaseLocations = []
                    samplestring = obj.lineRead
                    location = obj.frameStart
                    endlocation = obj.frameEnd
                    cutstring=samplestring[(location+2):(endlocation+4)]#Based on format
                    samplelist=([m.start() for m in re.finditer(interruption, cutstring, re.I)])
                    k=3#Based on format
                    #this finds the g location in gtt we want the t location(three off)
                    res = [x + k for x in samplelist]#Based on format
                    count=len(res)
                    indexstring=0
                    for a in cutstring:
                            indexstring=indexstring+1
                            if (a.islower()) == True:#Based on format
                                    lowercaseLocations.append(indexstring)
                    #Read Interruptions from left for flanking
                    reversedcutstring=''.join(reversed(cutstring))
                    reversedinterruption=''.join(reversed(interruption))
                    LEFTsamplelist=([m.start() for m in re.finditer(reversedinterruption, reversedcutstring, re.I)])
                    ATXN2Interruptions.append((i, interruptioncount(res, LEFTsamplelist, count, lowercaseLocations)))
                    for k, v in ATXN2Interruptions:
                            inter[k].append(v)
                    ATXN2Interruptions.clear()
                    obj.lineRead=cutstring#TO SEE cutstring
    for obj in flanking:
            lowercaseLocations = []
            lineReadholder=obj.lineRead
            frameStartholder=obj.frameStart
            frameEndholder = obj.frameEnd
            frameholder="-"
            k=3#Based on format
            #this finds the g location in gtt we want the t location(three off)
            if frameStartholder == 8:
                    frameholder="From End"
            if frameEndholder == 161:
                    frameholder="From Beginning"
            ILholder=([m.start() for m in re.finditer(interruption, lineReadholder, re.I)])
            ILholder = [x + k for x in ILholder]#Based on format
            INTcount = len(ILholder)
            Rholder=([m.start() for m in re.finditer(regrepeat, lineReadholder, re.I)])
            Rholder = [x + k for x in Rholder]
            REPcount = len(Rholder)
            if (frameholder == "From End") == True:
                    reversedlinereadholder=''.join(reversed(lineReadholder))
                    reversedregrepeat=''.join(reversed(regrepeat))
                    reveresedinterruption=''.join(reversed(interruption))
                    ILholder=([m.start() for m in re.finditer(reversedregrepeat, reversedlinereadholder, re.I)])
                    ILholder = [x + k for x in ILholder]
                    INTcount = len(ILholder)
                    Rholder=([m.start() for m in re.finditer(reversedinterruption, reversedlinereadholder, re.I)])
                    Rholder = [x + k for x in Rholder]
                    REPcount = len(Rholder)
            indexstring=0
            for a in lineReadholder:
                    indexstring=indexstring+1
                    if (a.islower()) == True:#Based on format
                            lowercaseLocations.append(indexstring)
            flankingfinal.append(flankingINPUT(lineReadholder, frameStartholder, frameEndholder, ILholder, INTcount, Rholder, REPcount, frameholder, lowercaseLocations))
    #Interpretation Section
    #tempspanninglist contains list of all the spanning lengths

    for obj in spanninglist:
            percentages.append(obj.reads/TotalSpanningReads)
            runner.append(obj.reads)
            spanningcheckerlist.append(spanningchecker(int(obj.spanningsize), obj.reads/TotalSpanningReads, obj.reads))

    for i in tempspanninglist:
        spanningsize = i
        percentagespanning=percentages[spanningindexnum]
        spanningindexnum=spanningindexnum+1
        readindexnum=1
        for obj in d[i]:
                lineread=obj.lineRead
                interruptioncheckerlist.append(interruptionchecker(spanningsize, readindexnum, percentagespanning, lineread, interruptionlocations, counts, lowercaselocations, truncatelclocations, flankingchecker, flankingmatchlist))
                readindexnum=readindexnum+1
        for obj in inter[i]:
                interruptioncheckerlist[runningindex].interruptionlocations=obj.interruptionlocation
                interruptioncheckerlist[runningindex].counts=obj.countHolder
                interruptioncheckerlist[runningindex].lowercaselocations=obj.LClocations
                runningindex=runningindex+1
    if testermode == 1:
            for obj in interruptioncheckerlist:
                print(obj.spanningsize, obj.readindex, obj.percentagespanning, obj.lineread, obj.interruptionlocations, obj.counts, obj.lowercaselocations, obj.truncatelclocations, obj.flankingchecker, obj.flankingmatchlist, sep =', ' )
            for obj in spanningcheckerlist:
                print(obj. spanningsize, obj.percentagespanning, obj.reads, sep =', ' )


    #NOT COMP
    for i in tempspanninglist:
            numsimiliar = 0
            LClocations = []
            interruptionnoncomp = []
            compinterruption = []
            comp=[]
            notcomp=[]
            compstatus=False
            for obj in interruptioncheckerlist:
                if obj.spanningsize==i:
                        if len(obj.lowercaselocations)==0:
                                runnervar = 0
                                for o in notcomp:
                                        if len(notcomp) == 0:
                                                continue
                                        if o.interruptionlocation == obj.interruptionlocations:
                                                o.numsimiliar = o.numsimiliar + 1
                                                o.readnumlist.append(obj.readindex)
                                                runnervar = 1
                                if runnervar == 0:
                                        readnumlist = []
                                        readnumlist.append(obj.readindex)
                                        notcomp.append(COMPinterruptionlocationholder(obj.interruptionlocations, obj.spanningsize, 1, readnumlist, LClocations, interruptionnoncomp, compinterruption, compstatus))
            for j in notcomp:
                   holdervariableCDT=str(j.spanningsize)
                   compdictransfer.append((holdervariableCDT, j))
                   if testermode == 1:
                           print(j.interruptionlocation, j.spanningsize, j.numsimiliar, j.readnumlist, j.LClocations, j.interruptionnoncomp, j.compinterruption, j.compstatus, sep =', ' )
    for k, v in compdictransfer:
            notcompdict[k].append(v)

    #Intial NonComp Interruptiontation
    if ((len(compdictransfer) == 0) == False):
            for x in tempspanninglist:
                    if (len(notcompdict[x])== 1):
                            for obj in notcompdict[x]:
                                    compresolver.append((x, obj.interruptionlocation))
                    if (len(notcompdict[x])== 0):
                            compresolver.append((x, "EMPTY"))
                            NOTES.append("Spanningsize " + str(x) + ": All Compromised")
                    if (len(notcompdict[x])> 1):
                            NUMSIMILARTOTAL=0
                            for obj in notcompdict[x]:
                                    NUMSIMILARTOTAL=NUMSIMILARTOTAL+obj.numsimiliar
                                    interpretor.append(interpret(obj.interruptionlocation, obj.spanningsize, obj.numsimiliar, 0))
                            for obj in interpretor:
                                    obj.precen = (obj.percen/NUMSIMILARTOTAL)
                            interpretor.sort(key=lambda x: x.percen, reverse = True)
                            compresolver.append((x, interpretor[0].interruptionlocation))
                            for obj in notcompdict[x]:
                                    if (obj.interruptionlocation == interpretor[0].interruptionlocation):
                                            continue
                                    norepeaterfornotes.append(obj.spanningsize)
                                    NOTES.append("NCSpanning "+obj.spanningsize+" w/ Interruptions@"+str(obj.interruptionlocation)+";#Reads: "+str(obj.numsimiliar)+"@ReadNumbers-"+str(obj.readnumlist))

    if (len(compdictransfer) == 0):
            for x in tempspanninglist:
                    compresolver.append((x, "EMPTY"))

    #COMP
    if testermode == 1:
            print("comp")
    compdictransfer=[]
    for i in tempspanninglist:
            numsimiliar = 0
            LClocations = []
            interruptionnoncomp = []
            compinterruption = []
            comp=[]
            notcomp=[]
            compstatus=True
            for obj in interruptioncheckerlist:
                lowercaseholderC=[]
                interruptionholderC=[]
                if obj.spanningsize==i:
                        if len(obj.lowercaselocations)>0:
                                runnervar = 0
                                lowercaseholderC=obj.lowercaselocations
                                interruptionholderC=obj.interruptionlocations
                                for o in comp:
                                        if len(comp) == 0:
                                                continue
                                        if o.interruptionlocation == obj.interruptionlocations:
                                                o.numsimiliar = o.numsimiliar + 1
                                                o.readnumlist.append(obj.readindex)
                                                if (len(interruptionholderC) == 0)==False:
                                                        for p in interruptionholderC:
                                                                for e in lowercaseholderC:
                                                                        effectivee = e-1
                                                                        comparelow = p-3
                                                                        comparehigh = p-1
                                                                        if (comparelow <= effectivee <= comparehigh):
                                                                                noncomprunner=0
                                                                                for h in compinterruption:
                                                                                                if h == p:
                                                                                                        noncomprunner=1
                                                                                if noncomprunner==0:
                                                                                        o.compinterruption.append(p)
                                                                                o.LClocations.append((p, obj.readindex))
                                                                        if (comparelow <= effectivee <= comparehigh) ==False:
                                                                                noncomprunner=0
                                                                                for h in interruptionnoncomp:
                                                                                                if h == e:
                                                                                                        noncomprunner=1
                                                                                for h in o.interruptionnoncomp:
                                                                                        if h==(e, obj.readindex):
                                                                                                noncomprunner=1
                                                                                if noncomprunner==0:
                                                                                        o.interruptionnoncomp.append((e, obj.readindex))#
                                                if len(interruptionholderC) == 0:
                                                        for u in compresolver:
                                                                if u[0] == i:
                                                                        if (u[1]=="EMPTY")==False:
                                                                                interruptionholderC=u[1]
                                                                                for p in interruptionholderC:
                                                                                        for e in lowercaseholderC:
                                                                                                effectivee = e-1
                                                                                                comparelow = p-3
                                                                                                comparehigh = p-1
                                                                                                if (comparelow <= effectivee <= comparehigh):
                                                                                                        noncomprunner=0
                                                                                                        for h in compinterruption:
                                                                                                                        if h == p:
                                                                                                                                noncomprunner=1
                                                                                                        if noncomprunner==0:
                                                                                                                o.compinterruption.append(p)
                                                                                                        o.LClocations.append((p, obj.readindex))
                                                                                                if (comparelow <= effectivee <= comparehigh) ==False:
                                                                                                        noncomprunner=0
                                                                                                        for h in interruptionnoncomp:
                                                                                                                        if h == e:
                                                                                                                                noncomprunner=1
                                                                                                        for h in o.interruptionnoncomp:
                                                                                                                if h==(e, obj.readindex):
                                                                                                                        noncomprunner=1
                                                                                                        if noncomprunner==0:
                                                                                                                o.interruptionnoncomp.append((e, obj.readindex))
                                                runnervar = 1
                                if runnervar == 0:
                                        readnumlist = []
                                        interruptionnoncomp = []
                                        compinterruption = []
                                        LCHelper= []
                                        lowercaseholderC=obj.lowercaselocations
                                        interruptionholderC=obj.interruptionlocations
                                        if (len(interruptionholderC) == 0)==False:
                                                for p in interruptionholderC:
                                                        for e in lowercaseholderC:
                                                                effectivee = e-1
                                                                comparelow = p-3
                                                                comparehigh = p-1
                                                                if (comparelow <= effectivee <= comparehigh):
                                                                        noncomprunner=0
                                                                        for h in compinterruption:
                                                                                        if h == p:
                                                                                                noncomprunner=1
                                                                        if noncomprunner==0:
                                                                                compinterruption.append(p)
                                                                        LCHelper.append((p, obj.readindex))
                                                                if (comparelow <= effectivee <= comparehigh) ==False:
                                                                        noncomprunner=0
                                                                        for h in interruptionnoncomp:
                                                                                        if h == e:
                                                                                                noncomprunner=1
                                                                        for h in interruptionnoncomp:
                                                                                        if h==(e, obj.readindex):
                                                                                                noncomprunner=1
                                                                        if noncomprunner==0:
                                                                                interruptionnoncomp.append((e, obj.readindex))
                                        if len(interruptionholderC) == 0:
                                                for u in compresolver:
                                                        if u[0] == i:
                                                                if (u[1]=="EMPTY")==False:
                                                                        interruptionholderC=u[1]
                                                                        for p in interruptionholderC:
                                                                                for e in lowercaseholderC:
                                                                                        effectivee = e-1
                                                                                        comparelow = p-3
                                                                                        comparehigh = p-1
                                                                                        if (comparelow <= effectivee <= comparehigh):
                                                                                                noncomprunner=0
                                                                                                for h in compinterruption:
                                                                                                                if h == p:
                                                                                                                        noncomprunner=1
                                                                                                if noncomprunner==0:
                                                                                                        compinterruption.append(p)
                                                                                                LCHelper.append((p, obj.readindex))
                                                                                        if (comparelow <= effectivee <= comparehigh) ==False:
                                                                                                noncomprunner=0
                                                                                                for h in interruptionnoncomp:
                                                                                                                if h == e:
                                                                                                                        noncomprunner=1
                                                                                                for h in interruptionnoncomp:
                                                                                                                if h==(e, obj.readindex):
                                                                                                                        noncomprunner=1
                                                                                                if noncomprunner==0:
                                                                                                        interruptionnoncomp.append((e, obj.readindex))
                                        readnumlist.append(obj.readindex)
                                        comp.append(COMPinterruptionlocationholder(obj.interruptionlocations, obj.spanningsize, 1, readnumlist, LCHelper, interruptionnoncomp, compinterruption, compstatus))
            for j in comp:
                   holdervariableCDT=str(j.spanningsize)
                   compdictransfer.append((holdervariableCDT, j))
                   if testermode == 1:
                           print(j.interruptionlocation, j.spanningsize, j.numsimiliar, j.readnumlist, j.LClocations, j.interruptionnoncomp, j.compinterruption, j.compstatus, sep =', ' )
    for k, v in compdictransfer:
            compdict[k].append(v)


    if testermode == 1:
            for x in tempspanninglist:
                for obj in compdict[x]:
                        print(obj.interruptionlocation, obj.spanningsize, obj.numsimiliar, obj.readnumlist, obj.LClocations, obj.interruptionnoncomp, obj.compinterruption, obj.compstatus, sep =', ')


    for x in tempspanninglist:
        RUNNERU=-1
        for u in compresolver:
                RUNNERU=RUNNERU+1
                if u[0] == x:
                        if u[1]=="EMPTY":
                                for obj in compdict[x]:
                                        if len(obj.interruptionlocation)>len(longest):
                                                longest=obj.interruptionlocation
                                del compresolver[RUNNERU]
                                compresolver.insert(RUNNERU, (x, longest))

    #Spanning Check
    if(len(spanningcheckerlist)==1):
        for obj in spanningcheckerlist:
            LG_Result=obj.spanningsize
        for x in tempspanninglist:
                if int(x) == spanningcheckerlist[0].spanningsize:
                        for u in compresolver:
                                if u[0] == x:
                                        Large_INT_LOC = u[1]
        NOTES.append("CHECK TO CONFIRM THAT IT IS SIMILIAR TO BH_GT + Check Flanking")
    if(len(spanningcheckerlist)==2):
        LG_Result=spanningcheckerlist[0].spanningsize
        for x in tempspanninglist:
                if int(x) == spanningcheckerlist[0].spanningsize:
                        for u in compresolver:
                                if u[0] == x:
                                        Large_INT_LOC = u[1]
        SM_RESULT=spanningcheckerlist[1].spanningsize
        for x in tempspanninglist:
                if int(x) == spanningcheckerlist[1].spanningsize:
                        for u in compresolver:
                                if u[0] == x:
                                        SMALL_INT_LOC = u[1]
        #NOTES.append("InterIssues") we need one that outputs the noncomp issues as well - DO LATER (InterIssues is a placeholder)
    #Sort based on percentages - then when outputing sort the two to output based on which is greate with two if statements
    spanningcheckerlist.sort(key=lambda x: x.percentagespanning, reverse = True)
    #Spanning  Selectivity
    if(len(spanningcheckerlist)>2):
        if int(spanningcheckerlist[0].percentagespanning)>=selectivity and int(spanningcheckerlist[1].percentagespanning)>=selectivity:
            if spanningcheckerlist[0].spanningsize > spanningcheckerlist[1].spanningsize:
                    LG_Result=spanningcheckerlist[0].spanningsize
                    for x in tempspanninglist:
                        if int(x) == spanningcheckerlist[0].spanningsize:
                                for u in compresolver:
                                        if u[0] == x:
                                                Large_INT_LOC = u[1]
                    SM_RESULT=spanningcheckerlist[1].spanningsize
                    for x in tempspanninglist:
                            if int(x) == spanningcheckerlist[1].spanningsize:
                                    for u in compresolver:
                                            if u[0] == x:
                                                    SMALL_INT_LOC = u[1]
            if spanningcheckerlist[1].spanningsize > spanningcheckerlist[0].spanningsize:
                    LG_Result=spanningcheckerlist[1].spanningsize
                    for x in tempspanninglist:
                        if int(x) == spanningcheckerlist[1].spanningsize:
                                for u in compresolver:
                                        if u[0] == x:
                                                Large_INT_LOC = u[1]
                    SM_RESULT=spanningcheckerlist[0].spanningsize
                    for x in tempspanninglist:
                            if int(x) == spanningcheckerlist[0].spanningsize:
                                    for u in compresolver:
                                            if u[0] == x:
                                                    SMALL_INT_LOC = u[1]
            for f in tempspanninglist:
                if (str(f) == str(LG_Result) or str(f) == str(SM_RESULT)) == True:
                    continue
                if (str(f) == str(LG_Result) or str(f) == str(SM_RESULT)) == False:
                    if (f in norepeaterfornotes) == False:
                        if len(notcompdict[f]) > 0:
                            NOTESINTER.append("NC:")
                        for obj in notcompdict[f]:
                            NOTESINTER.append("Spanningsize "+obj.spanningsize+" w/ Interruptions@"+str(obj.interruptionlocation)+";#Reads: "+str(obj.numsimiliar)+"@ReadNumbers-"+str(obj.readnumlist))
                    if len(compdict[f]) > 0:
                        NOTESINTER.append("~C:")
                    for obj in compdict[f]:
                        NOTESINTER.append("Spanningsize "+obj.spanningsize+" w/ Interruptions@"+str(obj.interruptionlocation)+";#Reads: "+str(obj.numsimiliar)+"@ReadNumbers-"+str(obj.readnumlist))
            NOTES.append(''.join(NOTESINTER))
            NOTESINTER = []
        elif int(spanningcheckerlist[0].percentagespanning)>=selectivity and ((int(spanningcheckerlist[1].percentagespanning)>=selectivity)==False):
                if (spanningcheckerlist[1].reads>(int(spanningcheckerlist[2].reads) + 2)):
                    if spanningcheckerlist[0].spanningsize > spanningcheckerlist[1].spanningsize:
                            LG_Result=spanningcheckerlist[0].spanningsize
                            for x in tempspanninglist:
                                if int(x) == spanningcheckerlist[0].spanningsize:
                                        for u in compresolver:
                                                if u[0] == x:
                                                        Large_INT_LOC = u[1]
                            SM_RESULT=spanningcheckerlist[1].spanningsize
                            for x in tempspanninglist:
                                    if int(x) == spanningcheckerlist[1].spanningsize:
                                            for u in compresolver:
                                                    if u[0] == x:
                                                            SMALL_INT_LOC = u[1]
                    if spanningcheckerlist[1].spanningsize > spanningcheckerlist[0].spanningsize:
                            LG_Result=spanningcheckerlist[1].spanningsize
                            for x in tempspanninglist:
                                if int(x) == spanningcheckerlist[1].spanningsize:
                                        for u in compresolver:
                                                if u[0] == x:
                                                        Large_INT_LOC = u[1]
                            SM_RESULT=spanningcheckerlist[0].spanningsize
                            for x in tempspanninglist:
                                    if int(x) == spanningcheckerlist[0].spanningsize:
                                            for u in compresolver:
                                                    if u[0] == x:
                                                            SMALL_INT_LOC = u[1]
                    for f in tempspanninglist:
                        if (str(f) == str(LG_Result) or str(f) == str(SM_RESULT)) == True:
                            continue
                        if (str(f) == str(LG_Result) or str(f) == str(SM_RESULT)) == False:
                            if (f in norepeaterfornotes) == False:
                                if len(notcompdict[f]) > 0:
                                    NOTESINTER.append("NC:")
                                for obj in notcompdict[f]:
                                    NOTESINTER.append("Spanningsize "+obj.spanningsize+" w/ Interruptions@"+str(obj.interruptionlocation)+";#Reads: "+str(obj.numsimiliar)+"@ReadNumbers-"+str(obj.readnumlist))
                            if len(compdict[f]) > 0:
                                NOTESINTER.append("~C:")
                            for obj in compdict[f]:
                                NOTESINTER.append("Spanningsize "+obj.spanningsize+" w/ Interruptions@"+str(obj.interruptionlocation)+";#Reads: "+str(obj.numsimiliar)+"@ReadNumbers-"+str(obj.readnumlist))
                    NOTES.append(''.join(NOTESINTER))
                    NOTESINTER = []
                if spanningcheckerlist[2].reads<=spanningcheckerlist[1].reads<=(int(spanningcheckerlist[2].reads) + 2):
                    if spanningcheckerlist[1].spanningsize > spanningcheckerlist[2].spanningsize:
                            if spanningcheckerlist[0].spanningsize > spanningcheckerlist[1].spanningsize:
                                    LG_Result=spanningcheckerlist[0].spanningsize
                                    for x in tempspanninglist:
                                        if int(x) == spanningcheckerlist[0].spanningsize:
                                                for u in compresolver:
                                                        if u[0] == x:
                                                                Large_INT_LOC = u[1]
                                    SM_RESULT=spanningcheckerlist[1].spanningsize
                                    for x in tempspanninglist:
                                            if int(x) == spanningcheckerlist[1].spanningsize:
                                                    for u in compresolver:
                                                            if u[0] == x:
                                                                    SMALL_INT_LOC = u[1]
                            if spanningcheckerlist[1].spanningsize > spanningcheckerlist[0].spanningsize:
                                    LG_Result=spanningcheckerlist[1].spanningsize
                                    for x in tempspanninglist:
                                        if int(x) == spanningcheckerlist[1].spanningsize:
                                                for u in compresolver:
                                                        if u[0] == x:
                                                                Large_INT_LOC = u[1]
                                    SM_RESULT=spanningcheckerlist[0].spanningsize
                                    for x in tempspanninglist:
                                            if int(x) == spanningcheckerlist[0].spanningsize:
                                                    for u in compresolver:
                                                            if u[0] == x:
                                                                    SMALL_INT_LOC = u[1]
                            NOTES.append("Error with the Small spanningsize; SimReads as Spanningsize: "+str(spanningcheckerlist[2].spanningsize))
                    if spanningcheckerlist[2].spanningsize > spanningcheckerlist[1].spanningsize:
                            if spanningcheckerlist[0].spanningsize > spanningcheckerlist[2].spanningsize:
                                    LG_Result=spanningcheckerlist[0].spanningsize
                                    for x in tempspanninglist:
                                        if int(x) == spanningcheckerlist[0].spanningsize:
                                                for u in compresolver:
                                                        if u[0] == x:
                                                                Large_INT_LOC = u[1]
                                    SM_RESULT=spanningcheckerlist[2].spanningsize
                                    for x in tempspanninglist:
                                            if int(x) == spanningcheckerlist[2].spanningsize:
                                                    for u in compresolver:
                                                            if u[0] == x:
                                                                    SMALL_INT_LOC = u[1]
                            if spanningcheckerlist[2].spanningsize > spanningcheckerlist[0].spanningsize:
                                    LG_Result=spanningcheckerlist[2].spanningsize
                                    for x in tempspanninglist:
                                        if int(x) == spanningcheckerlist[2].spanningsize:
                                                for u in compresolver:
                                                        if u[0] == x:
                                                                Large_INT_LOC = u[1]
                                    SM_RESULT=spanningcheckerlist[0].spanningsize
                                    for x in tempspanninglist:
                                            if int(x) == spanningcheckerlist[0].spanningsize:
                                                    for u in compresolver:
                                                            if u[0] == x:
                                                                    SMALL_INT_LOC = u[1]
                            NOTES.append("Error with the Small spanningsize; SimReads as Spanningsize: "+str(spanningcheckerlist[1].spanningsize))
        else:
                if spanningcheckerlist[0].spanningsize > spanningcheckerlist[1].spanningsize:
                    LG_Result=spanningcheckerlist[0].spanningsize
                    for x in tempspanninglist:
                            if int(x) == spanningcheckerlist[0].spanningsize:
                                    for u in compresolver:
                                            if u[0] == x:
                                                    Large_INT_LOC = u[1]
                    SM_RESULT=spanningcheckerlist[1].spanningsize
                    for x in tempspanninglist:
                            if int(x) == spanningcheckerlist[1].spanningsize:
                                    for u in compresolver:
                                            if u[0] == x:
                                                    SMALL_INT_LOC = u[1]
                if spanningcheckerlist[1].spanningsize > spanningcheckerlist[0].spanningsize:
                    LG_Result=spanningcheckerlist[1].spanningsize
                    for x in tempspanninglist:
                            if int(x) == spanningcheckerlist[1].spanningsize:
                                    for u in compresolver:
                                            if u[0] == x:
                                                    Large_INT_LOC = u[1]
                    SM_RESULT=spanningcheckerlist[0].spanningsize
                    for x in tempspanninglist:
                            if int(x) == spanningcheckerlist[0].spanningsize:
                                    for u in compresolver:
                                            if u[0] == x:
                                                    SMALL_INT_LOC = u[1]
                for f in tempspanninglist:
                    if (str(f) == str(LG_Result) or str(f) == str(SM_RESULT)) == True:
                        continue
                    if (str(f) == str(LG_Result) or str(f) == str(SM_RESULT)) == False:
                        if (f in norepeaterfornotes) == False:
                            if len(notcompdict[f]) > 0:
                                NOTESINTER.append("NC:")
                            for obj in notcompdict[f]:
                                NOTESINTER.append("Spanningsize "+obj.spanningsize+" w/ Interruptions@"+str(obj.interruptionlocation)+";#Reads: "+str(obj.numsimiliar)+"@ReadNumbers-"+str(obj.readnumlist))
                        if len(compdict[f]) > 0:
                            NOTESINTER.append("~C:")
                        for obj in compdict[f]:
                            NOTESINTER.append("Spanningsize "+obj.spanningsize+" w/ Interruptions@"+str(obj.interruptionlocation)+";#Reads: "+str(obj.numsimiliar)+"@ReadNumbers-"+str(obj.readnumlist))
                NOTES.append(''.join(NOTESINTER))
                NOTESINTER = []

    #CSV - PRODUCTION
    Large=len(Large_INT_LOC)
    SMALL=len(SMALL_INT_LOC)
    NOTES = '(;)'.join(NOTES)
    Flanking_Reads = ', '.join(Flanking_Reads)
    Error_Reads = ', '.join(Error_Reads)
    for i in Large_INT_LOC:
        joinertemp.append(str(i))
    Large_INT_LOC = ', '.join(joinertemp)
    joinertemp = []
    for i in SMALL_INT_LOC:
        joinertemp.append(str(i))
    SMALL_INT_LOC = ', '.join(joinertemp)
    if (outputfile == 'N') == False:
            with open(csvfile, "a", newline='') as fp:
                    wr = csv.writer(fp, dialect='excel')
                    for obj in vcflist:
                            fileexistenceholder=obj.existence
                            exp_res=obj.EXP_RES
                    wr.writerow([str(z), fileexistenceholder, IGM_SUB, GROUP, BH_GT, exp_res, LG_Result, Large, Large_INT_LOC, SM_RESULT, SMALL, SMALL_INT_LOC, NOTES, ERROR, Flanking_Reads, Error_Reads])

    #Print Section
    if (outputfile == 'N') == True:
            print("The CHGVID: " + z)
            print("LG_Result: " +str(LG_Result))
            print("Large: " +str(Large))
            print("Large_INT_LOC: " +str(Large_INT_LOC))
            print("SM_RESULT: " +str(SM_RESULT))
            print("SMALL: " +str(SMALL))
            print("SMALL_INT_LOC: " +str(SMALL_INT_LOC))
            print("NOTES: " +str(NOTES))
            print("ERROR: " +str(ERROR))
            print("Flanking_Reads: " +str(Flanking_Reads))
            print("Error_Reads: " +str(Error_Reads))
    if testermode == 1:
            #CHECK (Excel Output)
            print("The CHGVID: " + z)
            print("LG_Result: " +str(LG_Result))
            print("Large: " +str(Large))
            print("Large_INT_LOC: " +str(Large_INT_LOC))
            print("SM_RESULT: " +str(SM_RESULT))
            print("SMALL: " +str(SMALL))
            print("SMALL_INT_LOC: " +str(SMALL_INT_LOC))
            print("NOTES: " +str(NOTES))
            print("ERROR: " +str(ERROR))
            print("Flanking_Reads: " +str(Flanking_Reads))
            print("Error_Reads: " +str(Error_Reads))

            for obj in spanninglist:
                print(obj.spanningsize, obj.reads, sep =', ' )

            for i in tempspanninglist:
                    print(i)
                    for obj in d[i]:
                            print(obj.lineRead, obj.frameStart, obj.frameEnd, sep =', ' )

            for i in tempspanninglist:
                    for obj in inter[i]:
                            print(i, obj.interruptionlocation, obj.LEFTinterruptionlocation, obj.countHolder, obj.LClocations, sep =', ' )

            print("This is the number of flanking reads: " + str(flankingreads))
            for obj in flankingfinal:
                print(obj.lineRead, obj.frameStart, obj.frameEnd, obj.interruptionlocation, obj.interruptioncount, obj.repeatlocation, obj.repeatcount, obj.frame, obj.LowerCaseLocations, sep =', ' )

            for obj in vcflist:
                    print( obj.filename, obj.existence, obj.EXP_RES, sep =', ' )

            for i in tempspanninglist:
                    print(i)
                    for obj in d[i]:
                            print(obj.lineRead, obj.frameStart, obj.frameEnd, sep =', ' )

            for i in tempspanninglist:
                    for obj in inter[i]:
                            print(i, obj.interruptionlocation, obj.LEFTinterruptionlocation, obj.countHolder, obj.LClocations, sep =', ' )

            print("This is the number of flanking reads: " + str(flankingreads))
            for obj in flankingfinal:
                print(obj.interruptionlocation, obj.interruptioncount, obj.repeatlocation, obj.repeatcount, obj.frame, obj.LowerCaseLocations, sep =', ' )
if testermode == 1 and ((outputfile == 'N')== False):
        print(open(outputfile+'.csv', 'r').read())
