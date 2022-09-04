SELECT 
 *
  FROM Electro
   FULL JOIN EVCSs
    USING (locations, lat, lng);
