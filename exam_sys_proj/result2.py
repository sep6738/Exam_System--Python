import json
import random
import time


def panduan():
    QUESTION_TYPES = ["判断题"]
    SUBJECTS = ["数学"]
    KNOWLEDGE_POINTS = ["四则运算", "三角函数", "线性代数", "微积分"]
    SCORES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    QUESTIONS = ["√", "X"]
    QUESTIONS2 = ["这是一道判断题：A某某是B某某发生的原因",
                 "这是一道判断题：B某某是A某某",
                 "这是一道判断题：A某某的B某某是钝角"]
    question_type = random.choice(QUESTION_TYPES)
    subject = random.choice(SUBJECTS)
    knowledge_point_count = random.randint(1, 2)
    knowledge_points = random.sample(KNOWLEDGE_POINTS, knowledge_point_count)
    difficulty = random.randint(1, 10)
    score = random.choice(SCORES)
    shuffle = True
    questions = random.sample(QUESTIONS, 2)
    main_content = f"编号为#{random.randint(1, 102400)}的判断题：" + f"{random.choice(QUESTIONS2)}"
    answer = ["0", "1"][random.randint(0, 1)]

    return {
        "type": question_type,
        "score": [score],
        "shuffle": shuffle,
        "questions": questions,
        "main_content": main_content,
        "answer": [answer],
        "subject": subject,
        "difficulty": difficulty,
        "knowledge_point": knowledge_points
    }


def xuanze():
    QUESTION_TYPES = ["选择题"]
    SUBJECTS = ["数学"]
    KNOWLEDGE_POINTS = ["四则运算", "三角函数", "线性代数", "微积分"]
    SCORES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    QUESTIONS = ["这是一道选择题：某某发生的原因_______",
        "这是一道选择题：_______是某某",
        "这是一道选择题：某某的_______是钝角"]
    OPTIONS = ["选项1", "选项2", "选项3", "选项4", "选项a", "选项b", "选项c", "选项d"]
    question_type = random.choice(QUESTION_TYPES)
    subject = random.choice(SUBJECTS)
    knowledge_points = random.sample(KNOWLEDGE_POINTS, random.choice([1, 2]))
    difficulty = random.randint(1, 10)
    score = random.choice(SCORES)
    shuffle = random.choice([True, False])
    questions = random.sample(OPTIONS, 4)
    main_content = f"编号为#{random.randint(1, 102400)}的选择题：" + f"{random.choice(QUESTIONS)}"
    answer = [str(random.randint(1, 4))]

    return {
        "type": question_type,
        "score": [score],
        "shuffle": shuffle,
        "questions": questions,
        "main_content": main_content,
        "answer": answer,
        "subject": subject,
        "difficulty": difficulty,
        "knowledge_point": knowledge_points
    }


def tiankong():
    QUESTION_TYPES = ["填空题"]
    SUBJECTS = ["数学"]
    KNOWLEDGE_POINTS = ["四则运算", "三角函数", "线性代数", "微积分"]
    SCORES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    QUESTIONS = [None]
    question_type = random.choice(QUESTION_TYPES)
    subject = random.choice(SUBJECTS)
    knowledge_point_count = random.randint(1, 2)
    knowledge_points = random.sample(KNOWLEDGE_POINTS, knowledge_point_count)
    difficulty = random.randint(1, 10)
    score = random.choice(SCORES)
    shuffle = False
    questions = random.sample(QUESTIONS, 1)
    main_content = random.choice([
        "这是一道填空题：某某发生的原因_______",
        "这是一道填空题：某某_______的是_______",
        "这是一道填空题：_______是某某",
        "这是一道填空题：某某的_______是钝角"
    ])
    main_content = f"编号为#{random.randint(1, 102400)}的填空题：" + main_content
    answer = random.sample(["填空题答案1", "填空题答案2"], 1)
    # cnt = random.randint(1, 10086)
    # main_content = f"{cnt}{main_content}"
    return {
        "type": question_type,
        "score": [score],
        "shuffle": shuffle,
        "questions": questions,
        "main_content": main_content,
        "answer": answer,
        "subject": subject,
        "difficulty": difficulty,
        "knowledge_point": knowledge_points
    }


