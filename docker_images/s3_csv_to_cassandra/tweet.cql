CREATE TABLE chrisadkin.tweet (
   tweet_id   bigint PRIMARY KEY
  ,text_body  text
  ,s_neg      decimal 
  ,s_pos      decimal
  ,s_neu      decimal
  ,s_compound decimal);
