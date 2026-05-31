/**
 * ============================================================================
 * Minimalist Todo Web Application Script (Expanded Version)
 * ----------------------------------------------------------------------------
 * 상태별 필터링, 일간 이동 기능, 주간 뷰 캘린더, 로컬스토리지 연동 기능을 
 * 모두 포함한 고기능 미니멀 생산성 웹 애플리케이션 스크립트입니다.
 * ============================================================================
 */

// ----------------------------------------------------------------------------
// 1. 애플리케이션 상태 (State) 및 기획 설정
// ----------------------------------------------------------------------------
// 할 일 데이터 배열. 각 객체 구조: { id: number, text: string, completed: boolean, date: "YYYY-MM-DD" }
let todoItemsState = [];

// 사용자 지정 선택 날짜 (기본값: 오늘 날짜)
let selectedDate = new Date();

// 주간 뷰에 노출되는 주의 '월요일' 날짜 객체
let currentWeekMonday = new Date();

// 현재 설정된 필터 상태 ('all' | 'active' | 'completed')
let selectedFilter = 'all';

// 수정 중인 할 일 항목의 ID (null일 때 수정 모드 아님)
let editingTodoId = null;

// 상수 정의
const LOCAL_STORAGE_KEY = 'MINIMAL_TODOS';
const dayNamesKorean = ['일', '월', '화', '수', '목', '금', '토'];

// ----------------------------------------------------------------------------
// 2. DOM 요소 선택 (DOM Elements)
// ----------------------------------------------------------------------------
const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');
const errorMessage = document.getElementById('error-message');
const emptyState = document.getElementById('empty-state');

// 날짜 제어 DOM 요소들
const weekTitle = document.getElementById('week-title');
const selectedDateText = document.getElementById('selected-date-text');
const btnPrevWeek = document.getElementById('btn-prev-week');
const btnNextWeek = document.getElementById('btn-next-week');
const btnPrevDay = document.getElementById('btn-prev-day');
const btnNextDay = document.getElementById('btn-next-day');
const btnToday = document.getElementById('btn-today');
const filterTabs = document.querySelectorAll('.filter-tab');

// ----------------------------------------------------------------------------
// 3. 날짜 계산 및 문자열 포맷팅 헬퍼 함수
// ----------------------------------------------------------------------------

/**
 * 특정 날짜가 속한 주의 월요일 날짜 객체를 구해 반환합니다.
 * @param {Date} date - 기준 날짜
 * @returns {Date} 해당 주의 월요일 날짜 객체
 */
function getMondayOfDate(date) {
  const targetDate = new Date(date);
  const dayIndex = targetDate.getDay(); // 0(일) ~ 6(토)
  
  // 월요일을 기준으로 가감해야 할 일수 계산
  // 일요일(0)일 경우 이전 주 월요일로 가지 않도록 뒤로 6일 이동, 나머지는 (요일 index - 1)만큼 뒤로 이동
  const diffDays = targetDate.getDate() - dayIndex + (dayIndex === 0 ? -6 : 1);
  return new Date(targetDate.getFullYear(), targetDate.getMonth(), diffDays);
}

/**
 * Date 객체를 "YYYY-MM-DD" 형태의 로컬 문자열로 포맷팅합니다.
 * @param {Date} date - 날짜 객체
 * @returns {string} YYYY-MM-DD 형식 문자열
 */
