def patientStates(vitals):
    #initialize the list of possible conditions the patient could be in
    comps = ['Cardiac Arrest', 'Respiratory Arrest', 'Inadequate Breathing', 'Hypoxia', 'Compensated Shock', 
        'Decompensated Shock', 'Anaphylaxis', 'Angina Pectoris', 'Opiate Overdose', 'Hypoglycemia', 'Hyperglycemia',
        'Mild Allergic Reaction', 'Pulmonary Edema', 'Stroke']

    #initialize the functions storage of vitals given from the vitals list in the parameter
    gcs = int(vitals[0]) if vitals[0] != "" and vitals[0].isdigit() else None
    pulse = int(vitals[1]) if vitals[1] != "" and vitals[1].isdigit() else None
    resp_rate = int(vitals[2]) if vitals[2] != ""  and vitals[2].isdigit() else None
    pulse_ox = int(vitals[3]) if vitals[3] != "" and vitals[3].isdigit() else None
    breath_sounds = vitals[4].lower()
    blood_pressure = int(vitals[5].split('/')[0]) if vitals[5] != ""  and vitals[5].split('/')[0].isdigit() else None
    pupils = vitals[6].lower() + vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    skin_condition = vitals[7].lower() + vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    extra_notes = vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    avpu = vitals[11].lower()
    avpu_int = 16

    if('alert' in avpu):
        avpu_int = 15
    if('verbal' in avpu):
        avpu_int = 14
    if('pain' in avpu):
        avpu_int = 10
    if('unresponsive' in avpu):
        avpu_int = 3
    gcs = min(avpu_int, gcs) if gcs is not None else None
    if (avpu_int != 16 and gcs is None):
        gcs = avpu_int


    #itertate through each vital, seeing which conditions we can eliminate at each step
    if(gcs is not None):
        if(gcs > 14):
            comps.remove('Cardiac Arrest') if 'Cardiac Arrest' in comps else None
            comps.remove('Respiratory Arrest') if 'Respiratory Arrest' in comps else None
            comps.remove('Decompensated Shock') if 'Decompensated Shock' in comps else None
            comps.remove('Opiate Overdose') if 'Opiate Overdose' in comps else None
            comps.remove('Hypoglycemia') if 'Hypoglycemia' in comps else None
            comps.remove('Hyperglycemia') if 'Hyperglycemia' in comps else None
            comps.remove('Stroke') if 'Stroke' in comps else None
        if(gcs < 15):
            comps.remove('Mild Allergic Reaction') if 'Mild Allergic Reaction' in comps else None

    if(pulse is not None):
        if(pulse > 0):
            comps.remove('Cardiac Arrest') if 'Cardiac Arrest' in comps else None
        if(bradycardic(pulse)):
            comps.remove('Decompensated Shock') if 'Decompensated Shock' in comps else None
            comps.remove('Mild Allergic Reaction') if 'Mild Allergic Reaction' in comps else None
            comps.remove('Compensated Shock') if 'Compensated Shock' in comps else None
            comps.remove('Stroke') if 'Stroke' in comps else None
        if(pulse == 0):
            comps.clear()
            comps.append('Cardiac Arrest')

    if(resp_rate is not None):
        if(tachypnea(resp_rate)):
            comps.remove('Mild Allergic Reaction') if 'Mild Allergic Reaction' in comps else None
        if(not bradypnea(resp_rate)):
            comps.remove('Opiate Overdose') if 'Opiate Overdose' in comps else None
        if(bradypnea(resp_rate)):
            comps.remove('Compensated Shock') if 'Compensated Shock' in comps else None
            comps.remove('Mild Allergic Reaction') if 'Mild Allergic Reaction' in comps else None
        if(not (tachypnea(resp_rate) or bradypnea(resp_rate))):
            comps.remove('Inadequate Breathing') if 'Inadequate Breathing' in comps else None
            comps.remove('Stroke') if 'Stroke' in comps else None
        if(resp_rate != 0):
            comps.remove('Respiratory Arrest') if 'Respiratory Arrest' in comps else None
            comps.remove('Cardiac Arrest') if 'Cardiac Arrest' in comps else None

    if(pulse_ox is not None):
        if(pulse_ox > 94):
            comps.remove('Respiratory Arrest') if 'Respiratory Arrest' in comps else None
            comps.remove('Cardiac Arrest') if 'Cardiac Arrest' in comps else None
            comps.remove('Decompensated Shock') if 'Decompensated Shock' in comps else None
            comps.remove('Opiate Overdose') if 'Opiate Overdose' in comps else None
            comps.remove('Inadequate Breathing') if 'Inadequate Breathing' in comps else None
            comps.remove('Anaphylaxis') if 'Anaphylaxis' in comps else None
            comps.remove('Hypoxia') if 'Hypoxia' in comps else None
        if(pulse_ox < 95):
            comps.remove('Mild Allergic Reaction') if 'Mild Allergic Reaction' in comps else None
    
    if(blood_pressure is not None):
        if(hypertensive(blood_pressure)):
            comps.remove('Decompensated Shock') if 'Decompensated Shock' in comps else None
            comps.remove('Opiate Overdose') if 'Opiate Overdose' in comps else None
            comps.remove('Hypoglycemia') if 'Hypoglycemia' in comps else None
            comps.remove('Anaphylaxis') if 'Anaphylaxis' in comps else None
        if(hypotensive(blood_pressure)):
            comps.remove('Hyperglycemia') if 'Hyperglycemia' in comps else None
            comps.remove('Mild Allergic Reaction') if 'Mild Allergic Reaction' in comps else None
            comps.remove('Stroke') if 'Stroke' in comps else None
        if(hypertensive(blood_pressure) or hypotensive(blood_pressure)):
            comps.remove('Respiratory Arrest') if 'Respiratory Arrest' in comps else None
            comps.remove('Cardiac Arrest') if 'Cardiac Arrest' in comps else None

    if(skin_condition is not None):
        if('red' in skin_condition or 'flushed' in skin_condition or 'warm' in skin_condition):
            comps.remove('Respiratory Arrest') if 'Respiratory Arrest' in comps else None
            comps.remove('Cardiac Arrest') if 'Cardiac Arrest' in comps else None
            comps.remove('Hypoglycemia') if 'Hypoglycemia' in comps else None
            comps.remove('Decompensated Shock') if 'Decompensated Shock' in comps else None
            comps.remove('Opiate Overdose') if 'Opiate Overdose' in comps else None
        if('pale' in skin_condition or 'pallor' in skin_condition or 'cool' in skin_condition):
            comps.remove('Hyperglycemia') if 'Hyperglycemia' not in comps else None
    
    if('Hypoxia' not in comps):
        comps.remove('Pulmonary Edema') if 'Pulmonary Edema' in comps else None

    if(('rale' not in breath_sounds) and ('crackle' not in breath_sounds)):
        comps.remove('Pulmonary Edema') if 'Pulmonary Edema' in comps else None


    if(extra_notes is not None):
        if('diabet' in extra_notes and (gcs is not None)):
            if gcs < 14:
                comps.clear()
                comps.append('Hypoglycemia')

        if('diabet' in extra_notes and (blood_pressure is not None)):
            if(hypertensive(blood_pressure)):
                comps.clear()
                comps.append('Hyperglycemia')
        if('angina' in extra_notes or 'atraumatic chest pain' in extra_notes):
            comps.clear()
            comps.append('Angina Pectoris')
        if('cincin' in extra_notes or 'droop' in extra_notes or 'slur' in extra_notes or 'drift' in extra_notes):
            comps.clear()
            comps.append('Stroke')
        if('pinpoint' in pupils):
            comps.clear()
            comps.append('Opiate Overdose')

        if(('urti' in skin_condition or 'hive' in skin_condition or 'allerg' in extra_notes)):
            if(pulse_ox is not None):
                if(pulse_ox < 95):
                    comps.clear()
                    comps.append('Anaphylaxis')
            else:
                comps.clear()
                comps.append('Mild Allergic Reaction')

    if(resp_rate is not None):
        if(resp_rate == 0):
            comps.clear()
            comps.append('Respiratory Arrest')
    if(pulse is not None):
        if(pulse == 0):
            comps.clear()
            comps.append('Cardiac Arrest')

    return comps





