# coding: utf8
from __future__ import unicode_literals

from psychopy import visual, core, event, logging
import os.path
import pandas as pd

import sys
import pygame
import os
import math
from random import randint

def randomization(randMethod = 'realRandom'):
    if randMethod == 'realRandom':
        r = randint(1,4) #integer 1, 2, 3 or 4
    #to do: pseudorand option
    return r

def getCdts_testPart(cdtNb, phaseLst):
    """ Gives the list of files corresponding to the condition

    Cd1 nb 1, 2, 3, 4 for : u-c, u-s, y-c, y-s

    in the excel file there is :
               1              2              3              4
0   uy-alt-yfirst      uy-same-u  uy-alt-ufirst      uy-same-y
1       uy-same-u  uy-alt-yfirst      uy-same-y  uy-alt-ufirst
2       uy-same-u      uy-same-u      uy-same-y      uy-same-y
3       uy-same-u      uy-same-u      uy-same-y      uy-same-y
4   uy-alt-yfirst  uy-alt-yfirst  uy-alt-ufirst  uy-alt-ufirst
5       uy-same-u      uy-same-u      uy-same-y      uy-same-y
6       uy-same-u      uy-same-u      uy-same-y      uy-same-y
7   uy-alt-yfirst  uy-alt-yfirst  uy-alt-ufirst  uy-alt-ufirst
8       uy-same-u      uy-same-u      uy-same-y      uy-same-y
9       uy-same-u      uy-same-u      uy-same-y      uy-same-y
10      uy-same-u      uy-same-u      uy-same-y      uy-same-y
11      uy-same-u      uy-same-u      uy-same-y      uy-same-y
12      uy-same-u      uy-same-u      uy-same-y      uy-same-y
13  uy-alt-yfirst  uy-alt-yfirst  uy-alt-ufirst  uy-alt-ufirst
    """


    if phaseLst == [3]:
        cdtsFile="/conditions_ai.xls"
    else:
        cdtsFile="/conditions_uy.xls"

    src = os.getcwd()
    filePath =src+cdtsFile
    filePath = filePath        # adapt the path to any OS to avoid slash issues

    df = pd.read_excel(filePath, header=0)

    cdtPgm = df.loc[:, cdtNb].ravel().tolist() # selects columns and put it to list

    return cdtPgm


def postProcessSaveOutput(dico, headerLine, tgt, curDateTime, expeFinished):
    df = pd.DataFrame.from_dict(dico)
    df = df.reindex(columns=["n", "on", "off", "end", "duration", "type", "stim"])

    # trick to add a first row and reset index properly
    df.loc[-1] = headerLine  # adding a row
    df.index = df.index + 1  # shifting index
    df = df.sort_index()  # sorting by index

    print(df)
    fileName = tgt + "output_" + curDateTime
    if not expeFinished:
        fileName += "_stoppedBeforeEnd"

    df.to_csv(fileName + ".csv")


def playVideo_stopHabituation(win, kwOut, keyPyglet, keyChecker, vid_path, dico, src_media_root, securityDelayRelease=2,
                maxNbHabTrials=10, nTrialsToCompare_Habituation=3, factorCompareAve=0.6, keySkipLst=['0'], minimalNbOfTrials=6):
    """ Loop trials until there is habituation (criteria: average duration of n (nTrialsToCompare_Habituation) last trials vs. n longest trials) or reach the maximum nb of trials (maxNbHabTrials)
    where: 1 trial = 1 movie play until end of movie

    Habituation criteria is : ave_last < factorCompareAve*ave_longest
    i.e. with current parameters = average duration 3 last trials > 0.6 * average duration 3 longest trials

    """
    list_length_trials = []

    skip = False
    while ( not skip ) & ( len(list_length_trials) < maxNbHabTrials ) :
        # =*=*=* Attention-getter : Loop until key press
        cur_attention = "attention"
        vid_path_att = src_media_root + "/" + cur_attention + ".mov"
        loopUntilKey = True  # todo : put False instead if you want to play attention getter only once - otherwise it will loop till key press as usual
        mov_att = visual.MovieStim3(win, vid_path_att, flipVert=False, flipHoriz=False, loop=loopUntilKey)
        timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov_att, win, kwOut, keyPyglet, keyChecker, keySkip="press")

        overallTrialNb = len(dico["n"]) + 1
        dico = updateOutput(dico, overallTrialNb, timeInfo, stoppedByKeyPress, "attention_getter",    cur_attention)  # (dico, n, timeInfo, end, type, stim)

        # =*=*=* SECOND VIDEO UNTIL KEY RELEASE
        mov = visual.MovieStim3(win, vid_path, flipVert=False, flipHoriz=False, loop=False)
        timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov, win, kwOut, keyPyglet, keyChecker, keySkip="release", maxNbOfPlay=None, keySkipLst=keySkipLst, securityDelayRelease=securityDelayRelease)

        list_length_trials.append( timeInfo["trialDuration"] )

        if len(list_length_trials) > minimalNbOfTrials:
            last_n = list_length_trials[-nTrialsToCompare_Habituation:] # get last n

            list_length_trials_sorted = sorted(list_length_trials)  # sort by increasing duration
            n_longest = list_length_trials_sorted[-nTrialsToCompare_Habituation:] # get n longest

            ave_last = sum(last_n) / 3
            ave_longest = sum(n_longest) / 3


            if ave_last < factorCompareAve*ave_longest: # if average of the trial duration over the last 3 trials is smaller than .60*average duration of the longest 3 trial
                skip = True # stop habituation

        temp = os.path.join("1", "2")
        temp = temp.replace('1', '');temp.replace('2', '')
        cur_file_name = vid_path.split(temp)[-1][:-4]
        overallTrialNb = len(dico["n"]) + 1
        dico = updateOutput(dico, overallTrialNb, timeInfo, stoppedByKeyPress, "habituation", cur_file_name)  # (dico, n, timeInfo, end, type, stim)
        overallTrialNb += 1

    return list_length_trials, nbOfFull, stoppedByKeyPress, dico


