
SELECT 
T.token, 
count(*) as C

FROM "TokenLinks" TL JOIN "Token" T
ON T.tokenid = TL.target
WHERE TL.source = 
(SELECT tokenid FROM "Token" T WHERE T.token = 'Portland')
AND TL.distance > -4 AND TL.distance < 28 and T.dateid=8

GROUP BY T.token HAVING count(*) > 2
ORDER BY C DESC
