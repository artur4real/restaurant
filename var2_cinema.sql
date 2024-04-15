-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 15 2024 г., 17:00
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `var2_cinema`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Bookings`
--

CREATE TABLE `Bookings` (
  `BookingID` int NOT NULL,
  `ClientName` varchar(255) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `MovieID` int NOT NULL,
  `SessionTime` time NOT NULL,
  `HallNumber` int NOT NULL,
  `TicketType` enum('Эконом','Комфорт','Детский') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Bookings`
--

INSERT INTO `Bookings` (`BookingID`, `ClientName`, `Phone`, `Email`, `MovieID`, `SessionTime`, `HallNumber`, `TicketType`) VALUES
(1, 'Иванов Иван', '1234567890', 'ivanov@example.com', 1, '10:00:00', 1, 'Эконом'),
(2, 'Петров Петр', '9876543210', 'petrov@example.com', 2, '14:00:00', 2, 'Комфорт'),
(3, 'Сидоров Сидор', '5555555555', 'sidorov@example.com', 3, '18:00:00', 3, 'Эконом'),
(4, 'уцауцацуа', 'цуацуацуацу', 'цуацацацу', 2, '18:00:00', 3, 'Комфорт'),
(5, 'ваиваиав', 'иваиа', 'иваиваиваива', 1, '10:00:00', 1, 'Эконом'),
(6, 'уцацуаца', 'цуацац', 'цууацацуа', 1, '10:00:00', 1, 'Эконом');

-- --------------------------------------------------------

--
-- Структура таблицы `ClientMovies`
--

CREATE TABLE `ClientMovies` (
  `ClientID` int NOT NULL,
  `ClientName` varchar(255) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `MovieID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `ClientMovies`
--

INSERT INTO `ClientMovies` (`ClientID`, `ClientName`, `Phone`, `Email`, `MovieID`) VALUES
(1, 'Иванов Иван', '1234567890', 'ivanov@example.com', 1),
(2, 'Петров Петр', '9876543210', 'petrov@example.com', 2),
(3, 'Сидоров Сидор', '5555555555', 'sidorov@example.com', 3);

-- --------------------------------------------------------

--
-- Структура таблицы `Managers`
--

CREATE TABLE `Managers` (
  `ManagerID` int NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Managers`
--

INSERT INTO `Managers` (`ManagerID`, `Username`, `Password`) VALUES
(1, 'manager', 'manager');

-- --------------------------------------------------------

--
-- Структура таблицы `Movies`
--

CREATE TABLE `Movies` (
  `MovieID` int NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Genre` varchar(255) DEFAULT NULL,
  `Director` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Movies`
--

INSERT INTO `Movies` (`MovieID`, `Title`, `Genre`, `Director`) VALUES
(1, 'Фильм 1', 'Жанр 1', 'Режиссер 1'),
(2, 'Фильм 2', 'Жанр 2', 'Режиссер 2'),
(3, 'Фильм 3', 'Жанр 3', 'Режиссер 3'),
(4, 'ЩУКПЩОКПКП', 'ПУКПУКПУКПУКПУКПУ', 'КУПУПУКПУКПУКПКУ');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Bookings`
--
ALTER TABLE `Bookings`
  ADD PRIMARY KEY (`BookingID`),
  ADD KEY `MovieID` (`MovieID`);

--
-- Индексы таблицы `ClientMovies`
--
ALTER TABLE `ClientMovies`
  ADD PRIMARY KEY (`ClientID`),
  ADD KEY `MovieID` (`MovieID`);

--
-- Индексы таблицы `Managers`
--
ALTER TABLE `Managers`
  ADD PRIMARY KEY (`ManagerID`);

--
-- Индексы таблицы `Movies`
--
ALTER TABLE `Movies`
  ADD PRIMARY KEY (`MovieID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Bookings`
--
ALTER TABLE `Bookings`
  MODIFY `BookingID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `ClientMovies`
--
ALTER TABLE `ClientMovies`
  MODIFY `ClientID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `Managers`
--
ALTER TABLE `Managers`
  MODIFY `ManagerID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `Movies`
--
ALTER TABLE `Movies`
  MODIFY `MovieID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Bookings`
--
ALTER TABLE `Bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`MovieID`) REFERENCES `Movies` (`MovieID`);

--
-- Ограничения внешнего ключа таблицы `ClientMovies`
--
ALTER TABLE `ClientMovies`
  ADD CONSTRAINT `clientmovies_ibfk_1` FOREIGN KEY (`MovieID`) REFERENCES `Movies` (`MovieID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
