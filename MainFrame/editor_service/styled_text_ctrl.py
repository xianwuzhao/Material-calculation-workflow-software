#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Taken from wxpython 4.0.7 post2, demo/Styled_text_ctrl_2.py.
   2020-3-1"""


from .text_editor_keyword import keyword_list

import wx
import wx.stc as stc


if wx.Platform == '__WXMSW__':
    faces = {'times': 'Times New Roman',
             'mono': 'Courier New',
             'helv': 'Arial',
             'other': 'Comic Sans MS',
             'size': 12,
             'size2': 8,
             }
elif wx.Platform == '__WXMAC__':
    faces = {'times': 'Times New Roman',
             'mono': 'Monaco',
             'helv': 'Arial',
             'other': 'Comic Sans MS',
             'size': 12,
             'size2': 10,
             }
else:
    faces = {'times': 'Times',
             'mono': 'Courier',
             'helv': 'Helvetica',
             'other': 'new century schoolbook',
             'size': 12,
             'size2': 10,
             }


class PythonSTC(stc.StyledTextCtrl):

    def __init__(self, parent, ID,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)

        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)  # ctrl +  放大
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)  # ctrl - 缩小
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword_list))  # 关键字
        # Setup a margin to hold fold markers
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        # and now set up the fold markers
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "black")
        # Global default style
        if wx.Platform == '__WXMSW__':
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                              'fore:#000000,back:#FFFFFF,face:Courier New')
        elif wx.Platform == '__WXMAC__':
            # TODO: if this looks fine on Linux too, remove the Mac-specific case
            # and use this whenever OS != MSW.
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                              'fore:#000000,back:#FFFFFF,face:Monaco')
        else:
            defsize = wx.SystemSettings.GetFont(wx.SYS_ANSI_FIXED_FONT).GetPointSize()
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                              'fore:#000000,back:#FFFFFF,face:Courier,size:%d' % defsize)
        # Clear styles and revert to default.
        self.StyleClearAll()
        # Following style specs only indicate differences from default.
        # The rest remains unchanged.
        # Line numbers in margin
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, 'fore:#000000,back:#99A9C2')
        # Highlighted brace
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, 'fore:#00009D,back:#FFFF00')
        # Unmatched brace
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, 'fore:#00009D,back:#FF0000')
        # Indentation guide
        self.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")

        # Python styles
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, 'fore:#000000')
        # Comments
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, 'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, 'fore:#008000,back:#F0FFF0')
        # Numbers
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, 'fore:#0000FF')
        # Strings and characters
        self.StyleSetSpec(wx.stc.STC_P_STRING, 'fore:#800080')
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, 'fore:#800080')
        # Keywords
        self.StyleSetSpec(wx.stc.STC_P_WORD, 'fore:#000080,bold')
        # Triple quotes
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, 'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, 'fore:#800080,back:#FFFFEA')
        # Class names
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        # Function names
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, 'fore:#008080,bold')
        # Operators
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, 'fore:#800000,bold')
        # Identifiers. I leave this as not bold because everything seems
        # to be an identifier if it doesn't match the above criterae
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')

        # Caret color
        self.SetCaretForeground("BLUE")
        # Selection background
        self.SetSelBackground(1, '#66CCFF')

        self.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

    def OnKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()

        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()

            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                                      'show some suff, maybe parameters..\n\n'
                                      'fubar(param1, param2)')
            # Code completion
            else:
                kw = keyword_list[:]
                kw.append("zzzzzz?2")
                kw.append("aaaaa?2")
                kw.append("__init__?3")
                kw.append("zzaaaaa?2")
                kw.append("zzbaaaa?2")
                kw.append("this_is_a_longer_value")
                kw.append("this_is_a_much_much_much_much_much_much_much_longer_value")

                kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(False)  # so this needs to match

                # Images are specified with a appended "?type"
                for i in range(len(kw)):
                    if kw[i] in keyword_list:
                        kw[i] = kw[i] + "?1"

                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()

    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)


    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
                    (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum + 1, lastChild)

            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels - 1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels - 1)
                    else:
                        line = self.Expand(line, False, force, visLevels - 1)
            else:
                line = line + 1

        return line
