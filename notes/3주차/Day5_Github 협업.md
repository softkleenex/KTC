---

---

---
## Github 협업의 중요성

---
### Github 협업의 중요성

git : 내 컴퓨터에 설치하는 로컬 버전 관리도구(기록, 저장, 가지치기)
github: git 저장소를 온라인에 올려 팀원들과 함께 쓰는 협업 플랫폼

| **구분**      | **Git**                 | **GitHub**                    |
| ----------- | ----------------------- | ----------------------------- |
| **설치 및 위치** | 내 컴퓨터 (Local)           | ✓ **웹 플랫폼 (Cloud)**           |
| **주요 목적**   | 버전 관리 (Version Control) | ✓ **협업 및 공유 (Collaboration)** |
| **작업 형태**   | 터미널 명령어 (CLI)           | ✓ **시각적 웹 인터페이스 (GUI)**       |
| **핵심 가치**   | 코드를 안전하게 저장하자           | ✓ **팀원과 코드를 함께 만들자**          |
|             |                         |                               |
Branch : 커밋 그래프에 붙는 논리적 이름표(포인터). 여러 사람이 같은 프로젝트 안에서 서로의 작업에 영향을 주지 않고, 각자의 Branch에서 평행하게 작업 진행가능.

Repository: 프로젝트의 모든것을 담는 물리적 저장소

Pull Request: 각자의 Branch에서 완료된 작업을 main Branch에 합치기 전 거치는 필수 관문. 코드 리뷰의 핵심 도구, 팀원들에게 코드 설명, 피드백을 주고받는 중요한 소통의 장

ISSUE: 모든 논의를 기록, 추적한다. 누가, 어떤 문제를 언제까지 해결할 것인지 명확히 할당해 프로젝트의 진행상황 투명하게 관리.

Wiki: 신입 개발자가 들어왔을 때 가장 먼저 확인하는 프로젝트의 설명서. 개발 활경 셋업 가이드, 코딩 컨벤션, 아키텍처 구조 등 누가 와도 바로 프로젝트를 파악할 수 있도록 지식을 자산화 함.



---
### Github 저장소 생성


로컬 저장소와 원격 저장소는 동기화를 통해 상호 작용
1. 로컬 저장소에서 작업
2. `git add`와 `git commit`으로 변경 사항 저장
3. 완료된 작업을 원격 저장소로 푸시(`push`)
4. 원격 저장소의 최신 변경 사항을 풀(`pull`)하여 로컬 저장소와 동기화
5. 페치(`fetch`)를 통해 원격 저장소의 상태를 확인

git clone 하는 방법
git Repo의 code 버튼 클릭, HTTPS 옵션의 주소 복사.
목표 디렉토리로 이동 이후,  `$ git clone <repository_url>`으로 원격 저장소에 있는 git repo 복사.

현재 작업하던 폴더를 repo에 연결하려면
`git remote add origin <repository_url>`
내 컴퓨터에 저장되어있는 저장소와 원격 저장소를 연결하기 위해서 사용하는 명령어. 원격 저장소의 단축 이름을 origin으로 저장한다는 의미.


---
### 효율적인 협업을 위한 Collaborator

Collaborator 등록을 통해서 팀을 만들수있고, repository 를 직접 수정하거나, 웹상에서 commit ,push가 가능하다.(당연히 )

git 협업 중에는 최신 버전 유지를 위해서, remote repository의 변경 사항 로컬 적용은 필수이다. 따라서 작업 전에 반드시 Pull 이후에 작ㅇ버해야한다.

---
### Branch 전략과 Merge

주요 브랜치

|**브랜치 이름**|**설명**|
|---|---|
|**main(master)**|제품 출시 버전을 관리하는 브랜치|
|**develop**|다음 출시 버전을 개발하는 브랜치|
|**feature**|새로운 기능을 개발할 때 사용하는 브랜치|
|**release**|다음 출시 버전을 준비하는 브랜치|
|**hotfix**|긴급한 버그 수정이 필요할 때 사용하는 브랜치|
브랜치 흐름

