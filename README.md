# Sirupata Farm House

A Django-based hotel website for Sirupata Farm House, featuring room bookings, reviews, gallery, and machine learning-powered recommendations.

## Features

- **Room Bookings**: Book rooms with date validation (prevents past dates and invalid check-out dates).
- **Reviews & Sentiment Analysis**: Submit reviews with star ratings; sentiment scores combine text analysis (via TextBlob) and ratings for "Overall Experience" sorting.
- **Review Sorting**: Sort reviews by date or overall experience with AJAX-powered dropdowns for dynamic updates.
- **Room Recommendations**: Content-based recommendations using TF-IDF and cosine similarity, plus popularity based on booking counts.
- **Gallery**: Display images and videos.
- **Admin Panel**: Django admin for managing content.

## Tech Stack

- **Backend**: Django 6.0, MySQL
- **ML Libraries**: TextBlob (sentiment), scikit-learn (TF-IDF, cosine similarity)
- **Frontend**: Bootstrap, FontAwesome, AJAX
- **Deployment**: Docker, docker-compose

## Setup

1. Clone the repo.
2. Run `docker-compose up --build` to start the app.
3. Access at `http://localhost:8000`.

## Usage

- Home: View reviews and sort them.
- Rooms: See room details with recommendations.
- Bookings: Submit booking forms (with validations).
- Admin: `/admin/` for content management.

## Future Enhancements

- Collaborative filtering for recommendations
- Demand forecasting
- Mobile responsiveness improvements
- Loading indicators for AJAX
- SEO and accessibility updates
- Error handling for ML operations
- Performance optimizations (caching, indexes)
- Payment integration
- Enhanced admin dashboard
