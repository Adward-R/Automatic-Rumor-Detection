Automatic-Rumor-Detection
=========================

SRTP Project

 - read_data.py is adjusted to become a data preparer for libSVM
 - read_data.py requires a file.xlsx for input, and a train.txt for output
 
 
 
 ----
 
 InfoVis Individual：
 
 - **index.html** : main ui & display
 
 - **weibo1.json** : stacks' data
 
 	- **cnt_spread_level.py** : /TestData/ to /LevelData/
 	
 	- **overall_json_convert.py** : distract properly organized data from /LevelData/ to weibo1.json
 	
 	- **mini_json_convert.py** : distract properly organized data from /LevelData/ to /json/*.json **(deprecated)**
  
 -  **_users.json** : forced-directed-graph's new data (need minor adjust)
 
 	- **v_users_select.py** : select V-users that appears in reposts for more than 15 times > v_users.txt
 	
 	- **v_user.txt** : V-user name list (part)
 	
 	- **force_graph_json_convert.py**  : rely on v_user.txt, re-distill properly organized data from /TestData/ to _users.json
 	
 - **users.json** : *deprecated* json data of forced-directed-graph