|**단계**|**브랜치**|**핵심 역할**|**흐름**|
|---|---|---|---|
|**1**|develop|개발 최신 코드|시작|
|**2**|feature|기능 개발|develop → feature|
|**3**|feature 병합|기능 완료|feature → develop|
|**4**|release|릴리즈 준비|develop → release|
|**5**|release 병합|안정화|release → develop|
|**6**|main 배포|최종 릴리즈|develop → main|
|**7**|main|안정 코드|-|
|**8**|hotfix|긴급 수정|main → hotfix → main|

브랜치 네이밍 가이드
기본 규칙
- 소문자와 하이픈(-)만 사용함
- 공백과 특수문자는 사용하지 않음
- 브랜치 이름은 짧고 명확하게 작성함

유형 및 접두사(prefix)

|**유형**|**접두사 예시**|**설명**|
|---|---|---|
|**기능 개발**|feature/|새로운 기능 개발 시 사용|
|**버그 수정**|bugfix/|일반 버그 수정|
|**긴급 수정**|hotfix/|프로덕션 환경의 긴급 버그/보안 수정|
|**릴리즈 준비**|release/|릴리즈 버전 준비 및 QA|
|**실험 / 테스트**|experiment/|실험적 기능 개발|
|**문서 작업**|docs/|문서 수정 및 추가|

네이밍 패턴
- type : 브랜치 유형 접두사(feature, bugfix, hotfix, ...)
- short-description : 작업 내용을 간결하게 설명 (하이픈으로 구분)
- Issue-number : (선택) GitHub/Jira 등의 이슈 번호

병합(merge)
- 한 브랜치의 변경 사항을 다른 브랜치로 통합하는 과정을 의미함
- Git에서는 두 개의 브랜치를 하나로 합치는 작업을 수행할 때 이를 이용함
- 이러한 병합 과정을 통해서 프로젝트의 모든 구성원이 동일한 메인 코드베이스에서 작업할 수 있음

브랜치 병합 전략(branch merge strategy)
- GitHub에서 브랜치들을 메인 브랜치로 병합할 때 사용할 수 있는 규칙들을 의미함
- 각각의 전략은 서로 다른 장단점을 가지고 있어 프로젝트의 특성과 팀의 워크플로우에 따라 적절한 규칙을 선택해야 함
- 특히, 프로젝트의 소스코드 히스토리를 어떻게 관리할 것인지에 대한 팀의 합의가 중요함

| **병합 전략**                | **설명**                       | **커밋 히스토리** | **단점**               |
| ------------------------ | ---------------------------- | ----------- | -------------------- |
| **Merge Commit (기본 병합)** | 모든 커밋 히스토리를 보존하면서 병합하는 방식    | 유지됨         | 히스토리가 복잡해짐           |
| **Squash and Merge**     | 여러 커밋을 하나의 커밋으로 압축하여 병합하는 방식 | 압축됨         | 작업 세부 기록은 사라짐        |
| **Rebase and Merge**     | 커밋들을 베이스 브랜치 위로 재배치하는 선형적 방식 | 변형됨         | 충돌 발생 시 복잡, 커밋 해시 변경 |
|                          |                              |             |                      |


---
### Branch 생성과 Pull Request

**Branch** 생성

Git Branch 생성부터 Pull Request 만들기까지

1. 작업할 프로젝트 폴더로 이동
    

터미널에서 작업할 Git 저장소 폴더로 이동한다.

```bash
cd ~/projects/my-repo
```

현재 브랜치 확인

```bash
git branch
```

출력 결과에서 별표가 붙은 브랜치가 현재 내가 작업 중인 브랜치다.

```text
* main
```

2. 새 브랜치 만들고 바로 이동
    

새 기능이나 문서 수정은 main에서 바로 하지 않고, 별도 브랜치를 만들어 작업하는 게 좋다.

```bash
git switch -c feature/readme
```

