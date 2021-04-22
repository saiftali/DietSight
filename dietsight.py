class Log: # Date indexed log of ingredients and symptoms
	def __init__(self):
		self.calendar = {}

	def add_entry(self, date, entry):
		if date in self.calendar:
			self.calendar[date].add_ingredients(entry.ingredients)
			self.calendar[date].add_symptoms(entry.symptoms)
		else:
			self.calendar[date] = entry

	def get_calendar(self):
		return self.calendar

class Entry: # Represents individual entry of ingredients and symptoms
	def __init__(self, ingredients=[], symptoms=[]):
		self.ingredients = []
		self.symptoms = []

		self.ingredients.extend(ingredients)
		self.symptoms.extend(symptoms)

	def get_ingredients(self):
		return self.ingredients

	def get_symptoms(self):
		return self.symptoms

	def set_ingredients(self, ingredients):
		self.ingredients = ingredients

	def set_symptoms(self, symptoms):
		self.symptoms = symptoms

	def add_ingredients(self, ingredients):
		for ingredient in ingredients:
			if ingredient not in self.ingredients:
				self.ingredients.append(ingredient)

	def add_symptoms(self, symptoms):
		for symptom in symptoms:
			if symptom not in self.symptoms:
				self.symptoms.append(symptom)

def analyze_triggers(log): # Uses Pearson's Phi-coefficient to numerically identify correlation between -1 and 1
	total_logs = 0
	total_symptoms = 0
	ingredient_counts = {}
	symptom_ingredient_counts = {}


	for date, entry in log.get_calendar().items():
		#print(date, entry.get_symptoms(), entry.get_ingredients())
		total_logs += 1

		for ingredient in entry.get_ingredients():
			if ingredient in ingredient_counts:
				ingredient_counts[ingredient] += 1
			else:
				ingredient_counts[ingredient] = 1

		if entry.get_symptoms():
			total_symptoms += 1
			for ingredient in entry.get_ingredients():
				if ingredient in symptom_ingredient_counts:
					symptom_ingredient_counts[ingredient] += 1
				else:
					symptom_ingredient_counts[ingredient] = 1


	analysis = {}
	for ingredient, count in ingredient_counts.items():
		is00 = total_logs - total_symptoms - count + (0 if ingredient not in symptom_ingredient_counts else symptom_ingredient_counts[ingredient])
		is01 = total_symptoms - (0 if ingredient not in symptom_ingredient_counts else symptom_ingredient_counts[ingredient]) 
		is10 = count - (0 if ingredient not in symptom_ingredient_counts else symptom_ingredient_counts[ingredient])
		is11 = (0 if ingredient not in symptom_ingredient_counts else symptom_ingredient_counts[ingredient])

		#print(ingredient, is00, is01, is10, is11)

		if ((is00 + is01) * (is00 + is10) * (is11 + is01) * (is11 + is10)) == 0:
			analysis[ingredient] = 0
		else:
			analysis[ingredient] = \
				(is00 * is11 - is01 * is10) / (((is00 + is01) * (is00 + is10) * (is11 + is01) * (is11 + is10)) ** 0.5)

	return analysis

def classify_triggers(analysis): # Classifies triggers between High, Medium, and Low risk
	high_risk = []
	medium_risk = []
	low_risk = []

	for ingredient, proportion in analysis.items():
		if proportion > 0.9:
			high_risk.append(ingredient)
		elif proportion > 0.7:
			medium_risk.append(ingredient)
		elif proportion > 0.5:
			low_risk.append(ingredient)

	print("High Risk: " + str(high_risk))
	print("Medium Risk: " + str(medium_risk))
	print("Low Risk: " + str(low_risk))

# Example Log
log = Log()

# Day 1
log.add_entry("1/12/2020", Entry(ingredients=['orange'])) # Orange
log.add_entry("1/12/2020", Entry(ingredients=['cheese', 'wheat', 'tomato', 'olive oil', 'yeast'])) # Pizza
log.add_entry("1/12/2020", Entry(ingredients=['wheat', 'egg', 'tomato', 'basil'])) # Pasta
log.add_entry("1/12/2020", Entry(symptoms=['heartburn']))

# Day 2
log.add_entry("1/13/2020", Entry(ingredients=['banana'])) # Banana
log.add_entry("1/13/2020", Entry(ingredients=['lettuce', 'olive oil', 'tomato'])) # Salad
log.add_entry("1/13/2020", Entry(ingredients=['cheese', 'lettuce', 'tomato', 'mayonaise', 'beef', 'wheat'])) # Burger
log.add_entry("1/13/2020", Entry(symptoms=['heartburn']))

# Day 3
log.add_entry("1/14/2020", Entry(ingredients=['orange'])) # Orange
log.add_entry("1/14/2020", Entry(ingredients=['strawberry jam', 'peanuts', 'wheat', 'egg'])) # PBJ Sandwich
log.add_entry("1/14/2020", Entry(ingredients=['wheat', 'egg', 'tomato', 'basil', 'onion', 'celery', 'carrot', 'olive oil', 'pork'])) # Pasta

# Day 4
log.add_entry("1/15/2020", Entry(ingredients=['orange'])) # Orange
log.add_entry("1/15/2020", Entry(ingredients=['strawberry jam', 'peanuts', 'wheat', 'egg'])) # PBJ Sandwich
log.add_entry("1/15/2020", Entry(ingredients=['wheat', 'egg', 'tomato', 'basil', 'onion', 'celery', 'carrot', 'olive oil', 'pork'])) # Pasta

# Day 5
log.add_entry("1/16/2020", Entry(ingredients=['oats', 'banana'])) # Oatmeal
log.add_entry("1/16/2020", Entry(ingredients=['cheese', 'wheat'])) # Grilled Cheese
log.add_entry("1/16/2020", Entry(ingredients=['rice', 'seaweed', 'fish'])) # Sushi
log.add_entry("1/16/2020", Entry(symptoms=['heartburn']))

# Day 6
log.add_entry("1/17/2020", Entry(ingredients=['banana'])) # Banana
log.add_entry("1/17/2020", Entry(ingredients=['rice', 'seaweed', 'fish'])) # Sushi
log.add_entry("1/17/2020", Entry(ingredients=['lettuce', 'olive oil', 'tomato'])) # Salad


# Day 7
log.add_entry("1/18/2020", Entry(ingredients=['cheese'])) # Cheese stick
log.add_entry("1/18/2020", Entry(ingredients=['cheese', 'beef', 'onion', 'mayonaise', 'wheat', 'yeast'])) # Burger
log.add_entry("1/18/2020", Entry(symptoms=['heartburn']))


print("Phi correlation coefficients: ", dict(sorted(analyze_triggers(log).items(), key=lambda item: item[1], reverse=True)), '\n')
classify_triggers(analyze_triggers(log))