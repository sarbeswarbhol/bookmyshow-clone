import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";

// Mock movie + show data
const mockMovie = {
  id: 1,
  title: "Inception",
  genre: "Sci-Fi",
  language: "English",
  description: "A mind-bending thriller where dreams are real.",
  poster_url: "https://i.imgur.com/YOA0U3d.jpg",
};

const mockShows = [
  {
    id: 101,
    time: "6:00 PM",
    theater: "PVR Bhubaneswar",
    price: 200,
  },
  {
    id: 102,
    time: "9:00 PM",
    theater: "INOX Patia",
    price: 250,
  },
];

function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [shows, setShows] = useState([]);

  useEffect(() => {
    // Replace with real API logic later
    setMovie(mockMovie);
    setShows(mockShows);
  }, [id]);

  if (!movie) return <div className="p-6">Loading...</div>;

  return (
    <div className="bg-light min-h-screen p-6">
      <div className="flex flex-col lg:flex-row gap-6 bg-white rounded-lg shadow p-4">
        <img
          src={movie.poster_url}
          alt={movie.title}
          className="w-full lg:w-64 h-auto rounded-md"
        />
        <div className="flex-1">
          <h1 className="text-3xl font-bold text-dark">{movie.title}</h1>
          <p className="text-muted mt-1 text-sm">
            {movie.language} | {movie.genre}
          </p>
          <p className="mt-4 text-dark">{movie.description}</p>

          <h2 className="text-xl font-semibold mt-6 text-dark">Available Shows</h2>
          <div className="mt-3 space-y-4">
            {shows.map((show) => (
              <div
                key={show.id}
                className="border border-muted p-4 rounded-md flex flex-col sm:flex-row justify-between items-start sm:items-center"
              >
                <div>
                  <p className="font-semibold text-dark">{show.theater}</p>
                  <p className="text-sm text-muted">{show.time}</p>
                </div>
                <div className="flex items-center mt-3 sm:mt-0 gap-3">
                  <p className="font-medium text-dark">₹{show.price}</p>
                  <Link
                    to={`/book/${show.id}`}
                    className="bg-primary text-white px-4 py-2 rounded hover:bg-red-600"
                  >
                    Book Now
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MovieDetail;