위 명령어를 실행하면 현재 브랜치를 기준으로 feature/readme 브랜치가 생성되고, 동시에 그 브랜치로 이동한다.

예전 방식도 가능하다.

```bash
git checkout -b feature/readme
```

다시 브랜치를 확인하면 현재 위치가 바뀐 것을 볼 수 있다.

```bash
git branch
```

```text
  main
* feature/readme
```

브랜치 이름 예시

```text
feature/login
feature/readme
fix/header-bug
docs/update-readme
refactor/api-service
```

3. README 파일 열기
    

VSCode로 README 파일을 열려면 아래 명령어를 사용한다.

```bash
code README.md
```

또는 VSCode 파일 탐색기에서 README.md를 직접 눌러 열어도 된다.

README는 Markdown 문법으로 작성한다.

자주 쓰는 문법 예시

```text
제목: 큰 글씨 형태로 작성
강조: 별표 두 개 사이에 넣기
목록: 하이픈으로 시작
링크: 대괄호 안에 이름, 소괄호 안에 주소
```

예시 내용

```text
First Repository

Git과 GitHub 학습용 저장소입니다.

브랜치, Pull Request, merge 등 협업 기능을 실습합니다.
```

수정 후 저장

맥에서는 아래 단축키를 사용한다.

```text
Command + S
```

4. 변경사항 확인
    

파일을 수정하고 저장한 뒤 현재 상태를 확인한다.

```bash
git status
```

예시 출력

```text
On branch feature/readme
Changes not staged for commit:

  modified: README.md
```

modified는 기존 파일이 수정되었다는 뜻이다.

untracked는 Git이 아직 관리하지 않는 새 파일이라는 뜻이다.

현재 브랜치도 함께 표시되므로, main에서 작업 중인지 feature/readme에서 작업 중인지 확인할 수 있다.

5. 실제 변경 내용 보기
    

이전 커밋과 비교해서 무엇이 바뀌었는지 확인한다.

```bash
git diff
```

예시

```diff
- Project
+ My Project
```

빨간 줄 또는 마이너스는 삭제된 내용이다.

초록 줄 또는 플러스는 추가된 내용이다.

6. 변경사항 스테이징
    

커밋할 파일을 선택해서 스테이징 영역에 올린다.

```bash
git add README.md
```

현재 변경된 파일을 전부 올리고 싶으면 아래를 사용한다.

```bash
git add .
```

스테이징 후 다시 확인한다.

```bash
git status
```

7. 커밋 만들기
    

변경사항을 로컬 저장소 기록으로 남긴다.

```bash
git commit -m "docs: update README title"
```

커밋 메시지는 무엇을 수정했는지 짧고 명확하게 적는다.

예시

```text
docs: update README title
feat: add login page
fix: resolve button alignment
refactor: clean up API service
```

커밋은 아직 내 컴퓨터의 로컬 브랜치에만 저장된 상태다. GitHub에는 아직 올라가지 않았다.

8. 원격 저장소 확인
    

현재 연결된 GitHub 저장소를 확인한다.

```bash
git remote -v
```

예시

```text
origin  https://github.com/team/repo.git
```

origin은 보통 GitHub 원격 저장소를 가리키는 기본 이름이다.

9. 브랜치를 GitHub에 올리기
    

처음 만든 브랜치를 원격 저장소에 올릴 때는 아래 명령어를 사용한다.

```bash
git push -u origin feature/readme
```

이 명령어는 내 로컬 feature/readme 브랜치를 GitHub의 feature/readme 브랜치로 업로드한다.

-u 옵션은 로컬 브랜치와 원격 브랜치를 연결해준다.

한 번 연결하고 나면 이후에는 브랜치 이름을 안 적고 아래처럼 쓸 수 있다.

```bash
git push
```

GitHub에서 최신 내용을 받아올 때도 간단하게 쓸 수 있다.

```bash
git pull
```

10. Pull Request 만들기
    

브랜치를 처음 push하면 터미널에 Pull Request 생성 링크가 나오는 경우가 많다.

