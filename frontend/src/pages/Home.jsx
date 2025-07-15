import { useEffect, useState } from "react";
import MovieCard from "../components/MovieCard";
import api from "../api"; // Make sure api.movie.getAll is defined

function Home() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const res = await api.movie.getAll(); // GET /api/movies/
        setMovies(res.data);
      } catch (err) {
        setError("Failed to load movies.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, []);

  return (
    <div className="bg-light min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-6 text-dark">Now Showing</h1>

      {loading && <p>Loading movies...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {movies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      )}
    </div>
  );
}

export default Home;
