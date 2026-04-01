import pandas as pd

# 读取Excel文件
excel_path = "./policy_data.xlsx"
df = pd.read_excel(excel_path)

print("原始数据形状:", df.shape)
print("原始数据列:", df.columns.tolist())

# 1. 检查并处理title列的重复值
print("\n1. 处理重复值:")
duplicate_count = df.duplicated('title').sum()
print(f"title列重复值数量: {duplicate_count}")

if duplicate_count > 0:
    print("去重前数据行数:", len(df))
    df = df.drop_duplicates(subset=['title'], keep='first')
    print("去重后数据行数:", len(df))
else:
    print("无重复值")

# 2. 检查并删除空列
print("\n2. 处理空列:")
empty_columns = []
for col in df.columns:
    if df[col].isnull().all():
        empty_columns.append(col)

print(f"空列数量: {len(empty_columns)}")
if empty_columns:
    print(f"空列: {empty_columns}")
    df = df.drop(columns=empty_columns)
    print("删除空列后的数据列:", df.columns.tolist())
else:
    print("无空列")

# 保存处理后的数据
df.to_excel("./policy_data_cleaned.xlsx", index=False)
print("\n处理完成，数据已保存到 policy_data_cleaned.xlsx")
print("处理后数据形状:", df.shape)