그 링크를 열거나 GitHub 저장소 페이지에서 Compare & pull request 버튼을 누른다.

Pull Request 작성 시 확인할 것

```text
base 브랜치: 보통 main
compare 브랜치: 내가 작업한 feature/readme
제목: 무엇을 수정했는지 간단히 작성
내용: 변경한 이유와 작업 내용을 작성
```

예시

```text
제목
README 제목 수정

내용
README의 프로젝트 제목을 더 명확하게 수정했습니다.
```

전체 흐름

```bash
cd ~/projects/my-repo

git branch

git switch -c feature/readme

code README.md

git status

git diff

git add README.md

git commit -m "docs: update README title"

git push -u origin feature/readme
```

핵심 구분

```text
브랜치 생성
작업 공간을 따로 만드는 것

파일 수정
실제 코드나 문서를 바꾸는 것

git add
커밋할 변경사항을 선택하는 것

git commit
내 컴퓨터 Git 기록에 저장하는 것

git push
GitHub 원격 저장소에 업로드하는 것

Pull Request
내 브랜치 변경사항을 main에 합쳐달라고 요청하는 것
```

Branch 생성은 내용은 같지만 따로 존재하는 remote reposity를 각자 직접 수정, 통합하는것. 각각의 개발자는 본인의 Repository를 수정하므로 서로의 수정 내용이 반영되지않는다.
이 둘을 동기화 하는것이 Pull Request와 Merge. 복사본에서 통합 요청을 하는것이 Pull Request(PR)이다. 

**Pull Request**
복사본에서 통합 요청을 하는것. 이를 승인시에 Merge되어 원본 또한 변경된다.





---
### 충돌 해결하기

**Git 충돌 해결**

Git은 대부분의 변경사항을 자동으로 합쳐준다.

하지만 같은 파일의 같은 부분을 여러 브랜치에서 다르게 수정하면 Git은 어떤 코드를 남겨야 할지 결정할 수 없다.

이때 발생하는 것이 충돌(Merge Conflict)이다.

---

**충돌이 발생하는 경우**

**같은 줄을 동시에 수정**

main 브랜치와 feature 브랜치가 같은 파일의 같은 줄을 각각 수정한 경우

Git은 어느 내용을 남겨야 할지 알 수 없다.

**삭제 vs 수정**

한 브랜치에서는 파일을 삭제하고

다른 브랜치에서는 같은 파일을 수정한 경우

삭제해야 하는지 유지해야 하는지 판단할 수 없다.

**대규모 리팩토링**

함수 이동

파일 이동

구조 변경

코드 정리 등이 겹치면 충돌이 발생할 수 있다.

---

**브랜치 전환 시 자주 하는 실수**

작업 중인데 다른 브랜치로 이동하려고 하는 경우

```
git switch other-branch
```

```
error: Your local changes would be overwritten by checkout
```

Git은 현재 작업 내용이 사라질 위험이 있으면 브랜치 전환을 막는다.

---

**해결 방법 1 - 커밋 후 이동**

```
git add .git commit -m "wip: 작업 중"git switch other-branch
```

장점

- 가장 안전함
- 히스토리가 남음
- 복구 쉬움

---

**해결 방법 2 - Stash 사용**

```
git stashgit switch other-branch
```

돌아왔을 때

```
git stash pop
```

장점

- 임시 저장 가능
- 빠르게 브랜치 이동 가능

---

**브랜치 이동 전 습관**

```
git status
```

확인할 것

- 수정된 파일이 있는가
- 스테이징된 파일이 있는가
- 커밋되지 않은 작업이 있는가

Git에서 가장 많이 보는 명령어 중 하나.

---

**VSCode에서 충돌 해결**

충돌 파일을 열면 Merge Editor가 나타난다.

---

**3-Way Merge Editor**

**Current**

현재 브랜치

내가 작업한 코드

---

**Incoming**

병합하려는 브랜치

상대방 코드

---

**Result**

최종 결과

실제로 저장되는 코드

결국 가장 중요한 영역은 Result