function formatDateToString(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Date 객체를 한국어 전체 날짜 포맷("YYYY년 M월 D일 (요일)")으로 포맷팅합니다.
 * @param {Date} date - 날짜 객체
 * @returns {string} 포맷팅된 한국어 날짜 텍스트
 */
function formatDateToKoreanString(date) {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const dayName = dayNamesKorean[date.getDay()];
  return `${year}년 ${month}월 ${day}일 (${dayName})`;
}

/**
 * 주간 뷰 상단의 타이틀 연월 정보를 반환합니다.
 * @param {Date} mondayDate - 주의 월요일 날짜 객체
 * @returns {string} 연월 표시 텍스트
 */
function formatWeekTitleString(mondayDate) {
  const year = mondayDate.getFullYear();
  const month = mondayDate.getMonth() + 1;
  return `${year}년 ${month}월`;
}

/**
 * 선택된 날짜에 맞추어 주간 캘린더의 시작 월요일을 자동으로 동기화합니다.
 */
function syncWeeklyViewWithSelectedDate() {
  currentWeekMonday = getMondayOfDate(selectedDate);
}

// ----------------------------------------------------------------------------
// 4. 로컬스토리지 연동 데이터 입출력
// ----------------------------------------------------------------------------

/**
 * 로컬스토리지로부터 저장되어 있는 할 일 목록 데이터를 파싱하여 불러옵니다.
 */
function loadTodosFromLocalStorage() {
  try {
    const rawData = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (rawData) {
      todoItemsState = JSON.parse(rawData);
    } else {
      todoItemsState = [];
    }
  } catch (error) {
    console.error('로컬스토리지 데이터를 파싱하는 중 오류가 발생했습니다.', error);
    todoItemsState = [];
  }
}

/**
 * 현재 할 일 목록 상태(State)를 JSON 문자열로 직렬화하여 로컬스토리지에 저장합니다.
 */
function saveTodosToLocalStorage() {
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(todoItemsState));
  } catch (error) {
    console.error('로컬스토리지에 데이터를 저장하는 데 실패했습니다.', error);
  }
}

// ----------------------------------------------------------------------------
// 5. 애플리케이션 초기화 (Initialization)
// ----------------------------------------------------------------------------
function initializeApp() {
  // 로컬스토리지 데이터 로드
  loadTodosFromLocalStorage();

  // 초기 날짜 동기화
  syncWeeklyViewWithSelectedDate();

  // 이벤트 바인딩
  todoForm.addEventListener('submit', handleAddTodo);
  todoInput.addEventListener('input', handleInputChange);
  
  // 일간 이동 및 캘린더 탐색 이벤트 바인딩
  btnPrevDay.addEventListener('click', navigateToPreviousDay);
  btnNextDay.addEventListener('click', navigateToNextDay);
  btnToday.addEventListener('click', navigateToToday);
  btnPrevWeek.addEventListener('click', navigateToPreviousWeek);
  btnNextWeek.addEventListener('click', navigateToNextWeek);

  // 상태 필터 탭 이벤트 바인딩
  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // 기존 활성화 클래스 제거 및 새 클래스 부여
      filterTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      selectedFilter = tab.dataset.filter;
      editingTodoId = null;
      hideInputValidationError();
      renderTodoApp();
    });
  });

  // 초기 전체 렌더링
  renderTodoApp();
}

// ----------------------------------------------------------------------------
// 6. 날짜 및 탭 이동 핸들러
// ----------------------------------------------------------------------------

function navigateToPreviousDay() {
  selectedDate.setDate(selectedDate.getDate() - 1);
  syncWeeklyViewWithSelectedDate();
  resetTemporaryStates();
  renderTodoApp();
}

function navigateToNextDay() {
  selectedDate.setDate(selectedDate.getDate() + 1);
  syncWeeklyViewWithSelectedDate();
  resetTemporaryStates();
  renderTodoApp();
}

function navigateToToday() {
  selectedDate = new Date();
  syncWeeklyViewWithSelectedDate();
  resetTemporaryStates();
  renderTodoApp();
}

function navigateToPreviousWeek() {
  currentWeekMonday.setDate(currentWeekMonday.getDate() - 7);
  renderTodoApp();
}

function navigateToNextWeek() {
  currentWeekMonday.setDate(currentWeekMonday.getDate() + 7);
  renderTodoApp();
}

/**
 * 캘린더나 날짜 변경 시 동작하는 에러/수정 모드 클리어 함수
 */
function resetTemporaryStates() {
  editingTodoId = null;
  hideInputValidationError();
}

// ----------------------------------------------------------------------------
// 7. 입력 폼 제어 및 검증
// ----------------------------------------------------------------------------

function handleInputChange() {
  if (todoInput.value.trim().length > 0) {
    hideInputValidationError();
  }
}

function showInputValidationError(message) {
  errorMessage.textContent = message;
  errorMessage.classList.add('visible');
}

function hideInputValidationError() {
  errorMessage.textContent = '';
  errorMessage.classList.remove('visible');
}

// ----------------------------------------------------------------------------
// 8. CRUD 비즈니스 로직
// ----------------------------------------------------------------------------

