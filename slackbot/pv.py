import time
from epics import PV
from slackbot import log

def check_pvs_connected(epics_pvs):
    """Checks whether all EPICS PVs are connected.
    Returns
    -------
    bool
        True if all PVs are connected, otherwise False.
    """

    slack_messages = ()
    all_connected = True

    MIR=['Au','?']
    GRT=['Bad MEG','HEG','MEG','?']
    SHU=['Opened','Closed']

    for key in epics_pvs:
        pv = PV(epics_pvs[key])
        time.sleep(.2)
        if not pv.connected:
            log.error('PV %s is not connected', pv.pvname)
            slack_messages += ('\nPV ' + pv.pvname + ' is not connected', )
            all_connected = False
        elif key == 'mirror':
            slack_messages += ('\n' + key + ': ' + MIR[pv.get() - 1],)
            log.info('%s: %s' % (key, MIR[pv.get() - 1]))
        elif key == 'grating':
            slack_messages += ('\n' + key + ': ' + GRT[pv.get() - 1],)
            log.info('%s: %s' % (key, GRT[pv.get() - 1]))
        elif key == 'scan positionner':
            pv_name=pv.get()
            pv_desc=PV(pv_name[:pv_name.find('.')] + '.DESC')
            if not pv_desc.connected:
                slack_messages += ('\n' + key + ': ' + pv.get(as_string=True), )
                log.info('%s: %s' % (key, pv.get(as_string=True)))
            else:
                slack_messages += ('\n' + key + ': ' + pv_desc.get(), )
                log.info('%s: %s' % (key, pv_desc.get()))
        elif key == 'C Shutter' or key == 'D Shutter':
            slack_messages += ('\n' + key + ': ' + SHU[pv.get()],)
            log.info('%s: %s' % (key, SHU[pv.get()]))
        else:
            log.info('%s: %s' % (key, pv.get(as_string=True)))
            slack_messages += ('\n' + key + ': ' + pv.get(as_string=True), )

    return all_connected, slack_messages

