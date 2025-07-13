import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

// Mock show data
const mockShow = {
  id: 101,
  movie: "Inception",
  theater: "PVR Bhubaneswar",
  date: "2025-07-13",
  time: "9:00 PM",
  price: 200,
};

const generateSeats = () => {
  const rows = ["A", "B", "C", "D", "E"];
  const seats = [];
  rows.forEach(row => {
    for (let i = 1; i <= 10; i++) {
      seats.push({ id: `${row}${i}`, booked: false });
    }
  });
  return seats;
};

function BookShow() {
  const { showId } = useParams();
  const navigate = useNavigate();
  const [seats, setSeats] = useState(generateSeats());
  const [selected, setSelected] = useState([]);
  const [showInfo, setShowInfo] = useState(null);

  useEffect(() => {
    // Simulate fetching show details
    setShowInfo(mockShow);
  }, [showId]);

  const handleSelect = (seatId) => {
    setSelected(prev =>
      prev.includes(seatId)
        ? prev.filter(s => s !== seatId)
        : [...prev, seatId]
    );
  };

  const handleConfirm = () => {
    if (!showInfo) return;

    const bookingData = {
      movie: showInfo.movie,
      theater: showInfo.theater,
      date: showInfo.date,
      time: showInfo.time,
      seats: selected,
    };

    navigate("/payment", { state: { booking: bookingData } });
  };

  if (!showInfo) return <div className="p-6">Loading show...</div>;

  return (
    <div className="min-h-screen bg-light p-6">
      <h1 className="text-2xl font-bold mb-4 text-dark">
        Book Seats for {showInfo.movie}
      </h1>

      <div className="grid grid-cols-10 gap-2 justify-center mb-8">
        {seats.map(seat => (
          <button
            key={seat.id}
            onClick={() => handleSelect(seat.id)}
            disabled={seat.booked}
            className={`p-2 text-sm rounded border font-semibold ${
              seat.booked
                ? "bg-muted text-white cursor-not-allowed"
                : selected.includes(seat.id)
                ? "bg-primary text-white"
                : "bg-white text-dark border-muted hover:bg-primary hover:text-white"
            }`}
          >
            {seat.id}
          </button>
        ))}
      </div>

      <div className="bg-white p-4 rounded shadow-md max-w-md mx-auto text-center">
        <h2 className="text-xl font-semibold text-dark">Selected Seats</h2>
        <p className="text-muted mt-1">
          {selected.length > 0 ? selected.join(", ") : "No seats selected."}
        </p>
        <p className="mt-2 text-dark font-medium">
          Total: ₹{selected.length * showInfo.price}
        </p>

        <button
          onClick={handleConfirm}
          disabled={selected.length === 0}
          className={`mt-4 w-full py-3 rounded text-white font-semibold ${
            selected.length === 0
              ? "bg-muted cursor-not-allowed"
              : "bg-primary hover:bg-red-600"
          }`}
        >
          Confirm Booking
        </button>
      </div>
    </div>
  );
}

export default BookShow;
