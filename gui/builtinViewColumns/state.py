#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from gui.viewColumn import ViewColumn
from gui import bitmapLoader
import wx
from eos.types import Drone, Module, Rack, Fit
from eos.types import State as State_

class State(ViewColumn):
    name = "State"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.resizable = False
        self.size = 16
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_IMAGE
        for name, state in (("checked", wx.CONTROL_CHECKED), ("unchecked", 0)):
            bitmap = wx.EmptyBitmap(16, 16)
            dc = wx.MemoryDC()
            dc.SelectObject(bitmap)
            dc.SetBackground(wx.TheBrushList.FindOrCreateBrush(fittingView.GetBackgroundColour(), wx.SOLID))
            dc.Clear()
            wx.RendererNative.Get().DrawCheckBox(fittingView, dc, wx.Rect(0, 0, 16, 16), state)
            dc.Destroy()
            setattr(self, "%sId" % name, fittingView.imageList.Add(bitmap))

    def getText(self, mod):
        return ""

    def getToolTip(self, mod):
        if isinstance(mod, Module) and not mod.isEmpty:
            return State_.getName(mod.state).title()

    def getImageId(self, stuff):
        generic_active = self.fittingView.imageList.GetImageIndex("state_%s_small" % State_.getName(1).lower(), "icons")
        generic_inactive = self.fittingView.imageList.GetImageIndex("state_%s_small" % State_.getName(-1).lower(), "icons")

        if isinstance(stuff, Drone):
            if stuff.amountActive > 0:
                return generic_active
            else:
                return generic_inactive
        elif isinstance(stuff, Rack):
            return -1
        elif isinstance(stuff, Module):
            if stuff.isEmpty:
                return -1
            else:
                return self.fittingView.imageList.GetImageIndex("state_%s_small" % State_.getName(stuff.state).lower(), "icons")
        elif isinstance(stuff, Fit):
            if stuff.projectionInfo is None:
                return -1
            if stuff.projectionInfo.amount > 0:
                return generic_active
            return generic_inactive
        else:
            active = getattr(stuff, "active", None)
            if active is None:
                return -1
            if active:
                return generic_active
            return generic_inactive

State.register()