#Helper functions for vitals:                    
def hypotensive(blood_pressure):
    if(blood_pressure < 100):
        return True
    return False

def hypertensive(blood_pressure):
    if(blood_pressure > 160):
        return True
    return False

def tachycardic(pulse):
    if(pulse > 100):
        return True
    return False

def bradycardic(pulse):
    if(pulse < 60):
        return True
    return False

def tachypnea(resp_rate):
    if(resp_rate > 20):
        return True
    return False

def bradypnea(resp_rate):
    if(resp_rate < 12):
        return True
    return False

def alteredLOC(gcs):
    if(gcs < 15):
        return True
    return False



#takes in a list of vitals, and returns all  medications that are contraindicated 
def contras(vitals):

    #initialize the list of possible contras
    contras = []

    #initialize the functions storage of vitals given from the vitals list in the parameter
    gcs = int(vitals[0]) if vitals[0] != "" and vitals[0].isdigit() else None
    pulse = int(vitals[1]) if vitals[1] != "" and vitals[1].isdigit() else None
    resp_rate = int(vitals[2]) if vitals[2] != ""  and vitals[2].isdigit() else None
    pulse_ox = int(vitals[3]) if vitals[3] != "" and vitals[3].isdigit() else None
    breath_sounds = vitals[4].lower()
    blood_pressure = int(vitals[5].split('/')[0]) if vitals[5] != ""  and vitals[5].split('/')[0].isdigit() else None
    pupils = vitals[6].lower() + vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    skin_condition = vitals[7].lower() + vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    extra_notes = vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    avpu = vitals[11].lower()
    avpu_int = 16

    if('alert' in avpu):
        avpu_int = 15
    if('verbal' in avpu):
        avpu_int = 14
    if('pain' in avpu):
        avpu_int = 10
    if('unresponsive' in avpu):
        avpu_int = 3
    gcs = min(avpu_int, gcs) if gcs is not None else None
    if (avpu_int != 16 and gcs is None):
        gcs = avpu_int


    if (gcs is not None):
        if(gcs < 13):
            contras.append('Glucose for Hypoglycemia') if 'Glucose for Hypoglycemia' not in contras else None
            contras.append('Aspirin for Angina Pectoris') if 'Aspirin for Angina Pectoris' not in contras else None
            contras.append('Nitroglycerin for Angina Pectoris') if 'Nitroglycerin for Angina Pectoris' not in contras else None
            contras.append('MDI/SVN for Hypoxia') if 'MDI/SVN for Hypoxia' not in contras else None
    
    if (blood_pressure is not None):
        if(blood_pressure < 100):
            contras.append('Nitroglycerin for Angina Pectoris') if 'Nitroglycerin for Angina Pectoris' not in contras else None

    if('gag refl' in extra_notes or 'unable to swall' in extra_notes or 'has not taken insul' in extra_notes):
        contras.append('Glucose for Hypoglycemia') if 'Glucose for Hypoglycemia' not in contras else None

    if('leeding' in extra_notes or 'lood' in extra_notes or 'preg' in extra_notes or 'aneurysm' in extra_notes):
        contras.append('Aspirin for Angina Pectoris') if 'Aspirin for Angina Pectoris' not in contras else None
    
    if('PDE' in extra_notes or 'head injury' in extra_notes):
        contras.append('Nitroglycerin for Angina Pectoris') if 'Nitroglycerin for Angina Pectoris' not in contras else None

    return contras

