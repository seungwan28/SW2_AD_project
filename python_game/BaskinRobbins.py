import sys, random
from PyQt5 import QtTest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,  QGridLayout, QLabel, QLineEdit, QTextEdit,
                             QToolButton, QComboBox)

from NumberDisplay import NumberDisplay

class BaskinRobbins(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 380, 150)
        # 숫자 디스플레이
        self.numberWindow = QTextEdit()
        self.numberWindow.setReadOnly(True)
        self.numberWindow.setAlignment(Qt.AlignLeft)
        font = self.numberWindow.font()
        font.setFamily('Courier New')
        self.numberWindow.setFont(font)

        # 숫자 디스플레이 레이아웃
        numberLayout = QGridLayout()
        numberLayout.addWidget(self.numberWindow, 0, 0)

        # 상태 레이아웃
        statusLayout = QGridLayout()

        # 순서 정하기 버튼
        self.firstButton = QToolButton()
        self.firstButton.setText('선공')
        self.laterButton = QToolButton()
        self.laterButton.setText('후공')
        self.firstButton.clicked.connect(self.firstClicked)
        self.laterButton.clicked.connect(self.laterClicked)
        statusLayout.addWidget(self.firstButton, 0, 0, 1, 2)
        statusLayout.addWidget(self.laterButton, 0, 1, 1, 2)

        # 사용자의 입력 위젯
        statusLayout.addWidget(QLabel('Player'), 1, 0)
        self.playerInput = QLineEdit()
        statusLayout.addWidget(self.playerInput, 2, 0)

        # 사용자의 입력 버튼
        self.confirmButton = QToolButton()
        self.confirmButton.setText('입력')
        self.confirmButton.clicked.connect(self.confirmClicked)
        statusLayout.addWidget(self.confirmButton, 2, 1)

        # 컴퓨터의 출력 위젯
        statusLayout.addWidget(QLabel('Com'), 3, 0)
        self.computerInput = QLineEdit()
        self.computerInput.setReadOnly(True)
        statusLayout.addWidget(self.computerInput, 4, 0)

        # 난이도 선택 박스
        self.difficulty = QComboBox()
        self.difficulty.addItem("난이도: Normal")
        self.difficulty.addItem("난이도: Hard")
        self.difficulty.activated[str].connect(self.difficultyChoice)
        statusLayout.addWidget(self.difficulty, 5, 0)

        # 새 게임 버튼
        self.newGameButton = QToolButton()
        self.newGameButton.setText('New Game')
        self.newGameButton.clicked.connect(self.startGame)
        statusLayout.addWidget(self.newGameButton, 6, 0)

        # 레이아웃 배치
        mainLayout = QGridLayout()
        mainLayout.addLayout(numberLayout, 0, 0)
        mainLayout.addLayout(statusLayout, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle('Baskin Robbins 31')

        self.show()
        self.startGame()

    # 게임 시작
    def startGame(self):
        self.numberDisplay = NumberDisplay()
        self.numberDisplay.startIndex = 0

        self.numberWindow.setPlaceholderText(self.numberDisplay.currentIndex())
        self.numberWindow.setText(self.numberDisplay.currentIndex())
        self.computerInput.clear()


    #사용자가 숫자 입력했을 때
    def confirmClicked(self):
        self.playerCall = self.playerInput.text()
        self.playerInput.clear()

        if len(self.playerCall) != 1:
            self.computerInput.setText("Enter 1, 2, 3")
            return

        if self.playerCall.isdigit() == False:
            self.computerInput.setText("Enter 1, 2, 3")
            return

        if self.playerCall in ['1', '2', '3']:
            self.playerPlay()
        else:
            self.computerInput.setText("Enter 1, 2, 3")
            return


    #선공
    def firstClicked(self):
        self.computerInput.setText("Player turn")


    #후공
    def laterClicked(self):
        if self.difficulty.currentIndex() == 0:
            self.computerPlay()
        elif self.difficulty.currentIndex() == 1:
            self.advancedComputerPlay()


    #난이도 설정
    def difficultyChoice(self):
        if self.difficulty.currentIndex() == 0:
            self.computerPlay()
            self.numberDisplay.decreaseIndex(int(self.computerCall))
            self.computerInput.clear()
            self.numberWindow.setText(self.numberDisplay.currentIndex())
        elif self.difficulty.currentIndex() == 1:
            self.advancedComputerPlay()
            self.numberDisplay.decreaseIndex(int(self.computerCall))
            self.computerInput.clear()
            self.numberWindow.setText(self.numberDisplay.currentIndex())


    #사용자의 입력 후 바로 컴퓨터 출력
    def playerPlay(self):
        try:
            self.numberDisplay.increaseIndex(self.playerCall)
            self.numberWindow.setText(self.numberDisplay.currentIndex())
            if self.numberDisplay.getIndex() >= 31:
                    self.computerInput.setText("Com win!")
            else:
                self.sleep(1)
                self.laterClicked()

        except IndexError:
            self.computerInput.setText("Press New Game")
            pass
    #시간 지연
    def sleep(self,time):
        QtTest.QTest.qWait(time * 1000)

    #보통 난이도 컴퓨터의 출력
    def computerPlay(self):
        try:
            if self.numberDisplay.getIndex() == 27:
                self.computerCall = '3'
            elif self.numberDisplay.getIndex() == 28:
                self.computerCall = '2'
            elif self.numberDisplay.getIndex() == 29:
                self.computerCall = '1'
            else:
                self.computerCall = str(random.randint(1, 3))
            self.computerInput.setText(self.computerCall)
            self.numberDisplay.increaseIndex(self.computerCall)
            self.numberWindow.setText(self.numberDisplay.currentIndex())

            if self.numberDisplay.getIndex() >= 31:
                self.computerInput.setText("Player win!")

        except IndexError:
            self.computerInput.setText("Press New Game")
            pass


    #어려움 난이도 컴퓨터의 출력
    def advancedComputerPlay(self):
        try:
            numList = [2, 6, 10, 14, 18, 22, 26, 30]
            if self.numberDisplay.getIndex() == 0:
                self.computerCall = '2'
            elif self.numberDisplay.getIndex() + 1 in numList or self.numberDisplay.getIndex() == 29:
                self.computerCall = '1'
            elif self.numberDisplay.getIndex() + 2 in numList or self.numberDisplay.getIndex() == 28:
                self.computerCall = '2'
            elif self.numberDisplay.getIndex() + 3 in numList or self.numberDisplay.getIndex() == 27:
                self.computerCall = '3'
            else:
                self.computerCall = str(random.randint(1, 3))
            self.computerInput.setText(self.computerCall)
            self.numberDisplay.increaseIndex(self.computerCall)
            self.numberWindow.setText(self.numberDisplay.currentIndex())

            if self.numberDisplay.getIndex() >= 31:
                self.computerInput.setText("Player win!")

        except IndexError:
            self.computerInput.setText("Press New Game")
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = BaskinRobbins()
    game.show()
    sys.exit(app.exec_())
