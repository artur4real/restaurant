import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QLineEdit, \
    QMessageBox, QDialog, QTableWidgetItem, QTableWidget
import mysql.connector


class ClientInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Клиентская информационная система")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.label_movies = QLabel("Фильмы в прокате:")
        layout.addWidget(self.label_movies)

        self.combo_movies = QComboBox()
        layout.addWidget(self.combo_movies)

        self.label_session_time = QLabel("Время сеанса:")
        layout.addWidget(self.label_session_time)

        self.combo_session_time = QComboBox()
        self.combo_session_time.addItems(["10:00", "14:00", "18:00", "22:00"])  # Пример времен сеансов
        layout.addWidget(self.combo_session_time)

        self.label_hall_number = QLabel("Номер зала:")
        layout.addWidget(self.label_hall_number)

        self.combo_hall_number = QComboBox()
        self.combo_hall_number.addItems(["1", "2", "3"])  # Пример номеров залов
        layout.addWidget(self.combo_hall_number)

        self.label_ticket_type = QLabel("Тип билета:")
        layout.addWidget(self.label_ticket_type)

        self.combo_ticket_type = QComboBox()
        self.combo_ticket_type.addItems(["Эконом", "Комфорт", "Детский"])
        layout.addWidget(self.combo_ticket_type)

        self.label_ticket_price = QLabel("Стоимость билета:")
        layout.addWidget(self.label_ticket_price)

        self.line_ticket_price = QLineEdit()
        self.line_ticket_price.setReadOnly(True)  # Делаем поле только для чтения
        layout.addWidget(self.line_ticket_price)

        self.btn_book_tickets = QPushButton("Забронировать билеты")
        self.btn_book_tickets.clicked.connect(self.book_tickets)
        layout.addWidget(self.btn_book_tickets)

        self.btn_buy_tickets = QPushButton("Купить билеты")
        self.btn_buy_tickets.clicked.connect(self.open_buy_tickets_dialog)
        self.btn_buy_tickets.hide()  # Скрываем кнопку покупки билетов
        layout.addWidget(self.btn_buy_tickets)

        self.btn_switch_to_manager = QPushButton("Перейти к интерфейсу менеджера")
        self.btn_switch_to_manager.clicked.connect(self.switch_to_manager)
        layout.addWidget(self.btn_switch_to_manager)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключение к базе данных
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="555"
        )

        # Получение списка фильмов из базы данных и заполнение ComboBox
        self.populate_movie_list()

        # Обновление стоимости билета при изменении выбранного типа билета
        self.combo_ticket_type.currentIndexChanged.connect(self.update_ticket_price)

    def populate_movie_list(self):
        try:
            mycursor = self.db_connection.cursor()
            mycursor.execute("SELECT * FROM Movies")
            movies = mycursor.fetchall()
            for movie in movies:
                self.combo_movies.addItem(movie[1], movie[0])  # Добавляем название фильма в комбобокс и сохраняем MovieID в качестве пользовательских данных
        except mysql.connector.Error as err:
            print("Ошибка при получении списка фильмов:", err)

    def update_ticket_price(self):
        ticket_types_prices = {
            "Эконом": 100,
            "Комфорт": 150,
            "Детский": 80
        }
        selected_type = self.combo_ticket_type.currentText()
        price = ticket_types_prices.get(selected_type, 0)
        self.line_ticket_price.setText(str(price))

    def book_tickets(self):
        try:
            selected_movie_id = self.combo_movies.currentData()  # Получаем MovieID выбранного фильма
            selected_time = self.combo_session_time.currentText()
            selected_hall = self.combo_hall_number.currentText()
            selected_type = self.combo_ticket_type.currentText()
            selected_price = self.line_ticket_price.text()

            # Предположим, что мы используем клиента с ID = 1 для бронирования (можно изменить на реального клиента)
            client_id = 1

            mycursor = self.db_connection.cursor()
            mycursor.execute("INSERT INTO Bookings (MovieID, SessionTime, HallNumber, TicketType, TicketPrice, ClientID) VALUES (%s, %s, %s, %s, %s, %s)",
                             (selected_movie_id, selected_time, selected_hall, selected_type, selected_price, client_id))
            self.db_connection.commit()
            QMessageBox.information(self, "Успех", "Билеты успешно забронированы!")
            self.btn_book_tickets.setEnabled(False)
            self.btn_buy_tickets.show()
        except mysql.connector.Error as err:
            print("Ошибка при бронировании билетов:", err)
            QMessageBox.critical(self, "Ошибка", "Ошибка при бронировании билетов.")

    def open_buy_tickets_dialog(self):
        dialog = BuyTicketsDialog(self.db_connection)
        dialog.exec_()

    def switch_to_manager(self):
        manager_window.show()
        self.hide()


class ManagerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерфейс менеджера")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.btn_add_session = QPushButton("Добавить киносеанс")
        self.btn_add_session.clicked.connect(self.add_session)
        layout.addWidget(self.btn_add_session)

        self.btn_view_bookings = QPushButton("Просмотреть бронирования")
        self.btn_view_bookings.clicked.connect(self.view_bookings)
        layout.addWidget(self.btn_view_bookings)

        self.btn_switch_to_client = QPushButton("Перейти к клиентской системе")
        self.btn_switch_to_client.clicked.connect(self.switch_to_client)
        layout.addWidget(self.btn_switch_to_client)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключение к базе данных
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="555"
        )

    def add_session(self):
        dialog = AddSessionDialog()
        if dialog.exec_() == QDialog.Accepted:
            # Если диалоговое окно закрыто с результатом "Принято" (т.е. новый сеанс добавлен), обновляем список фильмов в интерфейсе клиента
            client_window.populate_movie_list()

    def view_bookings(self):
        dialog = ViewBookingsDialog(self.db_connection)
        dialog.exec_()

    def switch_to_client(self):
        client_window.show()
        self.hide()


class AddSessionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить киносеанс")

        layout = QVBoxLayout()

        self.label_movie_title = QLabel("Название фильма:")
        layout.addWidget(self.label_movie_title)

        self.line_movie_title = QLineEdit()
        layout.addWidget(self.line_movie_title)

        self.label_session_time = QLabel("Время сеанса:")
        layout.addWidget(self.label_session_time)

        self.line_session_time = QLineEdit()
        layout.addWidget(self.line_session_time)

        self.label_hall_number = QLabel("Номер зала:")
        layout.addWidget(self.label_hall_number)

        self.line_hall_number = QLineEdit()
        layout.addWidget(self.line_hall_number)

        self.btn_add_session = QPushButton("Добавить")
        self.btn_add_session.clicked.connect(self.accept)
        layout.addWidget(self.btn_add_session)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        layout.addWidget(self.btn_cancel)

        self.setLayout(layout)


class ViewBookingsDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Просмотр бронирований")
        self.db_connection = db_connection

        layout = QVBoxLayout()

        self.table_bookings = QTableWidget()
        layout.addWidget(self.table_bookings)

        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.refresh_table)
        layout.addWidget(self.btn_refresh)

        self.setLayout(layout)

        self.refresh_table()

    def refresh_table(self):
        try:
            mycursor = self.db_connection.cursor()
            mycursor.execute("SELECT * FROM Bookings")
            bookings = mycursor.fetchall()

            self.table_bookings.setRowCount(len(bookings))
            self.table_bookings.setColumnCount(6)
            self.table_bookings.setHorizontalHeaderLabels(["Номер брони", "Номер сеанса", "Номер зала", "Тип билета", "Стоимость билета", "Куплен"])

            for row_number, booking in enumerate(bookings):
                for column_number, data in enumerate(booking):
                    self.table_bookings.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении таблицы бронирований: {err}")


class BuyTicketsDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Покупка билетов")
        self.db_connection = db_connection

        layout = QVBoxLayout()

        self.label_booking_number = QLabel("Номер брони:")
        layout.addWidget(self.label_booking_number)

        self.line_booking_number = QLineEdit()
        layout.addWidget(self.line_booking_number)

        self.btn_search_booking = QPushButton("Найти бронь")
        self.btn_search_booking.clicked.connect(self.search_booking)
        layout.addWidget(self.btn_search_booking)

        self.table_tickets = QTableWidget()
        layout.addWidget(self.table_tickets)

        self.btn_buy_tickets = QPushButton("Купить выбранные билеты")
        self.btn_buy_tickets.clicked.connect(self.buy_tickets)
        layout.addWidget(self.btn_buy_tickets)

        self.setLayout(layout)

    def search_booking(self):
        booking_number = self.line_booking_number.text()
        try:
            mycursor = self.db_connection.cursor()
            query = ("SELECT * FROM Bookings WHERE BookingID = %s")
            mycursor.execute(query, (booking_number,))
            booking = mycursor.fetchone()

            if booking:
                self.display_tickets(booking)
            else:
                QMessageBox.warning(self, "Предупреждение", "Бронь с указанным номером не найдена.")

        except mysql.connector.Error as err:
            print("Ошибка при поиске брони:", err)
            QMessageBox.critical(self, "Ошибка", "Ошибка при поиске брони.")

    def display_tickets(self, booking):
        try:
            mycursor = self.db_connection.cursor()
            query = ("SELECT * FROM Tickets WHERE BookingID = %s")
            mycursor.execute(query, (booking[0],))
            tickets = mycursor.fetchall()

            self.table_tickets.clear()
            self.table_tickets.setRowCount(len(tickets))
            self.table_tickets.setColumnCount(4)
            self.table_tickets.setHorizontalHeaderLabels(["ID", "Тип билета", "Стоимость билета", "Куплен"])

            for row_number, ticket in enumerate(tickets):
                for column_number, data in enumerate(ticket):
                    self.table_tickets.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except mysql.connector.Error as err:
            print("Ошибка при отображении билетов:", err)
            QMessageBox.critical(self, "Ошибка", "Ошибка при отображении билетов.")

    def buy_tickets(self):
        selected_rows = self.table_tickets.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите хотя бы один билет для покупки.")
            return

        booking_number = self.line_booking_number.text()
        try:
            mycursor = self.db_connection.cursor()

            for row in selected_rows:
                ticket_id = self.table_tickets.item(row.row(), 0).text()
                query = ("UPDATE Tickets SET Purchased = 1 WHERE TicketID = %s AND BookingID = %s")
                mycursor.execute(query, (ticket_id, booking_number))
                self.db_connection.commit()

            QMessageBox.information(self, "Успех", "Выбранные билеты успешно куплены.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при покупке билетов: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_window = ClientInterface()
    manager_window = ManagerInterface()
    client_window.show()
    sys.exit(app.exec_())