---

**VSCode 충돌 해결 옵션**

**Accept Current Change**

내 변경만 유지

상대 변경은 버림

---

**Accept Incoming Change**

상대 변경만 유지

내 변경은 버림

---

**Accept Both Changes**

양쪽 변경 모두 유지

중복 코드나 순서 문제는 직접 정리해야 함

---

**Compare Changes**

좌우 비교 화면 열기

변경사항을 보면서 직접 수정 가능

---

**충돌 마커 읽기**

Git은 충돌이 발생하면 파일 안에 마커를 삽입한다.

```
<<<<<<< HEADconsole.log("내 코드");=======console.log("상대 코드");>>>>>>> feature/login
```

---

**<<<<<<< HEAD**

현재 브랜치 코드 시작

---

**=======**

두 변경사항을 나누는 구분선

---

**>>>>>>> feature/login**

상대 브랜치 코드 끝

---

**충돌 해결 순서**

충돌 발생

↓

충돌 파일 열기

↓

Current / Incoming 확인

↓

Accept 또는 직접 수정

↓

저장

↓

```
git add .
```

↓

```
git commit
```

↓

병합 완료

---

**실무에서 기억할 것**

충돌은 오류가 아니다.

Git이 자동으로 결정하지 못해서 사람에게 판단을 요청하는 상태다.

Current = 내 코드

Incoming = 상대 코드

Result = 최종 결과

브랜치 전환 전에는 항상

```
git status
```

습관적으로 확인하기.

충돌을 해결하는 기준은

"누가 맞는가?"

가 아니라

"최종적으로 어떤 코드가 남아야 하는가?"

이다.



---
### Git LFS 개념 및 활용 방법


**Git LFS (Large File Storage)**

Git이 효율적으로 관리하지 못하는 대용량 파일을 위한 공식 확장 기능.

일반 Git은 텍스트 파일 관리에 최적화되어 있지만 이미지, 영상, PSD, 모델링 파일 같은 바이너리 파일은 비효율적으로 저장된다.

Git LFS는 실제 파일 대신 **포인터(Pointer) 파일**만 Git에 저장하고, 원본 파일은 별도 LFS 서버에 저장한다.



**왜 필요한가?**

기존 Git은 커밋마다 Snapshot을 저장한다.

텍스트 파일은 변경된 부분만 추적하므로 효율적이다.

하지만 이미지, 영상, 압축파일 같은 바이너리 파일은 작은 수정이 발생해도 Git 입장에서는 새로운 파일로 인식한다.

결과적으로

- 저장소 크기 증가
- Clone 속도 저하
- Push/Pull 시간 증가
- 불필요한 히스토리 공유

문제가 발생한다.



**Git LFS 동작 방식**

일반 Git

```
Git Repository ├─ code ├─ code └─ movie.mp4
```

Git LFS

```
Git Repository ├─ code ├─ code └─ movie.mp4 (Pointer)LFS Server └─ movie.mp4 (실제 파일)
```

즉

Git → 파일 위치 정보 저장

LFS → 실제 파일 저장



**Pointer 파일이란?**

실제 파일 대신 저장되는 작은 텍스트 파일

예시

```
version https://git-lfs.github.com/spec/v1oid sha256:xxxxxxxxxxxxxxxxsize 123456789
```

포함 정보

- 파일 해시값
- 파일 크기
- 파일 식별 정보

실제 파일 데이터는 포함하지 않는다.



**Git LFS의 장점**

**저장소 크기 감소**

대용량 파일 자체가 Git에 저장되지 않음



**Clone 속도 향상**

필요한 파일만 내려받음



**Git 워크플로우 유지**

기존 Git 명령어 그대로 사용

```
git addgit commitgit pushgit pull
```



**대용량 파일 버전 관리 가능**

GB 단위 파일도 추적 가능



**협업 효율 향상**

모든 사용자가 불필요한 대용량 파일 히스토리를 받지 않아도 됨



**설치**

Mac

```
brew install git-lfsgit lfs install
```

