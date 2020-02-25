import numpy as np
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size

        # You are white or black
        self.color = color

        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out

        # You need add your decision into your candidate_list.
        # System will get the end of your candidate_list as your decision.
        self.candidate_list = []

        # The input is current chessboard.

    # 给定一个位置， 找到它周围棋子情况
    @staticmethod
    def getPos(chessboard, currPos, i, j):
        x = currPos[0]
        y = currPos[1]
        if i == 0:
            x += j
        if i == 1:
            x += j
            y += j
        if i == 2:
            y += j
        if i == 3:
            x -= j
            y += j
        if i == 4:
            x -= j
        if i == 5:
            x -= j
            y -= j
        if i == 6:
            y -= j
        if i == 7:
            x += j
            y -= j
        if x < 0 or y < 0 or x > 14 or y > 14:
            return 2
        else:
            return chessboard[x][y]

    # 计算对于给定一个空位置对应的一条线， 计算我方棋子下在那里该空位置对应的线 得分情况
    @staticmethod
    def caulateValueArrayFr(arr, friend):
        line_infor = []
        start = 0
        i = 0
        while i <= 8:
            if arr[i] != friend:
                line_infor.append(start)
                line_infor.append(i)
                start = i + 1
            i = i + 1
        line_infor.append(start)
        line_infor.append(i)

        if len(line_infor) == 2 and line_infor[0] == 4 and line_infor[1] == 5:
            return 0

        value = 0
        j = 0
        while j < len(line_infor):
            left = line_infor[j]
            right = line_infor[j + 1]-1
            length = right - left + 1

            # 判断棋型
            if left <= 4 and right >= 4:
                # 成5
                if length >= 5:
                    value = 500000
                    return value
                if length == 4:
                    # 活4
                    if arr[left - 1] == 0 and arr[right + 1] == 0:
                        if value < 50000:
                            value = 50000
                    # 冲4
                    if (arr[left - 1] != 0 and arr[right + 1] == 0) or (
                        arr[left - 1] == 0 and arr[right + 1] != 0):
                        if value < 5000:
                            value = 5000
                if length == 3:

                    # 冲4
                    if (arr[left - 1] == 0 and arr[left - 2] == friend) or (
                            arr[right + 1] == 0 and arr[right + 2] == friend
                    ):
                        if value < 5000:
                            value = 5000

                    # 活3
                    if (arr[left - 1] == 0 and arr[right + 1] == 0 and arr[left - 2] == 0) or (
                            arr[left - 1] == 0 and arr[right + 1] == 0 and arr[right + 2] == 0
                    ):
                        if value < 3000:
                            value = 3000
                    # 冲3
                    if (arr[left - 1] != 0 and arr[right + 1] == 0 and arr[right + 2] == 0) or (
                        arr[right + 1] != 0 and arr[left - 1] == 0 and arr[left - 2] == 0) or (
                        arr[left - 1] == 0 and arr[right + 1] == 0
                    ):
                        if value < 1300:
                            value = 1300


                if length == 2:
                    # 冲4
                    if (arr[3] == friend and arr[0] == friend and arr[1] == friend and arr[2] == 0) or (
                        arr[5] == friend and arr[6] == 0 and arr[7] == friend and arr[8] == friend) or (
                        arr[3] == friend and arr[5] == 0 and arr[6] == friend and arr[7] == friend) or (
                        arr[5] == friend and arr[3] == 0 and arr[1] == friend and arr[2] == friend
                    ):
                        if value < 5000:
                            value = 5000

                    # 活3
                    if (arr[left-1] == 0 and arr[right + 1] == 0 and arr[left - 2] == friend and arr[left - 3] == 0) or(
                      arr[left - 1] == 0 and arr[right + 1] == 0 and arr[right + 2] == friend and arr[right + 3] == 0
                    ):
                        if value < 2999:
                            value = 2999

                    # 冲3
                    if(arr[3] == friend and arr[2] == 0 and arr[1] == friend and (arr[0] == 0 or arr[5] == 0)) or (
                        arr[3] == friend and arr[5] == 0 and arr[6] == friend and (arr[2] == 0 or arr[7] == 0)) or (
                        arr[5] == friend and arr[6] == 0 and arr[7] == friend and (arr[3] == 0 or arr[8] == 0)) or (
                        arr[5] == friend and arr[3] == 0 and arr[2] == friend and (arr[1] == 0 or arr[6] == 0)) or (
                        arr[left - 1] == 0 and arr[left - 2] == 0 and arr[left - 3] == friend) or (
                        arr[right + 1] == 0 and arr[right + 2] == 0 and arr[right + 3] == friend):

                        if value < 1300:
                            value = 1300

                    # 活2
                    if (arr[left - 1] == 0 and arr[left - 2] == 0 and arr[right + 1] == 0 and (arr[left - 3] == 0 or
                        arr[right + 2] == 0)) or (
                        arr[left - 1] == 0 and arr[right + 1] == 0 and arr[right + 2] == 0 and (arr[left - 2] == 0 or
                        arr[right + 3] == 0)):

                        if value < 1100:
                            value = 1100

                    # 冲2
                    if (arr[right + 1] == 0 and arr[right + 2] == 0 and arr[right + 3] == 0) or (
                        arr[left - 1] == 0 and arr[left - 2] == 0 and arr[left - 3] == 0) or (
                        arr[right + 1] == 0 and arr[left - 1] == 0 and arr[left - 2] == 0) or (
                        arr[left - 1] == 0 and arr[right + 1] == 0 and arr[right + 2] == 0):

                        if value < 300:
                            value = 300

                if length == 1:

                    # 冲4
                    if (arr[3] == 0 and arr[2] == friend and arr[1] == friend and arr[0] == friend) or (
                        arr[5] == 0 and arr[6] == friend and arr[7] == friend and arr[8] == friend
                    ):
                        if value < 5000:
                            value = 5000
                    # 活3
                    if (arr[3] == 0 and arr[2] == friend and arr[1] == friend and arr[0] == 0 and arr[5] == 0) or(
                        arr[3] == 0 and arr[5] == 0 and arr[6] == friend and arr[7] == friend and arr[8] == 0
                    ):
                        if value < 2999:
                            value = 2999
                    # 冲3
                    if (arr[1] == friend and arr[2] == friend and arr[3] == 0 and (arr[0] == 0 or arr[5] == 0)) or (
                        arr[5] == 0 and arr[6] == friend and arr[7] == friend and (arr[3] == 0 or arr[8] == 0)) or (
                        arr[3] == 0 and arr[2] == 0 and arr[1] == friend and arr[0] == friend) or (
                        arr[5] == 0 and arr[6] == 0 and arr[7] == friend and arr[8] == friend) or (
                        arr[2] == friend and arr[3] == 0 and arr[5] == 0 and arr[6] == friend) or (
                        arr[5] == 0 and arr[6] == friend and arr[7] == 0 and arr[8] == friend) or (
                        arr[0] == friend and arr[1] == 0 and arr[2] == friend and arr[3] == 0
                    ):

                        if value < 1299:
                            value = 1299

                    # 活2
                    if(arr[3] == 0 and arr[2] == friend and arr[1] == 0 and arr[5] == 0 and (arr[0] == 0 or arr[6] == 0)) or (
                       arr[3] == 0 and arr[5] == 0 and arr[6] == friend and arr[7] == 0 and (arr[2] == 0 or arr[8] == 0)) or (
                        arr[0] == 0 and arr[1] == friend and arr[2] == 0 and arr[3] == 0 and arr[5] == 0) or (
                        arr[3] == 0 and arr[5] == 0 and arr[6] == 0 and arr[7] == friend and arr[8] == 0
                    ):
                        if value < 1099:
                            value = 1099

                    # 冲2
                    if (arr[3] == 0 and arr[2] == friend and arr[1] == 0 and arr[5] == 0) or (
                        arr[3] == 0 and arr[5] == 0 and arr[6] == friend and arr[7] == 0) or (
                        arr[5] == 0 and arr[6] == 0 and arr[7] == friend and arr[8] == 0) or (
                        arr[1] == friend and arr[2] == 0 and arr[3] == 0 and arr[5] == 0) or (
                        arr[5] == 0 and arr[6] == 0 and arr[7] == 0 and arr[8] == friend) or (
                        arr[0] == friend and arr[1] == 0 and arr[2] == 0 and arr[3] == 0
                    ):
                        if value < 299:
                            value = 299
            j = j + 2
        return value

    # 计算对于给定一个空位置对应的一条线， 计算我方棋子下在那里该空位置对应的线 得分情况
    @staticmethod
    def caulateValueArrayEn(arr, enemy):
        line_infor = []
        start = 0
        i = 0
        while i <= 8:
            if arr[i] != enemy:
                line_infor.append(start)
                line_infor.append(i)
                start = i + 1
            i = i + 1
        line_infor.append(start)
        line_infor.append(i)

        if len(line_infor) == 2 and line_infor[0] == 4 and line_infor[1] == 5:
            return 0

        value = 0
        j = 0
        while j < len(line_infor):
            left = line_infor[j]
            right = line_infor[j + 1] - 1
            length = right - left + 1

            # 判断棋型
            if left <= 4 and right >= 4:
                # 成5
                if length >= 5:
                    value = 249999
                    return value
                if length == 4:
                    # 活4
                    if arr[left - 1] == 0 and arr[right + 1] == 0:
                        if value < 24999:
                            value = 24999
                    # 冲4
                    if (arr[left - 1] != 0 and arr[right + 1] == 0) or (
                            arr[left - 1] == 0 and arr[right + 1] != 0):
                        if value < 4600:
                            value = 4600
                if length == 3:

                    # 冲4
                    if (arr[left - 1] == 0 and arr[left - 2] == enemy) or (
                            arr[right + 1] == 0 and arr[right + 2] == enemy
                    ):
                        if value < 4600:
                            value = 4600

                    # 活3
                    if (arr[left - 1] == 0 and arr[right + 1] == 0 and arr[left - 2] == 0) or (
                            arr[left - 1] == 0 and arr[right + 1] == 0 and arr[right + 2] == 0
                    ):
                        if value < 2500:
                            value = 2500
                    # 冲3
                    if (arr[left - 1] != 0 and arr[right + 1] == 0 and arr[right + 2] == 0) or (
                        arr[right + 1] != 0 and arr[left - 1] == 0 and arr[left - 2] == 0) or (
                        arr[left - 1] == 0 and arr[right + 1] == 0
                    ):
                        if value < 1000:
                            value = 1000

                if length == 2:
                    # 冲4
                    if (arr[3] == enemy and arr[0] == enemy and arr[1] == enemy and arr[2] == 0) or (
                            arr[5] == enemy and arr[6] == 0 and arr[7] == enemy and arr[8] == enemy) or (
                            arr[3] == enemy and arr[5] == 0 and arr[6] == enemy and arr[7] == enemy) or (
                            arr[5] == enemy and arr[3] == 0 and arr[1] == enemy and arr[2] == enemy
                    ):
                        if value < 4600:
                            value = 4600

                    # 活3
                    if (arr[left-1] == 0 and arr[right + 1] == 0 and arr[left - 2] == enemy and arr[left - 3] == 0) or (
                        arr[left - 1] == 0 and arr[right + 1] == 0 and arr[right + 2] == enemy and arr[right + 3] == 0
                    ):
                        if value < 2499:
                            value = 2499

                    # 冲3
                    if (arr[3] == enemy and arr[2] == 0 and arr[1] == enemy and (arr[0] == 0 or arr[5] == 0)) or (
                        arr[3] == enemy and arr[5] == 0 and arr[6] == enemy and (arr[2] == 0 or arr[7] == 0)) or (
                        arr[5] == enemy and arr[6] == 0 and arr[7] == enemy and (arr[3] == 0 or arr[8] == 0)) or (
                        arr[5] == enemy and arr[3] == 0 and arr[2] == enemy and (arr[1] == 0 or arr[6] == 0)) or (
                        arr[left - 1] == 0 and arr[left - 2] == 0 and arr[left - 3] == enemy) or (
                        arr[right + 1] == 0 and arr[right + 2] == 0 and arr[right + 3] == enemy):

                        if value < 1000:
                            value = 1000

                    # 活2
                    if (arr[left - 1] == 0 and arr[left - 2] == 0 and arr[right + 1] == 0 and (arr[left - 3] == 0 or
                        arr[right + 2] == 0)) or (
                        arr[left - 1] == 0 and arr[right + 1] == 0 and arr[right + 2] == 0 and (arr[left - 2] == 0 or
                        arr[right + 3] == 0)):

                        if value < 900:
                            value = 900

                    # 冲2
                    if (arr[right + 1] == 0 and arr[right + 2] == 0 and arr[right + 3] == 0) or (
                        arr[left - 1] == 0 and arr[left - 2] == 0 and arr[left - 3] == 0) or (
                        arr[right + 1] == 0 and arr[left - 1] == 0 and arr[left - 2] == 0) or (
                        arr[left - 1] == 0 and arr[right + 1] == 0 and arr[right + 2] == 0):

                        if value < 200:
                            value = 200

                if length == 1:

                    # 冲4
                    if (arr[3] == 0 and arr[2] == enemy and arr[1] == enemy and arr[0] == enemy) or (
                            arr[5] == 0 and arr[6] == enemy and arr[7] == enemy and arr[8] == enemy
                    ):
                        if value < 4600:
                            value = 4600
                    # 活3
                    if (arr[3] == 0 and arr[2] == enemy and arr[1] == enemy and arr[0] == 0 and arr[5] == 0) or (
                            arr[3] == 0 and arr[5] == 0 and arr[6] == enemy and arr[7] == enemy and arr[8] == 0
                    ):
                        if value < 2499:
                            value = 2499
                    # 冲3
                    if (arr[1] == enemy and arr[2] == enemy and arr[3] == 0 and (arr[0] == 0 or arr[5] == 0)) or (
                        arr[5] == 0 and arr[6] == enemy and arr[7] == enemy and (arr[3] == 0 or arr[8] == 0)) or (
                        arr[3] == 0 and arr[2] == 0 and arr[1] == enemy and arr[0] == enemy) or (
                        arr[5] == 0 and arr[6] == 0 and arr[7] == enemy and arr[8] == enemy) or (
                        arr[2] == enemy and arr[3] == 0 and arr[5] == 0 and arr[6] == enemy) or (
                        arr[5] == 0 and arr[6] == enemy and arr[7] == 0 and arr[8] == enemy) or (
                        arr[0] == enemy and arr[1] == 0 and arr[2] == enemy and arr[3] == 0
                    ):

                        if value < 999:
                            value = 999

                    # 活2
                    if (arr[3] == 0 and arr[2] == enemy and arr[1] == 0 and arr[5] == 0 and (arr[0] == 0 or arr[6] == 0)) or (
                        arr[3] == 0 and arr[5] == 0 and arr[6] == enemy and arr[7] == 0 and (arr[2] == 0 or arr[8] == 0)) or (
                        arr[0] == 0 and arr[1] == enemy and arr[2] == 0 and arr[3] == 0 and arr[5] == 0) or (
                        arr[3] == 0 and arr[5] == 0 and arr[6] == 0 and arr[7] == enemy and arr[8] == 0
                    ):
                        if value < 899:
                            value = 899

                    # 冲2
                    if (arr[3] == 0 and arr[2] == enemy and arr[1] == 0 and arr[5] == 0) or (
                        arr[3] == 0 and arr[5] == 0 and arr[6] == enemy and arr[7] == 0) or (
                        arr[5] == 0 and arr[6] == 0 and arr[7] == enemy and arr[8] == 0) or (
                        arr[1] == enemy and arr[2] == 0 and arr[3] == 0 and arr[5] == 0) or (
                        arr[5] == 0 and arr[6] == 0 and arr[7] == 0 and arr[8] == enemy) or (
                        arr[0] == enemy and arr[1] == 0 and arr[2] == 0 and arr[3] == 0
                    ):
                        if value < 199:
                            value = 199

            j = j + 2
        return value

    # 计算对于一个给定空位置， 计算我方和敌方棋子下在该空位置得分
    def pointValue(self, chessboard, currPos, friend):
        valueF = 0
        valueE = 0
        if friend == 1:
            enemy = -1
        else:
            enemy = 1
        arr = []
        for i in range(0, 4):
            arr.clear()
            for j in range(0, 4):
                arr.append(self.getPos(chessboard, currPos, i + 4, 4 - j))
            arr.append(friend)
            for j in range(1, 5):
                arr.append(self.getPos(chessboard, currPos, i, j))
            valueF = valueF + self.caulateValueArrayFr(arr, friend)

        for i in range(0, 4):
            arr.clear()
            for j in range(0, 4):
                arr.append(self.getPos(chessboard, currPos, i + 4, 4 - j))
            arr.append(enemy)
            for j in range(1, 5):
                arr.append(self.getPos(chessboard, currPos, i, j))
            valueE = valueE + self.caulateValueArrayEn(arr, enemy)

        return (valueF, valueE)

    # 判断color对应的那方是否胜利
    def is_GameOver(self, chessboard, last_step, color):
        arr = []
        for i in range(0, 4):
            arr.clear()
            for j in range(0, 4):
                arr.append(self.getPos(chessboard, last_step, i + 4, 4 - j))
            arr.append(color)
            for j in range(1, 5):
                arr.append(self.getPos(chessboard, last_step, i, j))
            line_infor = []
            start = 0
            k = 0
            while k <= 8:
                if arr[k] != color:
                    line_infor.append(start)
                    line_infor.append(k)
                    start = k + 1
                k = k + 1
            line_infor.append(start)
            line_infor.append(k)
            k = 0
            while k < len(line_infor):
                left = line_infor[k]
                right = line_infor[k + 1] - 1
                length = right - left + 1
                if length >= 5:
                    return (True, 5000000)
                k = k + 2
        return (False, 0)

    def max_value(self, chessboard, alpha, beta, depth, friend, enemy, coord):
        result = self.is_GameOver(chessboard, coord, enemy)
        if result[0]:
            return -result[1]

        if depth == 0:
            idx = np.where(chessboard == COLOR_NONE)
            empty = list(zip(idx[0], idx[1]))
            result = 0
            for i in range(0, len(empty)):
                point = self.pointValue(chessboard, empty[i], friend)
                result += point[0] - point[1]*0.8

            return result

        idx = np.where(chessboard == COLOR_NONE)
        empty = list(zip(idx[0], idx[1]))
        result = []
        for i in range(0, len(empty)):
            point = self.pointValue(chessboard, empty[i], friend)
            value = point[0] + point[1] * 0.7
            result.append((i, value))
        result.sort(reverse=True, key=lambda x: x[1])
        i = 0
        v = -25000000
        while i < 2 and i < len(result):
            coord = empty[result[i][0]]
            chessboard[coord[0]][coord[1]] = friend
            min = self.min_value(chessboard, alpha, beta, depth - 1, friend, enemy, coord)
            if min > v:
                v = min
            chessboard[coord[0]][coord[1]] = 0
            if v >= beta:
                return v
            if v > alpha:
                alpha = v
            i = i + 1
        return v

    def min_value(self, chessboard, alpha, beta, depth, friend, enemy, coord):
        result = self.is_GameOver(chessboard, coord, friend)
        if result[0]:
            return result[1]

        if depth == 0:
            idx = np.where(chessboard == COLOR_NONE)
            empty = list(zip(idx[0], idx[1]))
            result = 0
            for i in range(0, len(empty)):
                point = self.pointValue(chessboard, empty[i], enemy)
                result += point[0] - point[1]*0.8
            return -result

        idx = np.where(chessboard == COLOR_NONE)
        empty = list(zip(idx[0], idx[1]))
        result = []
        for i in range(0, len(empty)):
            point = self.pointValue(chessboard, empty[i], enemy)
            value = point[0] + point[1] * 0.7
            result.append((i, value))
        result.sort(reverse=True, key=lambda x: x[1])

        i = 0
        v = 25000000
        while i < 2 and i < len(result):
            coord = empty[result[i][0]]
            chessboard[coord[0]][coord[1]] = enemy
            max = self.max_value(chessboard, alpha, beta, depth - 1, friend, enemy, coord)
            if max < v:
                v = max
            chessboard[coord[0]][coord[1]] = 0

            if v <= alpha:
                return v
            if v < beta:
                beta = v
            i = i + 1
        return v

    def go(self, chessboard):
        start = time.time()
        # Clear candidate_list
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        friend = self.color
        if friend == 1:
            enemy = -1
        else:
            enemy = 1
        idx = np.where(chessboard == COLOR_NONE)
        empty = list(zip(idx[0], idx[1]))
        if len(empty) == 225:
            self.candidate_list.append((7, 7))
        else:
            result = []
            for i in range(0, len(empty)):
                point = self.pointValue(chessboard, empty[i], friend)
                value = point[0] + point[1] * 0.7
                result.append((i, value))
            result.sort(reverse=True, key=lambda x: x[1])
            i = 0
            best_score = -25000000
            beta = 25000000
            if len(result) <= 4:
                self.candidate_list.append(empty[result[0][0]])
            else:
                while i < 4 and i < len(result):
                    coord = empty[result[i][0]]
                    chessboard[coord[0]][coord[1]] = friend
                    v = self.min_value(chessboard, best_score, beta, 4, friend, enemy, coord)
                    if v > best_score:
                        best_score = v
                        best_coord = coord
                        self.candidate_list.append(best_coord)
                    chessboard[coord[0]][coord[1]] = 0
                    i = i + 1
            end = time.time()
            print(end - start)

