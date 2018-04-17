# Basic events description for IC control system
# possibly need to move this to DB or


from settings.cx import ctl_server, v2k_cas


# cdaclient @t100:cxhw:0.sounddev.filename@u=\"'~/berkaev/sound/vepp3RampStart.wav vol 0.4'\"
# cdaclient @t100:cxhw:0.sounddev.filename@u=\"'~/berkaev/sound/vepp3RemagnStart.wav vol 0.4'\"
# cdaclient @t100:cxhw:0.sounddev.filename@u=\"'~/berkaev/sound/vepp3InjectionStart.wav vol 0.4'\"

actions = {
    'BEP electrons': {
        'chans': {
            ctl_server + '.bep.polarityt': {
                'type': 'text',
                'max_len': 100,
                'values': {True: 'e', False: 'p'}
            },
            ctl_server + '.sounddev.filename':{
                'type': 'text',
                'max_len': 100,
                'values': {
                    True: '~/berkaev/sound/vepp2kChangePolarity.wav vol 0.4',
                    False: '~/berkaev/sound/vepp2kChangePolarity.wav vol 0.4'
                }
            }
        }

    },

    'BEP is busy': {
        'chans': {
            ctl_server + '.bep.busy': {
                'type': 'double',
            }
        }
    },

    'BEP is out': {
        'chans': {
            ctl_server + '.bep.offline': {
                'type': 'double',
            }

        }

    },
}

events = {
    # VEPP-3 events
    'vepp3 inject e+': {
        'chans': {
            'vepp4-pult6:0.vepp3.statust': {
                'type': 'text',
                'max_len': 100,
                'value': 'Injection'
            },
            'vepp4-pult6:0.vepp3.polarityt': {
                'type': 'text',
                'max_len': 100,
                'value': 'e+'
            },
        },
    },

    'vepp3 inject e-': {
        'chans': {
            'vepp4-pult6:0.vepp3.statust': {
                'type': 'text',
                'max_len': 100,
                'value': 'Injection'
            },
            'vepp4-pult6:0.vepp3.polarityt': {
                'type': 'text',
                'max_len': 100,
                'value': 'e-'
            },
        }
    },

    'vepp3 acceleration e-': {
        'chans': {
            'vepp4-pult6:0.vepp3.statust': {
                'type': 'text',
                'max_len': 100,
                'prev_value': 'Injection',
                'value': 'Acceleration'
            },
            'vepp4-pult6:0.vepp3.polarityt': {
                'type': 'text',
                'max_len': 100,
                'value': 'e-'
            },
        }
    },

    'vepp3 acceleration e+': {
        'chans': {
            'vepp4-pult6:0.vepp3.statust': {
                'type': 'text',
                'max_len': 100,
                'prev_value': 'Injection',
                'value': 'Acceleration'
            },
            'vepp4-pult6:0.vepp3.polarityt': {
                'type': 'text',
                'max_len': 100,
                'value': 'e+'
            },
        }
    },

    'vepp3 experiment': {
        'chans': {
            'vepp4-pult6:0.vepp3.statust': {
                'type': 'text',
                'max_len': 100,
                'value': 'Experiment'
            },
        }
    },

    # VEPP-4 events

    # BEP events
    # Regim 1,2 - electrons expected, other - positrons expected

    # BEP.Energy.E_set
    # BEP/Currents/ePMT
    # BEP/Currents/pPMT
    # BEP/RF/Probros
    # B-3M/BEP_Inflektor

    # BEP/State
    # '1->2' or '2->1' or '3->4' or '4->3' - BEP ramping
    # 2 or 4 BEP extraction
    # 1 or 4 BEP storage?
    # Remagn-3 Remagn-1

    'BEP electrons': {
        'chans': {
            v2k_cas + '.Regime': {
                'type': 'text',
                'max_len': 100,
                'cond_type': 'in',
                'values': {'1', '2'}
            }
        }
    },


    'BEP is busy': {
        'chans': {
            v2k_cas + '.BEP.State': {
                'type': 'text',
                'max_len': 100,
                'cond_type': 'in',
                'values': {'1->2', '2->1', '3->4', '4->3', '2', '4', 'Remagn-1', 'Remagn-3'}
            },
        }
    },

    'BEP is out': {
        'chans': {
            v2k_cas + '.B-3M.BEP_Inflektor': {
                'type': 'text',
                'max_len': 100,
                'value': '0'
            },
            v2k_cas + '.BEP.RF.Probros': {
                'type': 'text',
                'max_len': 100,
                'value': '1'
            }
        },
        'cond_expression': 'any'
    },


    #injection complex events
    #'ic mode update':{
    #
    #
    #}



}