#takes in a list of vitals, and returns all  medications that are to be used with caution
def warnings(vitals):
    
    #initialize the list of possible conditions the patient could be in
    warnings = []

    #initialize the functions storage of vitals given from the vitals list in the parameter
    gcs = int(vitals[0]) if vitals[0] != "" and vitals[0].isdigit() else None
    pulse = int(vitals[1]) if vitals[1] != "" and vitals[1].isdigit() else None
    resp_rate = int(vitals[2]) if vitals[2] != ""  and vitals[2].isdigit() else None
    pulse_ox = int(vitals[3]) if vitals[3] != "" and vitals[3].isdigit() else None
    breath_sounds = vitals[4].lower()
    blood_pressure = int(vitals[5].split('/')[0]) if vitals[5] != ""  and vitals[5].split('/')[0].isdigit() else None
    pupils = vitals[6].lower() + vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    skin_condition = vitals[7].lower() + vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    extra_notes = vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    avpu = vitals[11].lower()
    avpu_int = 16

    if('alert' in avpu):
        avpu_int = 15
    if('verbal' in avpu):
        avpu_int = 14
    if('pain' in avpu):
        avpu_int = 10
    if('unresponsive' in avpu):
        avpu_int = 3
    gcs = min(avpu_int, gcs) if gcs is not None else None
    if (avpu_int != 16 and gcs is None):
        gcs = avpu_int

    if('coronary' in extra_notes or 'heart' in extra_notes or 'brain tum' in extra_notes or 'arrythm' in extra_notes or 
        'polypharm' in extra_notes):
        warnings.append('Narcan for Opiate Overdose')

    if('coronary' in extra_notes or 'ischem' in extra_notes):
        warnings.append('Epinephrine for Anaphylaxis')

    return warnings