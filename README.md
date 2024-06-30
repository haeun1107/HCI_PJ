2024년 1학기 인간컴퓨터상호작용 6조 <퍼즐 위치 가이드>

## 1000피스 퍼즐.. 언제 다 맞추지?
> 1시간째 퍼즐 조각의 위치를 못 찾고 있나요?<br>
>
> 끝까지 퍼즐을 맞추지 못해 포기한 적이 있나요?<br>
>
> 혼자 고민하지 말고, 🤔 **퍼즐 위치 가이드**에서 **힌트**를 받아보세요!<br>

![WELCOME (1)](https://github.com/haeun1107/HCI_PUZZLE/assets/84195580/f4a525dc-fe39-424c-94a6-a52ae01fd939)


<br><br>

## 🧩 프로젝트 소개

### 퍼즐을 스스로 해결할 수 있도록 적절한 힌트 제공 서비스, 퍼즐 위치 가이드 ✨
 퍼즐 맞추기는 많은 사람들이 즐기는 인기 있는 취미 활동으로, 특히 1000피스 이상의 대형 퍼즐은 집중력과 인내심을 요구하는 도전적인 활동으로 주목받고 있습니다. 연구에 따르면, 퍼즐 맞추기는 단순한 취미 활동을 넘어서 인지 능력 향상, 스트레스 해소 등의 여러 긍정적인 효과를 제공합니다. 하지만 퍼즐을 맞추는 과정에서 특정 퍼즐 조각을 찾는 데 많은 시간이 소요되는 문제가 있고, 끝까지 퍼즐을 맞추지 못해 포기하는 상황도 자주 발생합니다.
 
**퍼즐 위치 가이드**는 사용자가 퍼즐 조각의 위치를 찾을 수 있도록 도움을 제공하는 퍼즐 조각 탐색 및 매칭 서비스입니다. 사용자가 퍼즐 조각을 빠르게 찾고, 다양한 난이도에 따른 힌트를 제공받아 퍼즐 맞추기의 흥미를 유지하도록 도와줍니다.
<br><br>

## 👀 주요 기능
- **퍼즐 조각 탐색 및 매칭** : 현재까지 맞춘 퍼즐 조각의 영역과 위치를 찾고자 하는 퍼즐 조각의 영역 표시
- **실시간 피드백 및 가이드** : 퍼즐 맞추기 과정에서 실시간으로 도움 제공
- **다양한 난이도의 힌트 제공** : 사용자 수준에 맞게 힌트 난이도 조절
<br><br>

## 🧬 설계 구조
<img width="636" alt="image" src="https://github.com/haeun1107/HCI_PUZZLE/assets/84195580/42b753d7-7912-4baa-8a3c-654d18b9b3fb">
<br><br>

## 🎆 이미지 전처리
<img width="739" alt="image" src="https://github.com/haeun1107/HCI_PUZZLE/assets/84195580/e0f51e38-5914-4b15-bea5-169180bac45a">
<br><br>

## 🗂️ 퍼즐 개수에 따른 유사도 결과 비교 분석
<img width="727" alt="유사도" src="https://github.com/haeun1107/HCI_PUZZLE/assets/84195580/2bbbbb8c-a911-4171-a6e5-bb8a462f0b51">
<br><br>

## 🧐 HCI 기반 결과 분석
<img width="639" alt="image" src="https://github.com/haeun1107/HCI_PUZZLE/assets/84195580/d0535cda-f434-4dfb-b574-43cb88e5e5ab">
<br><br>

## 👛 실제 상품성 및 실용성 평가
<img width="702" alt="image" src="https://github.com/haeun1107/HCI_PUZZLE/assets/84195580/036854de-1275-413c-9f46-15835d0ad8f5">
<br><br>

## ⚔️ 기술 스택
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) <img src="https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0" alt="MacOS" style="zoom:80%;" />
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Flask](https://img.shields.io/badge/flask-FF0000?style=for-the-badge&logo=flask&logoColor=000000) 
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
<br><br>

## 📷 시연 영상
- 링크 : https://www.youtube.com/watch?v=IrURwGzas4Q
<br><br>

## 📁 프로젝트 파일 구조
```
├── 1000p
│   ├── current.jpg
│   ├── current2.jpg
│   ├── origin.jpg
│   └── target.jpg
├── 500p
│   ├── current.jpeg
│   ├── origin.png
│   └── target.png
├── 60p
│   ├── current.jpg
│   ├── origin.jpg
│   └── target.png
├── app.py
├── results
│   ├── 06c1cf6d-d8c0-415e-8ea0-9022c7a8df4f.png
│   ├── 14327826-a803-4b96-bc10-56b03bbd1ca5.png
│   └── 804ff65b-a68e-4041-8a7f-022dd012eebd.png
├── static
│   ├── puzzle1.svg
│   └── puzzle2.svg
├── templates
│   ├── index.html
│   └── result.html
└── uploads
    ├── current_image.jpg
    ├── main_image.jpg
    └── template_image.jpg
```
<br><br>
