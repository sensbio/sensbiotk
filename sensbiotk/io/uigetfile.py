# -*- coding: utf-8 -*-
# This file is a part of sensbiot
# Contact : sensbiotk@inria.fr
# Copyright (C) 2015  INRIA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
MATLAB-like "uigetfile" function.
@author: bsijober
"""
# disabling pylint errors 'E1101' no-member, false positive from pylint
# disabling pylint errors 'C0103' invalid variable name, for variables : a,b
# pylint:disable=I0011,E1101,C0103

def uigetfile(title=None, filetypes=[("All files", "*.*")], initialdir=None):
    """
    MATLAB-like "uigetfile" function. Enables the user to
    graphically choose a file and get its absolute path.

    Parameters
    ----------
    title : string
     The displayed GUI title
    filetypes : tuple
     ex : filetypes = [("All files", "*.*")]
    initialdir : string
           Specifies that the files in directory should be displayed
           when the dialog pops up

    Returns
    -------
    file_path : string
     The GUI selected file path
     """
    import Tkinter
    import tkFileDialog

    root = Tkinter.Tk()
    root.geometry('0x0+0+0')
    # window on top (for Windows only)
    root.wm_attributes("-topmost", 1)
    file_path = tkFileDialog.askopenfilename(parent=root, title=title,
                                             filetypes=filetypes,
                                             initialdir=initialdir)
    root.destroy()
    return str(file_path)


if __name__ == '__main__':
    print uigetfile('Titre test')
