
token_query = '''
    SELECT 
        T.token, 
        count(*) as C

    FROM "TokenLinks" TL JOIN "Token" T
    ON T.tokenid = TL.target

    WHERE TL.source = 
    (SELECT tokenid FROM "Token" T WHERE T.token = :token)
    AND TL.distance > -4 AND TL.distance < 28 and T.dateid=:id

    GROUP BY T.token HAVING count(*) > 2
    ORDER BY C DESC
    LIMIT 10000;'''

token_query2 = '''
    SELECT 
        T.token, 
        TL.index,
        TL.distance
        --SUM(TL.index + TL.distance) as loc

    FROM "TokenLinks" TL JOIN "Token" T
    ON T.tokenid = TL.target

    WHERE TL.source = 
    (SELECT tokenid FROM "Token" T WHERE T.token = :token)
    AND TL.distance > -4 AND TL.distance < 28
    and T.dateid=:id

    --GROUP BY T.token, TL.distance HAVING count(*) > 2
    --ORDER BY loc DESC
    ORDER BY TL.index, TL.distance
    LIMIT 10000;'''
