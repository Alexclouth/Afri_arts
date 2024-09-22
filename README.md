# Afri-Arts Gallery Showcase

Afri-Arts is an online platform where artists can display and sell their artwork while interacting with art enthusiasts. The project is structured to support both artists and art collectors with features such as artwork posting, reviews, and online transactions.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Developers](#developers)

## Project Overview
Afri-Arts aims to empower artists by providing a platform to display, showcase, and sell their art. Users can interact with art, leave reviews, and make purchases via integrated payment gateways. The website is designed to offer a seamless user experience while supporting multiple user types (artists, members).

## Features
- **Artist Registration**: Artists can register and create a profile.
- **Artwork Posting**: Artists can upload and display their artwork.
- **Artwork Preview**: Users can view art pieces with detailed descriptions.
- **Review System**: Users can like or dislike artwork, providing feedback for the artist.
- **Transaction System**: Users can purchase artworks via Chapa payment integration.
- **Mobile-Friendly**: Fully responsive design for mobile and desktop devices.

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- Flask
- MySQL Server
- `mysqlclient` package
- Git

### Setup Instructions
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/afri-arts.git
    cd afri-arts
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Database Setup**:
    - Create a MySQL database and a user for the project:
      ```sql
      CREATE DATABASE afri_arts_db;
      CREATE USER 'afri_user'@'localhost' IDENTIFIED BY 'password';
      GRANT ALL PRIVILEGES ON afri_arts_db.* TO 'afri_user'@'localhost';
      FLUSH PRIVILEGES;
      ```

    - Update the `/etc/config.json` file with your MySQL credentials.

5. **Run Migrations**:
    ```bash
    flask db upgrade
    ```

6. **Run the Application**:
    ```bash
    flask run
    ```

## Usage

### Running the Application
1. Activate your virtual environment:
    ```bash
    source venv/bin/activate
    ```

2. Start the Flask server:
    ```bash
    flask run
    ```

3. Open your browser and go to:
    ```
    http://127.0.0.1:5000/
    ```

### User Registration
- Artists and members can register through the sign-up page.
- If `Artist` is selected, additional fields (First Name, Last Name, City, Country, Bio) will be displayed.

### Posting Artwork
Artists can upload their artwork by providing the required details such as:
- Title
- Description
- Price
- Art Type
- Style
- Image Upload

## API Endpoints
Below are some key API endpoints:

### `POST /register`
Registers a new user. Accepts:
- `username`
- `email`
- `password`
- `is_artist`

### `POST /artwork`
Allows an artist to post a new artwork. Required fields:
- `title`
- `description`
- `price`
- `image`


## Deployment

### Deploying on a Linux Server
Follow these steps to deploy the Afri-Arts website on a Linux server using **Nginx**, **Gunicorn**, and **Supervisor**:

1. **Install Nginx**:
    ```bash
    sudo apt install nginx
    ```

2. **Install Gunicorn**:
    ```bash
    pip install gunicorn
    ```

3. **Configure Nginx**:
    Create an Nginx configuration file for the application:
    ```bash
    sudo nano /etc/nginx/sites-available/afri-arts
    ```
    Add the following:
    ```
    server {
        listen 80;
        server_name your_domain_or_IP;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

4. **Enable the Nginx Configuration**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/afri-arts /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

5. **Start Gunicorn with Supervisor**:
    - Install Supervisor:
      ```bash
      sudo apt install supervisor
      ```
    - Configure Supervisor to manage Gunicorn:
      ```bash
      sudo nano /etc/supervisor/conf.d/afri-arts.conf
      ```
      Add:
      ```
      [program:afri-arts]
      command=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app
      directory=/path/to/afri-arts
      autostart=true
      autorestart=true
      stderr_logfile=/var/log/afri-arts.err.log
      stdout_logfile=/var/log/afri-arts.out.log
      ```

    - Reload Supervisor:
      ```bash
      sudo supervisorctl reread
      sudo supervisorctl update
      sudo supervisorctl start afri-arts
      ```

6. **Verify Deployment**:
    Visit your domain to check if the app is running successfully.

---

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Server**: Nginx, Gunicorn, Supervisor
- **Version Control**: Git, GitHub

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**:
    ```bash
    git clone https://github.com/yourusername/afri-arts.git
    cd afri-arts
    ```

2. **Create a New Branch**:
    ```bash
    git checkout -b feature/your-feature
    ```

3. **Commit Your Changes**:
    ```bash
    git commit -m "Add feature"
    ```

4. **Push to the Branch**:
    ```bash
    git push origin feature/your-feature
    ```

5. **Create a Pull Request** on GitHub.

Make sure your code is clean and passes all tests before submitting.

---

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

---

## Developers

### Backend Developer
**Alazer Gebrekidan**  
Email: [alazeralphilo@gmail.com](mailto:alazeralphilo@gmail.com)

### Frontend Developer
**Senay Frehiwot**  
Email: [tomasfrehiwot@gmail.com](mailto:tomasfrehiwot@gmail.com)

