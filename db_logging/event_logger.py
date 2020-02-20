class EventLogger():

	def __init__(self, db_name='simlog.db'):
		self.conn = sqlite3.connect(db_name)
		
		with open(r'logging_schema.txt','r') as log_schema_file:
			table_creation = []
			for