/**
 * [CREATE] 현재 선택된 날짜와 함께 새로운 Todo 항목을 추가합니다.
 */
function handleAddTodo(event) {
  event.preventDefault();
  
  const textValue = todoInput.value.trim();

  // 빈 내용 검증
  if (!textValue) {
    showInputValidationError('할 일을 입력해주세요.');
    todoInput.focus();
    return;
  }

  // 할 일 객체 생성 시, 선택된 날짜 문자열 저장 ("YYYY-MM-DD")
  const newTodoItem = {
    id: Date.now(),
    text: textValue,
    completed: false,
    date: formatDateToString(selectedDate)
  };

  todoItemsState.push(newTodoItem);
  
  // 로컬스토리지에 최신 상태 영속화
  saveTodosToLocalStorage();
  
  // 폼 및 안내 초기화
  todoInput.value = '';
  hideInputValidationError();
  
  renderTodoApp();
}

/**
 * [DELETE] 특정 할 일을 ID 기준으로 상태에서 영구 삭제합니다.
 */
function deleteTodoItem(todoId) {
  todoItemsState = todoItemsState.filter(todo => todo.id !== todoId);
  
  if (editingTodoId === todoId) {
    editingTodoId = null;
  }

  saveTodosToLocalStorage();
  renderTodoApp();
}

/**
 * [UPDATE - 완료 상태 변경] 할 일의 진행 상태를 전환합니다.
 */
function toggleTodoCompletionState(todoId) {
  todoItemsState = todoItemsState.map(todo => {
    if (todo.id === todoId) {
      return { ...todo, completed: !todo.completed };
    }
    return todo;
  });
  
  saveTodosToLocalStorage();
  renderTodoApp();
}

/**
 * [UPDATE - 수정 모드 시작] 해당 할 일을 텍스트 편집 모드로 바꿉니다.
 */
function enterTodoEditMode(todoId) {
  editingTodoId = todoId;
  hideInputValidationError();
  renderTodoApp();
}

/**
 * [UPDATE - 저장] 수정한 텍스트 데이터를 저장하고 로컬스토리지와 렌더링에 동기화합니다.
 */
function saveEditedTodoText(todoId, updatedText) {
  const trimmedText = updatedText.trim();
  
  if (!trimmedText) {
    showInputValidationError('할 일 내용은 비어 둘 수 없습니다.');
    return;
  }

  todoItemsState = todoItemsState.map(todo => {
    if (todo.id === todoId) {
      return { ...todo, text: trimmedText };
    }
    return todo;
  });
  
  editingTodoId = null;
  hideInputValidationError();
  
  saveTodosToLocalStorage();
  renderTodoApp();
}

/**
 * [UPDATE - 취소] 텍스트 수정 사항을 버리고 일반 모드로 복귀합니다.
 */
function cancelTodoEditMode() {
  editingTodoId = null;
  hideInputValidationError();
  renderTodoApp();
}

// ----------------------------------------------------------------------------
// 9. UI 동적 렌더링 제어
// ----------------------------------------------------------------------------

/**
 * 주간 캘린더 그리드를 그려내고 날짜 선택 상호작용을 처리합니다.
 */
