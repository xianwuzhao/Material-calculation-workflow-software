# -*- coding: utf-8 -*-
"""Taken from wxpython 4.0.7 post2, demo/Main.py.
   2020-3-1"""

import wx
from wx import stc
from .styled_text_ctrl import PythonSTC

class TextEditor(PythonSTC):
    def __init__(self, parent, style=wx.BORDER_NONE):
        PythonSTC.__init__(self, parent, -1, style=style)
        self.SetUpEditor()

    def OpenFile(self, path):
        # Just use LoadFile()
        with open(path) as f:
            value = f.read()
            self.SetValue(value)

    # Some methods to make it compatible with how the wxTextCtrl is used
    def SetValue(self, value):
        val = self.GetReadOnly()
        self.SetReadOnly(False)
        self.SetText(value)
        self.EmptyUndoBuffer()
        self.SetSavePoint()
        self.SetReadOnly(val)

    def SetEditable(self, val):
        self.SetReadOnly(not val)

    def IsModified(self):
        return self.GetModify()

    def Clear(self):
        self.ClearAll()

    def SetInsertionPoint(self, pos):
        self.SetCurrentPos(pos)
        self.SetAnchor(pos)

    def ShowPosition(self, pos):
        line = self.LineFromPosition(pos)
        # self.EnsureVisible(line)
        self.GotoLine(line)

    def GetLastPosition(self):
        return self.GetLength()

    def GetPositionFromLine(self, line):
        return self.PositionFromLine(line)

    def GetRange(self, start, end):
        return self.GetTextRange(start, end)

    def GetSelection(self):
        return self.GetAnchor(), self.GetCurrentPos()

    def SetSelection(self, start, end):
        self.SetSelectionStart(start)
        self.SetSelectionEnd(end)

    def SelectLine(self, line):
        start = self.PositionFromLine(line)
        end = self.GetLineEndPosition(line)
        self.SetSelection(start, end)

    def SetUpEditor(self):
        # Enable folding
        self.SetProperty("fold", "1")
        # Highlight tab/space mixing (shouldn't be any)
        self.SetProperty("tab.timmy.whinge.level", "1")
        # Set left and right margins
        self.SetMargins(2, 2)
        # Set up the numbers in the margin for margin #1
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        # Reasonable value for, say, 4-5 digits using a mono font (40 pix)
        self.SetMarginWidth(1, 40)
        # Indentation and tab stuff
        self.SetIndent(4)  # Proscribed indent size for wx
        self.SetIndentationGuides(True)  # Show indent guides
        self.SetBackSpaceUnIndents(True)  # Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)  # Tab key indents
        self.SetTabWidth(4)  # Proscribed tab size for wx
        self.SetUseTabs(False)  # Use spaces rather than tabs, or
        # TabTimmy will complain!
        # White space
        self.SetViewWhiteSpace(False)  # Don't view white space
        # EOL: Since we are loading/saving ourselves, and the
        # strings will always have \n's in them, set the STC to
        # edit them that way.
        self.SetEOLMode(wx.stc.STC_EOL_LF)
        self.SetViewEOL(False)
        # No right-edge mode indicator
        self.SetEdgeMode(stc.STC_EDGE_NONE)

    def RegisterModifiedEvent(self, event):
        self.Bind(wx.stc.EVT_STC_CHANGE, event)