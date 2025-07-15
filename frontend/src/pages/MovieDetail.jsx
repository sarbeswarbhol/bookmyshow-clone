import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api";
import { format } from "date-fns";

function MovieDetail() {
  const { slug } = useParams();
  const [movie, setMovie] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const res = await api.movie.getBySlug(slug);
        setMovie(res.data);
      } catch (err) {
        setError("Failed to load movie.");
        console.error(err);
      }
    };

    fetchMovie();
  }, [slug]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!movie) return <p>Loading...</p>;

  return (
    <div className="min-h-screen bg-light p-6">
      <div className="flex flex-col lg:flex-row gap-8">
        <img
          src={movie.poster}
          alt={movie.title}
          className="w-full max-w-sm object-cover rounded shadow"
        />

        <div>
          <h1 className="text-3xl font-bold mb-2 text-dark">{movie.title}</h1>
          <p className="text-muted mb-2">{movie.genre} | {movie.language} | {movie.duration} mins</p>
          <p className="text-yellow-600 font-semibold mb-2">⭐ {movie.rating}</p>
          <p className="text-sm mb-4 text-muted">
            Release Date: {format(new Date(movie.release_date), "dd MMM yyyy")}
          </p>
          <p className="text-dark mb-6">{movie.description}</p>

          <div>
            <h2 className="text-lg font-semibold mb-2 text-dark">Cast</h2>
            <div className="flex flex-wrap gap-4">
              {movie.cast.map((member) => (
                <div key={member.id} className="w-20 text-center">
                  <img
                    src={member.profile_picture}
                    alt={member.name}
                    className="w-16 h-16 rounded-full object-cover border"
                  />
                  <p className="text-xs mt-1">{member.name}</p>
                  <p className="text-[10px] text-muted">{member.role}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MovieDetail;
