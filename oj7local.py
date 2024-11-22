import pycurl as c
import json
from urllib.parse import urlencode

curl = c.Curl()

class ProblemStatistics:
    def __init__ (self, /, ac_num = 0, submit_num = 0):
        self.ac_num = ac_num
        self.submit_num = submit_num

class ProblemStatement:
    def __init__ (self, /, title = "", description = "", input_format = "", 
                  output_format = "", example = "", limit_and_hint = "",
                  additional_file_id = ""):
        self.title = title
        self.description = description
        self.input_format = input_format
        self.output_format = output_format
        self.example = example
        self.limit_and_hint = limit_and_hint
        self.additional_file_id = additional_file_id

class ProblemSetup:
    def __init__(self, /, time_limit = 1000, memory_limit = 524288, is_public = 1, 
                file_io = 0, file_io_input_name = "", file_io_output_name = ""):
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.is_public = is_public
        self.file_io = file_io
        self.file_io_input_name = file_io_input_name
        self.file_io_output_name = file_io_output_name

class Problem:
    def __init__(self, id, /, title = "致敬传奇特级作弊大师 1_2_3_4_5_9 取得 2150 rating", 
                description = "test problem", input_format = "", output_format = "",
                example = "", limit_and_hint = "", additional_file_id = "",
                ac_num = 0, submit_num = 0, is_public = 1, file_io = 0,
                file_io_input_name = "", file_io_output_name = "",
                time_limit = 1000, memory_limit = 524288):
        self.id = id
        self.setup = ProblemSetup(time_limit=time_limit,memory_limit=memory_limit,
                                  is_public=is_public,file_io=file_io,
                                  file_io_input_name=file_io_input_name,
                                  file_io_output_name=file_io_output_name)
        self.statement = ProblemStatement(title=title,description=description,input_format=input_format,
                                    output_format=output_format, limit_and_hint=limit_and_hint,
                                    additional_file_id=additional_file_id,example=example)
        self.stats = ProblemStatistics(ac_num=ac_num,submit_num=submit_num)

    def pack (self):
        result = {
            "id": self.id,
            "title": self.statement.title,
            "description": self.statement.description,
            "input_format": self.statement.input_format,
            "output_format": self.statement.output_format,
            "example": self.statement.example,
            "limit_and_hint": self.statement.limit_and_hint,
            "additional_file_id": self.statement.additional_file_id,
            "ac_num": self.stats.ac_num,
            "submit_num": self.stats.submit_num,
            "is_public": self.setup.is_public,
            "file_io": self.setup.file_io,
            "file_io_input_name": self.setup.file_io_input_name,
            "file_io_output_name": self.setup.file_io_output_name,
            "time_limit": self.setup.time_limit,
            "memory_limit": self.setup.memory_limit
        }
        return result


class OJ7Local:
    def __init__(self):
        self.cookie = ""
        self.OJ7_URL = ""
        self.COOKIE = ""

    def load_config (self, filename):
        with open (filename, "r") as config_file:
            config = json.load(config_file)
            
            # Load configuration
            self.COOKIE = config["COOKIE"]
            self.OJ7_URL = config["OJ7_URL"]
        
    def post(self, url, form_data = {}):
        curl.reset ()
        curl.setopt (c.URL, self.OJ7_URL+url)
        curl.setopt (c.COOKIE, self.COOKIE)
        curl.setopt (c.POSTFIELDS, urlencode(form_data))
        return curl.perform ()
    
    def create_problem (self, problem):
        return self.post (f"/problem/0/edit", problem.pack ())

    def delete_problem (self, problem_id):
        return self.post (f"/problem/{problem_id}/delete")

if __name__ == "__main__":
    oj7 = OJ7Local ()
    oj7.load_config ("config.json")