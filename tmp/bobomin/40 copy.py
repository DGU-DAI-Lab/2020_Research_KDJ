raw = '..A..\n.A.A.\nAAAAA\nA...A\nA...A'
print(hash('..A..'))
      
# # 42
# print('..A..\n.A.A.\nAAAAA\nA...A\nA...A')

# # 46
# print('..A..\n.A.A.\n'+'A'*5+'\nA...A\nA...A')

# # 40
# print('..A..\n.A.A.\nAAAAA'+'\nA...A'*2)

# # 59
# print('\n'.join(['..A..','.A.A.','AAAAA','A...A','A...A']))


# # 42
# print("""..A..
# .A.A.
# AAAAA
# A...A
# A...A""")

# # 42
# print("""..A..
# .A.A.
# AAAAA"""+'\nA...A'*2)

# # 43
# print("""..A..
# .A.A.
# """+'A'*5+'\nA...A'*2)