import { Link } from "react-router-dom";

function MovieCard({ movie }) {
  return (
    <Link
      to={`/movie/${movie.slug}`}
      className="bg-white rounded-xl overflow-hidden shadow hover:scale-105 transition block"
    >
      <img
        src={movie.poster}
        alt={movie.title}
        className="w-full h-64 object-cover"
      />

      <div className="p-4 space-y-1">
        <h3 className="text-xl font-bold text-dark">{movie.title}</h3>
        <p className="text-muted text-sm">
          {movie.language} | {movie.genre}
        </p>
        <p className="text-yellow-600 font-semibold text-sm">⭐ {movie.rating}</p>
      </div>
    </Link>
  );
}

export default MovieCard;
