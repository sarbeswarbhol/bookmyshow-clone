import os
import random
from datetime import datetime, timedelta
from django.core.files import File
from io import BytesIO
from django.utils.text import slugify
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyshow.settings')
import django
django.setup()

from users.models import User
from theaters.models import Theater, Screen, Show
from movies.models import Movie, CastMember, Review
from bookings.models import ShowSeatPricing, Seat, Booking, BookedSeat, Payment, Ticket

# Constants
NUM_USERS = 20
NUM_THEATERS = 5
NUM_SCREENS_PER_THEATER = 3
NUM_SEATS_PER_SCREEN = 50
NUM_MOVIES = 10
NUM_CAST_MEMBERS = 30
NUM_SHOWS_PER_SCREEN = 5
NUM_BOOKINGS = 50

# Helper functions
def random_date(start_date, end_date):
    time_between = end_date - start_date
    random_days = random.randrange(time_between.days)
    return start_date + timedelta(days=random_days)

def random_time():
    return f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"

def create_random_image():
    image = Image.new('RGB', (100, 100), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    return File(buffer, name=f"random_{random.randint(1, 10000)}.jpg")

# Create Users
def create_users():
    roles = ['user', 'theater_owner', 'movie_owner', 'admin']
    genders = ['male', 'female', 'other']
    
    for i in range(NUM_USERS):
        role = random.choice(roles)
        username = f"user{i+1}"
        email = f"{username}@example.com"
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password='testpass123',
            role=role,
            phone=f"{random.randint(7000000000, 9999999999)}",
            location=f"City {random.randint(1, 10)}",
            date_of_birth=random_date(datetime(1970, 1, 1), datetime(2005, 1, 1)),
            gender=random.choice(genders)
        )
        
        if random.random() < 0.3:  # 30% chance to have profile picture
            user.profile_picture = create_random_image()
            user.save()
    
    print(f"Created {NUM_USERS} users")

# Create Theaters
def create_theaters():
    theater_owners = User.objects.filter(role='theater_owner')
    if not theater_owners.exists():
        print("No theater owners found. Please create some first.")
        return
    
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    
    for i in range(NUM_THEATERS):
        owner = random.choice(theater_owners)
        city = random.choice(cities)
        
        Theater.objects.create(
            name=f"Theater {i+1}",
            location=f"{city}, {random.choice(['Main Road', 'Mall', 'Downtown', 'Suburb'])}",
            created_by=owner
        )
    
    print(f"Created {NUM_THEATERS} theaters")

# Create Screens
def create_screens():
    theaters = Theater.objects.all()
    if not theaters.exists():
        print("No theaters found. Please create some first.")
        return
    
    for theater in theaters:
        for i in range(NUM_SCREENS_PER_THEATER):
            Screen.objects.create(
                theater=theater,
                name=f"Screen {i+1}",
                created_by=theater.created_by
            )
    
    print(f"Created {NUM_SCREENS_PER_THEATER} screens per theater")

