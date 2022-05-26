# D-FLEX



# 1. 팀원 정보 및 업무 분담 내역

### `팀장` 임진현

- Back-End
- Python
- Django

### `팀원` 함희주

- Frond-End
- HTML
- CSS
- JavaScript
- BootStrap 5



# 2. 목표 서비스 구현 및 실제 구현 정도

목표

영화 검색, 추천 서비스







## URLs

|           | URL                                            | View            |
| :-------- | ---------------------------------------------- | --------------- |
|           |                                                |                 |
| /         | /                                              | home            |
|           | search/                                        | search          |
| accounts/ |                                                |                 |
|           | signup/                                        | signup          |
|           | login/                                         | login           |
|           | logout/                                        | logout          |
|           | profile/`<username>`/                          | profile         |
|           | update/                                        | update          |
|           | password/                                      | change_password |
|           | kakao_login/                                   | kakao_login     |
|           | kakao_unlink/                                  | kakao_unlink    |
|           | auth/                                          | auth            |
| articles/ | /                                              | articles        |
|           | create/                                        | article_create  |
|           | `<article_pk>`/                                | article_detail  |
|           | `<article_pk>`/update/                         | article_update  |
|           | `<article_pk>`/delete/                         | article_detail  |
|           | `<article_pk>`/like/                           | article_like    |
|           | `<article_pk>`/comments/create/                | comment_create  |
|           | `<article_pk>`/comments/`<comment_pk>`/update/ | comment_update  |
|           | `<article_pk>`/comments/`<comment_pk>`/delete/ | comment_delete  |
| movies/   | /                                              | movies          |
|           | `<movie_pk>`/                                  | movie_detail    |
|           | `<movie_pk>`/reviews/create/                   | review_create   |
|           | `<movie_pk>`/reviews/`<review_pk>`/update/     | review_update   |
|           | `<movie_pk>`/reviews/`<review_pk>`/delete/     | review_delete   |
|           | for-you/`<movie_pk>`/                          | for_you         |
|           | for-you2/`<movie_pk>`/                         | for_you2        |
|           | for-you3/`<movie_pk>`/                         | for_you3        |



## Views

|          | 이름            | 역할                                        |
| -------- | --------------- | ------------------------------------------- |
| home     | home            | 홈 페이지 렌더링                            |
|          | searching       | 데이터 탐색, 탐색 페이지 렌더링             |
| accounts | signup          | 회원 가입 폼 렌더링, 회원 가입              |
|          | login           | 로그인 폼 렌더링, 로그인                    |
|          | logout          | 로그아웃                                    |
|          | profile         | 유저 프로필 렌더링                          |
|          | update          | 유저 정보 변경 폼 렌더링, 유저 정보 변경    |
|          | change_password | 비밀번호 변경 폼 렌더링, 비밀번호 변경      |
|          | kakao_login     | 카카오 로그인 진행                          |
|          | kakao_unlink    | 카카오 정보 삭제 진행                       |
|          | oauth           |                                             |
| articles | articles        | 커뮤니티 게시글 리스트 렌더링               |
|          | article_create  | 커뮤니티 게시글 폼 렌더링, 게시글 작성      |
|          | article_detail  | 커뮤니티 단일 게시글, 댓글, 댓글 폼 렌더링  |
|          | article_update  | 커뮤니티 게시글 수정 폼 렌더링, 게시글 수정 |
|          | article_delete  | 커뮤니티 게시글 삭제                        |
|          | article_like    | 커뮤니티 게시글 좋아요 (axios)              |
|          | comment_create  | 커뮤니티 댓글 작성                          |
|          | comment_update  | 커뮤니티 댓글 수정 폼 렌더링, 댓글 수정     |
|          | comment_delete  | 커뮤니티 댓글 삭제                          |
| movies   | movies          | 영화 목록 페이지네이션 렌더링               |
|          | movie_detail    | 단일 영화 렌더링                            |
|          | review_create   | 리뷰 작성                                   |
|          | review_update   | 리뷰 수정 폼 렌더링, 리뷰 수정              |
|          | review_delete   | 리뷰 삭제                                   |
|          | for_you         | 배우 관련 영화 추천                         |
|          | for_you2        | 장르 관련 영화 추천                         |
|          | for_you3        | 줄거리 관련 영화 추천                       |
|          |                 |                                             |



## 기능

### 0. nav

