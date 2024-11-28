import pycurl as c
import json
import time
from urllib.parse import urlencode
from io import BytesIO as by

curl = c.Curl()

class Problem:
    def __init__ (self, /, id=123459, title = "致敬传奇特级作弊大师 1_2_3_4_5_9 取得 2150 rating", description = "", input_format = "", 
                  output_format = "", example = "", limit_and_hint = "", tags=[]):
        self.id = id
        self.title = title
        self.description = description
        self.input_format = input_format
        self.output_format = output_format
        self.example = example
        self.limit_and_hint = limit_and_hint
        self.tags = []

    def pack (self):
        result = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "input_format": self.input_format,
            "output_format": self.output_format,
            "example": self.example,
            "limit_and_hint": self.limit_and_hint,
            "tags": self.tags
        }
        return result

def unroll_fd (raw_data):
    form_data = []
    for i in raw_data.keys ():
        if type(raw_data[i]) == list:
            for j in raw_data[i]:
                form_data.append ((i, j))
        else:
            form_data.append ((i, raw_data[i]))
    return form_data

class OJ7Local:
    def __init__(self):
        self.cookie = ""
        self.OJ7_URL = ""
        self.COOKIE = ""

    def load_config (self, filename):
        with open (filename, "r") as config_file:
            config = json.load(config_file)
            
            # Load configuration
            self.OJ7_URL = config["OJ7_URL"]
            self.COOKIE = config["COOKIE"]

    def post(self, url, form_data = []):
        curl.reset ()
        curl.setopt (c.URL, self.OJ7_URL+url)
        curl.setopt (c.COOKIE, self.COOKIE)
        curl.setopt (c.POSTFIELDS, urlencode(unroll_fd(form_data)))
        okay = False
        result = None
        while not okay:
            try:
                result = curl.perform ()
                okay = True
            except c.error as e:
                print (f"Encountered error when executing POST {url}: {e}")
        return result

    def resurrect (self, /, prob_id="", user_id="", lang="", status=""):
        self.post ("/admin/restart")
        time.sleep(10) # Wish this does not cause disaster
        self.post ("/admin/rejudge", {
            "type": "rejudge",
            "problem_id": prob_id,
            "submitter": user_id,
            "language": lang,
            "status": status,
            "min_id": "",
            "min_score": "",
            "min_time": "1970-01-01+8:00:00",
            "max_id": "",
            "max_score": "",
            "max_time": "2038-01-19+11:14:07"
        })

    def create_problem (self, problem):
        return self.post (f"/problem/0/edit", problem.pack ())

    def delete_problem (self, problem_id):
        return self.post (f"/problem/{problem_id}/delete")

if __name__ == "__main__":
    oj7 = OJ7Local ()
    oj7.load_config ("config2.json")
