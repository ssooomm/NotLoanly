-- 기존 데이터베이스가 존재하면 삭제
DROP DATABASE IF EXISTS notLoanly;
-- 새로운 데이터베이스 생성
CREATE DATABASE notLoanly;
USE notLoanly;

-- 새로운 Users 테이블 생성
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTO_INCREMENT, -- 기본키
    name TEXT NOT NULL,                         -- 사용자 이름
    monthly_income INTEGER NOT NULL,            -- 월 수입
    monthly_expense INTEGER NOT NULL,           -- 월 지출
    available_funds INTEGER GENERATED ALWAYS AS (monthly_income - monthly_expense) STORED, -- 사용 가능 자금
    loan_amount INTEGER,               -- 대출 금액
    interest_rate REAL,                -- 대출 이자율
    loan_date TIMESTAMP,
    repayment_period INTEGER,          -- 상환 기간 (개월)
    monthly_repayment_goal INTEGER,    -- 월별 상환 목표
    selected_plan_group_id INTEGER DEFAULT NULL,-- 선택된 플랜 그룹 ID (NULL 가능)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 생성일
);

-- Categories 테이블
CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    category_name TEXT NOT NULL
);

-- UserExpenses 테이블
CREATE TABLE UserExpenses (
    user_expense_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    month INTEGER NOT NULL,
    original_amount INTEGER NOT NULL,
    is_hard_to_reduce BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
);

-- RepaymentPlans 테이블 생성
CREATE TABLE RepaymentPlans (
    plan_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    plan_name TEXT NOT NULL,
    total_amount INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    details JSON NOT NULL,                  -- JSON 데이터 타입 사용
    hashtags TEXT,                 -- 추가된 hashtags 칼럼
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);


-- RepaymentHistory 테이블
CREATE TABLE RepaymentHistory (
    repayment_id INTEGER PRIMARY KEY auto_increment,
    user_id INTEGER NOT NULL,
    repayment_date DATE NOT NULL,
    repayment_amount INTEGER NOT NULL,
    interest_amoun INTEGER NOT NULL,
    remaining_balance INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);


-- Transactions 테이블
CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    amount INTEGER NOT NULL,
    description TEXT,
    payment_method TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
);

