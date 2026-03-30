import database

messages = database.get_all_messages()
print(f"{'ID':<3} | {'CONTENIDO':<55} | {'FECHA':<20} | {'IP':<15}")
print("-" * 100)
for m in messages:
  print(f"{m[0]:<3} | {m[1]:<55} | {m[2]:<20} | {m[3]:<15}")