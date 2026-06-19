# Pose-Reactive PetBot 🤖
 
**YOLOv8-Pose 기반 실시간 관절 인식 및 4단계 행동 상태 머신 구현**
 
<br>
 
## 팀 정보
 
| 항목 | 내용 |
|---|---|
| 팀명 | 코어 |
| 팀원 | 2371051 임도경 |
 
<br>
 
## 프로젝트 설명
 
카메라 영상에서 반려동물(강아지)의 관절 자세를 YOLOv8-Pose로 실시간 인식하고, Box height 변화율과 관절 방향성(정면/후면)을 조합하여 Approach(접근) / Retreat(회피) / Follow(추종) / Sleep(대기) 4단계 행동 상태를 판단, TurtleBot4가 Gazebo 시뮬레이션 환경에서 그에 맞게 반응하는 인터랙션 로봇 시스템
 
추가 센서 없이 단일 카메라 영상만으로 동물의 행동 상태를 추론하는 경량 시스템을 목표로 하며, ROS2 노드 3개(인지 → 판단 → 제어)가 토픽 기반 비동기 통신으로 구성
 
<br>
 
## 역할 분담
 
1인 팀으로 아래 과정들을 수행
 
| 영역 | 수행 내용 |
|---|---|
| 주제 선정 및 기획 | 문제 정의, 핵심 아이디어 설계, 프로젝트 제안서 및 중간보고서 작성 |
| 모델 학습 | Ultralytics Dog-Pose 데이터셋으로 YOLOv8-Pose fine-tuning (best.pt) |
| 시스템 설계 | ROS2 노드 구조 설계, 토픽 인터페이스 정의 |
| 인지 노드 구현 | pose_detector_node — 카메라 영상 구독, 관절 keypoint 및 box height 추출 |
| 판단 로직 구현 | pet_state_classifier_node — 변화율 기반 4단계 FSM 분류 로직 설계 및 임계값 보정 |
| 제어 노드 구현 | robot_controller_node — 상태별 속도 명령(cmd_vel) 생성 |
| 시뮬레이션 환경 구성 | ROS2 Humble + Gazebo Fortress + TurtleBot4 통합, 환경 호환성 문제 해결 |
| 테스트 및 디버깅 | 실측 데이터 기반 분류 임계값 재보정, 로봇 제어 간섭 현상 원인 분석 및 해결 |
| 발표자료 및 데모 | 데모 영상 촬영, 발표자료 및 발표 스크립트 작성 |
 
<br>
 
## AI 투명성 리포트
 
본 프로젝트는 Anthropic Claude를 보조 도구로 활용하였으며 사용 범위는 아래와 같이 구분
 
| 구분 | 내용 |
|---|---|
| 직접 수행한 영역 | 주제 선정, 문제 정의, 핵심 아이디어 설계, 시스템 구조 및 ROS2 노드 설계, 발표자료 제작 및 발표 스크립트 작성 |
| AI 도움을 받은 영역 | 구현 과정에서의 코드 작성 보조, 환경 구성 중 발생한 오류(TurtleBot3-Gazebo Fortress 호환성 문제, 로봇 자율 안전 행동으로 인한 제어 간섭 현상 등) 디버깅 과정에서의 원인 분석 및 해결 방안 도출, 분류 로직 임계값을 실측 데이터 기반으로 재보정하는 과정 |
 
<br>
 
## 참고 자료
 
| 자료 | 링크 |
|---|---|
| Ultralytics YOLOv8 Pose Estimation Documentation | https://docs.ultralytics.com/tasks/pose/ |
| Ultralytics Dog-Pose Dataset | https://docs.ultralytics.com/datasets/pose/dog-pose/ |
| TurtleBot4 User Manual | https://turtlebot.github.io/turtlebot4-user-manual/ |
| TurtleBot4 Simulation (Gazebo) Guide | https://turtlebot.github.io/turtlebot4-user-manual/software/simulation.html |
| Gazebo Fortress (Ignition) Documentation | https://gazebosim.org/docs/fortress/getstarted |
| ROS 2 Humble Documentation | https://docs.ros.org/en/humble/ |
| AP-10K: Animal Pose Dataset | https://github.com/AlexTheBad/AP-10K |
| Jocher, G. et al. (2023). YOLOv8 by Ultralytics | https://github.com/ultralytics/ultralytics |
 
<br>
 
## 발표 영상
 
YouTube: https://youtu.be/w6MUVZBxkW0

<br>
 
## GitHub 저장소
 
GitHub: https://github.com/ldkxllux/PoseReactive_PetBot
