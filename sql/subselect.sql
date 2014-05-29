SELECT 
	T.token,
	T.count,
	TL.dateid, 
	TL.source, 
	(SELECT Ts.token from "Token" Ts WHERE Ts.tokenid = TL.target),
	TL.target, 
	TL.distance, 
	TL.index 
  FROM 
	"Token" T INNER JOIN "TokenLinks" TL
  ON
	T.tokenid = TL.source
  WHERE T.token =  'Portland'
LIMIT 10000;
