import requests
from requests.structures import CaseInsensitiveDict

TestCenter_dict = {
 1: {'name':'Cork (The Lee)', 'Eircode':'T23 KR96', 'fkey':'$2y$10$hBn3hjFW8P5mZ.EYmfk8VuTfNigh1hedw0dtD0yDrb06iDjaANlDS', 'ids':14090},
 2: {'name':'Cork (Dunmanway)', 'Eircode':'P47CK70','fkey':'$2y$10$Uk5jlMs51USPHnC/PoAatuRx5NLMeoqvNwO3kVzPRIOdjynyIxxqW', 'ids':14161},
 3: {'name':'Cork (South Douglas)', 'Eircode':'T12 TW2C','fkey':'$2y$10$Oo2NrnetzGq0A1lsVPTFa.8l8M.scIJi4Uks4D0XlUnDuoNslA2b2', 'ids':14692},
 4: {'name':'Cork (Cork Airport)', 'Eircode':'T12 WK83','fkey':'$2y$10$d7EJ2ECTnOn4nfrQOsbuMeUae1XTS0JAqWTnto1C7BG6jfFqm2I9S', 'ids':17125},
 5: {'name':'Cork (St. Raphaels Centre)', 'Eircode':'P36 C596','fkey':'$2y$10$znwICcFZgkJEnhXgQnlwIeKtiqfTis6q.2OhALT/sHJrPe80Eix82', 'ids':17059},
}

for k in TestCenter_dict:
    url = "https://covid19test.healthservice.ie/swiftflow.php?future_days=1&minutes_buffer=60&enforce_future_days=1&enforce_today_or_tomorrow_only=0"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json, text/plain, */*"
    headers["content-type"] = "application/json"
    data = f'{{"task":"getConsultantAvailability","facility_id":"{TestCenter_dict[k]["fkey"]}","type_id":{TestCenter_dict[k]["ids"]},"flow":"routine"}}'
    resp = requests.post(url, headers=headers, data=data)
    Result = resp.json()
    Availablility = Result['data']['type']['total_slots_available']

    if Availablility > 0:
        print(f'The Following Test Center: {TestCenter_dict[k]["name"]} has: {Availablility} available Slots Free')
    
    #To-Do
     # Send a Twilio Text Message
      # Use Selenium Chrome-Browser to Book the Appointment if needed. 
    
    

    

   





