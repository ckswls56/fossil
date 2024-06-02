class Food:
    def __init__(self, id, calcium, carbohydrate, classification, detail_classification,
                 dietary_fiber, energy, fat, food_code, iron, moisture, name,
                 phosphorus, protein, selenium, serving_size, sodium,
                 vitamin_a, vitamin_b1, vitamin_b2, vitamin_c):
        self.id = id
        self.calcium = calcium
        self.carbohydrate = carbohydrate
        self.classification = classification
        self.detail_classification = detail_classification
        self.dietary_fiber = dietary_fiber
        self.energy = energy
        self.fat = fat
        self.food_code = food_code
        self.iron = iron
        self.moisture = moisture
        self.name = name
        self.phosphorus = phosphorus
        self.protein = protein
        self.selenium = selenium
        self.serving_size = serving_size
        self.sodium = sodium
        self.vitamin_a = vitamin_a
        self.vitamin_b1 = vitamin_b1
        self.vitamin_b2 = vitamin_b2
        self.vitamin_c = vitamin_c

    def to_dice(self):
                return {
                "id": self.id,
                "calcium": self.calcium,
                "carbohydrate": self.carbohydrate,
                "classification": self.classification,
                "detail_classification": self.detail_classification,
                "dietary_fiber": self.dietary_fiber,
                "energy": self.energy,
                "fat": self.fat,
                "food_code": self.food_code,
                "iron": self.iron,
                "moisture": self.moisture,
                "name": self.name,
                "phosphorus": self.phosphorus,
                "protein": self.protein,
                "selenium": self.selenium,
                "serving_size": self.serving_size,
                "sodium": self.sodium,
                "vitamin_a": self.vitamin_a,
                "vitamin_b1": self.vitamin_b1,
                "vitamin_b2": self.vitamin_b2,
                "vitamin_c": self.vitamin_c
                }   
