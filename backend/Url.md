# Movie Theater Booking System API

## Overview

This is a comprehensive API for a movie theater booking system that includes functionality for:
- User authentication and profiles
- Movie management
- Theater, screen, and show management
- Seat booking and ticketing
- Payment processing

## API Endpoints

### Authentication (users app)
- `POST /api/users/register/` - Register a new user
- `POST /api/users/login/` - Login and get JWT tokens
- `POST /api/users/token/refresh/` - Refresh JWT token
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile

### Movies
- `GET /api/movies/` - List all active movies
- `POST /api/movies/create/` - Create a new movie
- `GET /api/movies/<slug>/` - Get movie details
- `PUT /api/movies/<slug>/update/` - Update a movie
- `DELETE /api/movies/<slug>/delete/` - Soft delete a movie
- `POST /api/movies/<slug>/restore/` - Restore a soft-deleted movie

#### Movie Cast
- `GET /api/movies/cast/` - List all active cast members
- `POST /api/movies/cast/create/` - Create a new cast member
- `GET /api/movies/cast/<id>/` - Get cast member details
- `PUT /api/movies/cast/<id>/update/` - Update a cast member
- `DELETE /api/movies/cast/<id>/delete/` - Soft delete a cast member
- `POST /api/movies/cast/<id>/restore/` - Restore a soft-deleted cast member

#### Movie Reviews
- `GET /api/movies/<slug>/reviews/` - List all reviews for a movie
- `POST /api/movies/<slug>/reviews/` - Create a new review
- `PUT /api/movies/<slug>/reviews/update/<pk>/` - Update a review
- `DELETE /api/movies/<slug>/reviews/delete/<pk>/` - Delete a review
- `POST /api/movies/<slug>/reviews/restore/<pk>/` - Restore a deleted review

### Theaters
- `GET /api/theaters/` - List all theaters
- `POST /api/theaters/create/` - Create a new theater
- `GET /api/theaters/<slug>/` - Get theater details
- `PUT /api/theaters/<slug>/update/` - Update a theater
- `DELETE /api/theaters/<slug>/delete/` - Soft delete a theater
- `POST /api/theaters/<slug>/restore/` - Restore a soft-deleted theater

#### Screens
- `GET /api/theaters/<slug>/screens/` - List all screens for a theater
- `POST /api/theaters/<slug>/screens/create/` - Create a new screen under theater
- `GET /api/theaters/screens/<pk>/` - Get screen details
- `PUT /api/theaters/screens/<pk>/update/` - Update a screen
- `DELETE /api/theaters/screens/<pk>/delete/` - Soft delete a screen
- `POST /api/theaters/screens/<pk>/restore/` - Restore a soft-deleted screen
- `POST /api/theaters/screens/<screen_slug>/create-seats/` - Bulk create seats for a screen

#### Shows
- `GET /api/theaters/<slug>/shows/` - List all shows for a theater
- `POST /api/theaters/<slug>/shows/create/` - Create a new show under theater
- `GET /api/theaters/shows/<pk>/` - Get show details
- `PUT /api/theaters/shows/<pk>/update/` - Update a show
- `DELETE /api/theaters/shows/<pk>/delete/` - Soft delete a show
- `POST /api/theaters/shows/<pk>/restore/` - Restore a soft-deleted show

### Bookings
- `GET /api/bookings/` - List user's active bookings
- `POST /api/bookings/create/` - Create a new booking
- `GET /api/bookings/<pk>/` - Get booking details
- `PUT /api/bookings/<pk>/` - Update booking
- `DELETE /api/bookings/<pk>/` - Delete booking
- `POST /api/bookings/<pk>/cancel/` - Cancel a booking

#### Payments
- `POST /api/bookings/payments/create/` - Create a payment
- `GET /api/bookings/payments/<pk>/` - Get payment details
- `PUT /api/bookings/payments/<pk>/update/` - Update payment

#### Tickets
- `GET /api/bookings/tickets/` - List user's tickets
- `GET /api/bookings/tickets/<pk>/` - Get ticket details

#### Seats
- `GET /api/bookings/seats/<show_id>/` - List available seats for a show
- `POST /api/bookings/seats/bulk-create/<screen_slug>/` - Bulk create seats (admin only)

#### Seat Pricing
- `GET /api/bookings/pricing/<show_id>/` - List seat pricing for a show
- `POST /api/bookings/pricing/create/` - Create seat pricing (admin only)
- `PUT /api/bookings/pricing/<pk>/update/` - Update seat pricing (admin only)

## Key Features

1. **User Authentication**: JWT-based authentication system with token refresh
2. **Soft Delete**: All major models support soft delete with restore functionality
3. **Permissions**: Fine-grained permission control for different user roles
4. **Booking Flow**: Complete booking workflow from seat selection to payment
5. **Theater Management**: Comprehensive theater, screen, and show management
6. **Movie Management**: Full CRUD for movies with cast and review systems
7. **Bulk Operations**: Support for bulk seat creation

## Models Overview

The system includes models for:
- Users and profiles
- Movies, cast members, and reviews
- Theaters, screens, and shows
- Seats, bookings, payments, and tickets
- Seat pricing configurations

## Permissions

The API implements various custom permissions:
- `IsRegularUser` - For regular users (non-admin)
- `IsBookingOwnerOrReadOnly` - For booking owners
- `IsPaymentOwner` - For payment owners
- `IsTicketOwner` - For ticket owners
- `IsTheaterOwner` - For theater owners
- `IsTheaterOwnerOfShowSeatPricing` - For theater owners managing seat pricing
- `IsMovieOwner` - For movie owners
- `IsMovieOwnerAndCreator` - For movie creators
- `IsReviewAuthor` - For review authors
- `IsAdminOrStaff` - For admin users

## Technical Details

- Built with Django REST Framework
- JWT authentication using `rest_framework_simplejwt`
- Soft delete implementation using custom model managers
- Nested URL structure for related resources
- Comprehensive serializer classes for data validation
- Detailed error handling and status codes