Windows

```
winget install git-lfsgit lfs install
```

또는

```
choco install git-lfsgit lfs install
```

Linux

```
sudo apt-get updatesudo apt-get install git-lfsgit lfs install
```



**파일 추적 시작**

PSD 파일 추적

```
git lfs track "*.psd"
```

영상 파일 추적

```
git lfs track "*.mp4"
```

Zip 파일 추적

```
git lfs track "*.zip"
```



추적 후 생성되는 파일

```
.gitattributes
```

예시

```
*.psd filter=lfs diff=lfs merge=lfs -text*.mp4 filter=lfs diff=lfs merge=lfs -text
```



**Git LFS 사용 흐름**

추적 설정

```
git lfs track "*.psd"
```

↓

커밋

```
git add .git commit -m "add design files"
```

↓

Push

```
git push origin main
```

↓

Git 저장소

```
Pointer 파일 저장
```

↓

LFS 서버

```
실제 PSD 파일 저장
```



**자주 사용하는 명령어**

현재 추적 중인 파일 확인

```
git lfs track
```



LFS 파일 목록 확인

```
git lfs ls-files
```



LFS 파일 다운로드

```
git lfs pull
```



파일만 미리 가져오기

```
git lfs fetch
```



체크아웃

```
git lfs checkout
```



캐시 정리

```
git lfs prune
```



**실무 활용 사례**

게임 개발

```
.psd.fbx.unitypackage.mp4.wav
```



AI 프로젝트

```
.pt.pth.ckpt.onnx
```



디자인 협업

```
.psd.ai.sketch.fig
```



데이터 분석

```
.csv.parquet.zip
```



**Git LFS vs Submodule vs Git-annex**

Git LFS

- 사용 쉬움
- 협업 친화적
- Git 워크플로우 유지
- 가장 많이 사용

Submodule

- 다른 저장소 연결 목적
- 대용량 파일 관리 용도 아님

Git-annex

- 매우 강력
- 사용 복잡
- 협업 난이도 높음

실무에서는 대부분 Git LFS 선택



**사용 시 주의사항**

모든 팀원이 설치 필요

```
git lfs install
```



Git 서버가 LFS 지원해야 함

대표 지원 서비스

- GitHub
- GitLab
- Bitbucket



스토리지 및 트래픽 제한 존재

특히 GitHub LFS는

- 저장 용량
- 다운로드 트래픽

제한이 있음



CI/CD 환경에서도 설치 필요

예시

```
git lfs pull
```

없으면 빌드 서버에서 파일을 찾지 못할 수 있음



**한 줄 요약**

Git LFS는 대용량 파일을 Git 밖의 LFS 서버에 저장하고, Git에는 포인터만 남겨 저장소 크기와 협업 비용을 줄여주는 Git의 공식 대용량 파일 관리 솔루션이다.




---
### 고급 Git 기능

**고급 Git 기능**

Git을 어느 정도 사용하다 보면 단순한 `add → commit → push`만으로는 해결되지 않는 상황이 생긴다.

이때 사용하는 대표적인 고급 기능

- Stash
    
- Cherry-pick
    
- Rebase
    
- Reflog
    
- Bisect
    
- Tag
    

◈ ◈ ◈

**Git Stash**

작업 중인 변경사항을 임시 저장하는 기능

커밋하기 애매한 상태에서 브랜치를 이동해야 할 때 사용한다.

대표 상황

- 작업 도중 긴급 수정 요청 발생
    
- 브랜치 전환 필요
    
- 작업 내용은 유지해야 함
    

주요 명령어

```bash
git stash
```

현재 작업 임시 저장

```bash
git stash list
```

저장된 Stash 목록 확인

```bash
git stash apply
```

최근 Stash 복원

(Stash 유지)

```bash
git stash pop
```

최근 Stash 복원

(Stash 삭제)

실무 팁

`apply`는 안전하게 복원

`pop`은 복원 후 자동 삭제

◈ ◈ ◈

**Git Cherry-pick**