function renderWeeklyCalendar() {
  const gridContainer = document.getElementById('weekly-days-grid');
  gridContainer.innerHTML = '';

  const mondayPointer = new Date(currentWeekMonday);
  const selectedDateStr = formatDateToString(selectedDate);
  const todayStr = formatDateToString(new Date());

  // 월요일(0)부터 일요일(6)까지 순서대로 7개 칸을 그림
  for (let i = 0; i < 7; i++) {
    const cellDate = new Date(mondayPointer);
    cellDate.setDate(mondayPointer.getDate() + i);

    const cellDateStr = formatDateToString(cellDate);

    // 날짜별 셀 컨테이너 DOM 생성
    const dayCell = document.createElement('div');
    dayCell.className = 'weekly-day-cell';
    dayCell.dataset.day = cellDate.getDay();

    // 상태 구분에 따른 동적 클래스 세팅
    if (cellDateStr === selectedDateStr) {
      dayCell.classList.add('selected');
    }
    if (cellDateStr === todayStr) {
      dayCell.classList.add('today');
    }

    // 요일 한글 텍스트 컴포넌트
    const dayNameSpan = document.createElement('span');
    dayNameSpan.className = 'weekly-day-name';
    dayNameSpan.textContent = dayNamesKorean[cellDate.getDay()];

    // 날짜 숫자 텍스트 컴포넌트
    const dayNumberSpan = document.createElement('span');
    dayNumberSpan.className = 'weekly-day-number';
    dayNumberSpan.textContent = cellDate.getDate();

    // 날짜 하단의 할 일 갯수 배지 계산 (해당 날짜에 해당하는 모든 Todo 개수)
    const taskCountForDay = todoItemsState.filter(todo => todo.date === cellDateStr).length;
    const taskBadge = document.createElement('span');
    taskBadge.className = 'weekly-day-badge';
    
    if (taskCountForDay > 0) {
      taskBadge.classList.add('has-tasks');
      taskBadge.textContent = taskCountForDay;
    } else {
      taskBadge.textContent = '0';
    }

    dayCell.appendChild(dayNameSpan);
    dayCell.appendChild(dayNumberSpan);
    dayCell.appendChild(taskBadge);

    // 셀 클릭 이벤트 - 날짜 변경 처리
    dayCell.addEventListener('click', () => {
      selectedDate = cellDate;
      resetTemporaryStates();
      renderTodoApp();
    });

    gridContainer.appendChild(dayCell);
  }
}

/**
 * 필터와 선택 날짜에 맞춰 리스트 뷰 및 빈 화면(Empty State)을 업데이트합니다.
 * @param {Array} filteredList - 필터링이 완료된 실제 출력 Todo 배열
 * @param {number} totalCountForDate - 선택 날짜의 상태 무관 총 할 일 개수
 */
function updateTodoListVisibility(filteredList, totalCountForDate) {
  if (filteredList.length === 0) {
    emptyState.classList.add('visible');
    todoList.style.display = 'none';
    
    const emptyStateText = document.getElementById('empty-state-text');
    
    if (totalCountForDate === 0) {
      emptyStateText.textContent = '이 날짜에 계획된 할 일이 없습니다. 새로운 계획을 추가해보세요!';
    } else if (selectedFilter === 'active') {
      emptyStateText.textContent = '이 날짜에 계획한 모든 할 일을 성공적으로 끝마쳤습니다! 🎉';
    } else if (selectedFilter === 'completed') {
      emptyStateText.textContent = '이 날짜에 완료된 할 일이 존재하지 않습니다.';
    } else {
      emptyStateText.textContent = '해당 필터에 일치하는 할 일이 존재하지 않습니다.';
    }
  } else {
    emptyState.classList.remove('visible');
    todoList.style.display = 'flex';
  }
}

/**
 * 애플리케이션의 전체 화면(주간 달력, 일간 상태 헤더, 투두 항목 목록)을 재배치 및 렌더링합니다.
 */
