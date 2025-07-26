from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta

from random import choice, randint, sample
from urllib.parse import quote
import requests
from faker import Faker
from datetime import datetime

from movies.models import CastMember, Movie, Review
from theaters.models import Theater, Screen, Show

User = get_user_model()
fake = Faker()

def download_svg_avatar(name):
    encoded = quote(name)
    url = f"https://avatar.arctixapis.workers.dev/?name={encoded}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return ContentFile(response.content, name=f"{encoded}.svg")
    except Exception as e:
        print(f"Error fetching SVG for {name}: {e}")
    return None

class Command(BaseCommand):
    help = 'Generate fake data for users, cast, real movies, theaters, screens, shows, and reviews.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("🚀 Generating fake data (until shows)..."))
        stats = {
            "users": 0, "cast": 0, "movies": 0,
            "theaters": 0, "screens": 0, "shows": 0, "reviews": 0
        }

        # --- Users (3 of each role)
        users = []
        credentials = []
        role_prefix = {
            'user': 'user',
            'movie_owner': 'movieowner',
            'theater_owner': 'theaterowner'
        }

        for role in role_prefix:
            for i in range(1, 4):  # Create 3 users per role
                username = f"{role_prefix[role]}{i}"
                password = "password123"
                user = User.objects.create_user(
                    username=username,
                    email=fake.unique.email(),
                    password=password,
                    phone=fake.unique.phone_number(),
                    location=fake.city(),
                    date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
                    role=role,
                    gender=choice(['male', 'female', 'other'])
                )
                if avatar := download_svg_avatar(username):
                    user.profile_picture.save(f"{username}.svg", avatar, save=True)
                users.append(user)
                credentials.append(f"{username} ({role}) - password: {password}")
                stats["users"] += 1

        # Save credentials to a text file
        with open("dev_users.txt", "w") as f:
            f.write(" DEV USER CREDENTIALS:\n\n")
            f.write("\n".join(credentials))

        movie_owner = next((u for u in users if u.role == 'movie_owner'), users[0])
        theater_owner = next((u for u in users if u.role == 'theater_owner'), users[1])

        # --- Cast Members
        names = [
            "Amitabh Bachchan", "Shah Rukh Khan", "Aamir Khan", "Salman Khan", "Akshay Kumar",
            "Hrithik Roshan", "Ranveer Singh", "Ranbir Kapoor", "Varun Dhawan", "Ayushmann Khurrana",
            "Deepika Padukone", "Priyanka Chopra", "Kareena Kapoor", "Alia Bhatt", "Katrina Kaif",
            "Anushka Sharma", "Kangana Ranaut", "Vidya Balan", "Taapsee Pannu", "Kiara Advani",
            "Rajkumar Hirani", "Sanjay Leela Bhansali", "Karan Johar", "Zoya Akhtar", "Anurag Kashyap",
            "A.R. Rahman", "Pritam", "Vishal-Shekhar", "Shankar-Ehsaan-Loy", "Amit Trivedi"
        ]

        role_mapping = {
            "Amitabh Bachchan": "actor", "Shah Rukh Khan": "actor", "Aamir Khan": "actor", "Salman Khan": "actor", "Akshay Kumar": "actor",
            "Hrithik Roshan": "actor", "Ranveer Singh": "actor", "Ranbir Kapoor": "actor", "Varun Dhawan": "actor", "Ayushmann Khurrana": "actor",
            "Deepika Padukone": "actress", "Priyanka Chopra": "actress", "Kareena Kapoor": "actress", "Alia Bhatt": "actress", "Katrina Kaif": "actress",
            "Anushka Sharma": "actress", "Kangana Ranaut": "actress", "Vidya Balan": "actress", "Taapsee Pannu": "actress", "Kiara Advani": "actress",
            "Rajkumar Hirani": "director", "Sanjay Leela Bhansali": "director", "Karan Johar": "director", "Zoya Akhtar": "director", "Anurag Kashyap": "director",
            "A.R. Rahman": "music_director", "Pritam": "music_director", "Vishal-Shekhar": "composer", "Shankar-Ehsaan-Loy": "composer", "Amit Trivedi": "composer"
        }

        cast_members = []
        for name in names:
            role = role_mapping.get(name, 'actor')
            cast = CastMember.objects.create(name=name, role=role)
            if avatar := download_svg_avatar(name):
                cast.profile_picture.save(f"{slugify(name)}.svg", avatar, save=True)
            cast_members.append(cast)
            stats["cast"] += 1

        # --- Movies
        real_movies = [
    {"title": "3 Idiots", "description": "Three friends challenge the traditional education system in India.", "language": "Hindi", "genre": "Drama", "duration": 171, "rating": 8.4, "release_date": "2009-12-25"},
    {"title": "Dangal", "description": "A former wrestler trains his daughters to become world-class wrestlers.", "language": "Hindi", "genre": "Biography", "duration": 161, "rating": 8.3, "release_date": "2016-12-23"},
    {"title": "Baahubali: The Beginning", "description": "A man discovers his heritage and a lost kingdom in this epic fantasy.", "language": "Telugu", "genre": "Action", "duration": 159, "rating": 8.0, "release_date": "2015-07-10"},
    {"title": "Gully Boy", "description": "A street rapper from the slums fights for his dream.", "language": "Hindi", "genre": "Musical", "duration": 153, "rating": 7.9, "release_date": "2019-02-14"},
    {"title": "Zindagi Na Milegi Dobara", "description": "Three friends rediscover life and themselves on a road trip through Spain.", "language": "Hindi", "genre": "Adventure", "duration": 155, "rating": 8.2, "release_date": "2011-07-15"},
    {"title": "PK", "description": "An alien questions religious dogmas during his time on Earth.", "language": "Hindi", "genre": "Comedy", "duration": 153, "rating": 8.1, "release_date": "2014-12-19"},
    {"title": "Barfi!", "description": "A love story involving a mute boy, an autistic girl, and a lot of heart.", "language": "Hindi", "genre": "Romance", "duration": 151, "rating": 8.1, "release_date": "2012-09-14"},
    {"title": "Drishyam", "description": "A man uses his wit to protect his family after a crime.", "language": "Hindi", "genre": "Thriller", "duration": 163, "rating": 8.2, "release_date": "2015-07-31"},
    {"title": "Andhadhun", "description": "A blind pianist gets entangled in a murder mystery.", "language": "Hindi", "genre": "Mystery", "duration": 139, "rating": 8.2, "release_date": "2018-10-05"},
    {"title": "Chak De! India", "description": "A disgraced hockey player coaches the national women's team.", "language": "Hindi", "genre": "Sports", "duration": 153, "rating": 8.1, "release_date": "2007-08-10"}
]

        movies = []
        for m in real_movies:
            movie = Movie.objects.create(
                title=m["title"],
                description=m["description"],
                language=m["language"],
                genre=m["genre"],
                duration=m["duration"],
                rating=m["rating"],
                release_date=datetime.strptime(m["release_date"], "%Y-%m-%d").date(),
                created_by=choice([u for u in users if u.role == 'movie_owner']),
                slug=slugify(m["title"])
            )
            if avatar := download_svg_avatar(m["title"]):
                movie.poster.save(f"{slugify(m['title'])}.svg", avatar, save=True)
            movie.cast.set(sample(cast_members, k=randint(3, 6)))
            movies.append(movie)
            stats["movies"] += 1

        # --- Theaters, Screens, Shows
        for _ in range(3):
            theater = Theater.objects.create(
                name=fake.company(),
                location=fake.address(),
                created_by=choice([u for u in users if u.role == 'theater_owner']),
            )
            stats["theaters"] += 1

            for i in range(2):
                screen = Screen.objects.create(
                    name=f"Screen {i+1}",
                    theater=theater,
                    created_by=choice([u for u in users if u.role == 'theater_owner']),
                )
                stats["screens"] += 1

                for j in range(2):
                    show = Show.objects.create(
                        screen=screen,
                        movie=choice(movies),
                        show_time=now() + timedelta(days=randint(1, 5), hours=randint(1, 5)),
                        created_by=choice([u for u in users if u.role == 'theater_owner']),
                    )
                    stats["shows"] += 1

        # --- Reviews
        normal_users = [u for u in users if u.role == 'user']
        reviewed = set()
        for user in normal_users:
            reviewed_movies = sample(movies, k=randint(2, 4))
            for movie in reviewed_movies:
                key = (user.id, movie.id)
                if key not in reviewed:
                    Review.objects.create(
                        movie=movie,
                        user=user,
                        rating=randint(3, 5),
                        comment=fake.sentence()
                    )
                    reviewed.add(key)
                    stats["reviews"] += 1

        # --- Final Log
        self.stdout.write(self.style.SUCCESS("✅ Fake data generation complete."))
        for k, v in stats.items():
            self.stdout.write(self.style.SUCCESS(f" → {k.capitalize()}: {v}"))
        self.stdout.write(self.style.SUCCESS("📝 Credentials saved to 'dev_users.txt'"))
