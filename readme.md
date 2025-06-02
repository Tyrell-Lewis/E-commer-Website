[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Tyrell-Lewis/E-commerce-Website.git)


# E-Commerce Website

This is a full-featured e-commerce platform built using **Flask (Python)**, designed to simulate real-world online shopping experiences. It includes user authentication, dynamic product listings, a favorites system, product search and filtering as well as Stripe-integrated checkout and payment processing.

---

## Tech Stack

- **Backend**: Flask, Flask-Login, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Payment**: Stripe API (Checkout, Webhooks)
- **Database**: SQLite with SQLAlchemy

---

## Core Features

- **Product Listings**: Items displayed using clean, responsive cards.
- **Favorites System**: Users can mark and manage favorite items.
- **Search & Filter**:
  - Search by **brand**, **color**, **name**, or **clothing type**
  - Filter by product clothing type.
- **User Authentication**:
  - Register / login via `Flask-Login`
  - Secure session management
- **Stripe Integration**:
  - Checkout with Stripe’s hosted interface
  - Webhook-based order status updates.
- **Order Management**:
  - Orders tracked in database
  - Automatic status changes based on Stripe responses

---

## Getting Started

### Setup Requirements
Before running the project ensure the following:

* Python Version: Ensure Python 3.9.10 is installed.

* Create a .env file based on the example and add:
  
- FLASK_ENV=development
- SECRET_KEY=your-secret-key
- STRIPE_SECRET_KEY=your-stripe-secret
- STRIPE_PUBLIC_KEY=your-stripe-publishable
- STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

> **Note:** This project is not currently deployed. To test it locally, follow these steps.

### 1. Clone the Repository

### 2. Installing Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command.

```bash
$ flask init
```

### 4. Run the server with the following command

```bash
flask run
```



