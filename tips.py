# 将list存入pandas的dataframe数据结构中


table_head = []
id = []
location = []
distric = []
df = pd.DataFrame({table_head[0]:id,table_head[1]:location......})

# 然后将dataframe存入csv文件中

df.to_csv('new.csv',index = False, sep = '')#index是是否显示行名，默认为True，sep是分隔符