function renderTodoApp() {
  // 1. 상단 주간 정보 헤더 업데이트
  weekTitle.textContent = formatWeekTitleString(currentWeekMonday);
  
  // 2. 주간 캘린더 그리드 렌더링
  renderWeeklyCalendar();
  
  // 3. 일간 상태 뷰 날짜 헤더 표시
  selectedDateText.textContent = formatDateToKoreanString(selectedDate);
  
  // 4. Todo 리스트 항목 DOM 갱신
  todoList.innerHTML = '';
  
  const selectedDateStr = formatDateToString(selectedDate);
  
  // 선택된 날짜에 매핑된 할 일들만 1차 분류
  const dateSpecificTodos = todoItemsState.filter(todo => todo.date === selectedDateStr);
  
  // 선택 탭 필터링 기준에 맞춘 2차 분류
  let finalFilteredTodos = [];
  if (selectedFilter === 'all') {
    finalFilteredTodos = dateSpecificTodos;
  } else if (selectedFilter === 'active') {
    finalFilteredTodos = dateSpecificTodos.filter(todo => !todo.completed);
  } else if (selectedFilter === 'completed') {
    finalFilteredTodos = dateSpecificTodos.filter(todo => todo.completed);
  }

  // 필터링 적용된 할 일들을 DOM 요소로 생성하여 추가
  finalFilteredTodos.forEach(todo => {
    const isCurrentlyEditing = editingTodoId === todo.id;
    
    const listItem = document.createElement('li');
    listItem.className = `todo-item ${todo.completed ? 'completed' : ''}`;
    
    // [좌측 영역]
    const itemLeftContainer = document.createElement('div');
    itemLeftContainer.className = 'todo-item-left';
    
    if (isCurrentlyEditing) {
      const textEditInput = document.createElement('input');
      textEditInput.type = 'text';
      textEditInput.className = 'todo-edit-input';
      textEditInput.value = todo.text;
      
      // 즉각적인 포커스 이동 처리
      setTimeout(() => {
        textEditInput.focus();
        const valueLength = textEditInput.value.length;
        textEditInput.setSelectionRange(valueLength, valueLength);
      }, 0);

      textEditInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
          saveEditedTodoText(todo.id, textEditInput.value);
        } else if (event.key === 'Escape') {
          cancelTodoEditMode();
        }
      });
      
      itemLeftContainer.appendChild(textEditInput);
    } else {
      // 커스텀 체크박스
      const checkboxLabel = document.createElement('label');
      checkboxLabel.className = 'checkbox-container';
      
      const realCheckbox = document.createElement('input');
      realCheckbox.type = 'checkbox';
      realCheckbox.checked = todo.completed;
      realCheckbox.addEventListener('change', () => toggleTodoCompletionState(todo.id));
      
      const customCheckmark = document.createElement('span');
      customCheckmark.className = 'checkmark';
      
      checkboxLabel.appendChild(realCheckbox);
      checkboxLabel.appendChild(customCheckmark);
      
      // 할 일 텍스트
      const textDisplay = document.createElement('span');
      textDisplay.className = 'todo-text';
      textDisplay.textContent = todo.text;
      
      itemLeftContainer.appendChild(checkboxLabel);
      itemLeftContainer.appendChild(textDisplay);
    }
    
    // [우측 제어 버튼 영역]
    const itemActionsContainer = document.createElement('div');
    itemActionsContainer.className = 'todo-item-actions';
    
    if (isCurrentlyEditing) {
      // 수정 중일 때: 저장, 취소 노출
      const saveButton = document.createElement('button');
      saveButton.className = 'btn-action btn-save';
      saveButton.setAttribute('aria-label', '저장');
      saveButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
        </svg>
      `;
      saveButton.addEventListener('click', () => {
        const textEditInput = itemLeftContainer.querySelector('.todo-edit-input');
        saveEditedTodoText(todo.id, textEditInput.value);
      });
      
      const cancelButton = document.createElement('button');
      cancelButton.className = 'btn-action btn-cancel';
      cancelButton.setAttribute('aria-label', '취소');
      cancelButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
        </svg>
      `;
      cancelButton.addEventListener('click', cancelTodoEditMode);
      
      itemActionsContainer.appendChild(saveButton);
      itemActionsContainer.appendChild(cancelButton);
    } else {
      // 일반 모드일 때: 수정, 삭제 노출
      const editStartButton = document.createElement('button');
      editStartButton.className = 'btn-action btn-edit';
      editStartButton.setAttribute('aria-label', '수정');
      editStartButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.83 20.013a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
        </svg>
      `;
      editStartButton.addEventListener('click', () => enterTodoEditMode(todo.id));
      
      const deleteButton = document.createElement('button');
      deleteButton.className = 'btn-action btn-delete';
      deleteButton.setAttribute('aria-label', '삭제');
      deleteButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
        </svg>
      `;
      deleteButton.addEventListener('click', () => deleteTodoItem(todo.id));
      
      itemActionsContainer.appendChild(editStartButton);
      itemActionsContainer.appendChild(deleteButton);
    }
    
    listItem.appendChild(itemLeftContainer);
    listItem.appendChild(itemActionsContainer);
    todoList.appendChild(listItem);
  });

  // 5. 조건별 빈 리스트 안내 출력 토글
  updateTodoListVisibility(finalFilteredTodos, dateSpecificTodos.length);
}

// ----------------------------------------------------------------------------
// 10. 진입점 이벤트 핸들러 작동
// ----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', initializeApp);
