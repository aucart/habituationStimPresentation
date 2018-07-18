# coding: utf8
from __future__ import unicode_literals

"""  Experiment #1: Looking-time infant study
Phase 3 : habituation
=*=*=**=*=*=*=*=*=*=*=*=*INSTRUCTIONS=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*

see instructions.txt

/!\ According to the phase run, not the same stim :
If run phase 3 alone, i.e. second argument "3" : a and i stimuli (instead of u and y)
In all other cases, u and y stimuli are used.

"""

from psychopy import visual, core, event, logging
import pandas as pd
import datetime

from helper_fcts import *
import pyglet

# MAIN =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
if __name__ == "__main__":
    tgt = ""
    # ********** parameters to change *******
    securityDelayRelease = 3    # delay (in sedoncsà) for skipping video after key release (! not fot key press)
    subj = 1
    phases = 3

    # fixed params
    randMethod = 'realRandom'
    maxNbHabTrials = 24
    nbTrialsForHabituation = 3

    src_media_root = "./media"

    currentlyCodedPhases = [3]
    factorCompareAve = 0.6 # Control parameter for habituation criteria : average_duration(3 last trials) < factorCompareAve * average_duration(3 longest trials)

    # Parameters  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
    # == Program environment parameter  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
    # Display parameters
    backgroundColor = [-1, -1, -1]  # black=(0,0,0)  -- gray = (150, 150, 150)

    if True: # check that was initially meant for command line, but better safe than sorry.
        # Format the parameters:
        subj = int(subj)
        phaseLst = [int(phaseDigit) for phaseDigit in str(phases)]
        # Check (2)
        for p in phaseLst:
            if p not in currentlyCodedPhases:
                raise IOError("Please specify phases only among : ", currentlyCodedPhases)

    print("Starting experiment phases ", phaseLst ,"for subj number ", subj)


    # Randomisation  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=
    cdtNb = randomization(randMethod) #1, 2, 3 or 4


    # Start  =*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
    # Params for the output
    curDateTime = datetime.datetime.now().strftime('%Y-%m-%d-%Hh%M')
    headerLine, dico = initOutput(subj, cdtNb, curDateTime) #takes date and time and prepare dictionnary for storing data for output
    expeFinished=False
    dicoInfoOut = {"dico":dico, "headerLine": headerLine,  "tgt": tgt, "curDateTime":curDateTime, "expeFinished": expeFinished}

    # INIT SCREEN
    win = visual.Window(fullscr=True, units='pix', monitor='testMonitor', color=backgroundColor)


    # INIT PYGLET (handle key press AND RELEASE -- because otherwise can only get key press)
    keyPyglet = pyglet.window.key
    keyPyglet_name = keyPyglet.NUM_ADD   #keyPyglet.SPACE
    keyChecker = keyPyglet.KeyStateHandler()
    win.winHandle.push_handlers(keyChecker)


    #****** SECURITY CHECK BEFORE STARTING EXPERIMENT - plays attention just once **********

    controlKey =  'space'
    # ****** Test Keyboard : first space to tset, second to start **********
    instr = visual.TextStim(win, text="Press the " + str(controlKey) + " key to skip the text, and '+' key to skip the videos.")
    event.clearEvents();    instr.draw();    win.flip()
    while True:
        if controlKey in event.getKeys() : #| ('+' in event.getKeys() ) | ('plus' in event.getKeys() ) :
            break

    cur_file_name = "attention"
    vid_path = src_media_root + "/" + cur_file_name + ".mov"
    # VIDEO BLOCK
    mov = visual.MovieStim3(win, vid_path, flipVert=False, flipHoriz=False, loop=False)
    timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov, win, dicoInfoOut, keyPyglet_name, keyChecker,
                                                      keySkip="press")

    instr = visual.TextStim(win, text="Press the " + str(controlKey) + " key to start, then '+' key to skip the videos.")
    event.clearEvents();    instr.draw();    win.flip()
    while True:
        if controlKey in event.getKeys():
            break


    #***** END CHECK**********


    # =*=*=* Attention-getter : Loop until key press
    cur_attention = "attention"
    vid_path_att = src_media_root + "/" + cur_attention + ".mov"
    mov_att = visual.MovieStim3(win, vid_path_att, flipVert=False, flipHoriz=False, loop=True)
    timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov_att, win, dicoInfoOut, keyPyglet_name, keyChecker, keySkip="press")

    overallTrialNb =  1
    dico = updateOutput(dico, overallTrialNb, timeInfo, stoppedByKeyPress, "attention_getter", cur_attention)

    # =*=*=* SECOND VIDEO UNTIL KEY RELEASE
    cur_file_name = "pretest"
    vid_path = src_media_root + "/" + cur_file_name + ".mov"
    mov = visual.MovieStim3(win, vid_path, flipVert=False, flipHoriz=False, loop=False)
    timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov, win, dicoInfoOut, keyPyglet_name, keyChecker, keySkip="release", securityDelayRelease=securityDelayRelease)
    overallTrialNb = 2
    dico = updateOutput(dico, overallTrialNb, timeInfo, stoppedByKeyPress, "pretest", cur_file_name)


    # =*=*=**=*=*=*=*=*=*=*=*  HABITUATION SECTION =*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*
    # LOAD VIDEO HABITUATION PHASE==============

    # hab - u.mp4  or hab - y.mp4   || phase 3 only : (uÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢a, y ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ i)
    if phaseLst == [3]: # Case where we ran phase 3 alone
        file_stimU = "hab-a"
        file_stimY = "hab-i"
    else:
        file_stimU = "hab-u"
        file_stimY = "hab-y"

    if cdtNb in [1,2]:
        cur_file_name = file_stimU
    else:
        cur_file_name = file_stimY

    vid_path = src_media_root + "/" + cur_file_name + "_trial.mp4"


    # VIDEO BLOCK
    loopUntilKey = False
    list_length_trials, nbOfFull, stoppedByKeyPress, dico =  playVideo_stopHabituation(win, dicoInfoOut, keyPyglet_name, keyChecker, vid_path, dico, src_media_root,
                      securityDelayRelease=securityDelayRelease,  maxNbHabTrials=maxNbHabTrials, nTrialsToCompare_Habituation=3, factorCompareAve=factorCompareAve)
                            # stop when criteria met or reached 24 habituation trial
                            # criteria is : ave_last < factorCompareAve*ave_longest
                            # i.e. with current parameters = average duration 3 last trials > 0.6 * average duration 3 longest trials


    # =*=*=**=*=*=*=*=*=*=*=* TEST SECTION =*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*

    # > 14 trials (attention then test), each trial ends when the file finishes, or when there's a key press

    cdtPgm = getCdts_testPart(cdtNb, phaseLst) # get the list of files corresponding to the condition
    overallTrialNb = len(dico["n"]) + 1

    cdtPgmToPlay = cdtPgm

    for testFileName in cdtPgmToPlay:
        # =*=*=* Attention-getter : Loop until key press
        cur_attention = "attention"
        vid_path_att = src_media_root + "/" + cur_attention + ".mov"
        mov_att = visual.MovieStim3(win, vid_path_att, flipVert=False, flipHoriz=False, loop=True)
        timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov_att, win, dicoInfoOut, keyPyglet_name, keyChecker,  keySkip="press")
        overallTrialNb = len(dico["n"]) + 1
        dico = updateOutput(dico, overallTrialNb, timeInfo, stoppedByKeyPress, "attention_getter",  cur_attention)  # (dico, n, timeInfo, end, type, stim)

        # =*=*=* SECOND VIDEO UNTIL KEY RELEASE
        vid_path = src_media_root + "/" + "test-" + testFileName + "_trial.mp4"
        mov = visual.MovieStim3(win, vid_path, flipVert=False, flipHoriz=False, loop=False)
        timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov, win, dicoInfoOut, keyPyglet_name, keyChecker,
                                               keySkip="release",  securityDelayRelease=securityDelayRelease)
        overallTrialNb = len(dico["n"]) + 1
        dico = updateOutput(dico, overallTrialNb, timeInfo, stoppedByKeyPress, "posttest", testFileName)


    # =*=*=**=*=*=*=*=*=*=*=* POSTTEST SECTION =*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*

    # =*=*=* Attention-getter : Loop until key press
    cur_attention = "attention"
    vid_path_att = src_media_root + "/" + cur_attention + ".mov"
    mov_att = visual.MovieStim3(win, vid_path_att, flipVert=False, flipHoriz=False, loop=True)
    timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov_att, win, dicoInfoOut, keyPyglet_name, keyChecker, keySkip="press")

    overallTrialNb = len(dico["n"]) + 1
    dico = updateOutput(dico, overallTrialNb, timeInfo, stoppedByKeyPress, "attention_getter",
                        cur_attention)  # (dico, n, timeInfo, end, type, stim)

    # =*=*=* SECOND VIDEO UNTIL KEY RELEASE
    cur_file_name = "pretest"
    vid_path = src_media_root + "/" + cur_file_name + ".mov"
    mov = visual.MovieStim3(win, vid_path, flipVert=False, flipHoriz=False, loop=False)
    timeInfo, nbOfFull, stoppedByKeyPress = playVideo(mov, win, dicoInfoOut, keyPyglet_name, keyChecker,
                                            keySkip="release", securityDelayRelease=securityDelayRelease)
    overallTrialNb = len(dico["n"]) + 1
    dico = updateOutput(dico, overallTrialNb, timeInfo, stoppedByKeyPress, "posttest", cur_file_name)

    expeFinished=True
    
    #***************************************
    # FINAL SCREEN
    instr = visual.TextStim(win, text="Esc to exit.")
    event.clearEvents()
    instr.draw()
    win.flip()

    #***************************************
    # POST PROCESSING CSV
    postProcessSaveOutput(dico, headerLine, tgt, curDateTime, expeFinished)

    #***************************************

    core.quit()