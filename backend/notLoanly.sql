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
    loan_amount INTEGER NOT NULL,               -- 대출 금액
    interest_rate REAL NOT NULL,                -- 대출 이자율
    repayment_period INTEGER NOT NULL,          -- 상환 기간 (개월)
    monthly_repayment_goal INTEGER NOT NULL,    -- 월별 상환 목표
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
('대출 상환'),
('금융'),
('주거 및 통신'),
('식비'),
('교통'),
('쇼핑'),
('여가'),
('건강'),
('기타');

-- Users 테이블에 데이터 삽입
INSERT INTO Users (name, monthly_income, monthly_expense, loan_amount, interest_rate, repayment_period, monthly_repayment_goal, selected_plan_group_id) 
VALUES 
('최민호', 2500000, 1350000, 3000000, 6.0, 6, 500000, 3),
('김민주', 2000000, 1100000, 2000000, 6.0, 10, 200000, NULL);


-- 최민호의 거래내역
-- 2024년 9월 거래내역
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(1, 1, '2024-09-01', 2500000, '급여 입금', 'Bank Transfer'),
(1, 3, '2024-09-01', 1000000, '저축/투자', 'Bank Transfer'),
(1, 4, '2024-09-02', 500000, '월세', 'Bank Transfer'),
(1, 5, '2024-09-03', 90000, '식료품 구매', 'Card'),
(1, 6, '2024-09-04', 45000, '대중교통 충전', 'Card'),
(1, 7, '2024-09-05', 35000, '생활용품 구매', 'Cash'),
(1, 8, '2024-09-06', 70000, '콘서트 티켓 구매', 'Card'),
(1, 9, '2024-09-07', 80000, '요가 수업 등록', 'Card'),
(1, 10, '2024-09-08', 100000, '부모님 선물', 'Cash'),
(1, 5, '2024-09-10', 60000, '외식', 'Card'),
(1, 4, '2024-09-12', 40000, '휴대폰 요금', 'Bank Transfer'),
(1, 2, '2024-09-15', 100000, '보험료 납부', 'Bank Transfer'),
(1, 6, '2024-09-18', 25000, '택시 이용', 'Cash'),
(1, 8, '2024-09-20', 30000, '전시회 관람', 'Card'),
(1, 7, '2024-09-22', 90000, '의류 구매', 'Card'),
(1, 9, '2024-09-25', 50000, '치과 진료비', 'Card'),
(1, 10, '2024-09-28', 20000, '기부', 'Cash');


-- 2024년 10월 거래내역
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(1, 1, '2024-10-01', 2500000, '급여 입금', 'Bank Transfer'),
(1, 3, '2024-10-01', 1000000, '저축/투자', 'Bank Transfer'),
(1, 4, '2024-10-02', 500000, '월세', 'Bank Transfer'),
(1, 5, '2024-10-03', 95000, '식료품 구매', 'Card'),
(1, 6, '2024-10-04', 50000, '대중교통 충전', 'Card'),
(1, 7, '2024-10-05', 40000, '생활용품 구매', 'Cash'),
(1, 8, '2024-10-06', 15000, '영화 관람', 'Card'),
(1, 9, '2024-10-07', 60000, '헬스장 이용료', 'Card'),
(1, 10, '2024-10-08', 100000, '친구 결혼식 축의금', 'Cash'),
(1, 5, '2024-10-10', 55000, '외식', 'Card'),
(1, 4, '2024-10-12', 30000, '인터넷 요금', 'Bank Transfer'),
(1, 2, '2024-10-15', 100000, '보험료 납부', 'Bank Transfer'),
(1, 6, '2024-10-18', 20000, '택시 이용', 'Cash'),
(1, 8, '2024-10-20', 20000, '카페 이용', 'Card'),
(1, 7, '2024-10-22', 85000, '의류 구매', 'Card'),
(1, 9, '2024-10-25', 30000, '병원 진료비', 'Card'),
(1, 10, '2024-10-28', 10000, '기부', 'Cash');



-- 김민주의 거래내역
-- 2024년 9월 거래내역
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(2, 1, '2024-09-02', 1700000, '알바 급여', 'Cash'),
(2, 3, '2024-09-02', 150000, '저축', 'Bank Transfer'),
(2, 4, '2024-09-03', 400000, '월세', 'Bank Transfer'),
(2, 5, '2024-09-04', 60000, '마트 장보기', 'Card'),
(2, 6, '2024-09-06', 20000, '대중교통 충전', 'Card'),
(2, 7, '2024-09-07', 15000, '세제 및 청소용품 구매', 'Cash'),
(2, 8, '2024-09-10', 17000, '넷플릭스 구독료', 'Card'),
(2, 9, '2024-09-15', 50000, '병원 진료비', 'Card'),
(2, 10, '2024-09-18', 10000, '이웃 도움 기부금', 'Cash'),
(2, 5, '2024-09-20', 35000, '외식', 'Card'),
(2, 4, '2024-09-22', 25000, '인터넷 요금', 'Bank Transfer'),
(2, 2, '2024-09-25', 45000, '대출 상환', 'Bank Transfer'),
(2, 8, '2024-09-28', 25000, '전시회 관람', 'Card');