- home, community, movies로 이동하는 링크
- 로그인 전: 로그인, 회원가입 화면으로 이동하는 링크
- 로그인 후: 프로필, 로그아웃 화면으로 이동하는 링크

### 1 - 1. home

- 검색 기능 (관련 영화, 유튜브, 게시글, 유저)

### 1 - 2. search

- 검색 결과로 관련 유튜브, 영화, 게시글, 유저 출력
- 유튜브 영상 재생, 유튜브 영상 링크로 이동
- 관련 영화 정보 조회, 해당 영화 detail로 이동
- 관련 community 게시글 조회, 해당 게시글 detail로 이동
- 관련 유저 정보 조회, 해당 유저 profile로 이동

### 2 - 1. community

- 게시글 목록 테이블로 조회
- 각 게시글 번호, 좋아요 수, 제목, 댓글 수, 작성자, 작성일 확인
- 게시글 생성
- 제목을 눌러 햐덩 게시글 detail로 이동
- 작성자를 눌러 해당 작성자 profile로 이동

### 2 - 2. community detail

- 게시글 detail 조회
- 게시글 제목, 작성자, 작성일, 수정일, 내용 조회
- 게시글 수정, 삭제 (게시글 작성자만)
- 게시글 좋아요, 좋아요 수 확인
- 댓글 목록 조회
- 댓글 작성
- 댓글 수정, 삭제 (댓글 작성자만)

### 3 - 1. movies

- 영화 목록 조회
- 영화 포스터, 제목, 줄거리 조회
- 제목, 줄거리는 포스터 hover시 표현
- 포스터 클릭시 영화 detail로 이동
- 영화 목록 페이지네이션

### 3 - 2. movies detail

- 단일 영화 조회
- 제목, 장르, 리뷰 점수 평균, 포스터, 줄거리
- 유튜브, 관련 사진, 배우 사진 조회
- 유튜브 재생
- 리뷰, 평점 목록 조회
- 리뷰, 평점 작성
- 리뷰, 평점 수정, 삭제 (리뷰 작성자만)

### 3 - 3. movies for you

- 배우 관련 영화 추천
- 장르 관련 영화 추천
- 줄거리 관련 영화 추천

### 4. profile

- 회원 정보 표시
- 작성 글, 작성 댓글, 좋아요 글 출력
- 프로필 이미지

### 5. admin

- 영화, 유저, 게시글 관리 기능

### 6. accounts

- 로그인 없이 community detail, movies detail로 이동시 로그인 페이지로 리다이렉트
- 로그인, 로그아웃
- 회원가입
- 회원 정보 변경
- 비밀번호 변경
- 카카오 로그인, 카카오 정보 삭제



# 3. 데이터베이스 모델링 (ERD)

![Movie Project](README.assets/Movie Project.png)



### User

| 설명          | 필드 명         |
| ------------- | --------------- |
| 유저 이름     | username        |
| 비밀번호1     | password1       |
| 비밀번호2     | password2       |
| 이메일        | email           |
| 프로필 이미지 | profile_image   |
| 썸네일 이미지 | thumbnail_image |
| 생일          | birthday        |
| 성별          | gender          |
| 팔로잉        | followings      |

### Article

| 설명          | 필드 명    |
| ------------- | ---------- |
| 제목          | title      |
| 내용          | content    |
| 작성일        | created_at |
| 수정일        | updated_at |
| 좋아요한 유저 | like_users |
| 작성자        | user       |

### Comment

| 설명   | 필드 명    |
| ------ | ---------- |
| 내용   | content    |
| 작성일 | created_at |
| 수정일 | updated_at |
| 작성자 | user       |
| 게시글 | article    |

### Movie

| 설명   | 필드 명      |
| ------ | ------------ |
| 제목   | title        |
| 줄거리 | overview     |
| 포스터 | poster_path  |
| 장르   | genres       |
| 인기도 | popularity   |
| 감독   | director     |
| 배우   | actors       |
| 개봉일 | release_date |
| 청불   | adult        |

### Review

| 설명   | 필드 명    |
| ------ | ---------- |
| 내용   | content    |
| 평점   | rating     |
| 작성일 | created_at |
| 수정일 | updated_at |
| 작성자 | user       |
| 영화   | movie      |



# 4. 필수 기능에 대한 설명



# 겪었던 어려움들



# 5. 배포 서버 URL



# 6. 기타 (느낀 점)



