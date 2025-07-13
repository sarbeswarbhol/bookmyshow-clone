import { Link } from "react-router-dom";

function MovieCard({ movie }) {
  return (
    <Link to={`/movie/${movie.id}`} className="bg-white rounded-xl overflow-hidden shadow hover:scale-105 transition">
      <img
        src={movie.poster_url}
        alt={movie.title}
        className="w-full h-64 object-cover"
      />
      <div className="p-4">
        <h3 className="text-xl font-bold text-dark">{movie.title}</h3>
        <p className="text-muted text-sm">{movie.language} | {movie.genre}</p>
      </div>
    </Link>
  );
}

export default MovieCard;