-- 2024년 10월 거래내역
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(2, 1, '2024-10-03', 1850000, '알바 급여', 'Cash'),
(2, 3, '2024-10-03', 180000, '저축', 'Bank Transfer'),
(2, 4, '2024-10-05', 400000, '월세', 'Bank Transfer'),
(2, 5, '2024-10-06', 50000, '시장 장보기', 'Card'),
(2, 6, '2024-10-08', 15000, '버스 충전', 'Card'),
(2, 7, '2024-10-09', 20000, '주방 용품 구매', 'Cash'),
(2, 8, '2024-10-12', 12000, '영화 관람', 'Card'),
(2, 9, '2024-10-14', 40000, '헬스장 등록', 'Card'),
(2, 10, '2024-10-20', 45000, '친구 생일 선물', 'Cash'),
(2, 5, '2024-10-22', 30000, '외식', 'Card'),
(2, 4, '2024-10-24', 30000, '휴대폰 요금', 'Bank Transfer'),
(2, 2, '2024-10-27', 50000, '대출 상환', 'Bank Transfer'),
(2, 8, '2024-10-29', 10000, '카페 이용', 'Card');

-- Transactions 11월 데이터 삽입
INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method) VALUES
(1, 1, '2024-11-01', 2500000, '급여 입금', 'Bank Transfer'),
(1, 3, '2024-11-01', 1000000, '저축/투자', 'Bank Transfer'),
(1, 4, '2024-11-02', 500000, '월세', 'Bank Transfer'),
(1, 5, '2024-11-03', 100000, '식료품 구매', 'Card'),
(1, 6, '2024-11-04', 50000, '대중교통 충전', 'Card'),
(1, 7, '2024-11-05', 30000, '생활용품 구매', 'Cash'),
(1, 8, '2024-11-06', 15000, '영화 관람', 'Card'),
(1, 9, '2024-11-07', 60000, '헬스장 이용료', 'Card'),
(1, 10, '2024-11-08', 40000, '친구 생일 선물', 'Cash'),
(1, 5, '2024-11-10', 50000, '외식', 'Card'),
(1, 4, '2024-11-12', 30000, '인터넷 요금', 'Bank Transfer'),
(1, 2, '2024-11-15', 100000, '보험료 납부', 'Bank Transfer'),
(2, 1, '2024-11-01', 1800000, '알바 급여', 'Cash'),
(2, 3, '2024-11-01', 150000, '저축', 'Bank Transfer'),
(2, 4, '2024-11-03', 400000, '월세', 'Bank Transfer'),
(2, 5, '2024-11-05', 25000, '편의점 간식 구매', 'Card'),
(2, 6, '2024-11-07', 20000, '대중교통 충전', 'Card'),
(2, 7, '2024-11-10', 15000, '빨래방 이용', 'Cash');

INSERT INTO RepaymentPlans (user_id, plan_name, total_amount, duration, details)
VALUES
(1, 
 '금융 중심 절약 플랜', 
 515000, 
 6, 
 '[
    {"category_id": 3, "reduced_amount": 400000, "saving_percentage": 40},
    {"category_id": 4, "reduced_amount": 53000, "saving_percentage": 10},
    {"category_id": 5, "reduced_amount": 27000, "saving_percentage": 10},
    {"category_id": 6, "reduced_amount": 7000, "saving_percentage": 10}
 ]'
),
(1, 
 '주거 및 통신 유지 플랜', 
 515000, 
 6, 
 '[
    {"category_id": 3, "reduced_amount": 250000, "saving_percentage": 25},
    {"category_id": 5, "reduced_amount": 81000, "saving_percentage": 30},
    {"category_id": 6, "reduced_amount": 14000, "saving_percentage": 20},
    {"category_id": 8, "reduced_amount": 17500, "saving_percentage": 50}
 ]'
),
(1, 
 '골고루 절약 플랜', 
 515000, 
 6, 
 '[
    {"category_id": 3, "reduced_amount": 300000, "saving_percentage": 30},
    {"category_id": 4, "reduced_amount": 106000, "saving_percentage": 20},
    {"category_id": 5, "reduced_amount": 27000, "saving_percentage": 10},
    {"category_id": 6, "reduced_amount": 7000, "saving_percentage": 10},
    {"category_id": 7, "reduced_amount": 22000, "saving_percentage": 20}
 ]'
);

INSERT INTO RepaymentHistory (user_id, repayment_date, repayment_amount, remaining_balance, description)
VALUES
(1, '2024-09-01', 50000, 2950000, '첫 번째 상환'),
(1, '2024-10-15', 50000, 2900000, '두 번째 상환'),
(2, '2024-10-10', 30000, 1970000, '첫 번째 상환');

INSERT INTO Notification (user_id, message)
VALUES
(1, '대출 상환일이 다가오고 있습니다. 2024-11-15까지 상환을 완료하세요.'),
(2, '대출 상환이 완료되었습니다. 잔액은 1,970,000원입니다.');


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

-- RepaymentHistory 테이블 데이터
DELETE FROM RepaymentHistory;

INSERT INTO RepaymentHistory (user_id, repayment_date, repayment_amount, remaining_balance, description)
VALUES
(1, '2024-09-15', 100000, 2950000, '첫 번째 상환'),
(1, '2024-10-15', 100000, 2850000, '두 번째 상환'),
(1, '2024-11-15', 100000, 2750000, '세 번째 상환'),
(2, '2024-09-25', 45000, 1955000, '첫 번째 상환'),
(2, '2024-10-27', 50000, 1905000, '두 번째 상환');

-- Transactions 테이블의 대출 상환 데이터 수정
DELETE FROM Transactions WHERE category_id = 2;

INSERT INTO Transactions (user_id, category_id, transaction_date, amount, description, payment_method)
VALUES
(1, 2, '2024-09-15', 100000, '대출 상환', 'Bank Transfer'),
(1, 2, '2024-10-15', 100000, '대출 상환', 'Bank Transfer'),
(1, 2, '2024-11-15', 100000, '대출 상환', 'Bank Transfer'),
(2, 2, '2024-09-25', 45000, '대출 상환', 'Bank Transfer'),
(2, 2, '2024-10-27', 50000, '대출 상환', 'Bank Transfer');



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