특정 커밋만 골라서 다른 브랜치에 적용하는 기능

브랜치 전체를 Merge하지 않고 필요한 커밋만 가져올 수 있다.

대표 상황

- 긴급 Hotfix 적용
    
- 운영 브랜치에 특정 수정만 반영
    
- 다른 브랜치의 특정 기능 재사용
    

예시

```bash
git cherry-pick <commit-hash>
```

예시

```bash
git cherry-pick a1b2c3d
```

결과

```text
feature 브랜치
 ├─ commit A
 ├─ commit B
 └─ commit C

main 브랜치
 └─ cherry-pick(commit B)
```

특정 커밋만 가져온다.

◈ ◈ ◈

**Git Rebase**

브랜치를 최신 기준으로 다시 정렬하는 기능

Merge와 달리 불필요한 Merge Commit을 만들지 않는다.

기존

```text
main
 └─ A ─ B

feature
       └─ C ─ D
```

Rebase 후

```text
main
 └─ A ─ B ─ C ─ D
```

장점

- 히스토리가 깔끔함
    
- 선형 구조 유지
    
- Commit 흐름 파악 쉬움
    

명령어

```bash
git rebase main
```

주의

이미 공유된 브랜치에서는 신중하게 사용

Commit Hash가 변경된다.

실무에서는

```bash
git pull --rebase
```

를 자주 사용한다.

◈ ◈ ◈

**Git Reflog**

Git의 타임머신

HEAD가 이동한 모든 기록을 저장한다.

실수로 삭제한 커밋이나 브랜치를 복구할 때 사용한다.

명령어

```bash
git reflog
```

예시

```text
HEAD@{0}
HEAD@{1}
HEAD@{2}
HEAD@{3}
```

복구

```bash
git reset --hard HEAD@{2}
```

대표 상황

- 잘못된 reset
    
- 잘못된 rebase
    
- 삭제한 브랜치 복구
    
- 잃어버린 Commit 찾기
    

실무에서는

"망했을 때 마지막 희망"

이라고 불린다.

◈ ◈ ◈

**Git Bisect**

버그가 발생한 Commit을 찾는 기능

이진 탐색(Binary Search)을 사용한다.

커밋이 수백 개여도 빠르게 원인을 찾을 수 있다.

시작

```bash
git bisect start
```

정상 버전 지정

```bash
git bisect good
```

문제 버전 지정

```bash
git bisect bad
```

Git이 중간 Commit으로 이동

테스트 후

```bash
git bisect good
```

또는

```bash
git bisect bad
```

반복

결과

버그를 만든 Commit을 자동 탐색

대표 상황

- 대규모 프로젝트
    
- 원인 불명 버그
    
- 최근 수정사항이 많은 경우
    

◈ ◈ ◈

**Git Tag**

특정 Commit에 버전 이름을 붙이는 기능

주로 릴리즈 버전 관리에 사용한다.

예시

```text
v1.0.0
v1.1.0
v2.0.0
```

명령어

```bash
git tag v1.0.0
```

태그 생성

```bash
git push origin v1.0.0
```

원격 저장소 업로드

활용

- 릴리즈 관리
    
- 배포 기준점 지정
    
- 버전 기록 관리
    

실무에서는

```text
v1.0.0
v1.1.0
v1.2.0
v2.0.0
```

형태의 Semantic Versioning을 많이 사용한다.

◈ ◈ ◈

**언제 사용하는가?**

|상황|사용하는 기능|
|---|---|
|작업 중 브랜치 이동|Stash|
|특정 커밋만 가져오기|Cherry-pick|
|히스토리 정리|Rebase|
|실수 복구|Reflog|
|버그 원인 추적|Bisect|
|릴리즈 버전 관리|Tag|

◈ ◈ ◈

**한 줄 요약**

Stash = 임시 보관소

Cherry-pick = 특정 커밋 복사

Rebase = 히스토리 정리

Reflog = Git 타임머신

Bisect = 버그 탐정

Tag = 릴리즈 버전 표시기