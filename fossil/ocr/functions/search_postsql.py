import psycopg2
from dto.food import Food

def search_postgresql(after_result):
    postgresql_result = []

    conn = psycopg2.connect(host='localhost',
                            user='postgres',
                            password='1234',
                            dbname='public')

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
            OR f."name" % %s
            ) AS sub
            CROSS JOIN 
            (
                SELECT 
                MAX(similarity(f."name", %s)) AS max_relevance
                FROM 
                public.foods f
                WHERE 
            to_tsvector(f."name") @@ to_tsquery(%s)
            OR f."name" % %s
            ) AS max_value
            where sub.relevance > 0.3
            ORDER BY sub.similarity_score desc
            limit 
	        1 offset 0;
            """
            
            for after_result_tuple in after_result:
                # SQL 쿼리 실행
                cursor.execute(sql, (after_result_tuple, after_result_tuple, after_result_tuple, after_result_tuple))
                
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
    
    return postgresql_result
