#from aQt.QtDesigner import QPyDesignerCustomWidgetCollectionPlugin

from .auxwidgets import HLine, BaseGridW, BaseFrameGridW
from .fcheckbox import FCheckBox
from .fcombobox import FComboBox
from .fdoublespinbox import FDoubleSpinBox
from .flcdnumber import FLCDNumber
# from .flineedit import
from .fspinbox import FSpinBox
from .ledwidget import LedWidget
from .fswitch import FSwitch

from .cx_checkbox import CXCheckBox
from .cx_combobox import CXTextComboBox
from .cx_doublespinbox import CXDoubleSpinBox
# from .cx_histplot import
from .cx_lcdnumber import CXLCDNumber
from .cx_led import CXEventLed
from .cx_lineedit import CXLineEdit
from .cx_progressbar import CXProgressBar
from .cx_pushbutton import CXPushButton
from .cx_spinbox import CXSpinBox
from .cx_switch import CXSwitch

from .cx_bpm_plot import BPMWidget, K500BPMWidget


__all__ = [HLine, BaseGridW, BaseFrameGridW, FCheckBox, FComboBox, FDoubleSpinBox, FLCDNumber,
           FSpinBox, LedWidget, FSwitch,
           CXCheckBox, CXTextComboBox, CXDoubleSpinBox, CXLCDNumber, CXEventLed, CXLineEdit, CXProgressBar,
           CXPushButton, CXSpinBox, BPMWidget, K500BPMWidget,
           CXSwitch
           ]

