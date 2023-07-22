def drugDescription(drug):
    #drug treatments:
    if(drug == 'Naloxone'):
        link = "https://nida.nih.gov/publications/drugfacts/naloxone"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Actions: Opioid antagonist that reverses the effects of overdose
            \n  - Dosage: 0.4mg
            \n  - Indications: Respiratory depression or arrest due to opiate overdose
            \n  - Contraindications: Patient is allergic, medication is expired, use cautiously in patients with cardiac disease, supraventricular arrhythmia, head trauma, brain tumor, or poly-subtance overdose
            \n  - Side effects: Agitation, diaphoresis, increased bp, nausea, vomiting, tachycardia, cardiac arrest, ventricular fibrillation, diarrhea, dyspnea, tremor, abdominal cramps, pulmonary edema
            \n  - Administration: Assemble syringe and administer intramuscularly in the lateral thigh
            \n  - {output}'''
    if(drug == 'Epinephrine'):
        link = "https://www.drugs.com/mtm/epinephrine-injection.html"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Actions: Vasoconstrictor and bronchodilator
            \n  - Dosage: 0.3mg (0.15mg for children < 4)
            \n  - Indications: Signs and symptoms of anaphylaxis with swelling airway, respiratory distress, or shock
            \n  - Contraindications: No absolute contraindications, use cautiously for patients with coronary disease
            \n  - Side efects: Anxiety, nervousness, headache, tremors, nausea, vomiting, chest pain, hypertension, cardiac arrythmias
            \n  - Administration: Administer intramuscularly into the lateral thigh and hold in place for ten seconds
            \n  - {output}'''
    if(drug == 'Oral Glucose'):
        link = "https://www.drugs.com/mtm/glucose.html"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Actions: Increases blood sugar
            \n  - Dosage: One full tube, not all at once
            \n  - Indications: Patients with altered mental status and known history of diabetes
            \n  - Contraindications: Patient is unconscious, a known diabetic who has not taken there insulin recently, or unable to swallow
            \n  - Side efects: May be aspirated by patient
            \n  - Administration: Place gel on tongue depressor and administer between the cheek and gum
            \n  - {output}'''
    if(drug == 'Metered Dose Inhaler'):
        link = "https://my.clevelandclinic.org/health/drugs/8694-inhalers"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Actions: Airway dilator
            \n  - Dosage: 2 pumps (spaced 30 seconds apart)
            \n  - Indications: Dyspnea and signs of respiratory distress associated with bronchospasm
            \n  - Contraindications: Patient is allergic, unable to use inhaler themselves, the maximum dose has been met, or the medication is expired
            \n  - Side effects: Hyperglycemia, anxiety, vomiting, nausea, hypertension, headache, throat irritation, hypokalemia, tremors, dry mouth, dyspepsia, sinus tach, paradoxical bronchospasm, palpitations, epistaxis, insomnia
            \n  - Administration: Instruct patient to exhale before activating inhaler, and take a deep inhale during administration
            \n  - {output}'''
    if(drug == 'CPAP'):
        link = "https://my.clevelandclinic.org/health/treatments/22043-cpap-machine"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Actions: Forces the airway open with positive pressure
            \n  - Dosage: 10cm H2O
            \n  - Indications: Dyspnea associated with pulmonary edema (breath sounds diminished, wheezing, rales)
            \n  - Contraindications: Apnea, hypotension, pneumothorax, facial/laryngeal/pulmonary trauma, tracheoesophageal fistula, tracheal/esophageal/gastric surgery, vomiting, upper GI bleeding, failure to tolerate/incomplete seal
            \n  - Side effects: Claustrophobia, excessive cooling, difficulty exhaling, pneumothorax, edema, subcutaneous emphysema, epistaxis, nausea, cardiac arrhythmia, pneumomediastinum, aerophagia, chest discomfort, sinus discomfort
            \n  - Administration: ASsure a snug fit of CPAP mask and adequate oxygen supply
            \n  - {output}'''
    if(drug == 'Aspirin'):
        link = "https://www.drugs.com/aspirin.html"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Actions: Platelet aggregation inhibitor
            \n  - Dosage: 325mg (1 tablet)
            \n  - Indications: Atraumatic chest discomfort
            \n  - Contraindications: Patient is allergic, has taken 325mg in past 24 hours, is bleeding/has bleeding disorder, pregnant, has AAA or TAA, medication is expired
            \n  - Side effects: Anaphylaxis, nausea, vomiting, bleeding, angioedema, stomach irritation
            \n  - Administration: Administer orally, making sure patient fully chews tablet
            \n  - {output}'''
    if(drug == 'Nitroglycerin'):
        link = "https://www.mayoclinic.org/drugs-supplements/nitroglycerin-oral-route-sublingual-route/proper-use/drg-20072863"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Actions: Vasodilator
            \n  - Dosage: 1 tablet (max 3 tablets in 15 minutes)
            \n  - Indications: Atraumatic chest discomfort
            \n  - Contraindications: Patient has taken 3 doses in a 15 minute period, a systolic BP < 100 mm Hg, recent head injury, use of PDE inhibitors in past 72 hours, medication is expired
            \n  - Side effects: Headache, cardiovascular collapse, lightheadedness, methemoglobinemia, bradycardia, flushing, hypotension
            \n  - Administration: Administer sublingually, repeat 1 dose every 5 minutes until 3 doses or pain subsides
            \n  - {output}'''
