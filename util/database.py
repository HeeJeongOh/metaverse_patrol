'''
위험발언에 대한 기록을 저장할 저장소
database = {
	id : {
				warn: 0,
				chat [{'role': 'user', 'content': 'hello'},
				...
				],
	...
    },
}
'''

# # __(더블언더바) : 접근 제한
# class Record:

#     def __init__(self, id, caution, chat):
#         self.id = id
#         self.caution = caution
#         self.chat = chat
    
#     def __str__(self) -> str:
#         return f'{id}: {caution} 경고 - 대화 {chat}'
    
#     def get_chat(self):
#         return chat
import json

database = {

}