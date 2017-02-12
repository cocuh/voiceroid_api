import comtypes
import comtypes.client

UIA_dll = comtypes.client.GetModule('UIAutomationCore.dll')
uic = comtypes.gen.UIAutomationClient
uia = comtypes.CoCreateInstance(
    uic.CUIAutomation().IPersist_GetClassID(),
    interface=uic.IUIAutomation,
    clsctx=comtypes.CLSCTX_INPROC_SERVER
)


def find_child(win, auto_id, control_type=None):
    conditions = []
    conditions.append(uia.CreatePropertyCondition(uic.UIA_AutomationIdPropertyId, auto_id))

    if control_type is not None:
        control_type = getattr(UIA_dll, 'UIA_{}ControlTypeId'.format(control_type))
        conditions.append(uia.CreatePropertyCondition(uic.UIA_ControlTypePropertyId, control_type))

    if len(conditions) == 1:
        cond = conditions[0]
    else:
        cond = uia.CreateAndConditionFromArray(conditions)

    elem = win.FindFirst(uic.TreeScope_Descendants, cond)

    if not elem:
        elem = None
    return elem


def search_window(title, parent=None):
    if parent is None:
        parent = uia.GetRootElement()
    cond = uia.CreatePropertyCondition(uic.UIA_NamePropertyId, title)
    win = parent.FindFirst(uic.TreeScope_Children, cond)
    if not win:
        win = None
    return win
