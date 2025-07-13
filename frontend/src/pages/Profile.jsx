import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

// Mock user data and bookings
const mockUser = {
  username: "john_doe",
  phone: "9999999999",
  role: "User",
};

const mockBookings = [
  {
    id: 1,
    movie: "Inception",
    theater: "PVR Bhubaneswar",
    seats: ["B2", "B3", "B4"],
    time: "9:00 PM",
    date: "2025-07-13",
    amount: 600,
  },
  {
    id: 2,
    movie: "Oppenheimer",
    theater: "INOX Esplanade",
    seats: ["C1", "C2"],
    time: "6:30 PM",
    date: "2025-06-30",
    amount: 400,
  },
];

function Profile() {
  const [user, setUser] = useState(null);
  const [bookings, setBookings] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Replace with auth/user API later
    setUser(mockUser);
    setBookings(mockBookings);
  }, []);

  if (!user) return <div className="p-6">Loading profile...</div>;

  return (
    <div className="min-h-screen bg-light p-6">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold text-dark mb-4">Welcome, {user.username}!</h2>
        <p className="text-muted mb-1"><strong>Phone:</strong> {user.phone}</p>
        <p className="text-muted mb-6"><strong>Role:</strong> {user.role}</p>

        <h3 className="text-xl font-semibold text-dark mb-3">Booking History</h3>
        <div className="space-y-4">
          {bookings.length === 0 ? (
            <p className="text-muted">No bookings found.</p>
          ) : (
            bookings.map((b) => (
              <div key={b.id} className="border border-muted rounded-md p-4">
                <p className="font-bold text-dark">{b.movie}</p>
                <p className="text-sm text-muted">{b.theater}</p>
                <p className="text-sm text-muted">Date: {b.date} | Time: {b.time}</p>
                <p className="text-sm text-muted">Seats: {b.seats.join(", ")}</p>
                <p className="text-sm text-dark font-medium mt-1">Paid: ₹{b.amount}</p>
              </div>
            ))
          )}
        </div>

        <button
          className="mt-6 bg-primary text-white px-6 py-2 rounded hover:bg-red-600"
          onClick={() => {
            // Fake logout
            alert("Logged out!");
            navigate("/login");
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default Profile;
