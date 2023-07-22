def treatmentDescription(condition):
    #medical treatments:
    if(condition == 'Cardiac Arrest'):
        link = "https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/algorithms"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Begin chest compressions and rescue breathing at a 30 : 2 ratio (or 15 : 2 ratio for pediatric)
            \n  - Attach AED as soon as it becomes available, and deliver shock if necessary
            \n  - Cycle compression, ventilation, and AED roles every 2 minutes
            \n  - Urgent transport to a higher level of care
            \n  - {output}'''
    if(condition == 'Respiratory Arrest'):
        link = "https://my.clevelandclinic.org/health/diseases/15283-acute-respiratory-distress-syndrome-ards#management-and-treatment"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Open the airway using the head-tilt chin-lift or jaw thrust maneuver, and suction if necessary
            \n  - Positive pressure ventilation with a BVM connected to high-flow supplemental oxygen
            \n  - Urgent transport to a higher level of care
            \n - {output}'''
    if(condition == 'Inadequate Breathing'):
        link = "https://my.clevelandclinic.org/health/symptoms/16942-dyspnea"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Open the airway using the head-tilt chin-lift or jaw thrust maneuver, and suction if necessary
            \n  - Positive pressure ventilation with a BVM connected to high-flow supplemental oxygen
            \n  - Urgent transport to a higher level of care
            \n  - {output}'''
    if(condition == 'Hypoxia'):
        link = "https://my.clevelandclinic.org/health/diseases/23063-hypoxia#management-and-treatment "
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Ensure a patent airway 
            \n  - Administer high-flow supplemental oxygen via a non-rebereather mask 
            \n  - If dypsnea is due to bronchospasm associated with COPD, asthma, etc., administer inhaler or nebulizer medication if indicated 
            \n  - Transport to a higher level of care, continuously monitoring patient's breathing rate and depth
            \n  - {output}'''
    if(condition == 'Pulmonary Edema'):
        link = "https://my.clevelandclinic.org/health/diseases/24218-pulmonary-edema"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Ensure a patent airway 
            \n  - Administer high-flow supplemental oxygen via a non-rebereather mask 
            \n  - Administer continuous positive airway pressure if indicated
            \n  - Transport to a higher level of care, continuously monitoring patient's breathing rate and depth
            \n  - {output}'''
    if(condition == 'Compensated Shock'):
        link = "https://www.mayoclinic.org/first-aid/first-aid-shock/basics/art-20056620"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Administer high-flow supplemental oxygen via a non-rebereather mask 
            \n  - Elevate the patient's legs to improve blood flow, and keep patient warm with a thick blanket 
            \n  - Transport to a higher level of care, continuously monitoring patient's blood pressure and heart rate
            \n  - {output}'''
    if(condition == 'Decompensated Shock'):
        link = "https://www.mayoclinic.org/first-aid/first-aid-shock/basics/art-20056620"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - If breathing is inadequate, administer positive pressure ventilation with a BVM connected to high-flow supplemental oxygen
            \n  - If breathing is adequate, administer high-flow supplemental oxygen via a non-rebereather mask
            \n  - Elevate the patient's legs to improve blood flow, and keep patient warm with a thick blanket 
            \n  - Transport to a higher level of care, continuously monitoring patient's blood pressure and heart rate
            \n  - {output}'''
    if(condition == 'Anaphylaxis'):
        link = "https://my.clevelandclinic.org/health/diseases/8619-anaphylaxis#management-and-treatment "
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - If breathing is inadequate, administer positive pressure ventilation with a BVM connected to high-flow supplemental oxygen
            \n  - If breathing is adequate, administer high-flow supplemental oxygen via a non-rebereather mask
            \n  - Administer epinephrine if indicated  
            \n  - Transport to a higher level of care, continuously monitoring patient's perfusion and breathing
            \n  - {output}'''
    if(condition == 'Mild Allergic Reaction'):
        link = "https://my.clevelandclinic.org/health/diseases/8610-allergies#management-and-treatment "
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Administer high-flow supplemental oxygen via a non-rebereather mask 
            \n  - Transport to a higher level of care, continuously monitoring patient's perfusion and breathing
            \n  - {output}'''
    if(condition == 'Angina Pectoris'):
        link = "https://my.clevelandclinic.org/health/diseases/21489-angina"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Administer high-flow supplemental oxygen via a non-rebereather mask
            \n  - Administer aspirin if indicated
            \n  - Administer nitroglycerin if indicated 
            \n  - Transport to a higher level of care, continuously monitoring patient's angina
            \n  - {output}'''
    if(condition == 'Opiate Overdose'):
        link = "https://my.clevelandclinic.org/health/diseases/24583-opioid-overdose#management-and-treatment "
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Open the airway using the head-tilt chin-lift or jaw thrust maneuver, and suction if necessary
            \n  - Positive pressure ventilation with a BVM connected to high-flow supplemental oxygen
            \n  - Administer naloxone if indicated
            \n  - Transport to a higher level of care, continuously monitoring patient's breathing
            \n  - {output}'''
    if(condition == 'Hypoglycemia'):
        link = "https://my.clevelandclinic.org/health/diseases/11647-hypoglycemia-low-blood-sugar#management-and-treatment "
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Administer high-flow supplemental oxygen via a non-rebereather mask
            \n  - Administer a tube of glucose if indicated
            \n  - Transport to a higher level of care, continuously monitoring patient's glucose levels and LOC
            \n  - {output}'''
    if(condition == 'Hyperglycemia'):
        link = "https://my.clevelandclinic.org/health/diseases/9815-hyperglycemia-high-blood-sugar"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Administer high-flow supplemental oxygen via a non-rebereather mask
            \n  - Transport to a higher level of care, continuously monitoring patient's glucose levels and LOC
            \n  - {output}'''
    if(condition == 'Stroke'):
        link = "https://www.healthline.com/health/stroke/stroke-first-aid"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Conduct a full patient assessment and maintain the airway, breathing, and circulation
            \n  - Provide supplmental oxygen if needed, but refrain from giving the patient something to bite on
            \n  - Place the patient's affected or paralyzed extremity in a secure and safe position during movement
            \n  - Transport to a hospital or designated stroke center, and continuously monitor patient vitals
            \n  - {output}'''
    if(condition == "Edema"):
        link = "https://emtprep.com/resources/article/understanding-pitting-edema"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Conduct a full patient assessment and attempt to evaluate the cause of edema
            \n  - Assess patient for burns, deep vein thrombosis, allergic reactions, and congestive heart failure
            \n  - Transport  to a hospital and continuously monitor patient vitals
            \n  - {output}'''

    #trauma treatments:
    if(condition == '1st Degree Burn' or condition == '2nd Degree Burn' or condition == '3rd Degree Burn'):
        link = "https://www.mayoclinic.org/first-aid/first-aid-burns/basics/art-20056649"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Cover the affected area with a dry, sterile dressing to protect it from infection, and assess for a patent airway
            \n  - Keep the patient warm to prevent hypothermia, while keeping the burn cool
            \n  - Do not attempt to pull clothing from the burn, or to put any ointments on the burn
            \n  - Transport to a burn center, and continuously monitor patient airway and body temperature
            \n  - {output}'''

    if(condition == 'Controlled Bleeding'):
        link = "https://www.jems.com/patient-care/trauma/wound-packing-essentials-for-emts-and-paramedics/"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Apply direct pressure to wound to control the bleeding
            \n  - Bandage the wound with a sterile gauze, using cravats as necessary
            \n  - Do not apply any pressure to wounds on the head or ears, as this can increase intracranial pressure
            \n  - If a bandage becomes saturated with blood after a period of time, simply place another one on top without removing the existing one
            \n  - Transport to a trauma center, and continuously monitor patient perfusion
            \n  - {output}'''

    if(condition == 'Uncontrolled Bleeding'):
        link = "https://redcross.softourniquet.com/"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - If local pressure does not control bleed, and the bleeding is appendicular, apply a tourniquet proximal to the wound and record the time of placement
            \n  - If the bleeding is axial, consider use of clotting agents such as QuikClot, and apply as much pressure to the area as reasonably possible
            \n  - Do not apply any pressure to wounds on the head or ears, as this can increase intracranial pressure
            \n  - Treat for shock by administering high-flow oxygen via a non re-breather mask, and keeping patient warm
            \n  - Transport to a trauma center, and continuously monitor patient perfusion
            \n  - {output}'''

    if(condition == 'Fracture' or condition == 'Sprain/Strain'):
        link = "https://medictests.com/units/emt-considerations-in-orthopedic-trauma"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Stabilize the affected limb in the position it was found, if possible, and take full spinal motion restriction precautions
            \n  - Immobilize the affected limb using a splint or sling, and pad all knots made on the patient
            \n  - If patient presents with mid-shaft femur fracture, apply a hare traction device if indicated
            \n  - Make sure pulse, motor, and sensory functions of the affected body part are assessed before and after splint/sling placement
            \n  - Administer high-flow oxygen via a non re-breather mask
            \n  - Transport to a trauma center, and continuously monitor patient vitals
            \n  - {output}'''

    if(condition == 'Dislocation'):
        link = "https://medictests.com/units/emt-considerations-in-orthopedic-trauma"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Stabilize the affected limb in the position it was found, if possible, and take full spinal motion restriction precautions
            \n  - If the join is not an elbow joint, attempt once to reduce the dislocation, and leave it be if initial attempt fails
            \n  - Immobilize the affected limb using a splint, and pad all knots made on the patient
            \n  - Make sure pulse, motor, and sensory functions of the affected body part are assessed before and after splint placement
            \n  - Administer high-flow oxygen via a non re-breather mask
            \n  - Transport to a trauma center, and continuously monitor patient vitals
            \n  - {output}'''

    if(condition == "Ecchymosis"):
        link = "https://www.verywellhealth.com/ecchymosis-4773870"
        output = f"Click <a href='{link}'>here</a> for more information"
        return f'''  - Conduct a full patient assessment and attempt to evaluate the mechanism of injury
            \n  - If possible, elevate the bruised area and apply ice to lessen symptoms such as pain and swelling
            \n  - Consider spinal immobilization of mechanism of injury is singificant
            \n  - Transport to a trauma center, and continuously monitor patient vitals
            \n  - {output}'''
