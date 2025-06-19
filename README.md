# Online Movie Ticket Booking System

## Overview

The Online Movie Ticket Booking System is a web application built with Django that allows users to browse movies, view showtimes, select seats, and book tickets online. The system also provides admin functionalities for managing movies, theaters, and bookings.

---

## Features

- User registration and authentication
- Browse movies and view details
- Search for movies and theaters
- View showtimes for different theaters
- Select seats and book tickets
- Manage bookings (view, cancel)
- Admin panel for managing movies, theaters, and shows
- Profile management with profile pictures
- Payment integration (dummy/extendable)

---

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite (default, can be changed)
- **Frontend:** HTML, CSS, Django Templates
- **Other:** Bootstrap (for UI), Pillow (for image handling)

---

## Folder Structure

```
movie_booking_system/
│
├── accounts/           # User authentication & profiles
├── admin_custom/       # Custom admin features
├── bookings/           # Booking logic & seat selection
├── movies/             # Movie management
├── payments/           # Payment handling
├── theaters/           # Theater & show management
├── movie_booking/      # Project settings & URLs
├── media/              # Uploaded images (posters, profiles)
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
├── db.sqlite3          # Default database
├── manage.py           # Django management script
└── venv/               # Virtual environment (not included in repo)
```

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtualenv (recommended)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd movie_booking_system
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is missing, install Django and Pillow:)*
   ```bash
   pip install django pillow
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - User site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Usage Guide

### For Users
1. **Register** for a new account or **login** if you already have one.
2. **Browse movies** on the homepage or search for a specific movie/theater.
3. **View movie details** and available showtimes.
4. **Select a showtime** and choose your seats.
5. **Add tickets to cart** and proceed to checkout.
6. **Complete the booking** (payment is simulated/dummy by default).
7. **View your bookings** in your profile and download tickets.

### For Admins
- Login to the admin panel to manage movies, theaters, shows, and bookings.
- Add new movies, upload posters, and schedule shows.

---

## Screenshots

> **Note:** Add actual screenshots here for better understanding.

- ![Homepage](screenshots/homepage.png)
- ![Movie Details](screenshots/movie_details.png)
- ![Seat Selection](screenshots/seat_selection.png)
- ![Booking Confirmation](screenshots/booking_confirmation.png)

---

## Contribution Guidelines

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Contact

For any queries or support, contact:
- **DANISH KHAN**
- Email: Hellodanish97@gmail.com
- GitHub: [Hellodanish9](https://github.com/your-github-username)

---

**Happy Booking!** 
