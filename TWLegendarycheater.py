import os, os.path
import shutil
import time

AutoSaveThreshold=20

TKTWDir = 'C://Users//Administrator//AppData//Roaming//The Creative Assembly//ThreeKingdoms//save_games'

BackupDir = 'G://Games//SaveGameBackup//AutoSave'

onGoingCampaignFileName = ''

testDir1 = 'G://Games//SaveGameBackup//test1'
testDir2 = 'G://Games//SaveGameBackup//test2'


class saveGameFileObj():
    fileDir = ''
    fileName = ''
    fileTime = ''
    destinationDir = ''
    allNameParts = []
    fileNameWithoutSuffix = ''
    fileSuffix = ''
    backupNumber = ''

    def __init__(self, svgmDir, svgmName, svgmTime, dstDir):
        self.fileDir = svgmDir
        self.fileName = svgmName
        self.fullPath=self.fileDir + '//' + self.fileName
        self.fileTime = svgmTime
        self.destinationDir = dstDir
        self.allNameParts = self.fileName.split('.')
        self.fileSuffix = self.allNameParts[-1]
        fileNameWithoutSuffixList = self.allNameParts[:-1]
        for aPart in fileNameWithoutSuffixList:
            self.fileNameWithoutSuffix += aPart+'.'
        self.fileNameWithoutSuffix=self.fileNameWithoutSuffix[:-1]

    def saveGameFileCopy(self, bkupNumber):
        srcFullPath = self.fileDir + '//' + self.fileName
        dstFullPath = self.destinationDir + '//' + self.fileNameWithoutSuffix + 'xxx' + str(bkupNumber) + '.' + self.fileSuffix
        shutil.copy2(srcFullPath, dstFullPath)


copyNumber = 0
while (True):
    allSrcFiles = []
    allDstFiles = []
    for filename in os.listdir(TKTWDir):
        tempSaveTime = os.path.getmtime(os.path.join(TKTWDir, filename))
        allSrcFiles.append(saveGameFileObj(TKTWDir, filename, tempSaveTime, BackupDir))

    allSrcFiles.sort(key=lambda aFile: aFile.fileTime)
    for filename in os.listdir(BackupDir):
        tempSaveTime = os.path.getmtime(os.path.join(BackupDir, filename))
        allDstFiles.append(saveGameFileObj(BackupDir, filename, tempSaveTime, BackupDir))

    allSrcFiles.sort(key=lambda aFile: aFile.fileTime)
    allDstFiles.sort(key=lambda aFile: aFile.fileTime)
    for aFile in allSrcFiles:
        print(aFile.fullPath,aFile.fileTime)
    for aFile in allDstFiles:
        print(aFile.fullPath,aFile.fileTime)
    print('===========================================All Files Loaded===========================================')
    if len(allDstFiles) > 0:
        if allSrcFiles[-1].fileTime != allDstFiles[-1].fileTime:
            print('===========================================Modification Detected In Newest File Comparison===========================================')

            if AutoSaveThreshold > len(allDstFiles):
                allSrcFiles[-1].saveGameFileCopy(copyNumber)
                copyNumber += 1
                allDstFiles.append(allSrcFiles[-1])
                allDstFiles.sort(key=lambda aFile: aFile.fileTime)
                for aFile in allDstFiles:
                    print('sorted=====================',aFile.fullPath, aFile.fileTime)
            else:
                os.remove(allDstFiles[0].fullPath)
                allDstFiles.pop(0)
                allSrcFiles[-1].saveGameFileCopy(copyNumber)
                copyNumber += 1
                allDstFiles.append(allSrcFiles[-1])
                allDstFiles.sort(key=lambda aFile: aFile.fileTime)

        else:
            print('===========================================Doing Nothing===========================================')
    else:
        allSrcFiles[-1].saveGameFileCopy(copyNumber)
        copyNumber += 1
        allDstFiles.append(allSrcFiles[-1])
        allDstFiles.sort(key=lambda aFile: aFile.fileTime)


    time.sleep(10)
