import sqlite3

class DateBaseSQL():
	db_name: str =  'SQL.db'
	def __init__(self, name = None):
		self.con = sqlite3.connect(name or self.db_name)
		self.cur = self.con.cursor()
		self.create_table()

	def set(self, name, score):
		db_score = self.get(name=name)
		if score is not None or score > db_score:
			self.cur.execute(f"DELETE FROM stocks WHERE name='{name}'")
			self.cur.execute(f"INSERT INTO stocks VALUES ('{name}', {score})")
			self.con.commit()

	def get(self, name=None, limit=5):
		if name:
			# SELECT <col1, col2, ...> FROM <table_name> where <condition>
			rows = self.cur.execute(f'SELECT score FROM stocks WHERE name="{name}" ORDER BY score')
			rows = list(rows)
			# getting first result and first position of the tuple
			return rows[0][0] if rows else None

		scores = list(self.cur.execute(f'SELECT * FROM stocks ORDER BY score DESC LIMIT {limit}'))
		return scores

	def create_table(self):
		self.cur.execute('''CREATE TABLE IF NOT EXISTS stocks (name text, score int)''')
		self.con.commit()