-- Notification 테이블
CREATE TABLE Notification (
    notification_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Categories 초기 데이터 삽입
INSERT INTO Categories (category_name) VALUES
('소득'),
('대출 소비'),
('금융'),
('주거 및 통신'),
('식비'),
('교통'),
('쇼핑'),
('여가'),
('건강'),
('기타');

-- Users 테이블에 데이터 삽입
INSERT INTO Users (name, monthly_income, monthly_expense, loan_amount, interest_rate, loan_date, repayment_period, monthly_repayment_goal, selected_plan_group_id) 
VALUES 
('최민호', 2500000, 1500000, 3000000, 6.0,'2024-10-09 09:06:35', 3, 1015000, 3),
('김민주', 2000000, 1500000, 2000000, 7.0,'2024-09-11 12:32:10', 6, 345000, 6);




-- ****************************** 9월 ****************************** 
-- Transactions 테이블에 데이터 삽입 (최민호 - 유저 1) -- 줄이기 전 
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(1, 1, '2024-09-01', 2500000, '급여 입금', 'Bank Transfer'),
(1, 3, '2024-09-01', 1000000, '저축/투자', 'Bank Transfer'),
(1, 4, '2024-09-02', 410000, '월세', 'Bank Transfer'),
(1, 5, '2024-09-03', 250000, '식료품 구매', 'Card'), -- 증가
(1, 6, '2024-09-04', 50000, '대중교통 충전', 'Card'), -- 증가
(1, 7, '2024-09-05', 50000, '생활용품 구매', 'Cash'), -- 증가
(1, 8, '2024-09-06', 80000, '콘서트 티켓 구매', 'Card'), -- 증가
(1, 8, '2024-09-07', 80000, '요가 수업 등록', 'Card'), -- 증가
(1, 10, '2024-09-08', 50000, '부모님 선물', 'Cash'), -- 증가
(1, 5, '2024-09-10', 80000, '외식', 'Card'), -- 증가
(1, 4, '2024-09-12', 50000, '휴대폰 요금', 'Bank Transfer'), -- 증가
(1, 2, '2024-09-15', 100000, '보험료 납부', 'Bank Transfer'), -- 증가
(1, 6, '2024-09-18', 35000, '택시 이용', 'Cash'), -- 증가
(1, 8, '2024-09-20', 50000, '전시회 관람', 'Card'), -- 증가
(1, 7, '2024-09-22', 150000, '의류 구매', 'Card'), -- 증가
(1, 9, '2024-09-25', 40000, '약 구매', 'Card'), -- 증가
(1, 10, '2024-09-28', 25000, '기부', 'Cash'); -- 증가
-- ****************************** 10월 ****************************** 
-- Transactions 테이블에 데이터 삽입 (최민호 - 유저 1 #10월) 이때부터 줄여야함 250 150 100 300 40 40 40 30 150
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(1, 1, '2024-10-01', 2500000, '급여 입금', 'Bank Transfer'),
(1, 3, '2024-10-01', 1000000, '저축/투자', 'Bank Transfer'),
(1, 4, '2024-10-02', 410000, '월세', 'Bank Transfer'),
(1, 5, '2024-10-03', 255000, '식료품 구매', 'Card'), 
(1, 6, '2024-10-04', 50000, '대중교통 충전', 'Card'), 
(1, 7, '2024-10-05', 80000, '생활용품 구매', 'Cash'), 
(1, 8, '2024-10-06', 75000, '콘서트 티켓 구매', 'Card'),
(1, 4, '2024-10-06', 50000, '휴대폰 요금', 'Card'),
(1, 9, '2024-10-07', 85000, '요가 수업 등록', 'Card'), 
(1, 10, '2024-10-08', 110000, '부모님 선물', 'Cash'), 
(1, 1, '2024-10-09', 3000000, 'KB비상금 대출', 'Bank Transfer'),
(1, 2, '2024-10-10', 400000, '경조사비 (1차)', 'Cash'),
(1, 2, '2024-10-12', 400000, '경조사비 (2차)', 'Cash'),
(1, 2, '2024-10-15', 400000, '경조사비 (3차)', 'Cash'),
(1, 2, '2024-10-18', 300000, '경조사비 (4차)', 'Cash'),
(1, 2, '2024-10-20', 1500000, '이사 비용', 'Bank Transfer'),
(1, 6, '2024-10-22', 30000, '택시 이용', 'Cash'), 
(1, 8, '2024-10-23', 35000, '전시회 관람', 'Card'), 
(1, 7, '2024-10-25', 100000, '의류 구매', 'Card'), 
(1, 9, '2024-10-28', 200000, '치과 진료비', 'Card'), 
(1, 10, '2024-10-30', 30000, '기부', 'Cash'); 

-- Transactions 테이블에 데이터 삽입 (유저 1 - 최민호)
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(1, 1, '2024-11-01', 2500000, '급여 입금', 'Bank Transfer'),
(1, 3, '2024-11-01', 300000, '저축/투자', 'Bank Transfer'),
(1, 4, '2024-11-02', 410000, '월세', 'Bank Transfer'),
(1, 5, '2024-11-03', 90000, '식료품 구매', 'Card'),
(1, 6, '2024-11-04', 45000, '대중교통 충전', 'Card'),
(1, 7, '2024-11-05', 35000, '생활용품 구매', 'Cash'),
(1, 9, '2024-11-08', 40000, '약 구매', 'Card'),
(1, 5, '2024-11-10', 40000, '외식', 'Card'),
(1, 4, '2024-11-15', 50000, '휴대폰 요금', 'Bank Transfer'),
(1, 8, '2024-11-20', 30000, '전시회 관람', 'Card');



-- ****************************** 8월 ****************************** 
-- Transactions 테이블에 데이터 삽입 (김민주 - 유저 2) -- 줄이기전 
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(2, 1, '2024-08-01', 2000000, '급여 입금', 'Bank Transfer'),
(2, 3, '2024-08-01', 500000, '저축/투자', 'Bank Transfer'),
(2, 4, '2024-08-02', 300000, '월세', 'Bank Transfer'), -- -300000
(2, 5, '2024-08-03', 300000, '식료품 구매', 'Card'),
(2, 6, '2024-08-04', 30000, '대중교통 충전', 'Card'), 
(2, 7, '2024-08-04', 120000, '의류 구매', 'Card'),
(2, 7, '2024-08-05', 20000, '생활용품 구매', 'Cash'),
(2, 8, '2024-08-06', 50000, '영화 관람', 'Card'), 
(2, 6, '2024-08-07', 40000, '택시 이용', 'Cash'),
(2, 9, '2024-08-07', 60000, '병원비', 'Card'), 
(2, 10, '2024-08-08', 80000, '부모님 선물', 'Cash'), 
(2, 5, '2024-08-10', 80000, '배달음식', 'Card'), 
(2, 5, '2024-08-10', 50000, '외식', 'Card'), 
(2, 4, '2024-08-12', 35000, '휴대폰 요금', 'Bank Transfer'), 
(2, 6, '2024-08-18', 40000, '택시 이용', 'Cash'),
(2, 8, '2024-08-20', 25000, '전시회 관람', 'Card'), 
(2, 7, '2024-08-22', 130000, '의류 구매', 'Card'),
(2, 7, '2024-08-21', 80000, '의류 구매', 'Card'),
(2, 9, '2024-08-25', 50000, '정기 검진 비용', 'Card'),
(2, 10, '2024-08-28', 10000, '기부', 'Cash');

-- Transactions 테이블에 데이터 삽입 (김민주 - 유저 2 #9월) 이달을 줄여야함 
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(2, 1, '2024-09-01', 2000000, '급여 입금', 'Bank Transfer'),
(2, 3, '2024-09-01', 500000, '저축/투자', 'Bank Transfer'),
(2, 4, '2024-09-02', 300000, '월세', 'Bank Transfer'), -- 300000
(2, 5, '2024-09-03', 300000, '식료품 구매', 'Card'),
(2, 6, '2024-09-04', 30000, '대중교통 충전', 'Card'),
(2, 7, '2024-09-05', 20000, '생활용품 구매', 'Cash'),
(2, 1, '2024-09-11', 2000000, 'KB비상금 대출', 'Bank Transfer'),
(2, 2, '2024-09-12', 2000000, '고양이 병원비', 'Bank Transfer'),
(2, 5, '2024-09-14', 80000, '배달음식', 'Card'),
(2, 8, '2024-09-15', 25000, '영화 티켓 구매', 'Card'),
(2, 4, '2024-09-20', 35000, '휴대폰 요금', 'Bank Transfer'),
(2, 6, '2024-09-22', 20000, '택시 이용', 'Cash'),
(2, 7, '2024-09-25', 130000, '의류 구매', 'Card'),
(2, 9, '2024-09-29', 45000, '정기 검진 비용', 'Card'),
(2, 10, '2024-09-30', 15000, '기부', 'Cash');

INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES 
(2, 1, '2024-10-01', 2000000, '급여 입금', 'Bank Transfer'),
(2, 3, '2024-10-01', 400000, '저축/투자', 'Bank Transfer'),
(2, 4, '2024-10-02', 300000, '월세', 'Bank Transfer'),
(2, 5, '2024-10-03', 250000, '식료품 구매', 'Card'),
(2, 6, '2024-10-04', 50000, '대중교통 충전', 'Card'),
(2, 7, '2024-10-04', 120000, '의류 구매', 'Card'),
(2, 7, '2024-10-05', 20000, '생활용품 구매', 'Cash'),
(2, 8, '2024-10-06', 50000, '영화 관람', 'Card'),
(2, 9, '2024-10-07', 50000, '병원비', 'Card'),
(2, 5, '2024-10-17', 40000, '배달음식', 'Card'),
(2, 10, '2024-10-08', 80000, '부모님 선물', 'Cash'),
(2, 5, '2024-10-10', 40000, '외식', 'Card'),
(2, 7, '2024-10-11', 45000, '의류 구매', 'Card'),
(2, 4, '2024-10-12', 35000, '휴대폰 요금', 'Bank Transfer'),
(2, 8, '2024-10-20', 25000, '전시회 관람', 'Card'),
(2, 7, '2024-10-22', 80000, '의류 구매', 'Card'),
(2, 9, '2024-10-25', 60000, '정기 검진 비용', 'Card'),
(2, 10, '2024-10-28', 10000, '기부', 'Cash');

-- Transactions 테이블에 데이터 삽입 (유저 2 - 김민주)
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(2, 1, '2024-11-01', 2000000, '급여 입금', 'Bank Transfer'),
(2, 3, '2024-11-01', 400000, '저축/투자', 'Bank Transfer'),
(2, 4, '2024-11-02', 300000, '월세', 'Bank Transfer'),
(2, 5, '2024-11-03', 40000, '식료품 구매', 'Card'),
(2, 6, '2024-11-04', 30000, '대중교통 충전', 'Card'),
(2, 7, '2024-11-05', 20000, '생활용품 구매', 'Cash'),
(2, 9, '2024-11-07', 50000, '병원비 (정기 검진)', 'Card'),
(2, 8, '2024-11-09', 25000, '공연 관람', 'Card'),
(2, 5, '2024-11-12', 30000, '외식', 'Card'),
(2, 10, '2024-11-15',80000, '부모님 선물', 'Cash'),
(2, 4, '2024-11-18', 35000, '휴대폰 요금', 'Bank Transfer'),
(2, 6, '2024-11-20', 15000, '택시 이용', 'Cash');



INSERT INTO RepaymentPlans (user_id, plan_name, total_amount, duration, details, hashtags) VALUES
(1, 
 '식비 절약 플랜', 
 1015000, 
 3, 
 '[
    {\"category_id\": 3, \"original_amount\": 1000000, \"reduced_amount\": 750000, \"saving_percentage\": 75.00}, 
    {\"category_id\": 5, \"original_amount\": 330000, \"reduced_amount\": 130000, \"saving_percentage\": 39.39}, 
    {\"category_id\": 7, \"original_amount\": 200000, \"reduced_amount\": 60000, \"saving_percentage\": 30.00}, 
    {\"category_id\": 8, \"original_amount\": 210000, \"reduced_amount\": 50000, \"saving_percentage\": 23.81}, 
    {\"category_id\": 6, \"original_amount\": 85000, \"reduced_amount\": 25000, \"saving_percentage\": 29.41}
 ]',
 '#냉장고 파먹기, #배달 금지!, #백종원 레시피'
),
(1, 
 '교통비 절약 플랜', 
 1015000, 
 3, 
 '[
    {\"category_id\": 3, \"original_amount\": 1000000, \"reduced_amount\": 800000, \"saving_percentage\": 80.00}, 
    {\"category_id\": 5, \"original_amount\": 330000, \"reduced_amount\": 100000, \"saving_percentage\": 30.30}, 
    {\"category_id\": 7, \"original_amount\": 200000, \"reduced_amount\": 30000, \"saving_percentage\": 15.00}, 
    {\"category_id\": 8, \"original_amount\": 210000, \"reduced_amount\": 40000, \"saving_percentage\": 19.05}, 
    {\"category_id\": 6, \"original_amount\": 85000, \"reduced_amount\": 45000, \"saving_percentage\": 52.94}
 ]',
 '#걸어다니자, #대중교통을 이용하자, #내가 바로 환경 지킴이'
),
(1, 
 '문화생활 절약 플랜', 
 1015000, 
 3, 
 '[
    {\"category_id\": 3, \"original_amount\": 1000000, \"reduced_amount\": 700000, \"saving_percentage\": 70.00}, 
    {\"category_id\": 5, \"original_amount\": 330000, \"reduced_amount\": 80000, \"saving_percentage\": 24.24}, 
    {\"category_id\": 7, \"original_amount\": 200000, \"reduced_amount\": 60000, \"saving_percentage\": 30.00}, 
    {\"category_id\": 8, \"original_amount\": 210000, \"reduced_amount\": 160000, \"saving_percentage\": 76.19}, 
    {\"category_id\": 6, \"original_amount\": 85000, \"reduced_amount\": 15000, \"saving_percentage\": 17.65}
 ]',
 '#산책가자, #친구야 OTT 같이보자, #집에서 노래나 듣자'
);

INSERT INTO RepaymentPlans (user_id, plan_name, total_amount, duration, details, hashtags) VALUES
(2, 
 '쇼핑 절약 플랜', 
 345000, 
 6, 
 '[
    {\"category_id\": 3, \"original_amount\": 500000, \"reduced_amount\": 100000, \"saving_percentage\": 20.00}, 
    {\"category_id\": 5, \"original_amount\": 430000, \"reduced_amount\": 80000, \"saving_percentage\": 18.60}, 
    {\"category_id\": 6, \"original_amount\": 110000, \"reduced_amount\": 20000, \"saving_percentage\": 18.18}, 
    {\"category_id\": 7, \"original_amount\": 350000, \"reduced_amount\": 135000, \"saving_percentage\": 38.57}, 
    {\"category_id\": 9, \"original_amount\": 110000, \"reduced_amount\": 10000, \"saving_percentage\": 9.09}
 ]',
 '#같은 거 입어, #ootd: 스티브 잡스, #옷장을 열어봐'
),
(2, 
 '식비 절약 플랜', 
 345000, 
 6, 
 '[
    {\"category_id\": 3, \"original_amount\": 500000, \"reduced_amount\": 0, \"saving_percentage\": 0.00}, 
    {\"category_id\": 5, \"original_amount\": 430000, \"reduced_amount\": 180000, \"saving_percentage\": 41.86}, 
    {\"category_id\": 6, \"original_amount\": 110000, \"reduced_amount\": 20000, \"saving_percentage\": 18.18}, 
    {\"category_id\": 7, \"original_amount\": 350000, \"reduced_amount\": 135000, \"saving_percentage\": 38.57}, 
    {\"category_id\": 9, \"original_amount\": 110000, \"reduced_amount\": 10000, \"saving_percentage\": 9.09}
 ]',
 '#냉장고 파먹기, #배달 금지!, #백종원 레시피'
),
(2, 
 '교통비 절약 플랜', 
 345000, 
 6, 
 '[
    {\"category_id\": 3, \"original_amount\": 500000, \"reduced_amount\": 100000, \"saving_percentage\": 20.00}, 
    {\"category_id\": 5, \"original_amount\": 430000, \"reduced_amount\": 100000, \"saving_percentage\": 23.26}, 
    {\"category_id\": 6, \"original_amount\": 110000, \"reduced_amount\": 60000, \"saving_percentage\": 54.55}, 
    {\"category_id\": 7, \"original_amount\": 350000, \"reduced_amount\": 85000, \"saving_percentage\": 24.29}, 
    {\"category_id\": 9, \"original_amount\": 110000, \"reduced_amount\": 0, \"saving_percentage\": 0.00}
 ]',
 '#걸어다니자, #대중교통을 이용하자, #내가 바로 환경 지킴이'
);

INSERT INTO RepaymentHistory (user_id, repayment_date, repayment_amount, interest_amount , remaining_balance, description)
VALUES
-- 사용자 1 상환기록
(1, '2024-11-09', 1000000, 15000 ,2000000, '첫 번째 상환'),
-- 사용자 2 상환기록
(2, '2024-10-11', 333333, 11667 , 1655000, '첫 번째 상환'),
(2, '2024-11-11', 333333, 11667 , 1340000, '두 번째 상환');

INSERT INTO Notification (user_id, message)
VALUES
(1, '대출 상환일이 다가오고 있습니다. 2024-11-09까지 상환을 완료하세요.'),
(2, '대출 상환일이 다가오고 있습니다. 2024-10-09까지 상환을 완료하세요.'),
(2, '대출 상환일이 다가오고 있습니다. 2024-11-09까지 상환을 완료하세요.'),

(1, '11월 대출 상환이 완료되었습니다. 잔액은 2,000,000원입니다.'),
(2, '10월 대출 상환이 완료되었습니다. 잔액은 1,655,000원입니다.'),
(2, '11월 대출 상환이 완료되었습니다. 잔액은 1,340,000원입니다.');


-- UserExpenses 계산 및 데이터 삽입
INSERT INTO UserExpenses (user_id, category_id, month, original_amount)
SELECT 
    t.user_id,
    t.category_id,
    MONTH(t.transaction_date) AS month,
    SUM(t.amount) AS original_amount
FROM Transactions t
JOIN Categories c ON t.category_id = c.category_id
WHERE t.category_id NOT IN (1, 2) -- 소득과 대출 상환은 제외
GROUP BY t.user_id, t.category_id, MONTH(t.transaction_date);

-- Transactions 테이블에 데이터가 추가될 떄 자동으로 UserExpenses 테이블 값 변경
DELIMITER $$

CREATE TRIGGER after_transaction_insert
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
    DECLARE existing_expense_id INT;

    -- UserExpenses 테이블에 기존 데이터가 있는지 확인
    SELECT user_expense_id INTO existing_expense_id
    FROM UserExpenses
    WHERE user_id = NEW.user_id
      AND category_id = NEW.category_id
      AND month = MONTH(NEW.transaction_date);
    -- 기존 데이터가 있으면 업데이트, 없으면 새로 삽입
    IF existing_expense_id IS NOT NULL THEN
        UPDATE UserExpenses
        SET original_amount = original_amount + NEW.amount
        WHERE user_expense_id = existing_expense_id;
    ELSE
        INSERT INTO UserExpenses (user_id, category_id, month, original_amount, is_hard_to_reduce)
        VALUES (NEW.user_id, NEW.category_id, MONTH(NEW.transaction_date), NEW.amount, FALSE);
    END IF;
END$$

DELIMITER ;
-- 유저 1의 건강 카테고리 줄이기 힘들다고 함
update userExpenses set is_hard_to_reduce = true where user_id = 1 and category_id = 9;