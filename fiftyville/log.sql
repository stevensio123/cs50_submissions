-- Keep a log of any SQL queries you execute as you solve the mystery.


-- 1. Find description of the crime scene on July 28, 2021:

SELECT description FROM crime_scene_reports WHERE day = 28 AND year = 2021 AND month = 7;

-- Description matched:

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.


-- 2. Look at transcript details of interviews conducted that day:
SELECT * FROM interviews WHERE year = 2021 AND month = 7 AND day =28;

--  Useful clues found:

 --  161 | Ruth    | 2021 | 7     | 28  | :
 --  Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
 --  If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

 --  162 | Eugene  | 2021 | 7     | 28  | :
 --  I don't know the thief's name, but it was someone I recognized.
 --  Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

 --  163 | Raymond | 2021 | 7     | 28  | :
 --  As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
 --  In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
 --  The thief then asked the person on the other end of the phone to purchase the flight ticket.



-- 3. Look at license plates from baker security logs at within 10 minutes of 10:15am:
SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25;


-- 4. Look at details of people with atm transactions at Leggett Street in july 28
SELECT * FROM people WHERE id IN (SELECT bank_accounts.person_id FROM atm_transactions JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE '%Leggett Street%');

-- 5. Look at phone calls at 28 July with duration under one minute:
SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60;

-- 6. Look at earliest flight destination on 29 July:
SELECT * FROM flights WHERE day = 29 AND month = 7 AND year = 2021;
-- Found flight with id no. 36 has the earliest hour:
--  id: 36 | origin_airport_id: 8 | destination_airport_id: 4 | Hour: 8 | Minute: 20

-- 7. Look at airport with id 8 and 4
SELECT * FROM airports WHERE id = 8 OR id = 4;
-- Found out a flight from Fiftyville to New York city were taken that day with id no. 36.

-- 8. Look at people who have called (5) and have license plates recorded in (3) during the crime.
--
SELECT name, id
FROM people
WHERE phone_number
IN
(SELECT caller
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60)
INTERSECT
SELECT name, id
FROM people
WHERE license_plate
IN
(SELECT license_plate
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25);


-- 9. Find people found in (8) that have a flight from Fiftyville to New York on July 29 (7):
SELECT *
FROM people
 WHERE passport_number
IN
    (SELECT passport_number
    FROM passengers
    WHERE flight_id = 36)
INTERSECT
    SELECT *
    FROM people
    WHERE phone_number
    IN
        (SELECT caller
        FROM phone_calls
        WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60
        INTERSECT
        SELECT phone_number
        FROM people
        WHERE license_plate
        IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25));

-- 10. Using people SELECTED from (9) and (4) to find suspect:
-- From (4):
SELECT * FROM people WHERE id IN (SELECT bank_accounts.person_id FROM atm_transactions JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE '%Leggett Street%')
INTERSECT
-- From (9):
SELECT *
FROM people
 WHERE passport_number
IN
    (SELECT passport_number
    FROM passengers
    WHERE flight_id = 36)
INTERSECT
    SELECT *
    FROM people
    WHERE phone_number
    IN
        (SELECT caller
        FROM phone_calls
        WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60
        INTERSECT
        SELECT phone_number
        FROM people
        WHERE license_plate
        IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25));
-- Found thief = Bruce , (367) 555-5533, 94KL13X

-- 11. Using phone number  of Bruce, search for receiver's phone number and person details:
SELECT * FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller = '(367) 555-5533' AND year = 2021 AND month = 7 AND day = 28 AND duration <= 60);