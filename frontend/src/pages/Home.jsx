import { useEffect, useState } from "react";
import MovieCard from "../components/MovieCard";

// Mock movie list
const mockMovies = [
  {
    id: 1,
    title: "Inception",
    genre: "Sci-Fi",
    language: "English",
    poster_url: "https://i.imgur.com/YOA0U3d.jpg",
  },
  {
    id: 2,
    title: "Oppenheimer",
    genre: "Drama",
    language: "English",
    poster_url: "https://i.imgur.com/Spj2TDY.jpg",
  },
  {
    id: 3,
    title: "Kantara",
    genre: "Action",
    language: "Kannada",
    poster_url: "https://i.imgur.com/GJDT6DJ.jpg",
  },
];

function Home() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    // Replace with API call later
    setMovies(mockMovies);
  }, []);

  return (
    <div className="bg-light min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-6 text-dark">Now Showing</h1>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {movies.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </div>
  );
}

export default Home;
