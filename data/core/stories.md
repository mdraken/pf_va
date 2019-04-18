## happy_path
* greet
   - utter_greet
## story_thankyou
* thankyou
    - utter_noworries
## story_findadoctor_happypath_1
* greet
   - utter_greet
* findadoctor
    - utter_ask_location
* inform{"location":"Richmond"}
    - utter_ask_speciality
* inform{"speciality":"orthopedic"}
    - find_providers
## story_findadoctor_happypath_2
* greet
   - utter_greet
* findadoctor
   - utter_ask_speciality
* inform{"speciality":"orthopedic"}
    - utter_ask_location
* inform{"location":"San Francisco"}
    - find_providers
## story_findadoctor_happypath_3
* greet
   - utter_greet
* inform{"speciality":"orthopedic"}
    - utter_ask_doctor_search
* affirm
    - utter_ask_location
* inform{"location":"New York"}
    - find_providers

## story_findadoctor_happypath_4
* greet
   - utter_greet
* inform{"location":"New York"}
    - utter_ask_doctor_search
* affirm
    - utter_ask_speciality
* inform{"speciality":"orthopedic"}
    - find_providers

## story_findadoctor_happypath_5
* greet
   - utter_greet
* inform{"location":"New York" ,"speciality":"orthopedic"}
    - utter_ask_doctor_search
    - find_providers

## story_findadoctor_happypath_6
* greet
   - utter_greet
* inform{"location":"Richmond"}
    - utter_ask_doctor_search
* affirm
    - utter_ask_speciality
* inform{"speciality":"orthopedic"}
    - find_providers

## story_findadoctor_happypath_7
* greet
   - utter_greet
* findadoctor
   - utter_ask_speciality
* inform{"speciality":"Urologist"}
    - utter_ask_location
* inform{"location":"San Antonio"}
    - find_providers

## story_findadoctor_happypath_8
* greet
   - utter_greet
* findadoctor
   - utter_ask_speciality
* inform{"speciality":"Urologist"}
    - utter_ask_location
* inform{"location":"San Antonio"}
    - find_providers


## story_findadoctor_happypath_9
* greet
   - utter_greet
* inform{"speciality":"orthopedic","location":"New York"}
    - utter_ask_doctor_search
    - find_providers

## story_findadoctor_happypath_10
* greet
   - utter_greet
* findadoctor
   - utter_ask_speciality
* inform{"speciality":"Radiologist"}
    - utter_ask_location
* inform{"location":"Las Vegas"}
    - find_providers

## story_findadoctor_happypath_11
* findadoctor
   - utter_ask_speciality
* inform{"speciality":"Urologist"}
    - utter_ask_location
* inform{"location":"Las Vegas"}
    - find_providers

## story_findadoctor_happypath_12
* findadoctor
   - utter_ask_speciality
* inform{"speciality":"Radiologist"}
    - utter_ask_location
* inform{"location":"San Antoni"}
    - find_providers

## story_findadoctor_happypath_12
* inform{"speciality":"orthopedic","location":"New York"}
    - utter_ask_location
* inform{"location":"San Antoni"}
    - find_providers