import sqlite3

class EventLogger():

    def __init__(self, db_name='db_logging/simlog.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = 1") # Enable foreign keys if not otherwise enabled
        self.c = self.conn.cursor()
        
        need_to_create = False
        # schema for tables
        self.must_have_tables = ['Requests','Schedules','Pickups','Dropoffs','SimRuns'] 

        self.c.execute("SELECT name from sqlite_master where type='table';")
        tables_in_db = self.c.fetchall()
        tables_in_db = [i[0] for i in tables_in_db]

        for tbl in self.must_have_tables:
            if tbl not in tables_in_db:
                need_to_create = True

        if need_to_create:
            with open(r'db_logging/logging_schema.txt','r') as log_schema_file:
                log_schema = log_schema_file.read()
                table_descriptions = log_schema.split(';')
                for i in range(len(table_descriptions)):
                    self.c.execute(table_descriptions[i] + ';')


    def log_events(event_list, table_name):
        prefix = f"INSERT INTO {table_name} values"
        for i, event in enumerate(event_list):
            event = "(" + str(i + self.curr_sim_id) + event[2:-1] + str(self.curr_sim_id) + ")"
            insert_str = prefix + event + ";"
            self.c.execute(insert_str)

    def log_sim(sim_tuple, table_name):
        row = self.c.execute("SELECT MAX(sim_id) from SimRuns;")
        max_sim_id = int(rows[0][0])
        self.curr_sim_id = max_sim_id + 1

        prefix = f"INSERT INTO {table_name} values"
        sim_tuple[0] = self.curr_sim_id

        query_str = prefix + str(sim_tuple) + ";"


    def log(sim_tuple, past_requests, past_schedules, past_pickups, past_dropoffs):
        self.log_sim(sim_tuple,self.must_have_tables[0])
        self.log_events(past_requests,self.must_have_tables[1])
        self.log_events(past_schedules, self.must_have_tables[2])
        self.log_events(past_pickups, self.must_have_tables[3])
        self.log_events(past_dropoffs, self.must_have_tables[4])
        self.conn.commit()
        self.c.close()
        self.conn.close()

        


