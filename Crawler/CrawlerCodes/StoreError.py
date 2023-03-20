import json
from datetime import datetime
from datetime import date

now = datetime.now()
today = date.today()
current_time = now.strftime(r"%H-%M-%S-%f")

def storeError(error: BaseException, message: str):
    print(message)
    print(error)
    
    with open(f"Crawler\\Errors\\json{today}--{current_time}.json", "w", encoding="utf-8") as jsonFile:
        json.dump([str(error.with_traceback()), error.__str__], jsonFile)