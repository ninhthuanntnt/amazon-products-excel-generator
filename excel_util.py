from copy import copy

from openpyxl.styles import NamedStyle


def copy_cell_all(source_cell, dest_cell):
    """
    Copy the style and formatting of a source cell to a destination cell.
    """
    dest_cell.value = source_cell.value

    if source_cell.has_style:
        dest_cell.font = copy(source_cell.font)
        dest_cell.border = copy(source_cell.border)
        dest_cell.fill = copy(source_cell.fill)
        dest_cell.number_format = copy(source_cell.number_format)
        dest_cell.protection = copy(source_cell.protection)
        dest_cell.alignment = copy(source_cell.alignment)