# Create Seats
def create_seats():
    screens = Screen.objects.all()
    if not screens.exists():
        print("No screens found. Please create some first.")
        return
    
    seat_types = ['regular', 'vip', 'premium']
    
    for screen in screens:
        for i in range(1, NUM_SEATS_PER_SCREEN + 1):
            row = chr(65 + (i // 10))  # A, B, C, etc.
            seat_num = i % 10 or 10
            seat_type = random.choices(seat_types, weights=[70, 20, 10], k=1)[0]
            
            Seat.objects.create(
                screen=screen,
                seat_number=f"{row}{seat_num}",
                seat_type=seat_type
            )
    
    print(f"Created {NUM_SEATS_PER_SCREEN} seats per screen")

# Create Cast Members
def create_cast_members():
    roles = [role[0] for role in CastMember.CAST_ROLE_CHOICES]
    names = [
        "Amitabh Bachchan", "Shah Rukh Khan", "Aamir Khan", "Salman Khan", "Akshay Kumar",
        "Hrithik Roshan", "Ranveer Singh", "Ranbir Kapoor", "Varun Dhawan", "Ayushmann Khurrana",
        "Deepika Padukone", "Priyanka Chopra", "Kareena Kapoor", "Alia Bhatt", "Katrina Kaif",
        "Anushka Sharma", "Kangana Ranaut", "Vidya Balan", "Taapsee Pannu", "Kiara Advani",
        "Rajkumar Hirani", "Sanjay Leela Bhansali", "Karan Johar", "Zoya Akhtar", "Anurag Kashyap",
        "A.R. Rahman", "Pritam", "Vishal-Shekhar", "Shankar-Ehsaan-Loy", "Amit Trivedi"
    ]
    
    for i in range(NUM_CAST_MEMBERS):
        name = random.choice(names)
        role = random.choice(roles)
        
        cast_member = CastMember.objects.create(
            name=name,
            role=role
        )
        
        if random.random() < 0.5:  # 50% chance to have profile picture
            cast_member.profile_picture = create_random_image()
            cast_member.save()
    
    print(f"Created {NUM_CAST_MEMBERS} cast members")

# Create Movies
def create_movies():
    movie_owners = User.objects.filter(role='movie_owner')
    if not movie_owners.exists():
        print("No movie owners found. Please create some first.")
        return
    
    languages = ['Hindi', 'English', 'Tamil', 'Telugu', 'Malayalam', 'Kannada', 'Bengali', 'Marathi']
    genres = ['Action', 'Comedy', 'Drama', 'Romance', 'Thriller', 'Horror', 'Sci-Fi', 'Fantasy']
    titles = [
        "The Great Adventure", "Love in the City", "Dark Secrets", "The Last Stand", "Midnight Dreams",
        "Ocean's Depth", "Mountain High", "Desert Winds", "Urban Legends", "Silent Whispers",
        "Lost Treasure", "Final Journey", "Eternal Love", "Broken Promises", "Hidden Truths",
        "The Forgotten", "Shadows of the Past", "Tomorrow Never Comes", "Echoes of Time", "Fading Memories"
    ]
    
    cast_members = list(CastMember.objects.all())
    
    for i in range(NUM_MOVIES):
        owner = random.choice(movie_owners)
        title = random.choice(titles)
        
        # Generate a unique title by adding a random number if needed
        base_title = f"{title} {random.randint(1, 100)}" if random.random() < 0.3 else title
        
        # Create the movie without saving to generate slug first
        movie = Movie(
            title=base_title,
            description=f"A {random.choice(genres)} movie about {random.choice(['love', 'betrayal', 'friendship', 'revenge', 'redemption'])}.",
            language=random.choice(languages),
            genre=random.choice(genres),
            duration=random.randint(90, 180),
            rating=round(random.uniform(3.0, 5.0), 1),
            release_date=random_date(datetime(2020, 1, 1), datetime(2023, 12, 31)),
            created_by=owner
        )
        
        # Manually generate a unique slug
        if not movie.slug:
            movie.slug = slugify(base_title)
            while Movie.objects.filter(slug=movie.slug).exists():
                movie.slug = f"{slugify(base_title)}-{random.randint(1, 1000)}"
        
        # Save the movie
        movie.save()
        
        # Add random cast members
        num_cast = random.randint(3, 8)
        movie.cast.set(random.sample(cast_members, num_cast))
        
        if random.random() < 0.7:  # 70% chance to have poster
            movie.poster = create_random_image()
            movie.save()
    
    print(f"Created {NUM_MOVIES} movies")
# Create Shows
def create_shows():
    screens = Screen.objects.all()
    movies = Movie.objects.all()
    if not screens.exists() or not movies.exists():
        print("No screens or movies found. Please create some first.")
        return
    
    for screen in screens:
        for i in range(NUM_SHOWS_PER_SCREEN):
            show_date = random_date(datetime.now().date(), datetime.now().date() + timedelta(days=30))
            show_time = datetime.combine(show_date, datetime.strptime(random_time(), "%H:%M").time())
            
            Show.objects.create(
                screen=screen,
                movie=random.choice(movies),
                show_time=show_time,
                created_by=screen.created_by
            )
    
    print(f"Created {NUM_SHOWS_PER_SCREEN} shows per screen")

# Create Show Seat Pricing
def create_show_seat_pricing():
    shows = Show.objects.all()
    if not shows.exists():
        print("No shows found. Please create some first.")
        return
    
    for show in shows:
        ShowSeatPricing.objects.create(
            show=show,
            seat_type='regular',
            price=random.randint(150, 300)
        )
        ShowSeatPricing.objects.create(
            show=show,
            seat_type='vip',
            price=random.randint(300, 500)
        )
        ShowSeatPricing.objects.create(
            show=show,
            seat_type='premium',
            price=random.randint(500, 1000)
        )
    
    print("Created seat pricing for all shows")

# Create Bookings
def create_bookings():
    users = User.objects.filter(role='user')
    shows = Show.objects.all()
    if not users.exists() or not shows.exists():
        print("No users or shows found. Please create some first.")
        return
    
    for i in range(NUM_BOOKINGS):
        user = random.choice(users)
        show = random.choice(shows)
        seats = Seat.objects.filter(screen=show.screen).order_by('?')[:random.randint(1, 5)]
        
        if not seats.exists():
            continue
        
        total_price = sum(seat.get_price(show) for seat in seats)
        
        booking = Booking.objects.create(
            user=user,
            show=show,
            total_price=total_price,
            status=random.choice(['confirmed', 'confirmed', 'confirmed', 'pending', 'cancelled_user'])
        )
        
        booking.seats.set(seats)
        
        # Create BookedSeat entries
        for seat in seats:
            BookedSeat.objects.create(
                show=show,
                seat=seat,
                booking=booking
            )
        
        # Create Payment if booking is confirmed
        if booking.status == 'confirmed':
            payment_methods = [method[0] for method in Payment.PAYMENT_METHOD_CHOICES]
            Payment.objects.create(
                booking=booking,
                amount=total_price,
                status='success',
                payment_method=random.choice(payment_methods),
                transaction_id=f"TXN{random.randint(1000000000, 9999999999)}",
                paid_at=booking.booked_at + timedelta(minutes=random.randint(1, 30))
            )
    
    print(f"Created {NUM_BOOKINGS} bookings")

# Create Reviews
def create_reviews():
    users = User.objects.filter(role='user')
    movies = Movie.objects.all()
    if not users.exists() or not movies.exists():
        print("No users or movies found. Please create some first.")
        return
    
    for movie in movies:
        num_reviews = random.randint(3, 10)
        reviewers = random.sample(list(users), min(num_reviews, users.count()))
        
        for user in reviewers:
            Review.objects.create(
                movie=movie,
                user=user,
                rating=random.randint(1, 5),
                comment=random.choice([
                    "Great movie!",
                    "Could be better.",
                    "Loved the performances.",
                    "The story was weak.",
                    "Amazing cinematography.",
                    "Not worth the hype.",
                    "One of the best this year!",
                    "Would watch again."
                ])
            )
    
    print("Created reviews for movies")

# Main function to run all generators
def generate_all_data():
    print("Starting data generation...")
    
    create_users()
    create_cast_members()
    create_movies()
    create_theaters()
    create_screens()
    create_seats()
    create_shows()
    create_show_seat_pricing()
    create_bookings()
    create_reviews()
    
    print("Data generation completed!")

if __name__ == '__main__':
    generate_all_data()