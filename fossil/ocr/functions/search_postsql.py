import psycopg2
from dto.food import Food

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

    def to_dict(self):
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

def search_postgresql(after_result):
    postgresql_result = []

    conn = psycopg2.connect(host='db',  # 호스트 수정
                            user='postgres',
                            password='1234',
                            dbname='postgres')  # 데이터베이스 이름 수정

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT 
                sub.*, 
                sub.relevance,
                sub.similarity_score
                FROM 
                (
                    SELECT 
                    f.*, 
                    similarity(f."name", %s) AS similarity_score,
                    ts_rank_cd(to_tsvector(f."name"), to_tsquery(%s)) AS relevance
                    FROM 
                    public.foods f
                    WHERE 
                    to_tsvector(f."name") @@ to_tsquery(%s)
                    OR f."name" ILIKE %s
                ) AS sub
                CROSS JOIN 
                (
                    SELECT 
                    MAX(similarity(f."name", %s)) AS max_relevance
                    FROM 
                    public.foods f
                    WHERE 
                    to_tsvector(f."name") @@ to_tsquery(%s)
                    OR f."name" ILIKE %s
                ) AS max_value
                WHERE similarity_score >= 0.3
                ORDER BY sub.similarity_score DESC
                LIMIT 1 OFFSET 0;
            """

            for after_result_tuple in after_result:
                # SQL 쿼리 실행
                cursor.execute(sql, (after_result_tuple, after_result_tuple, after_result_tuple, after_result_tuple, after_result_tuple, after_result_tuple, after_result_tuple))

                # Food 객체로 변환하여 postgresql_result에 추가, Food 객체의 name가 postgresql_result의 name에 없을 경우에만 추가
                result = cursor.fetchall()
                if result:
                    for row in result:
                        food = Food(
                            id=row[0],
                            calcium=row[1],
                            carbohydrate=row[2],
                            classification=row[3],
                            detail_classification=row[4],
                            dietary_fiber=row[5],
                            energy=row[6],
                            fat=row[7],
                            food_code=row[8],
                            iron=row[9],
                            moisture=row[10],
                            name=row[11],
                            phosphorus=row[12],
                            protein=row[13],
                            selenium=row[14],
                            serving_size=row[15],
                            sodium=row[16],
                            vitamin_a=row[17],
                            vitamin_b1=row[18],
                            vitamin_b2=row[19],
                            vitamin_c=row[20]
                        )
                        postgresql_result.append(food)

    finally:
        # 데이터베이스 연결 종료
        conn.close()

    return [food.to_dict() for food in postgresql_result]
