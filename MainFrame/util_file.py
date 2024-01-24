# -*- coding: utf-8 -*-
import os

def is_structure_file(file_name):
    if file_name.lower().split('.')[-1] in ['xyz', 'cif', 'xsf', 'pdb'] \
            or os.path.basename(file_name) in ['POSCAR', 'POTCAR']:
        return True
    else:
        return False


def is_edit_file(file_name):
    if file_name.lower().split('.')[-1] not in ['xyz', 'cif', 'xsf', 'pdb', 'cfg', 'ini']:
        return True
    else:
        return False


def is_cfg_file(file_name):
    if file_name.lower().split('.')[-1] in ['cfg', 'ini']:
        return True
    else:
        return False

def is_picture_file(file_name):
    if file_name.lower().split('.')[-1] in ['png', 'jpg', 'bmp', 'ico']:
        return True
    else:
        return False