def zhuguan():
    QUESTION_TYPES = ["主观题"]
    SUBJECTS = ["数学"]
    KNOWLEDGE_POINTS = ["四则运算", "三角函数", "线性代数", "微积分"]

    SCORES = list(range(5, 21))
    MAIN_CONTENT = [
        "哥德巴赫猜想是一个著名的数学猜想,至今没有人去证明。你想试试吗?",
        "线性代数是数学的一个重要分支,涉及到向量、矩阵等概念。你对这方面有什么了解吗?",
        "写作是英语学习的重要组成部分,需要掌握各种写作技巧。你有什么经验可以分享吗?",
        "阅读理解是考试中的重点内容,需要理解文章的主旨和细节。你有什么好的方法吗?",
        "力学是物理学的基础,包括经典力学和量子力学。你对这个领域有什么见解吗?",
        "电磁学是物理学的另一个重要分支,研究电磁现象。你了解这方面的知识吗?",
        "有机化学是化学的重要组成部分,研究碳化合物。你对这个领域有什么认识吗?", "无机化学研究无机物质,如金属、酸碱等。你在这方面有什么心得吗?"
    ]
    QUESTIONS = [
        "请说出哥德巴赫猜想的第一个猜想", "请说出哥德巴赫猜想的第二个猜想", "请简要介绍线性代数中向量的概念",
        "请谈谈你在英语写作中的经验和技巧", "请说明在英语阅读理解中你的一些方法和心得",
        "请简要描述牛顿力学的基本定律", "请简要解释电磁感应的原理",
        "请简要介绍有机化学中的烷烃概念", "请简要介绍无机化学中酸碱的定义"
    ]
    ANSWERS = [
        "每一个可以写成两个素数之和的整数,也可以写成任意多的素数之和,直到所有项都是单位1",
        "每个大于2的整数都可以写成三个素数之和", "向量是一个有大小和方向的量,可以用来表示物理量,如位移、速度、力等",
        "在英语写作中,需要先确定主题,然后组织结构,注意语法、词汇的使用,并进行多次修改完善",
        "在英语阅读理解中,需要仔细读懂文章,找出主旨大意,并理解细节信息",
        "牛顿力学的三大定律分别是:惯性定律、作用力-反作用力定律、加速度与作用力成正比",
        "电磁感应是根据麦克斯韦方程中的电磁诱导现象,当磁通量变化时会产生感应电动势",
        "烷烃是饱和烃,分子式为CnH2n+2,是最简单的有机化合物", "酸是质子给体,能够使溶液pH值下降;碱是质子受体,能够使溶液pH值上升"
    ]
    question_type = random.choice(QUESTION_TYPES)
    subject = random.choice(SUBJECTS)
    knowledge_points = random.sample(KNOWLEDGE_POINTS, random.choice([1, 2, 3, 4]))
    difficulty = random.randint(1, 10)
    score = random.choice(SCORES)
    main_content = random.choice(MAIN_CONTENT)
    main_content = f"编号为#{random.randint(1, 102400)}的主观题：" + main_content
    question = random.sample(QUESTIONS, random.randint(1, 4))
    answer = random.choice(ANSWERS)
    for i in range(len(question)):
        question[i] = f"编号为#{random.randint(1, 102400)}的主观题小题：" + question[i]
    # question = f"{cnt}{question}"
    # main_content = f"{cnt}{main_content}"
    return {
        "type": question_type,
        "score": [score],
        "shuffle": False,
        "questions": question,
        "main_content": main_content,
        "answer": [answer],
        "subject": subject,
        "difficulty": difficulty,
        "knowledge_point": knowledge_points
    }


a = int(input("选择题个数:\n"))
b = int(input("判断题个数:\n"))
c = int(input("填空题个数:\n"))
d = int(input("主观题个数:\n"))
random.seed(None)
result = []
for i in range(a):
    result.append(xuanze())
for i in range(b):
    result.append(panduan())
for i in range(c):
    result.append(tiankong())
for i in range(d):
    result.append(zhuguan())
with open("result.json", "w", encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
# dic = {}
# for i in result:
#     data = i['difficulty']
#     if data in dic:
#         dic[data] += 1
#     else:
#         dic[data] = 1
# print(dic)