def playVideo(mov, win, kwOut, keyPyglet_name, keyChecker, keySkip,  maxNbOfPlay=None, keySkipLst = ['space'], securityDelayRelease=2):
    stoppedByKey = False
    trialClock = core.Clock()
    tStartLoop = trialClock.getTime()

    timeFistRelease = 0; timeAfterFirstRelease=0

    response = False
    while (mov.status != visual.FINISHED) & (not response):
       mov.draw(win)
       win.flip()

       for key in event.getKeys():
          if key in ['escape','q']:
             postProcessSaveOutput(**kwOut)
             win.close()
             core.quit()

       if keySkip=="press" :  #'NUM_0' '0' 'ENTER'  key.RETURN key.NUM_ENTER key.NUM_ADD key.NUM_1
           if (keyChecker[keyPyglet_name] is True): #keyPyglet.NUM_0]
               tEnd = trialClock.getTime()
               response = True
               mov.pause() # for some reason, mov.stop() only stops video and not sound. So both pause() and stop() are needed
               mov.stop()
               stoppedByKey=True
       else: #release
           if (keyChecker[keyPyglet_name] is False):
               if timeFistRelease == 0:
                   timeFistRelease = trialClock.getTime()
                   tEnd = timeFistRelease
               else:
                   timeAfterFirstRelease = trialClock.getTime() - timeFistRelease

               if timeAfterFirstRelease > securityDelayRelease:
                   response = True
                   mov.pause()
                   mov.stop()
                   stoppedByKey=True

           else: # if re-press after a release, reinitialise timeFistRelease
               timeFistRelease = 0

       durMovie = mov.duration
       curDurationSinceStartPlay = trialClock.getTime() - tStartLoop
       nbOfFullPlays = math.floor( curDurationSinceStartPlay / durMovie)

       if maxNbOfPlay is not None:
           if (nbOfFullPlays>=maxNbOfPlay):
               tEnd = trialClock.getTime()
               response = True
               mov.pause()
               mov.stop()

    if (mov.status == visual.FINISHED) & (not response): # if option mov (input) was not loop,  got out of the loop before keypresss and because movie had to be played once entirely
        tEnd = trialClock.getTime()

    timeInfo = {}
    timeInfo["tStartLoop"] = tStartLoop
    timeInfo["tEnd"] = tEnd
    timeInfo["trialDuration"] = tEnd-tStartLoop #duration in seconds

    return timeInfo, nbOfFullPlays, stoppedByKey


def initOutput(subj, cdtNb, curDateTime):

    # "header" part : dd main informations on the first row (to be read in line and not in column like the rest)
    dicoFirstRow={}
    dicoFirstRow[0] = ["MainInfo", "ID", subj, "TimeDate", curDateTime, "CdtNb", cdtNb]
    dfFirstRow = pd.DataFrame.from_dict(dicoFirstRow)
    headerLine = dfFirstRow.T.iloc[0,:].ravel().tolist()

    # what will be updated throughout the experiment
    dico = {}
    dico["n"] = []
    dico["on"] = []
    dico["off"] = []
    dico["end"] = []
    dico["duration"] = []
    dico["type"] = []
    dico["stim"] = []

    return headerLine, dico


def updateOutput(dico, n, timeInfo, end, type, stim):

    if end: #stoppedByKeyPress = True
        endStr = "keypress"
    else:
        endStr = "end"

    on = timeInfo["tStartLoop"]
    off = timeInfo["tEnd"]
    dur = timeInfo["trialDuration"]

    dico["n"].append(n)
    dico["on"].append(on)
    dico["off"].append(off)
    dico["end"].append(endStr)
    dico["duration"].append(dur)
    dico["type"].append(type)
    dico["stim"].append(stim)

    return dico
